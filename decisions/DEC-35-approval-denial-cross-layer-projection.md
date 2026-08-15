# DEC-35 — Approval Denial Cross-Layer Projection

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Composition of Tool authorization outcomes with Task and Agent lifecycle projections.

## Problem

The Tool contract returns `NXR-2003` for authorization denial, DEC-30 maps Task approval denial and approval expiry to `TaskLifecycle.WaitingApproval → Failed`, and AgentLifecycle separately maps `WaitingApproval → Paused`. The repository did not state how these independent projections compose when an Agent is executing a Task whose Tool approval transaction is denied or expires.

## Decision

The authorization result remains owned by the Tool/Permission boundary. `NXR-2003` and its subreason remain the canonical error identity and denial meaning.

The Task projection is authoritative for the operation outcome:

- `USER_DENIED` commits the existing Task `Failed` effect.
- `POLICY_DENIAL` from approval expiry commits the existing Task `Failed` effect.
- No automatic retry, bypass, silent approval, or deadline renewal is permitted.

The Agent projection is independent and reflects execution availability rather than replacing the Task outcome:

- The Agent may transition `WaitingApproval → Paused` after denial or expiry so the stable Agent remains available for later user-directed work.
- The Agent MUST NOT transition to `Running` for the denied Tool operation, and it MUST NOT report the Task as successful.
- A later user-directed operation may resume or start the Agent only through the existing Agent guards and a new authorization attempt. The denied Task is not resumed under the same approval transaction.

The ToolInvocation projection remains a denied/non-success result with no Tool side effect. The activity feed, notification, correlated trace, permission audit, Task history, and Agent status event MUST preserve the same approval transaction, denial subreason, Task failure, Agent pause projection, and final disposition.

## Ownership and recovery

The PermissionModel owns permission resolution and approval transaction validity. The Tool System owns the no-side-effect authorization barrier and ToolInvocation result. TaskLifecycle owns Task terminal effect. AgentLifecycle owns Agent availability state. Runtime orchestration correlates these projections but does not replace any lifecycle authority. Recovery is a new user-directed operation and a new authorization attempt; it is not an automatic retry of the denied call.

## Invariants

No new lifecycle state, permission scope, Tool identity, or error code is created. Task failure and Agent pause are not equivalent states and must not be collapsed. A denied Tool call cannot produce a successful Tool result, Task completion, or final user-facing success claim. Existing classifier and blocked-list final-denial rules remain unchanged.

## Required projections

Update `state-machines/AgentLifecycle.md`, `state-machines/TaskLifecycle.md` only with cross-layer references, `docs/api/Tool-API.md`, `protocols/Tool-Protocol.md`, `protocols/Agent-Protocol.md`, `architecture/RUNTIME.md`, `security/PermissionModel.md` only where needed to reference the composition, UI/activity-feed and notification projections, traceability, completeness inventory, and approval/cancellation tests. Existing DEC files are not modified.

## Validation obligations

Planned evidence must verify user denial, approval expiry, policy denial, classifier denial, blocked-list denial, no Tool side effect, Task `Failed`, Agent `Paused`, no automatic retry, new authorization transaction on later user action, audit correlation, notification, and non-success finalization.
