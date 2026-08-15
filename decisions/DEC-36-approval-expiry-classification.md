# DEC-36 — Approval-Expiry Classification Under NXR-2003

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Classification of an approval transaction that reaches expiry before a valid approval outcome is committed.

## Problem

The repository already establishes one NXR-2003 authorization-denial identity and uses existing Task and Agent lifecycle effects for approval expiry. The error catalog defines `POLICY_DENIAL` as an effective policy `DENY`, while DEC-30 and DEC-35 project an expired approval transaction to `NXR-2003 / POLICY_DENIAL`. The repository also requires audit, trace, notification, and activity-feed projections to preserve the expiry cause and distinguish expired from explicitly denied outcomes.

## Decision

An approval transaction that expires before a valid approval outcome is committed is classified as an authorization-gate denial under the existing `NXR-2003 / POLICY_DENIAL` projection. For this specific authorization-gate outcome, `POLICY_DENIAL` means that the requested Tool call did not obtain an effective authorization decision before the approval transaction deadline; it does not mean that the user explicitly rejected the approval, and it does not change the meaning of an effective policy `DENY` when that policy decision is the direct cause.

`USER_DENIED` remains reserved for an explicit user rejection of an `ASK` approval. `MALFORMED_APPROVAL` remains reserved for invalid approval-transaction structure or correspondence. No new NXR top-level error code or NXR-2003 subreason is created.

## Cross-layer effects

The existing cross-layer effects remain unchanged:

- The Tool/Permission boundary returns `NXR-2003` with the applicable denial subreason and executes no Tool side effect.
- The owning Task commits `WaitingApproval → Failed`.
- The participating Agent may project `WaitingApproval → Paused` to remain available for later user-directed work; this does not resume or alter the failed Task.
- No automatic retry, silent approval, bypass, deadline renewal, or reuse of the expired transaction is permitted.
- Later work requires a new authorization transaction and follows the existing authorization gates.

## Observability and persistence

The expiry cause remains distinct from explicit denial in the existing approval transaction, denial/expiry reason, execution history, permission audit trail, correlated trace, notification, activity-feed, Task history, Agent status, and final-disposition projections. This distinction is an observability and provenance requirement; it does not create a new lifecycle state or error identity.

## Ownership

The PermissionModel owns permission resolution and approval-transaction validity. The Tool System owns the no-side-effect authorization barrier and ToolInvocation result. The error catalog owns `NXR-2003` identity and shared recovery metadata. TaskLifecycle owns the Task terminal effect. AgentLifecycle owns Agent availability state. Runtime orchestration correlates these projections without replacing any lifecycle authority.

## Invariants

No new Task, Agent, Execution, Tool, or approval lifecycle state is created. No existing Task or Agent transition changes. No new permission scope, Tool identity, API operation, protocol message, persistence identity, retry path, or recovery path is introduced. Existing DEC-30 and DEC-35 decisions remain immutable and are reconciled by this later, narrow classification decision without rewriting them.

## Required projections

The error catalog, PermissionModel, active approval/authorization projections, API and protocol documentation, completeness inventory, traceability, decision log, and planned approval tests MUST use the classification and distinctions defined here. Existing TaskLifecycle and AgentLifecycle state effects remain authoritative and require no new transition.

## Validation obligations

Planned evidence must verify policy denial, explicit user denial, approval expiry, malformed approval, classifier denial, no Tool side effect, Task `Failed`, optional Agent `Paused`, distinct audit/activity outcomes, no automatic retry, and new-transaction-only continuation.

## Compatibility

This decision preserves the existing NXR-2003 umbrella, DEC-30 and DEC-35 cross-layer effects, PermissionModel fail-closed behavior, Task and Agent lifecycle topology, and all existing authorization and recovery boundaries. It resolves only the semantic interpretation of the already-selected approval-expiry projection.
