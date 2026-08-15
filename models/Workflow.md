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
    val name: String,
    val correlationId: String,
    val status: WorkflowStatus,
    val currentStepId: String?,
    val steps: List<WorkflowStep>,
    val onError: ErrorStrategy = ErrorStrategy.RETRY,
    val maxRetries: Int = 3,
    val version: Long,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null
)

enum class WorkflowStatus {
    DEFINED,
    VALIDATED,
    RUNNING,
    PAUSED,
    STEP_PENDING,
    STEP_RUNNING,
    STEP_COMPLETED,
    COMPLETED,
    FAILED,
    CANCELLED
}

enum class ErrorStrategy { RETRY, SKIP, ABORT, FALLBACK }

sealed class WorkflowStep {
    abstract val id: String
    abstract val dependsOn: List<String>
    abstract val status: StepStatus

    data class ExecuteTool(
        override val id: String,
        override val dependsOn: List<String>,
        override val status: StepStatus,
        val toolId: String,
        val params: JsonObject
    ) : WorkflowStep()

    data class RunAgent(
        override val id: String,
        override val dependsOn: List<String>,
        override val status: StepStatus,
        val agentType: String,
        val goal: String
    ) : WorkflowStep()

    data class Condition(
        override val id: String,
        override val dependsOn: List<String>,
        override val status: StepStatus,
        val condition: String,
        val ifTrue: List<String>,
        val ifFalse: List<String>
    ) : WorkflowStep()

    data class WaitForApproval(
        override val id: String,
        override val dependsOn: List<String>,
        override val status: StepStatus,
        val message: String
    ) : WorkflowStep()

    data class Iterative(
        override val id: String,
        override val dependsOn: List<String>,
        override val status: StepStatus,
        val bodySteps: List<String>,
        val maxIterations: Int,
        val convergenceCondition: String?
    ) : WorkflowStep()
}

enum class StepStatus {
    PENDING,
    RUNNING,
    COMPLETED,
    FAILED,
    SKIPPED
}
```

## Lifecycle and Step Semantics

`status` is the durable workflow lifecycle projection aligned to [state-machines/WorkflowLifecycle.md](../state-machines/WorkflowLifecycle.md). Step execution details are subordinate runtime state and MUST NOT replace workflow lifecycle state. Workflow transition events MUST be deduplicated by `(workflowId, version, transition)`.

### Operational Traversal and Branching

- The engine evaluates step readiness topologically using the step dependencies (`dependsOn`).
- Independent parallel lanes run concurrently in separate coroutine scopes.
- Workflow cancellation or catastrophic step failures without fallback trigger rolling cascading aborts of all active children, transitioning the overall status to `FAILED` or `CANCELLED` and releasing resource locks.

### Cross-Layer Contract Projection

- `WaitForApproval` uses the existing PermissionModel approval transaction and audit contract. Approval denial and approval expiry retain the existing Task/Agent effects and canonical `NXR-2003` mappings; they do not create a new Workflow state, permission scope, error identity, or automatic retry path. The step completes only after the authorized operation produces a valid result under its existing acceptance conditions.
- `RETRY`, `SKIP`, `ABORT`, and `FALLBACK` select workflow graph behavior only. Canonical error identity, Task/Execution lifecycle effects, Tool/Provider retry legality, operation idempotency, effective deadlines, cancellation, and checkpoint persistence remain governed by their owning authorities. Workflow retry and iteration progress must not reset parent retry budgets, deadlines, failure lineage, or execution identity.
- A Tool step with `UNKNOWN_COMPLETION` remains unresolved until Tool System reconciliation resolves the side effect. The model must not project that step as successful, skipped, or safely replayable solely because a timeout or transport interruption occurred.
- Dependency validation rejects unbounded or ambiguous cycles. Bounded cycles are represented only by `Iterative` steps with the existing `maxIterations` and/or `convergenceCondition` fields.
