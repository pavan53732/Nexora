# DEC-13 — Conversation Identity and Persistence Contract

> **Status: CANONICAL DECISION**
> This decision selects a narrow Conversation identity contract. It does not select Session-to-Conversation cardinality, Conversation resumption mechanics, Session-closure/expiration effects on Conversation, branch-lineage ownership beyond DEC-9, a metadata schema, message/turn ordering representation, storage technology, retention policy, or implementation.

## Context

DEC-8 and DEC-9 require a conversation checkpoint and a non-destructive rollback branch, both of which depend on a "conversation identity" and an "ordered conversation record." DEC-10 established Conversation/Session responsibility for conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branch construction, but explicitly left the canonical Conversation identity/persistence authority to a future decision. `architecture/CONVERSATION_CHECKPOINTS.md` explicitly states that Conversation identity, message ordering, and the Conversation-to-Session relationship remain unresolved architecture decisions, and that the repository does not establish whether a Conversation survives process death, app restart, or Session closure.

This decision is the future pass referenced by DEC-10. Its scope is limited to what DEC-8, DEC-9, and DEC-10 already require plus the minimum additional selection needed to make those decisions coherent. It does not resolve every open question identified in `architecture/CONVERSATION_CHECKPOINTS.md`.

## Repository evidence

- DEC-8 requires the checkpoint to capture "the conversation identity" and "the ordered conversation record boundary."
- DEC-9 requires a branch to receive "a distinct conversation identity" and to record "its parent conversation and source checkpoint lineage." The source conversation "remains preserved and addressable."
- DEC-10 establishes Conversation/Session responsibility for conversation identity and conversation-local records, and states a future pass "must establish the canonical Conversation identity/persistence authority before implementation begins."
- `state-machines/SessionLifecycle.md` is canonical for Session states (`CREATED`, `ACTIVE`, `IDLE`, `CLOSED`, `EXPIRED`) and transitions. It does not reference Conversation identity, Conversation attachment, or Conversation cardinality in any state, guard, or invariant.
- `models/Session.md` defines the Session record with no `conversationId` or equivalent field, and no cardinality statement toward Conversation.
- `architecture/CONVERSATION_CHECKPOINTS.md` explicitly states that a Session "is not automatically identical to a Conversation," that it does not establish Conversation survival across process death, app restart, or Session closure, and that "Conversation identity, message ordering, and the Conversation-to-Session relationship remain unresolved architecture decisions."
- No canonical or supporting document in the repository defines Session-to-Conversation cardinality, Conversation resumption mechanics, or the effect of Session `CLOSED`/`EXPIRED` on Conversation identity.

## Decision

Nexora selects the following narrow Conversation identity contract, and no more:

**Conversation as a concept.** A Conversation is the ordered user/agent conversation record and conversation-local metadata already required by DEC-8 and referenced by DEC-9. It is distinct from Session, Task, Execution, ConversationCheckpoint, Execution checkpoint, ContextSnapshot, Workspace snapshot, and Memory artifact — this distinction is already established by DEC-8's exclusion list and is restated here for clarity, not re-decided.

**Conversation identity.** A Conversation has a distinct conversation identity, consistent with DEC-8 (checkpoint captures "the conversation identity") and DEC-9 (branch receives "a distinct conversation identity"). This decision additionally selects that this identity is durable and immutable for the lifetime of the Conversation record it identifies — this durability/immutability selection is a new element of this decision, not an restatement of a prior fact, and it does not select a concrete identifier representation (no UUID, database key, or other encoding is chosen).

**Conversation identity is distinct from checkpoint identity**, consistent with `state-machines/ConversationCheckpointLifecycle.md`, which already states checkpoint identity is distinct from conversation identity.

**Branching preserves DEC-9 exactly.** Rollback creates a new Conversation identity for the branch; the source Conversation remains unchanged and addressable; the branch records parent Conversation and source-checkpoint lineage. This decision does not change any part of DEC-9.

**Branch-lineage ownership is not decided here.** DEC-9 requires that lineage be recorded and preserved. Whether that lineage is owned by a durable Conversation record, by the ConversationCheckpoint artifact, or by a separate lineage structure is **not established by the repository** and is **left unresolved** by this decision. No ownership beyond "lineage must be recorded and preserved, per DEC-9" is selected.

**Conversation-to-Session relationship is not decided here.** The repository establishes that Session and Conversation are distinct concepts (per `architecture/CONVERSATION_CHECKPOINTS.md` and DEC-10) and that Session has its own independently canonical lifecycle (`state-machines/SessionLifecycle.md`) that does not reference Conversation. This decision does **not** select:

- Session-to-Conversation cardinality (one-to-one, one-active-at-a-time, one-to-many, many-to-one, or many-to-many);
- whether a Conversation may be resumed through a later Session, or the mechanics of any such resumption;
- any effect of Session `CLOSED`, Session `EXPIRED`, or Session recreation on Conversation identity or Conversation persistence;
- any effect of process death or application restart on Conversation identity or Conversation persistence.

All of the above remain **OWNER DECISION REQUIRED / UNRESOLVED**. A future decision must establish them; this decision does not attempt to answer them by inference from Session durability or from the existence of Conversation identity.

**Conversation-local metadata boundary is not fully defined here.** DEC-8 already requires "conversation-local metadata required to interpret" the conversation record boundary. This decision does not enumerate, schematize, or bound that metadata beyond what DEC-8 already states. The complete content/field boundary of conversation-local metadata remains unresolved.

**Message/turn ordering.** The repository already establishes an "ordered conversation record" (DEC-8) and "completed conversation turn" as a checkpoint trigger (`architecture/CONVERSATION_CHECKPOINTS.md`). This decision affirms that ordering is a property of the Conversation record, without selecting any ordering mechanism, representation, or persistence structure (no sequence number, timestamp field, append-only log, or other encoding is chosen).

**Non-absorption clarification.** Consistent with DEC-8's exclusion list, Task, Execution, provider, ContextSnapshot, Memory, file, workspace, Git, permission, and external-side-effect state are not owned or restored by the Conversation checkpoint/rollback boundary. This exclusion concerns checkpoint restoration ownership; it does not assert that those subsystems can never hold references, projections, or derived history associated with a Conversation.

**Ownership boundary.** Consistent with DEC-10, the Conversation/Session responsibility governs conversation identity and conversation-local records as scoped above. This decision does not expand that responsibility to Session cardinality, Session lifecycle semantics, Memory ownership, Runtime ownership, or Database/schema ownership. Session lifecycle remains solely governed by `state-machines/SessionLifecycle.md`.

## Non-decisions

This decision does not select: Session-to-Conversation cardinality; Conversation resumption mechanics; the effect of Session closure, expiration, or recreation on Conversation identity or persistence; the effect of process death or app restart on Conversation persistence; branch-lineage ownership beyond DEC-9's recording requirement; a conversation-local metadata schema or field list; a message/turn ordering mechanism or representation; storage technology; transaction mechanism; database schema; API shape; retention, expiration, deletion, quota, or cleanup policy; or any implementation detail.

## Consequences

- `architecture/CONVERSATION_CHECKPOINTS.md` may rely on a durable, immutable Conversation identity distinct from checkpoint identity, without those unresolved dependencies being treated as settled.
- The Conversation-to-Session relationship, Conversation resumption, Session-closure/expiration effects on Conversation, branch-lineage ownership, and the conversation-local metadata boundary remain explicitly open and must be addressed by future, separately scoped architecture decisions.
- Retention, expiration, deletion, quota, and cleanup policy remain a separate later phase and are not advanced by this decision.
- A future decision may determine whether a dedicated Conversation lifecycle artifact is required; this decision does not require or preclude one.
