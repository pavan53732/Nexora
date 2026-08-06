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

- `DRAFT → PENDING`: Task created and queued.
- `PENDING → QUEUED`: Resources available, scheduled.
- `QUEUED → RUNNING`: Execution started.
- `RUNNING → BLOCKED`: Dependency/resource unavailable.
- `BLOCKED → QUEUED`: Blockage resolved.
- `RUNNING → WAITING_APPROVAL`: Approval gate reached.
- `WAITING_APPROVAL → RUNNING`: Approval granted.
- `RUNNING → COMPLETED`: Task finished successfully.
- `RUNNING → FAILED`: Unrecoverable error.
- `FAILED → RETRY_PENDING`: Retry scheduled.
- `RETRY_PENDING → QUEUED`: Retry triggered.
- `* → CANCELLED`: Cancellation requested.