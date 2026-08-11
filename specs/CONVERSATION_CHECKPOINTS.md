# Conversation Checkpoint and Rollback Specification — Nexora

> **Status: SUPPORTING**. This document defers to `architecture/CONVERSATION_CHECKPOINTS.md` for semantic architecture, ownership, boundaries, and lifecycle. It only states implementation-facing contract obligations and must not redefine them.

## Contract

The operation described here is the non-destructive branch operation selected by the canonical architecture document. It restores only the conversation record boundary and conversation-local metadata. It references, but does not restore, task, execution, context, memory, file, workspace, provider, Git, or external state.

## Preconditions

The request must identify an addressable source conversation and checkpoint, pass conversation-data authorization, pass integrity and freshness validation, and not conflict with a concurrent mutation of the source conversation. Invalid, stale, expired, or unauthorized requests fail without modifying the source conversation.

## Idempotency

A caller-supplied operation identity makes repeated submission safe. A completed request returns the existing branch result. An incomplete request is recovered as either no branch or one complete branch; partial branch state is not exposed as success.

## Ordering

Validation precedes mutation. The implementation must durably commit branch identity, parent lineage, checkpoint reference, and initial conversation boundary as one logical commit. User-visible success is emitted only after that commit. Failure is emitted without claiming a branch exists.

## Non-effects

The operation does not replay or reverse tool calls, duplicate or cancel execution, consume retry budget, restore a file version, restore a workspace snapshot, rewrite Git history, repeat provider requests, resend messages, perform device actions, or compensate external mutations.

## Open architecture dependencies

Conversation identity, Conversation-to-Session relationship, message/turn ordering, retention/deletion policy, and authorization subject scope remain architecture dependencies. This specification must not be classified implementation-ready until those dependencies are assigned canonical authority.

## Open dependency

The canonical conversation/session persistence policy and authorization subject identifiers remain governed by their existing authorities. This specification does not create a second persistence or security model.
