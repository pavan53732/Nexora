> **Status: DERIVED** for Agent-API API.
> This document describes the api surface for Agent-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Agent-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Agent API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/AGENT_RUNTIME.md](../../architecture/AGENT_RUNTIME.md)

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

The Agent API defines how agents are created, configured, and executed. Each agent type (Planner, Coder, etc.) implements this API.

## Agent Interface

```kotlin
package com.nexora.app.runtime.agents

interface Agent {
    val id: String
    val type: AgentType
    val name: String
    val description: String
    val capabilities: List<String>
    val defaultTools: List<String>  // Tool IDs this agent uses by default
    val systemPrompt: String  // Agent-specific system prompt

    suspend fun execute(task: AgentTask, context: AgentContext): AgentResult
}

enum class AgentType {
    PLANNER, RESEARCHER, CODER, REVIEWER, TESTER, DEBUGGER,
    DOCUMENTATION_WRITER, REFACTORING, DEPLOYMENT, SECURITY_AUDITOR,
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR,
    ARCHITECT, CUSTOM  // ARCHITECT = AGT-016; CUSTOM = user-defined agents (not a built-in type)
}

data class AgentContext(
    val workspaceId: String,
    val agentId: String,
    val memoryManager: MemoryManager,
    val eventBus: EventBus,
    val sessionId: String? = null
)

data class AgentTask(
    val id: String,
    val goal: String,
    val workspaceId: String,
    val parentTaskId: String?,
    val assignedAgentType: AgentType,
    val context: Map<String, Any>
)

data class AgentResult(
    val taskId: String,
    val success: Boolean,
    val output: String,
    val artifacts: List<Artifact>,
    val steps: List<AgentStep>
)
```

## Agent Registry API

```kotlin
// Register a built-in agent
agentRegistry.register(PlannerAgent())

// Create an instance for a specific workspace
val planner = agentRegistry.create(
    type = AgentType.PLANNER,
    workspaceId = "ws-001"
)

// Execute a task
val result = planner.execute(task, agentContext)
```

See [registry/AGENTS.md](../../registry/AGENTS.md) for the complete agent registry with stable IDs.
