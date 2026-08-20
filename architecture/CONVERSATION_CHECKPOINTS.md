# Conversation Checkpoints — Nexora

> **Status: CANONICAL** for conversation checkpoint and rollback semantics.
> Ownership: the Conversation/Session responsibility established by DEC-10 owns Conversation and Session–Conversation semantic boundaries; the distinct BranchLineage artifact selected by DEC-22 owns rollback parent/source lineage; ConversationCheckpoint remains the checkpoint boundary and lifecycle artifact. The repository has a canonical Session lifecycle (`state-machines/SessionLifecycle.md`), but no separate canonical Conversation lifecycle artifact. DEC-13 establishes durable immutable Conversation identity and DEC-14 establishes the Session–Conversation relationship as a first-class semantic relationship. DEC-15 assigns ownership of the relationship semantic contract to the existing Conversation/Session responsibility; DEC-17 establishes no independent relationship identity; DEC-18 establishes participant-based semantic representation without a separate relationship representation; DEC-19 establishes at most one active Session ↔ Conversation association in either direction at a point in time without all-time uniqueness; DEC-20 establishes no independent relationship lifecycle and terminal Session states ending active association; DEC-21 establishes later-Session continuation with preserved Conversation identity and a new active association.
> Decision authority: `decisions/DEC-8-conversation-checkpoint-rollback.md`, `DEC-9-conversation-rollback-operation.md`, `DEC-10-conversation-checkpoint-ownership.md`, `DEC-13-conversation-identity-persistence.md`, and `decisions/DEC-14-session-conversation-relationship-semantic-status.md` through `decisions/DEC-24-conversation-local-metadata-boundary.md`; BranchLineage operational policy is selected by `decisions/DEC-31-branch-lineage-and-checkpoint-operational-policy.md` and its formal lifecycle is owned by `state-machines/BranchLineageLifecycle.md`.

## Scope

A conversation checkpoint is an immutable boundary over one conversation's ordered conversation record and conversation-local metadata. It is not a generic name for other checkpoint or snapshot artifacts.

| Artifact | Owner | Purpose | Conversation rollback relationship |
|---|---|---|---|
| Execution checkpoint | Execution/runtime authority | Crash recovery and resume | Referenced only; not restored by conversation rollback |
| Context snapshot | Context management authority | Reproducible provider context | Referenced only; not restored by conversation rollback |
| File version | File-system authority | File history and file restore | Separate operation; not restored by conversation rollback |
| Workspace snapshot | Sandbox/workspace authority | Workspace snapshot restore | Separate operation; not restored by conversation rollback |
| Conversation checkpoint | Conversation/session authority | Conversation boundary and checkpoint lifecycle | Source of non-destructive branch; references BranchLineage for parent/source lineage |

## Conversation and session boundary

A Session is a durable runtime context container governed by `state-machines/SessionLifecycle.md`; it is not automatically identical to a Conversation. Per DEC-13, a Conversation has a distinct, durable, immutable conversation identity, an ordered conversation record, and conversation-local metadata; the concrete identifier representation remains intentionally unselected. DEC-14 establishes that the Session–Conversation relationship is first-class semantic architecture. DEC-15 assigns ownership of its canonical semantic contract to the existing Conversation/Session responsibility. Under DEC-17 through DEC-21, the relationship has no independent identity or lifecycle, is represented through the participants and relationship contract, permits at most one active association in either direction at a point in time, ends active association when Session is CLOSED or EXPIRED, and permits later-Session continuation with preserved Conversation identity and a new active association.

## Checkpoint contents

DEC-16 deferred relationship identity status, DEC-17 selects no independent relationship semantic identity, DEC-18 represents the relationship semantically through the participating Session and Conversation concepts plus the DEC-15 contract, DEC-19 selects one active Session ↔ one active Conversation at a point in time without selecting all-time uniqueness, DEC-20 establishes participant-driven association semantics, and DEC-21 allows Conversation continuation through a later Session with preserved Conversation identity and ordered record continuity; such continuation creates a new active association, while rollback branching remains a new Conversation. This does not select reference encoding, persistence, storage, schema, API, or implementation.

The checkpoint records the conversation identity, ordered conversation-record boundary, conversation-local metadata, creation provenance, integrity information, and parent/lineage information when applicable. Under DEC-24, Conversation-local metadata is semantically limited to creation provenance and integrity information required to interpret and validate the Conversation record boundary; concrete fields and encodings remain downstream. Parent/source lineage is owned by BranchLineage under DEC-22. The checkpoint may reference related artifacts for inspection. References do not transfer ownership or restoration semantics.

Task, execution, plan, provider, context, memory, file, workspace, Git, permission, and external-side-effect state are outside the checkpoint's owned contents.

## Creation

The selected creation triggers are: completed conversation turn (automatic post-turn creation) and explicit user-requested checkpoint. Pre-tool, pre-risk-operation, task-completion, crash-recovery, and agent-arbitrary checkpoint triggers are not selected as conversation-checkpoint triggers; those concerns remain with their existing authorities.

Execution crash-recovery checkpoints, pre-tool checkpoints, file snapshots, workspace snapshots, and context snapshots remain controlled by their existing authorities and are not automatically converted into conversation checkpoints.

## Rollback/branch

Rollback validates the source conversation, checkpoint lineage, authorization, and freshness. It creates a new conversation branch with a new conversation identity and parent/source-checkpoint lineage. The source conversation remains unchanged. Per DEC-9, this lineage must be recorded and preserved. DEC-22 assigns ownership of the semantic parent/source lineage relationship to the distinct BranchLineage artifact; DEC-31 selects its operational identity, lifecycle, dependency protection, retention, quota, and cleanup policy. Concrete encoding and transaction mechanics remain downstream.

The branch starts at the selected conversation boundary. No tool call, task, execution, provider request, message, Git operation, device action, or external mutation is replayed or reversed by this operation.

## Atomicity and recovery

The branch lineage and initial conversation boundary must have one atomic consistency boundary. The persistence technology, transaction mechanism, and concurrency primitive are intentionally not selected by this architecture document. An interrupted operation must recover to no branch or one complete branch. A caller-supplied operation identity is required to make repeated submission safe; its format, storage schema, and transport representation are implementation decisions governed by the future persistence/API specification. Conflicts with a concurrent mutation reject without modifying the source conversation.

If branch creation fails and rollback/cleanup of the attempted branch also fails, the operation MUST commit the existing non-success outcome and recover to no branch. The operation MUST NOT be reported as successful, expose or claim any partial branch, or promote partial lineage work into the BranchLineage lifecycle. The source Conversation and source checkpoint MUST remain unchanged. The existing operation identity, source/checkpoint lineage, original error, rollback error, partial-artifact references, and audit result MUST be retained for reconciliation and result/status reporting. The owning Conversation/BranchLineage responsibility MAY continue only existing eligible automatic mechanisms, including idempotent same-operation-identity recovery and DEC-31 daily cleanup; no manual-recovery disposition is required. This contract creates no new rollback state, error taxonomy, identity, authority, or compensation authority. Conversation rollback still does not reverse external side effects, and any compensation remains a separate future decision under DEC-9.

## Retention, authorization, and audit

Checkpoint retention, expiration, deletion, quotas, cleanup, and branch/source dependency safety are governed by DEC-23 and operationally selected by DEC-31; they remain outside the Session–Conversation relationship contract. DEC-31 selects a 30-day superseded retention window, a default per-workspace quota of 100 retained checkpoints, and daily idempotent cleanup. Creation and rollback require the existing authorization boundary for conversation data, with audit records for actor, source conversation, checkpoint, result, and failure reason.

## User boundary

The runtime may create and use checkpoints automatically. The user-visible surface is limited to a rollback/recover action, necessary confirmation, and result/status. Internal checkpoint identifiers and checkpoint management are not an administrative dashboard.


## Engineering handoff references

Implementation-facing projections of this canonical architecture are documented in:
- `models/Conversation.md`
- `models/Session.md`
- `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`
- `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md`
- `specs/SESSION_CONVERSATION_ERRORS.md`
- `testing/SESSION_CONVERSATION_TEST_MATRIX.md`
- `docs/SESSION_CONVERSATION_IMPLEMENTATION_HANDOFF.md`
