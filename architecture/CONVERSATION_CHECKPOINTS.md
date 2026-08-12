# Conversation Checkpoints — Nexora

> **Status: CANONICAL** for conversation checkpoint and rollback semantics.
> Ownership: the Conversation/Session responsibility established by DEC-10. The repository has a canonical Session lifecycle (`state-machines/SessionLifecycle.md`), but no separate canonical Conversation lifecycle artifact. DEC-13 establishes a narrow Conversation identity contract and DEC-14 establishes the Session–Conversation relationship as a first-class semantic relationship; Conversation-to-Session cardinality, Conversation resumption, Session-closure/expiration effects on Conversation, relationship ownership, relationship identity, relationship representation, branch-lineage ownership, and the conversation-local metadata boundary remain unresolved architecture dependencies to be completed before implementation.
> Decision authority: `decisions/DEC-8-conversation-checkpoint-rollback.md`, `DEC-9-conversation-rollback-operation.md`, `DEC-10-conversation-checkpoint-ownership.md`, and `DEC-13-conversation-identity-persistence.md`.

## Scope

A conversation checkpoint is an immutable boundary over one conversation's ordered conversation record and conversation-local metadata. It is not a generic name for other checkpoint or snapshot artifacts.

| Artifact | Owner | Purpose | Conversation rollback relationship |
|---|---|---|---|
| Execution checkpoint | Execution/runtime authority | Crash recovery and resume | Referenced only; not restored by conversation rollback |
| Context snapshot | Context management authority | Reproducible provider context | Referenced only; not restored by conversation rollback |
| File version | File-system authority | File history and file restore | Separate operation; not restored by conversation rollback |
| Workspace snapshot | Sandbox/workspace authority | Workspace snapshot restore | Separate operation; not restored by conversation rollback |
| Conversation checkpoint | Conversation/session authority | Conversation boundary and branch lineage | Source of non-destructive branch |

## Conversation and session boundary

A Session is a durable runtime context container governed by `state-machines/SessionLifecycle.md`; it is not automatically identical to a Conversation. Per DEC-13, a Conversation has a distinct, durable, immutable conversation identity, an ordered conversation record, and conversation-local metadata; the concrete identifier representation remains intentionally unselected. DEC-14 establishes that the Conversation-to-Session relationship is first-class semantic architecture. It does not select cardinality, relationship ownership, relationship identity, relationship representation, whether a Conversation may be resumed through a later Session, or the effect of Session closure, expiration, or recreation on Conversation identity or persistence; those remain unresolved architecture decisions.

## Checkpoint contents

The checkpoint records the conversation identity, ordered conversation-record boundary, conversation-local metadata, creation provenance, integrity information, and parent/lineage information when applicable. It may reference related artifacts for inspection. References do not transfer ownership or restoration semantics.

Task, execution, plan, provider, context, memory, file, workspace, Git, permission, and external-side-effect state are outside the checkpoint's owned contents.

## Creation

The selected creation triggers are: completed conversation turn (automatic post-turn creation) and explicit user-requested checkpoint. Pre-tool, pre-risk-operation, task-completion, crash-recovery, and agent-arbitrary checkpoint triggers are not selected as conversation-checkpoint triggers; those concerns remain with their existing authorities.

Execution crash-recovery checkpoints, pre-tool checkpoints, file snapshots, workspace snapshots, and context snapshots remain controlled by their existing authorities and are not automatically converted into conversation checkpoints.

## Rollback/branch

Rollback validates the source conversation, checkpoint lineage, authorization, and freshness. It creates a new conversation branch with a new conversation identity and parent/source-checkpoint lineage. The source conversation remains unchanged. Per DEC-9, this lineage must be recorded and preserved; its precise ownership (Conversation-owned versus checkpoint-owned) remains an unresolved architecture decision not answered by DEC-13.

The branch starts at the selected conversation boundary. No tool call, task, execution, provider request, message, Git operation, device action, or external mutation is replayed or reversed by this operation.

## Atomicity and recovery

The branch lineage and initial conversation boundary must have one atomic consistency boundary. The persistence technology, transaction mechanism, and concurrency primitive are intentionally not selected by this architecture document. An interrupted operation must recover to no branch or one complete branch. A caller-supplied operation identity is required to make repeated submission safe; its format, storage schema, and transport representation are implementation decisions governed by the future persistence/API specification. Conflicts with a concurrent mutation reject without modifying the source conversation.

## Retention, authorization, and audit

Checkpoint retention, expiration, deletion, quotas, and branch/source dependency policy remain unresolved architecture decisions. They must be defined by the conversation/session persistence policy before implementation; no numeric quota is asserted here. Creation and rollback require the existing authorization boundary for conversation data, with audit records for actor, source conversation, checkpoint, result, and failure reason.

## User boundary

The runtime may create and use checkpoints automatically. The user-visible surface is limited to a rollback/recover action, necessary confirmation, and result/status. Internal checkpoint identifiers and checkpoint management are not an administrative dashboard.
