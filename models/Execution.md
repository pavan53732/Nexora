> **Status: DERIVED** for Execution domain model.
> This document defines the shape and semantics of Execution in the data model.
>
> Depends on: the canonical architecture document for Runtime and execution lifecycle sources.
> Referenced by: protocols, APIs, and storage implementations.

# Domain Model: Execution

```kotlin
data class Execution(
    val id: String,
    val workspaceId: String,
    val correlationId: String,
    val retryAttempt: Int = 0,  // DEC-7: retry attempt index, scoped per-Execution
    val taskId: String?,
    val status: ExecutionStatus,
    val phase: ExecutionPhase,
    val version: Long,
    val checkpointId: String?,
    val priorExecutionId: String? = null,
    val latestError: CanonicalErrorEnvelope? = null,
    val escalationPayload: JsonObject? = null,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null
)

enum class ExecutionStatus {
    CREATED,
    RUNNING,
    COMPLETED,
    FAILED,
    CANCELLED
}

// ExecutionPhase is canonically defined here; models/Task.md references this enum.
enum class ExecutionPhase {
    REQUIREMENT_ANALYSIS,
    PLANNING,
    TASK_DECOMPOSITION,
    AGENT_SELECTION,
    SKILL_SELECTION,
    TOOL_SELECTION,
    DEPENDENCY_RESOLUTION,
    EXECUTION,
    BUILD,
    STATIC_ANALYSIS,
    TESTING,
    VERIFICATION,
    COMPLETION_REPORTING
}

data class CanonicalErrorEnvelope(
    val code: String,
    val category: String,
    val message: String,
    val retryability: String,
    val idempotency: String,
    val lifecycleEffect: String,
    val recoveryOwner: String,
    val correlationId: String,
    val details: JsonObject? = null
)
```

> **Canonical envelope ownership:** This is the single model-level definition of `CanonicalErrorEnvelope`; other models (e.g. `models/Task.md`) reference it rather than redefining it. The semantic contract — field responsibilities, categories, and recovery metadata — is owned by [../errors/ERROR_CODES.md](../errors/ERROR_CODES.md).


## Retry Lineage

`priorExecutionId` is `null` for the original execution. It is set only for an
explicit retry/restart after a committed terminal state (`FAILED`, `CANCELLED`,
`COMPLETED`). It points to the immediate terminal predecessor; the chain is acyclic.
It does not replace `correlationId`.

## Execution Phase Semantics

Execution events are append-only and at-least-once. Consumers MUST deduplicate by execution ID and sequence/version. A checkpoint event is durable only after the referenced checkpoint has been committed. `phase` is transient execution activity; `status` is the durable lifecycle projection. `CREATED` represents an existing Execution that has not yet started; it is also the post-recovery projection selected by DEC-7 when the preserved Execution awaits a future start after its Task returns to `Queued`.