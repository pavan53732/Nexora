> **Status: DERIVED** for Workflow domain model.
> This document defines the shape and semantics of Workflow in the data model.
>
> Depends on: the canonical workflow architecture and lifecycle sources.
> Referenced by: protocols, APIs, registries, and orchestration implementations.

# Domain Model: Workflow

```kotlin
data class Workflow(
    val id: String,
    val workspaceId: String,
    val correlationId: String,
    val status: WorkflowStatus,
    val currentStepId: String?,
    val steps: List<WorkflowStep>,
    val version: Long,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null
)
```

## Lifecycle and Step Semantics

`status` is the durable workflow lifecycle projection aligned to [state-machines/WorkflowLifecycle.md](../state-machines/WorkflowLifecycle.md). Step execution details are subordinate runtime state and MUST NOT replace workflow lifecycle state. Workflow transition events MUST be deduplicated by `(workflowId, version, transition)`.
