# DEC-23 — Conversation Checkpoint Retention and Deletion Safety Policy

> **Status: CANONICAL DECISION**
> This decision selects semantic safety rules for checkpoint retention, expiration, physical deletion, quotas, cleanup, and branch dependencies. Numeric durations and quota values remain configuration choices and are not selected here.

## Problem

DEC-8 through DEC-10 and DEC-13 establish immutable conversation checkpoints and non-destructive rollback, but retention, expiration, deletion, quotas, cleanup, and branch/source dependency policy remained unresolved. A policy is required that protects rollback lineage, source Conversations, audit evidence, and existing lifecycle invariants without inventing numeric resource limits.

## Repository evidence

- `state-machines/ConversationCheckpointLifecycle.md` defines `Expired` and `Invalidated` as unavailable for normal rollback use and states that expiration or invalidation does not by itself define physical deletion.
- `architecture/CONVERSATION_CHECKPOINTS.md` requires non-destructive rollback and preservation of the source Conversation.
- DEC-9 requires the source Conversation to remain unchanged and addressable after rollback.
- DEC-22 assigns rollback parent/source lineage to the distinct BranchLineage artifact while leaving its concrete lifecycle and storage mechanics unselected.
- `models/Conversation.md` preserves checkpoint references and branch lineage as semantic persistence concerns while leaving concrete storage and cleanup mechanisms downstream.

## Decision

Nexora applies the following checkpoint policy:

1. **Retention.** A checkpoint remains retained and addressable while its lifecycle state permits normal use and while an applicable retention policy has not expired it. The canonical architecture does not select a numeric retention duration; that value is a downstream configuration choice.

2. **Expiration.** A retention-policy decision may transition a `Created` or `Superseded` checkpoint to `Expired` through the canonical checkpoint lifecycle. An `Expired` checkpoint cannot be used as a rollback source. Expiration does not delete the source Conversation, branch Conversation, or BranchLineage artifact.

3. **Invalidation.** An integrity, authorization, or lineage failure may transition a checkpoint to `Invalidated`. An `Invalidated` checkpoint cannot be used as a rollback source. Invalidation does not by itself perform physical deletion.

4. **Physical deletion.** Physical checkpoint deletion is permitted only after the checkpoint is `Expired` or `Invalidated`, no recorded BranchLineage depends on it, and required audit/retention obligations are satisfied. Physical deletion must not delete or mutate a source Conversation or an existing branch Conversation as a side effect.

5. **Branch dependency protection.** A recorded BranchLineage dependency on the checkpoint prevents physical deletion of that checkpoint. A checkpoint may become deletion-eligible only after no recorded BranchLineage depends on it. This decision does not select the BranchLineage lifecycle or the mechanism by which a dependency becomes inactive.

6. **Quotas.** Quotas are enforced before a new checkpoint is durably created. A quota rejection leaves existing checkpoints, Conversations, and BranchLineage artifacts unchanged. Quota enforcement must not bypass authorization, silently delete a checkpoint, or delete a source or branch Conversation. Numeric quota values remain downstream configuration choices.

7. **Cleanup.** Cleanup may physically delete only checkpoints that satisfy the deletion rule above. Cleanup is idempotent, auditable, and must tolerate repeated execution and concurrent eligibility checks without deleting protected artifacts. Cleanup scheduling and implementation remain downstream choices.

## Explicit non-decisions

This decision does not select numeric retention durations, numeric quotas, storage technology, table layout, serialization, cleanup scheduler, transaction mechanism, API shape, authorization schema, BranchLineage lifecycle, or implementation language. Those choices remain downstream provided that they preserve this policy and the canonical lifecycle states.

## Compatibility

- DEC-8 and DEC-9 remain unchanged: checkpoints are immutable boundaries and rollback is non-destructive.
- DEC-13 remains unchanged: Conversation identity is durable and immutable; retention and deletion do not alter that identity contract.
- DEC-22 remains unchanged: BranchLineage owns rollback parent/source lineage, while its lifecycle and storage remain separate decisions.
- `state-machines/ConversationCheckpointLifecycle.md` remains canonical for checkpoint states and legal transitions; this decision supplies the previously missing retention/deletion guards.

## Validation obligations

Future implementation and test specifications must cover expiration, invalidation, quota rejection with no change, protected active lineage, eligible cleanup, repeated cleanup, concurrent cleanup, audit recording, and preservation of source and branch Conversations.
