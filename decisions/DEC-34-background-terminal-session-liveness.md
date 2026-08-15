# DEC-34 — Background Terminal Session Liveness

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Liveness, deadline binding, cancellation, restart, and orphan cleanup for background terminal sessions.

## Problem

The terminal specification permits `run_background` sessions to remain `Running` or `Detached` until process exit or workspace shutdown, while the derived `TerminalSession` model does not carry a required Task or Execution identity. That leaves a possible background process without a documented deadline, cancellation owner, or deterministic reclamation path.

## Decision

Every background terminal invocation created through an agent or Task execution MUST be bound to the creating `taskId`, `executionId`, `workspaceId`, and `correlationId`. The binding is execution metadata and does not create a new TerminalSession lifecycle state.

The background terminal session inherits the parent Task’s immutable effective deadline. The deadline cannot be renewed by the terminal session, and expiry MUST initiate the existing cancellation/termination path, capture recoverable checkpoint state when the terminal contract permits it, and produce the existing terminal execution outcome. A background session cannot outlive a cancelled, terminal, or deadline-expired parent execution.

A background terminal session created without a parent Task or Execution is not an agent-execution operation and is outside the autonomous background capability. Such a request is rejected before process creation through the existing authorization/validation boundary. The documentation does not create a separate user-owned indefinite-process mode.

On app restart, the persisted parent Execution and TerminalSession records are authoritative. A recoverable session resumes only through the existing `Detached → Attached → Running` restore path. If the parent execution is terminal, missing, cancelled, or deadline-expired, the session is terminated and transitions to the existing terminal `Closed` or `Failed` outcome according to the terminal failure contract.

An idempotent cleanup worker MUST reconcile background sessions whose parent execution is terminal, missing, or expired. Cleanup is a recovery operation, not a new lifecycle state; it records the existing terminal session event, process outcome, correlation ID, and audit disposition before removing the orphan process or marking cleanup failure.

## Ownership

The Task/Execution lifecycle owns the parent deadline, cancellation, and business outcome. The TerminalSession lifecycle owns terminal session state. The terminal execution specification owns process termination, checkpoint, restore, and resource-release mechanics. The background scheduler owns reconciliation scheduling. No owner is inferred from the terminal session alone.

## Invariants

A background process cannot continue after parent deadline exhaustion or committed parent cancellation. No new `Suspended`, `Restored`, `Orphaned`, or cleanup lifecycle state is created. `Detached` with `suspended=true` remains the only suspended representation. Financial cost or internal credit is never used as a termination gate. Unknown completion remains unresolved until the existing Tool System reconciliation contract resolves it.

## Required projections

Update `models/TerminalSession.md`, `specs/TERMINAL.md`, `specs/BACKGROUND_EXECUTION.md`, `state-machines/TerminalSessionLifecycle.md` only where the existing state contract needs a reference, `architecture/RUNTIME.md`, `docs/api/Runtime-API.md`, database schema projections, security/permission escalation projections, traceability, the completeness inventory, and planned background-terminal tests. Existing DEC files are not modified.

## Validation obligations

Planned evidence must cover parent-deadline expiry, cancellation propagation, app restart, workspace shutdown, missing-parent reconciliation, duplicate cleanup, process termination failure, checkpoint restore, resource release, audit persistence, and rejection of unbound autonomous background sessions.
