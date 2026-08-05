> **Status: DERIVED** for session lifecycle narrative.
> This document describes session lifecycle in prose. No standalone state-machine
> companion exists for Session — session state is tracked inline through the
> runtime module. Any state names used below are descriptive prose, not formal enums.
>
> Depends on: [../architecture/RUNTIME.md](../architecture/RUNTIME.md).

# Session Lifecycle Authority — Nexora

## States

`Created`, `Active`, `Idle`, `Closed`, `Expired`

## Rules

Session lifecycle is the durable authority for session context availability. Active task or agent references are subordinate runtime associations and MUST NOT replace session lifecycle state.

## Transition Minimums

Transitions SHOULD emit session identity, workspace identity, prior state, new state, version, and timestamp.

## Expanded Lifecycle Specification (S3 — Option A)

### States
`Initiated`, `Active`, `Paused`, `Completed`, `Failed`, `Restored`

### Transitions
- `Initiated → Active`: User or agent starts session; workspace context loaded.
- `Active → Paused`: User pauses; checkpoint saved (`FR-AS-001`, `FR-AS-002`).
- `Paused → Active`: User resumes; checkpoint restored (`FR-AS-013` exactly-once recovery).
- `Active → Completed`: Session goal achieved; results aggregated; evidence validated (`FR-EV-006`).
- `Active → Failed`: Unrecoverable error; error strategy applied (`FR-EL-007`); audit logged.
- `Failed/Completed → Restored`: Session state reconstructed from checkpoint + memory (`FR-AS-013`).

### Dependencies
- `docs/LIFECYCLES.md` — session lifecycle overview.
- `models/Session.md` — session model.
- `protocols/Agent-Protocol.md` — session context in protocol.
