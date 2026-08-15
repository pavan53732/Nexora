# DEC-31 — BranchLineage and Checkpoint Operational Policy

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Concrete operational policy within the semantic safety rules already established by DEC-22 and DEC-23.

## Problem

DEC-22 assigns rollback parent/source lineage to the distinct BranchLineage artifact, and DEC-23 defines safe checkpoint expiration, deletion, quota, and cleanup guards. The remaining documentation boundary is the operational identity, lifecycle, retention, quota, cleanup, and dependency behavior needed for implementation handoff.

## Decision

### 1. BranchLineage identity and ownership

BranchLineage is a first-class persisted artifact with a stable domain-prefixed identifier `BRANCH-###` or an implementation-equivalent stable identifier that preserves uniqueness and immutable identity. The BranchLineage artifact owns the relationship between source Conversation, source checkpoint, and branch Conversation. It does not own Conversation content, checkpoint content, execution state, or workspace file history.

### 2. BranchLineage lifecycle

BranchLineage uses the following lifecycle states: `RECORDED`, `ACTIVE`, `DETACHED`, and `DELETED`.

`RECORDED` means the source/checkpoint/branch relationship is durably recorded before branch success is observable. `ACTIVE` means the branch remains linked to the source lineage. `DETACHED` means the branch no longer requires the source checkpoint for normal operation, but the lineage record remains available for audit and history. `DELETED` is terminal and is permitted only after retention and audit obligations are satisfied.

A BranchLineage dependency prevents physical deletion of its source checkpoint while the lineage is `RECORDED` or `ACTIVE`. Detaching is an explicit successful branch-preservation operation; it does not delete or mutate the source Conversation or branch Conversation.

### 3. Retention and cleanup

Conversation checkpoints use the existing `Created → Superseded → Expired/Invalidated` lifecycle. The default operational retention is 30 days after a checkpoint becomes `Superseded`, while the latest `Created` checkpoint for an active Conversation remains retained. A checkpoint with a `RECORDED` or `ACTIVE` BranchLineage is not physically deleted even after the normal retention window; it becomes eligible only after the BranchLineage is `DETACHED` or `DELETED`, required audit retention is satisfied, and the checkpoint is `Expired` or `Invalidated`.

Cleanup runs as an idempotent daily WorkManager job under existing background constraints. It rechecks eligibility transactionally, records an audit event for every deletion or protected skip, and never deletes a source Conversation, branch Conversation, or active BranchLineage as a side effect.

### 4. Quota and storage pressure

The default per-workspace checkpoint quota is 100 retained checkpoints, with the latest active Conversation checkpoint and all checkpoints protected by `RECORDED` or `ACTIVE` BranchLineage excluded from deletion candidates. A quota rejection occurs before durable checkpoint creation and leaves existing checkpoints, Conversations, and lineage unchanged. Under storage pressure, cleanup may first remove only eligible `Expired` or `Invalidated` checkpoints; it may not bypass lineage, audit, or authorization guards.

### 5. Compatibility

This decision does not change Conversation identity, non-destructive rollback, checkpoint immutability, source Conversation preservation, BranchLineage ownership, or the existing checkpoint state machine. It selects operational values and lifecycle mechanics only within DEC-22 and DEC-23 safety constraints.

## Validation obligations

Implementation and planned evidence must cover stable BranchLineage identity, atomic branch recording, active/de­tached dependency protection, latest-checkpoint protection, 30-day superseded retention, 100-checkpoint quota rejection, daily idempotent cleanup, concurrent eligibility checks, audit recording, and preservation of source and branch Conversations. Documentation presence is not executed evidence.
