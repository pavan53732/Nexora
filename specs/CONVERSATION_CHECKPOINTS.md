# Conversation Checkpoint and Rollback Specification — Nexora

> **Status: SUPPORTING**. This document defers to `architecture/CONVERSATION_CHECKPOINTS.md` for semantic architecture, ownership, boundaries, and lifecycle. It states implementation-facing contract obligations only and must not redefine them.
> Supporting engineering references: `models/Conversation.md`, `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`, `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md`, and `specs/SESSION_CONVERSATION_ERRORS.md`. Retention and deletion safety rules are governed by `decisions/DEC-23-conversation-checkpoint-retention-deletion-policy.md` and operationally selected by `decisions/DEC-31-branch-lineage-and-checkpoint-operational-policy.md`.

## Contract

The operation described here is the non-destructive branch operation selected by the canonical architecture document. It restores only the conversation record boundary and conversation-local metadata. It references, but does not restore, task, execution, context, memory, file, workspace, provider, Git, or external state.

## Preconditions

The request must identify an addressable source Conversation and checkpoint, pass conversation-data authorization, pass integrity and freshness validation, and not conflict with a concurrent mutation of the source Conversation. Invalid, stale, expired, or unauthorized requests fail without modifying the source Conversation.

## Idempotency

A caller-supplied operation identity makes repeated submission safe. A completed request returns the existing branch result. An incomplete request is recovered as either no branch or one complete branch; partial branch state is not exposed as success.

## Ordering

Validation precedes mutation. The implementation must durably commit branch identity, parent lineage, checkpoint reference, and initial conversation boundary as one logical commit. User-visible success is emitted only after that commit. Failure is emitted without claiming a branch exists.

## Non-effects

The operation does not replay or reverse tool calls, duplicate or cancel execution, consume retry budget, restore a file version, restore a workspace snapshot, rewrite Git history, repeat provider requests, resend messages, perform device actions, or compensate external mutations.

## Relationship to Session

Rollback does not by itself decide Session lifecycle. If the branch later becomes the current active Conversation for a Session, that association must still respect the Session–Conversation engineering contract: no independent relationship identity, no independent relationship lifecycle, and at most one active Session ↔ one active Conversation at a point in time.

## Retention and cleanup safety

A checkpoint may expire or become invalidated under the canonical lifecycle. Physical deletion is permitted only after the checkpoint is `Expired` or `Invalidated`, no recorded BranchLineage depends on it, and required audit/retention obligations are satisfied. Quota rejection and cleanup leave protected Conversations and BranchLineage artifacts unchanged. Under DEC-31, a superseded checkpoint uses the selected 30-day operational retention window, the default per-workspace retained-checkpoint quota is 100, and cleanup runs as an idempotent daily WorkManager job; concrete storage encoding and transaction mechanics remain downstream.

## Engineering boundary

The semantic architecture required for implementation is closed by DEC-8 through DEC-24 and DEC-31. Remaining implementation work includes persistence encoding, storage schema realization, API transport shape, concurrency primitives, and recovery mechanics. The selected retention, quota, dependency-protection, and cleanup semantics must be preserved; their concrete transaction and storage mechanisms remain implementation choices.
