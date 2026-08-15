# DEC-30 — Agent Loop Liveness and Retry Bounds

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Task dependency liveness, approval and clarification waits, Agent failure retry identity, provider rate-limit waiting, delegation depth, and the already-corrected stream/tool liveness contracts.

## Problem

The canonical documents define many local progress controls but left several cross-state liveness boundaries unresolved. This decision closes those boundaries without creating new lifecycle states, collapsing Task/Execution/Agent/Provider/Tool ownership, weakening security, or introducing internal credit/cost gating.

## Decision

### 1. Task dependency graph and blocked work

Task dependency graphs MUST be acyclic and MUST be validated before a task becomes `Queued`. An invalid dependency reference or cycle is rejected without mutating the Task lifecycle. A dependency that reaches terminal `FAILED` or `CANCELLED` makes a dependent task unsatisfiable; the dependent task transitions to existing `FAILED` with the canonical dependency-resolution error envelope and does not automatically retry the failed dependency.

A Task in `Pending` or `Blocked` inherits its immutable effective deadline. If the dependency or resource condition is not resolved before that deadline, the Task transitions to existing `FAILED` with the canonical task-deadline error envelope. Dependency completion or explicit resource release remains the only normal `Blocked → Running` path. The Workflow graph validator is not reused as Task authority; the Task scheduler owns Task dependency validation and readiness.

### 2. Approval denial and clarification expiry

`WaitingApproval` is a legitimate external wait. Approval transitions the Task to `Running`; explicit user denial transitions the Task to existing `FAILED` with `NXR-2003` and denial subreason `USER_DENIED`; automatic retry is not allowed. An expired approval transaction transitions the Task to existing `FAILED` with `NXR-2003` and denial subreason `POLICY_DENIAL`; it does not silently approve, retry, or bypass the permission gate.

`BlockedAwaitingInput` remains the clarification/capability-gap state. `resolveEscalation(answer)` resumes the same execution from its checkpoint. If the effective deadline expires before an answer arrives, the Task transitions to existing `FAILED` with the canonical task-deadline error envelope. Neither state creates a new lifecycle state.

The approval transaction, denial/expiry reason, question or requested capability, deadline, checkpoint, and final disposition are persisted and projected through the existing audit, correlated trace, notification, and activity-feed contracts.

### 3. Agent failure and retry identity

`AgentStatus.FAILED` is terminal for the current runtime incarnation. `retry()` does not mutate a committed failed execution back to active execution. It creates a new runtime incarnation using the same stable registered `agentId`, increments the Agent version, creates or references a new `executionId`, and preserves the failed predecessor through existing prior-execution/correlation linkage. The new incarnation enters `READY` only after its startup guards pass.

A Task or Execution retry is governed by Task/Execution lifecycle and does not imply an Agent lifecycle retry. Agent failure caused by a runtime crash and task failure caused by an operation error remain distinct outcomes.

### 4. Provider rate-limit waiting

Provider `Retry-After` remains a provider-layer signal and does not create a new Task or Provider lifecycle state. The Provider layer parses a valid non-negative delay and schedules the request no later than the parent Task effective deadline. Missing, invalid, or repeatedly renewed delays use the configured bounded backoff policy and the remaining parent deadline; they MUST NOT create an unbounded queue.

When the parent deadline is exhausted before a request can safely run, the request is removed from the pending retry queue, recoverable state is checkpointed, and the owning Task/Execution receives the existing task-deadline error envelope. Internal credit or financial-cost gating is not introduced.

### 5. Delegation depth

Delegation depth is a bounded coordination parameter, not a lifecycle state. The root task has depth `0`; each delegated child has parent depth plus one. The maximum active delegation depth is `4`. A request beyond that bound is rejected with existing coordination failure semantics (`NXR-3011`), recorded in the correlated trace, and returned to the parent for re-planning. The parent deadline, concurrency cap, duplicate-scope prevention, and deadlock watchdog remain independently enforced.

### 6. Stream and Tool liveness bindings

The canonical ProviderStream lifecycle includes the bounded `STALLED → RECONNECTING` failover transition. NXR-2002 Tool timeout handling preserves `UNKNOWN_COMPLETION` until reconciliation and permits retry only when the operation's idempotency and retry policy authorize it. `RetryPending → Running` requires elapsed backoff and TaskScheduler authorization. Agent `Completing → Completed` requires the explicit finalization guard. Stream failure/cancellation, denied Tool calls, missing committed drafts, and unsatisfied completion gates route through existing non-success effects rather than successful completion synthesis.

## Invariants

No new Task, Agent, Execution, Provider, Tool, or approval lifecycle state is created. Terminal Execution identities remain immutable. Approval and classifier denial remain fail-closed. Unknown completion is never converted into success or failure before reconciliation. Child operations cannot outlive the parent deadline. Delegation does not grant permissions, mutate the static capability matrix, or bypass sandbox/security policy.

## Required projections

The following documents MUST reflect this decision: `state-machines/TaskLifecycle.md`, `state-machines/AgentLifecycle.md`, `state-machines/ProviderStreamLifecycle.md`, `architecture/AGENT_RUNTIME.md`, `architecture/RUNTIME.md`, `architecture/MULTI_AGENT_SYSTEM.md`, `security/PermissionModel.md`, `specs/EXECUTION_LIFECYCLE.md`, `specs/BACKGROUND_EXECUTION.md`, `protocols/Execution-Protocol.md`, `docs/api/Tool-API.md`, `errors/ERROR_CODES.md`, `models/Task.md`, `models/Agent.md`, `testing/*`, `docs/TRACEABILITY.md`, and the active completeness inventory.

## Validation obligations

Implementation and planned evidence must cover dependency-cycle rejection, failed-dependency propagation, blocked deadline expiry, approval denial and expiry, clarification deadline expiry, Agent incarnation retry, Retry-After queue bounds, delegation-depth rejection, stream stall failover, unknown-completion reconciliation, RetryPending backoff, finalization, and non-success routing. Documentation presence is not executed evidence.
