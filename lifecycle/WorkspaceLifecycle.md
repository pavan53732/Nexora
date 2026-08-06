> **Status: DERIVED** for workspace lifecycle narrative.
> This document describes workspace lifecycle in prose. The canonical state machine
> definition is owned by [../state-machines/WorkspaceLifecycle.md](../state-machines/WorkspaceLifecycle.md).
> This file must not be treated as an alternate source of truth for any state enum.
>
> Depends on: [../state-machines/WorkspaceLifecycle.md](../state-machines/WorkspaceLifecycle.md).

# Workspace Lifecycle Authority — Nexora

## States

`Created`, `Active`, `Suspended`, `Archived`, `Deleted`

## Rules

Workspace lifecycle is the durable authority for workspace availability and ownership context. Task, session, execution, and terminal activity may occur within a workspace but MUST NOT replace workspace lifecycle state.

## Transition Minimums

Every durable transition SHOULD emit workspace identity, prior state, new state, correlation reference when applicable, version, and timestamp.

## Expanded Lifecycle Specification (S3 — Option A)

### States (detailed)
- `Created`: Workspace initialized; no active agents; sandbox clean; settings default.
- `Active`: Workspace has running agents, tasks, or background execution; resources allocated.
- `Suspended`: Workspace paused (user request or budget exhaustion); state preserved; no active execution.
- `Archived`: Workspace frozen; read-only; no execution; data retained per retention policy.
- `Deleted`: Workspace removed; sandbox cleaned; data deleted or archived per policy.

### Transitions
- `Created → Active`: First agent/task/background execution starts.
- `Active → Suspended`: User suspends; budget limit reached (`FR-AS-003`); heartbeat failure (`FR-AS-002`).
- `Suspended → Active`: User resumes; budget restored.
- `Active/Active → Archived`: User archives; automatic archive after user-initiated action or inactivity policy (see WorkspaceLifecycle state machine).
- `Archived → Deleted`: User deletes; automatic deletion after retention period expires.

### Lifecycle Authorities
- `WorkspaceLifecycle.md` (this file) — canonical state machine.
- `state-machines/WorkspaceLifecycle.md` — canonical state machine (Created/Active/Suspended/Archived/Deleted).
- this file — thin lifecycle authority / narrative reference.
- `docs/LIFECYCLES.md` — overview referencing this document.
- `docs/MODULE_BOUNDARIES.md` — workspace module boundary (runtime ownership).
- `models/Workspace.md` — workspace model (`Workspace.md` updated with `maxConcurrency` per S1).
