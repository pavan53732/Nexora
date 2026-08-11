# DEC-9 — Conversation Rollback Operation

> **Status: CANONICAL DECISION**
> This decision selects rollback semantics. It does not implement rollback.

## Context and evidence

Nexora's product principles prioritize agent-first interaction and preservation of historical information. Existing file and workspace restore operations are separate from execution recovery. No repository evidence establishes destructive deletion of conversation history or reversal of external effects.

## Alternatives

- Destructive rewind of one conversation.
- Non-destructive branch from a checkpoint.
- New conversation derived from a checkpoint without lineage.
- Composite rollback across all Nexora and external state.

## Decision

Nexora selects **non-destructive branching**.

Rolling back to a conversation checkpoint creates a new conversation branch whose initial logical conversation boundary is the selected checkpoint. The source conversation and all records after the checkpoint remain preserved and addressable. The branch receives a distinct conversation identity and records its parent conversation and source checkpoint lineage.

Rollback restores only the conversation record boundary and conversation-local metadata selected by DEC-8. It does not restore task, execution, provider, memory, file, workspace, Git, or external system state.

A rollback request does not replay tool calls, duplicate execution, consume retry budget, rewrite Git history, resend messages, repeat provider requests, or reverse arbitrary external side effects.

## Preconditions and safety

A rollback request must identify a source conversation and checkpoint and must pass authorization and freshness validation. A stale or non-addressable checkpoint is rejected without changing either conversation. Repeating an already-created branch request with the same operation identity must not create a second branch.

Rollback is rejected while the selected source conversation is undergoing a conflicting conversation mutation. It does not cancel or rewind an unrelated running task; task cancellation remains governed by task/execution authorities.

The operation is durable only after the new branch lineage and conversation boundary are committed within one atomic consistency boundary. An interrupted operation must be recoverable as either no branch or one complete branch; partial branch state is not a successful result.

## Side-effect boundary

Conversation rollback does not reverse external API mutations, sent messages, pushed Git commits, completed provider requests, device actions, or other external side effects. Any future compensation capability requires a separate decision and contract.

## Non-decisions

This decision does not define database tables, endpoint names, UI component names, retention numbers, or executable tests.
