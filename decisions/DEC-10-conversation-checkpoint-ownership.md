# DEC-10 — Conversation Checkpoint Ownership

> **Status: CANONICAL DECISION**

## Decision

The repository has a canonical `Session` lifecycle (`state-machines/SessionLifecycle.md`) but does not yet have an independently canonical `Conversation` lifecycle or `Conversation` model artifact. DEC-10 therefore establishes a **Conversation/Session responsibility** for conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branch construction. This is an architecture responsibility selection, not proof that a distinct Conversation subsystem already exists in the repository.

The runtime requests checkpoint or rollback operations when required by execution flow, but does not own conversation semantics. The UI requests user-controlled operations and displays results, but does not own checkpoint state. Memory, context, execution, task, file, workspace, Git, provider, and permission subsystems retain ownership of their own artifacts and lifecycles.

A distinct `ConversationCheckpoint` lifecycle artifact is selected. Its lifecycle is defined in `state-machines/ConversationCheckpointLifecycle.md`; its focused contract is defined in `specs/CONVERSATION_CHECKPOINTS.md`.

## Rationale

This preserves existing lifecycle boundaries and avoids assigning cross-domain conversation semantics to the runtime, memory, or workflow engine merely because those systems reference conversation data.

## Consequences

Supporting documents must reference the conversation checkpoint specification and must not redefine checkpoint contents or rollback semantics. Cross-subsystem references remain references, not ownership transfers. A future implementation/documentation pass must establish the canonical Conversation identity/persistence authority before implementation begins.
