# DEC-13 — Conversation Identity and Persistence Contract

> **Status: CANONICAL DECISION**

## Decision

The repository requires a canonical Conversation identity and persistence contract before any checkpoint retention, expiration, deletion, quota, cleanup, or conversation-recovery policy can be finalized.

A **Conversation** is selected as a durable product-state record of one ordered user/agent conversation within a workspace. It is distinct from Session, Task, Execution, ConversationCheckpoint, Execution checkpoint, ContextSnapshot, Workspace snapshot, and Memory artifact.

A Conversation has a **distinct durable conversation identity**. The concrete identifier representation remains unselected in this decision. Conversation identity is immutable for the lifetime of that Conversation record.

A **Session** remains the canonical durable runtime context container governed by `state-machines/SessionLifecycle.md`. Session and Conversation are related but not identical. This decision does **not** collapse Conversation into Session, does **not** make Session the Conversation identity, and does **not** make Conversation a substitute for Session lifecycle state.

The minimum selected relationship is:

- a Session MAY host interaction against one Conversation at a time;
- a Conversation MAY be resumed through a later Session;
- closing, expiring, or recreating a Session does not by itself redefine Conversation identity;
- Task and Execution references remain separate runtime artifacts and do not become Conversation-owned merely because they are visible from a conversation surface.

The authoritative Conversation record is the ordered conversation record and conversation-local metadata referenced by DEC-8 and DEC-9. Message/turn ordering is canonical within that Conversation record. Task, Execution, provider, ContextSnapshot, Memory, file, workspace, Git, permission, and external-side-effect state remain outside Conversation-owned state unless another canonical authority explicitly delegates a subset.

For DEC-9 non-destructive branching, rollback creates a **new Conversation identity** whose initial logical boundary is the selected ConversationCheckpoint. The new Conversation records immutable lineage to:

- the parent/source Conversation identity; and
- the source ConversationCheckpoint identity.

The source Conversation remains unchanged by branching. Branch lineage is authoritative Conversation state, not merely checkpoint-local metadata. A branch MAY itself become the source of later branching; each later branch receives its own new Conversation identity and preserves parent/source-checkpoint lineage.

This decision selects **Conversation/Session responsibility** as the architecture boundary for Conversation identity, Conversation-owned record semantics, and Conversation-to-Session attachment semantics, consistent with DEC-10. However, the repository does not yet establish a separate canonical Conversation lifecycle state machine, database schema, API contract, or implementation component. Those remain future work derived from this identity/persistence contract rather than being selected here.

The minimum persistence guarantees required by this decision are:

- durable Conversation identity;
- durable ordered conversation record boundary;
- durable conversation-local metadata necessary to interpret that record;
- durable parent/source-checkpoint lineage for branched Conversations;
- atomic creation of a new branch Conversation and its initial boundary, or no branch at all.

This decision does **not** select retention duration, expiration rules, deletion policy, quota values, cleanup scheduling, storage technology, transaction mechanism, foreign-key schema, API shape, or authorization-subject granularity. Those remain separate architecture and specification work.

## Rationale

DEC-8 through DEC-10 already require a conversation-bound checkpoint and a non-destructive branch that creates a new Conversation identity. The repository also already defines Session as a durable runtime context container, but no canonical Conversation identity/persistence authority existed. This decision establishes the smallest contract needed to make Conversation-bound branching, persistence, and future retention policy coherent without redefining Session, Task, Execution, or checkpoint authorities.

## Consequences

- `architecture/CONVERSATION_CHECKPOINTS.md` may rely on durable Conversation identity and Conversation-owned ordered record semantics without selecting retention policy.
- Supporting specifications may treat Conversation identity, Conversation-to-Session attachment, and branch lineage as resolved dependencies.
- Retention/expiration/deletion/quota policy remains a separate next-phase decision.
- A future architecture pass must determine whether a dedicated Conversation lifecycle artifact is required or whether Conversation persistence can be fully governed without a standalone lifecycle state machine.
