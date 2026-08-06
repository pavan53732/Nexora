> **Status: CANONICAL** for Session lifecycle states and transitions.
> This document owns Session states, valid transitions, transition guards,
> and lifecycle events. The prose lifecycle narrative in
> [lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md) is SUPPORTING.
>
> Depends on: [../architecture/RUNTIME.md](../architecture/RUNTIME.md).
> Referenced by: [../models/Session.md](../models/Session.md), [../docs/LIFECYCLES.md](../docs/LIFECYCLES.md).

# Session Lifecycle State Machine — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## States

```
CREATED
ACTIVE
IDLE
CLOSED
EXPIRED
```

## State Definitions

| State | Description |
|---|---|
| `CREATED` | Durable Session record exists; no active interaction attached. |
| `ACTIVE` | Session has active interaction or runtime context. |
| `IDLE` | Session remains available but has no active task or agent interaction. Context is retained. |
| `CLOSED` | Session was explicitly closed by the user or agent; terminal. |
| `EXPIRED` | Session exceeded the configured retention or inactivity limit; terminal. |

## Transitions

| Trigger | From | To | Guard |
|---|---|---|---|
| `start` | `CREATED` | `ACTIVE` | Workspace context loaded |
| `start` | `IDLE` | `ACTIVE` | Checkpoint restored |
| `close` | `CREATED` | `CLOSED` | None |
| `close` | `ACTIVE` | `CLOSED` | Active Tasks detached or completed; active Executions drained or cancelled |
| `close` | `IDLE` | `CLOSED` | None |
| `idleTimeout` | `CREATED` | `EXPIRED` | No activity within TTL |
| `idleTimeout` | `ACTIVE` | `IDLE` | No active task; configured idle TTL elapsed |
| `idleTimeout` | `IDLE` | `EXPIRED` | Configured retention TTL elapsed |
| `expireNow` | `CREATED` | `EXPIRED` | Authorized admin/system actor |
| `expireNow` | `IDLE` | `EXPIRED` | Authorized admin/system actor |
| `expireNow` | `ACTIVE` | `EXPIRED` | Authorized actor AND no active nonterminal Task/Execution; otherwise cancel or detach first |

## Terminal States

`CLOSED` and `EXPIRED` are terminal. No transition exits a terminal state. Reopening a terminal Session creates a new Session identity.

## Invariants

1. Session state does **not** replace Task state.
2. Session state does **not** replace Execution state.
3. Task completion does not imply Session closure.
4. Task failure does not create a Session `FAILED` state.
5. Closing an `ACTIVE` Session must detach or complete active Task and Execution references (per Task lifecycle and Execution lifecycle rules).
6. Expiration from `ACTIVE` must first detach or complete active Tasks; a pending non-terminal Task blocks the `ACTIVE → EXPIRED` transition unless cancellation is executed first.
7. Expiration from `IDLE` does not require Task detachment (IDLE by definition has no active task).

## Transition Events

Every transition emits a lifecycle event carrying:

- `sessionId`
- `workspaceId`
- `priorState`
- `newState`
- `version`
- `correlationId` (when present)
- `occurredAt`
- `trigger`
- `actor`

Durable commit occurs before lifecycle-event publication. Events are at-least-once; consumers deduplicate by `(sessionId, version)`.

## Invalid Transition Contract

An invalid transition returns a canonical error without changing persisted state. The error identifies: current state, requested trigger, sessionId, correlationId.

## Implementation Notes

The lifecycle is enforced by `SessionStateMachine` in the core module. Guards are evaluated synchronously. Session state is persisted in Room with versioned optimistic concurrency — a conflicting version on commit returns a canonical error.
