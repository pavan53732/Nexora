> **Status: DERIVED** for Runtime-API API.
> This document describes the api surface for Runtime-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Runtime-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Runtime API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/RUNTIME.md](../../architecture/RUNTIME.md)

---

## Normative Operation Contract

The operation below is a contract boundary, not merely a Kotlin convenience method. Implementations MUST preserve the lifecycle, event, error, security, retry, cancellation, and idempotency semantics shown here. Transport-specific names MAY differ only when the mapping is documented and lossless.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `execute` / `startTask` | Task `Draft/Pending → Queued → Running`; Agent `Ready → Running` | Task projection plus correlation ID | Invalid input, unavailable agent/provider, permission/approval, timeout, cancellation, internal fault; use `NXR-*` envelope | Client retries require idempotency key; duplicate key returns original task; execution retry is lifecycle-controlled | Workspace authorization and tool policy checked before side effects; cancellation emits lifecycle event and performs cleanup | Runtime integration and end-to-end tests |
| `cancel` / `cancelTask` | Active task/agent → `Cancelled` | Committed cancellation projection | Not found, already terminal, conflict, cleanup failure | Idempotent for same task and cancellation key; repeated request returns committed result | Caller must own workspace/task; cancellation propagates to child jobs and sandbox operations | Lifecycle and cancellation tests |
| `getTaskStatus` | No lifecycle change | Durable status, execution phase, version, latest error | Not found, unauthorized, storage failure | Safe to retry; read is versioned | Redact sensitive error details according to caller scope | API contract tests |
| `invoke` | ToolCall `Pending → Approved/Denied → Executing → Completed/Error` | Tool result, event sequence, correlation ID | Permission denied, approval required, timeout, cancellation, invalid parameters, sandbox/provider failure | Re-execution requires tool idempotency declaration; duplicate call key MUST NOT repeat non-idempotent effects | Permission and sandbox checks precede execution; cancellation releases resources | Tool protocol and security tests |
| `complete` / `stream` | Provider remains lifecycle-authorized; request execution gets committed result or canonical failure | Completion response or ordered stream with terminal marker | Provider unavailable, rate limit, timeout, invalid request, capability mismatch | Retry follows error envelope; non-idempotent external effects require key; stream reconnect must declare resume policy | Provider credentials never cross boundary; cancellation closes stream and records outcome | Provider protocol and integration tests |
| `install` / `activate` | Plugin lifecycle follows verification/install/activation transitions | Plugin projection and registered capabilities | Integrity failure, incompatibility, dependency, permission, timeout, cancellation | Install keyed by plugin/version; duplicate operation returns existing result; activation is not repeated after commit | Signature, compatibility, permission, and sandbox checks precede activation; cancellation rolls back partial artifacts | Plugin lifecycle and security tests |

Every operation MUST return or emit a correlation ID. Errors MUST preserve `code`, `category`, `retryability`, `idempotency`, `lifecycleEffect`, `recoveryOwner`, and redacted `details` from [ERROR_CODES.md](../../errors/ERROR_CODES.md). Lifecycle events are published only after durable state commit and are deduplicated by entity plus transition version.

## Overview

The Runtime API is the central coordination point. It connects the planner, executor, tool manager, and provider system into the agent loop.

## Core API

```kotlin
package com.nexora.app.runtime

/**
 * Main entry point for executing agent tasks.
 */
interface NexoraRuntime {
    // Execute a goal within a workspace
    suspend fun execute(goal: String, workspaceId: String): Task

    // Cancel a running task
    suspend fun cancel(taskId: String)

    // Get task status
    suspend fun getTaskStatus(taskId: String): Task

    // List running tasks
    suspend fun getRunningTasks(workspaceId: String): List<Task>

    // Get execution history
    suspend fun getHistory(workspaceId: String, limit: Int): List<ExecutionEvent>
}
```

## Event Bus API

```kotlin
interface EventBus {
    fun publish(event: NexoraEvent)
    fun subscribe(eventType: KClass<out NexoraEvent>, handler: (NexoraEvent) -> Unit)
    fun unsubscribe(eventType: KClass<out NexoraEvent>, handler: (NexoraEvent) -> Unit)
}

// Usage
eventBus.subscribe(TaskProgress::class) { event ->
    updateUI(event)
}
```

## Background Service API

```kotlin
/**
 * Android Foreground Service for long-running agent execution.
 * Survives app minimize and device restart.
 */
class AgentExecutionService : LifecycleService() {
    fun startTask(taskId: String, goal: String, workspaceId: String)
    fun cancelTask(taskId: String)
    fun getActiveTasks(): List<String>
}
```
