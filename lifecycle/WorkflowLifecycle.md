> **Status: SUPPORTING** for workflow lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/WorkflowLifecycle.md](../state-machines/WorkflowLifecycle.md).**
> This file describes the workflow lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/WorkflowLifecycle.md](../state-machines/WorkflowLifecycle.md).

# Workflow Lifecycle Authority — Nexora

## States

`DEFINED`, `VALIDATED`, `RUNNING`, `PAUSED`, `STEP_PENDING`, `STEP_RUNNING`, `STEP_COMPLETED`, `COMPLETED`, `FAILED`, `CANCELLED`

### Step Sub-States

Each step tracks: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `SKIPPED`

## Transitions

- `DEFINED → VALIDATED`: Graph validated (no invalid cycles).
- `VALIDATED → RUNNING`: Execution started.
- `RUNNING → PAUSED`: Pause requested.
- `PAUSED → RUNNING`: Resume requested; pending steps exist.
- `RUNNING → STEP_RUNNING`: Step starts (upstream deps completed).
- `STEP_RUNNING → STEP_COMPLETED`: Step finished successfully.
- `STEP_COMPLETED → STEP_PENDING`: Next step eligible.
- `STEP_COMPLETED → COMPLETED`: No pending steps remain.
- `STEP_RUNNING → FAILED`: Step failed; no error handler.
- `STEP_RUNNING → STEP_RUNNING`: Fallback edge exists; alternates available.
- `STEP_COMPLETED → STEP_RUNNING`: Iterative step has remaining iterations.
- `* → CANCELLED`: Cancellation requested.

### Iteration Control

`Iterative` steps carry `maxIterations` and optional `convergenceCondition`. The engine increments the counter and re-evaluates downstream readiness only when the condition is met or the limit is reached.