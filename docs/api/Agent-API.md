> **Status: DERIVED** for Agent API.
> This document describes the api surface for Agent. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Agent.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Agent API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/AGENT_RUNTIME.md](../../architecture/AGENT_RUNTIME.md)

---

## Normative Operation Contract

The Agent API defines the boundary for agent lifecycle, execution startup, assignment, cancellation, and status/query operations. Tool invocation, provider completion, and plugin installation are **not owned by this API** and MUST be delegated to their canonical APIs.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `registerAgent` | Agent `Created → Configured → Ready` | Durable agent projection with version | Duplicate ID, invalid manifest, incompatible SDK/version, storage failure | Duplicate `(agentId, version)` is idempotent | Registration validates capabilities, declared skills, and permission scope before visibility | Registry and SDK conformance tests |
| `startTask` | Task `Draft/Pending → Queued → Running`; Agent `Ready → Running` | Task projection plus correlation ID | Invalid input, unavailable dependencies, permission/approval, timeout, cancellation, internal fault | Client retries require idempotency key; duplicate key returns original task projection | Workspace authorization checked before side effects; cancellation emits lifecycle event after durable commit | Runtime integration and E2E tests |
| `cancelTask` | Active task/agent → `Cancelled` | Committed cancellation projection | Not found, already terminal, conflict, cleanup failure | Idempotent for same task and cancellation key | Caller must own workspace/task; cancellation propagates to child jobs and delegated work | Lifecycle and cancellation tests |
| `getTaskStatus` | No lifecycle change | Durable task/execution status, phase, version, latest redacted error | Not found, unauthorized, storage failure | Safe to retry; read is versioned | Sensitive error details are redacted by caller scope | API contract tests |
| `listAgents` / `getAgent` | No lifecycle change | Stable projection(s), capability metadata, pagination cursor | Not found, invalid filter, unauthorized, storage failure | Safe to retry; reads are side-effect free | Internal-only agents/capabilities MUST be redacted by caller scope | Registry and API contract tests |

Every response and emitted event MUST include `correlationId`. Long-running or streaming operations MUST expose `resumeToken` when resumable. Durable commit MUST precede lifecycle event publication. Events MUST be deduplicated by `(entityId, version, transition)`.

## Contract Shapes

### Start Request

```kotlin
data class StartTaskRequest(
    val requestId: String,
    val correlationId: String,
    val idempotencyKey: String?,
    val workspaceId: String,
    val taskId: String?,
    val agentId: String,
    val goal: String,
    val input: JsonObject,
    val caller: CallerRef,
    val priority: TaskPriority = TaskPriority.NORMAL,
    val approvals: List<ApprovalRef> = emptyList(),
    val timeoutMs: Long?,
    val metadata: Map<String, String> = emptyMap()
)
```

### Task Projection

```kotlin
data class TaskProjection(
    val correlationId: String,
    val taskId: String,
    val workspaceId: String,
    val agentId: String,
    val status: TaskStatus,
    val phase: ExecutionPhase,
    val version: Long,
    val createdAt: Instant,
    val updatedAt: Instant,
    val latestError: CanonicalErrorEnvelope?,
    val childTaskIds: List<String> = emptyList(),
    val delegatedAgentIds: List<String> = emptyList(),
    val resumeToken: String? = null
)
```

### Event Envelope

```kotlin
data class AgentLifecycleEvent(
    val eventId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val taskId: String?,
    val transition: String,
    val version: Long,
    val publishedAt: Instant,
    val payload: JsonObject,
    val terminal: Boolean
)
```

### Required Rules

- `taskId` MUST remain stable across retries once assigned.
- `version` is the durable state version used for optimistic reads and event deduplication.
- `resumeToken` MUST be opaque and only present when resumable progress or event streaming is supported.
- Child tasks and delegated work MUST be represented explicitly through `childTaskIds` and `delegatedAgentIds`; hidden fan-out is not allowed at the contract boundary.

## Overview

The Agent API defines how agents are registered, discovered, assigned work, cancelled, and queried. It does **not** redefine tool, provider, or plugin operations.

## Agent Interface

```kotlin
package com.nexora.app.runtime.agent

interface AgentApi {
    suspend fun registerAgent(descriptor: AgentDescriptor): AgentProjection
    suspend fun startTask(request: StartTaskRequest): TaskProjection
    suspend fun cancelTask(taskId: String, correlationId: String, cancellationKey: String?): TaskProjection
    suspend fun getTaskStatus(taskId: String): TaskProjection
    suspend fun getAgent(agentId: String): AgentProjection
    suspend fun listAgents(filter: AgentFilter, page: PageRequest): Page<AgentProjection>
}
```

## Agent Registry API

```kotlin
data class AgentProjection(
    val agentId: String,
    val version: Long,
    val name: String,
    val description: String,
    val declaredSkills: List<String>,
    val requiredPermissions: List<String>,
    val supportsDelegation: Boolean,
    val supportsBackgroundExecution: Boolean,
    val status: AgentStatus,
    val phase: AgentExecutionPhase
)
```

## Ownership Boundaries

- Tool-call lifecycle belongs to [Tool-API.md](./Tool-API.md).
- Provider completion and streaming belong to [Provider-API.md](./Provider-API.md).
- Plugin installation/activation belongs to [Plugin-API.md](./Plugin-API.md).
- Runtime orchestration and event bus guarantees belong to [Runtime-API.md](./Runtime-API.md).

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| registerAgent | NXR-1001, NXR-1002, NXR-5007 |
| startTask | NXR-1003, NXR-1004, NXR-2002, NXR-2003, NXR-7004 |
| cancelTask | NXR-1005, NXR-7007 |
| getTaskStatus | NXR-1006, NXR-7001 |
| getAgent / listAgents | NXR-1001, NXR-7001 |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for canonical envelope requirements.
