# DEC-33 — Task Liveness Error Identities

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Error identities for Task dependency validation, unsatisfied dependencies, and effective-deadline expiry selected by DEC-30.

## Problem

DEC-30 selected Task dependency validation, failed-dependency propagation, and effective-deadline expiry, but the supporting projections referred to unnamed dependency-resolution and task-deadline error envelopes. The canonical error envelope requires a stable `NXR-####` identity at every protocol, API, persistence, background-worker, and audit boundary. No existing catalog entry precisely identifies these Task liveness conditions.

## Decision

The following unused core-runtime identities are added to the canonical error catalog and are reserved for the stated conditions:

1. `NXR-1014` — **Task dependency invalid**. Category: `Client`. This error means that a Task contains an unknown dependency reference or a dependency cycle discovered before queueing. The Task lifecycle remains unchanged, the Task is not queued, and the caller must correct the dependency graph. It is not used for a dependency that later reaches terminal failure.

2. `NXR-1015` — **Task dependency unsatisfied**. Category: `Server`. This error means that a referenced dependency reached terminal `FAILED` or `CANCELLED`, making the dependent Task unsatisfiable. The dependent Task transitions through the existing `Failed` effect, does not retry the failed dependency automatically, and remains attributable to the dependency failure in its structured details.

3. `NXR-1016` — **Task deadline expired**. Category: `Infrastructure`. This error means that a Task’s immutable effective deadline was reached while the Task was `Pending`, `Blocked`, `BlockedAwaitingInput`, waiting for approval, or waiting for a provider rate-limit delay. The owning Task/Execution lifecycle commits the existing `Failed` effect, checkpoints recoverable state where applicable, and does not automatically renew the deadline or retry budget.

These identities are error-catalog identities only. The Task lifecycle continues to own legal state effects; the operation owner continues to own idempotency and retry conditions; and boundary adapters continue to serialize and redact the canonical envelope without reinterpretation.

## Invariants

No new Task, Execution, Agent, Provider, Tool, or approval lifecycle state is created. Invalid dependency references and cycles leave the Task unchanged. Failed dependencies do not cause automatic retry of the failed dependency. Deadline expiry cannot silently approve, resume, renew, or reset a Task. Existing `NXR-2003` approval denial and expiry subreasons remain unchanged.

## Required projections

The error catalog, Task lifecycle, Task model, Runtime architecture, execution lifecycle specification, background execution specification, Runtime and Agent API error mappings, database/protocol error projections, traceability, completeness inventory, regression tests, and changelog must reference these identities consistently. Existing DEC files are not modified.

## Validation obligations

Documentation and planned evidence must verify invalid-reference rejection, cycle rejection, failed-dependency propagation, deadline expiry in each bounded wait state, parent-deadline provider waiting, no deadline renewal, stable correlation and persistence, and absence of automatic retry. Tests must assert the exact canonical code and lifecycle effect.
