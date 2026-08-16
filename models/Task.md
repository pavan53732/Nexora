> **Status: DERIVED** for Task domain model.
> This document defines the shape and semantics of Task in the data model.
>
> Depends on: the canonical architecture and task lifecycle sources.
> Referenced by: protocols, APIs, SDKs, and storage implementations.

# Domain Model: Task

```kotlin
data class Task(
    val id: String,
    val workspaceId: String,
    val agentId: String,
    val correlationId: String,
    val parentTaskId: String?,
    val dependsOnTaskIds: List<String>,
    val status: TaskStatus,
    val phase: ExecutionPhase,
    val priority: TaskPriority = TaskPriority.NORMAL,
    val version: Long,
    val goal: String,
    val input: JsonObject,
    val output: JsonObject?,
    val childTaskIds: List<String>,
    val delegatedAgentIds: List<String>,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null,
    val latestError: CanonicalErrorEnvelope? = null,
    val effectiveDeadline: Instant,
    val retryNotBefore: Instant? = null
)

enum class TaskStatus {
    DRAFT,
    PENDING,
    QUEUED,
    RUNNING,
    BLOCKED,
    BLOCKED_AWAITING_INPUT,
    WAITING_APPROVAL,
    COMPLETED,
    FAILED,
    CANCELLED,
    RETRY_PENDING
}

enum class TaskPriority {
    LOW,
    NORMAL,
    HIGH,
    CRITICAL
}
```

> **Shared type ownership:** `ExecutionPhase` is defined once, canonically, in [Execution.md](./Execution.md); Task's `phase` field references that same enum and MUST NOT be redefined here. `CanonicalErrorEnvelope` is likewise defined once in [Execution.md](./Execution.md) as the model-level shape of the canonical envelope whose semantic contract (fields, categories, recovery metadata) is owned by [../errors/ERROR_CODES.md](../errors/ERROR_CODES.md).


> **DEC-7 (2026-08-11):** `TaskStatus.RETRY_PENDING` remains a Task lifecycle state, but retry-attempt indexing is not stored on Task. The authoritative retry-attempt index is `Execution.retryAttempt`, and RetryPending is EPHEMERAL. See [../decisions/DEC-7-retry-attempt-state.md](../decisions/DEC-7-retry-attempt-state.md).

## Lifecycle and Execution Semantics

`status` is a durable lifecycle projection aligned to [state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md). `phase` represents transient execution phase and MUST NOT replace lifecycle state. `dependsOnTaskIds` is validated as an acyclic dependency graph before queueing. `effectiveDeadline` is inherited by dependency waits and child operations. `retryNotBefore` is authoritative for RetryPending backoff and cannot be bypassed by direct start. Task identity and `correlationId` remain stable throughout retries of the same logical task once assigned.


### Error Envelope Propagation

When a task fails (transitioning to `FAILED` or `RETRY_PENDING`), the terminal or transient error MUST be mapped into a `CanonicalErrorEnvelope`. This envelope is stored in the `latestError` field of the Task and propagated across all API and protocol boundaries. Under DEC-33, invalid dependency references or cycles use `NXR-1014`, unsatisfied terminal dependencies use `NXR-1015`, and effective-deadline expiry uses `NXR-1016`; the lifecycle effect remains owned by TaskLifecycle. The envelope guarantees that exact recovery rules, retryability, and lifecycle effects are accessible to calling orchestrators and user interfaces alike.
