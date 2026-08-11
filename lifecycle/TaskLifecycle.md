> **Status: SUPPORTING** for task lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md).**
> This file describes the task lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md).

# Task Lifecycle Authority — Nexora

## States

`DRAFT`, `PENDING`, `QUEUED`, `RUNNING`, `BLOCKED`, `WAITING_APPROVAL`, `COMPLETED`, `FAILED`, `CANCELLED`, `RETRY_PENDING`

## Transitions

This supporting narrative summarizes the canonical transitions in
[state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md); it does not redefine
ownership, guards, or state semantics.

- `DRAFT → PENDING`: Task submitted.
- `PENDING → QUEUED`: Dependencies are satisfied and the Task is enqueued.
- `QUEUED → RUNNING`: `start()` is accepted by the canonical guard.
- `RUNNING → BLOCKED`: Dependency or resource blocking occurs.
- `BLOCKED → RUNNING`: The canonical unblock condition is satisfied.
- `RUNNING → WAITING_APPROVAL`: An approval gate is reached.
- `WAITING_APPROVAL → RUNNING`: Approval is granted.
- `RUNNING → COMPLETED`: The result is validated.
- `RUNNING → FAILED`: The error is non-retryable.
- `RUNNING → RETRY_PENDING`: The error is retryable and retry policy permits it.
- `RETRY_PENDING → QUEUED`: Ordinary retry backoff elapses, or the distinct DEC-7 process-death recovery reconciliation succeeds; the latter preserves the existing Execution and is not ordinary retry.
- `* → CANCELLED`: Cancellation is accepted by the canonical guard.