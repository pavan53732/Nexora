> **Status: DERIVED** for Workflow entity shape.
> This document defines the data model for Workflow. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Workflow.
> Referenced by: APIs, SDKs, protocols, and tests that consume Workflow.


# Domain Model: Workflow

> Canonical domain model. See [architecture/WORKFLOW_ENGINE.md](../architecture/WORKFLOW_ENGINE.md).

```kotlin
package com.nexora.app.runtime.workflow

data class Workflow(
    val id: String,
    val name: String,
    val steps: List<WorkflowStep>,
    val onError: ErrorStrategy = ErrorStrategy.RETRY,
    val maxRetries: Int = 3,
    val workspaceId: String,
    val createdAt: Instant
)

enum class ErrorStrategy { RETRY, SKIP, ABORT, FALLBACK }
```

## Lifecycle and Step Semantics

Workflow lifecycle is owned by [state-machines/WorkflowLifecycle.md](../state-machines/WorkflowLifecycle.md). Workflow-level state and step sub-state are separate: a workflow can be `Running` while multiple steps are `StepRunning`, `Pending`, or `StepCompleted`. Step updates MUST be versioned and persisted before workflow transition events are emitted.

```kotlin
enum class WorkflowLifecycleState { DEFINED, VALIDATED, RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED }
enum class WorkflowStepState { PENDING, RUNNING, COMPLETED, FAILED, SKIPPED }
```
