> **Status: SUPPORTING** for agent lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/AgentLifecycle.md](../state-machines/AgentLifecycle.md).**
> This file describes the agent lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/AgentLifecycle.md](../state-machines/AgentLifecycle.md).

# Agent Lifecycle Authority — Nexora

## States

`CREATED`, `CONFIGURED`, `READY`, `RUNNING`, `PAUSED`, `WAITING_APPROVAL`, `REFLECTING`, `COMPLETING`, `COMPLETED`, `FAILED`, `CANCELLED`

## Transitions

- `CREATED → CONFIGURED`: Agent initialized with configuration.
- `CONFIGURED → READY`: Agent ready to accept tasks.
- `READY → RUNNING`: Task started.
- `RUNNING → PAUSED`: Pause requested.
- `PAUSED → RUNNING`: Resume requested.
- `RUNNING → WAITING_APPROVAL`: Approval gate reached.
- `WAITING_APPROVAL → RUNNING`: Approval granted.
- `RUNNING → REFLECTING`: Reflection phase started.
- `REFLECTING → RUNNING`: Reflection complete.
- `RUNNING → COMPLETING`: Task completion in progress.
- `COMPLETING → COMPLETED`: Task finished successfully.
- `* → FAILED`: Unrecoverable error.
- `* → CANCELLED`: Cancellation requested.