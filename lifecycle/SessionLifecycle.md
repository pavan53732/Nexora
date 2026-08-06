> **Status: SUPPORTING** for session lifecycle narrative.
> This document describes session lifecycle in prose. The canonical Session state
> machine is [../state-machines/SessionLifecycle.md](../state-machines/SessionLifecycle.md).
> All Session state names and transitions defined here are projections of the
> canonical state machine; the state machine is authoritative.
>
> Depends on: [../state-machines/SessionLifecycle.md](../state-machines/SessionLifecycle.md),
> [../architecture/RUNTIME.md](../architecture/RUNTIME.md).

# Session Lifecycle Narrative — Nexora

## Canonical States

The canonical Session states are defined by `state-machines/SessionLifecycle.md`:

`CREATED`, `ACTIVE`, `IDLE`, `CLOSED`, `EXPIRED`

## Behavior Narrative

### Created → Active

A Session is created with a durable identity in Room. When a user or agent first attaches context (workspace loaded, goal set), the Session transitions to `ACTIVE`. The Session is the durable context container, not a substitute for Task or Execution state.

### Active ↔ Idle

When no active Task or agent interaction exists within the configured idle timeout, the Session transitions to `IDLE`. Context is retained — memory, workspace state, and checkpoint remain available. Resuming the Session (user returns, agent starts a new Task) transitions back to `ACTIVE`.

### Active → Closed

When the user explicitly closes the Session, active Tasks are detached or completed per Task lifecycle rules. The Session transitions to `CLOSED` and is terminal.

### Idle → Closed

An idle Session may be explicitly closed without Task interaction. Transition to `CLOSED` is terminal.

### Idle → Active

A user returning to an idle Session triggers checkpoint restoration and transition to `ACTIVE`.

### Expiration

- `CREATED → EXPIRED`: Sessions with no activity within the initial TTL expire.
- `ACTIVE → IDLE`: Idle timeout expires while no Task is active.
- `IDLE → EXPIRED`: Retention TTL expires for idle Sessions.
- A pending non-terminal Task blocks `ACTIVE → EXPIRED` unless cancelled first.

### Terminal States

`CLOSED` and `EXPIRED` are terminal. Reopening creates a new Session identity.

## Invariants

1. Session state never replaces Task or Execution state.
2. Task completion does not imply Session closure.
3. Task failure does not create a Session `FAILED` state — Task failure is tracked in Task lifecycle, not Session lifecycle.
4. Every transition emits session identity, workspace identity, prior state, new state, version, and timestamp.

## Dependencies

- `state-machines/SessionLifecycle.md` — canonical state machine.
- `models/Session.md` — Session domain model.
- `docs/LIFECYCLES.md` — session lifecycle overview.
- `docs/CANONICAL_SOURCES.md` — ownership declaration.
