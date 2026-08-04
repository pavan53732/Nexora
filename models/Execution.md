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
    val taskId: String?,
    val status: ExecutionStatus,
    val phase: ExecutionPhase,
    val version: Long,
    val checkpointId: String?,
    val latestError: CanonicalErrorEnvelope? = null,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null
)
```

## Execution Phase Semantics

Execution events are append-only and at-least-once. Consumers MUST deduplicate by execution ID and sequence/version. A checkpoint event is durable only after the referenced checkpoint has been committed. `phase` is transient execution activity; `status` is the durable lifecycle projection.
