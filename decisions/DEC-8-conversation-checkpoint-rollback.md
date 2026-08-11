# DEC-8 — Conversation Checkpoint and Rollback Semantics

> **Status: CANONICAL DECISION**
> This decision selects semantics for conversation checkpoints and rollback. It does not implement the capability.

## Context

Nexora already defines execution checkpoints for crash recovery, immutable context snapshots, file history, and workspace snapshots. These artifacts have separate purposes and owners. The repository did not define a conversation checkpoint or a user-facing conversation rollback operation.

## Repository evidence

- `architecture/AGENT_RUNTIME.md` defines execution checkpoint saving for crash recovery.
- `specs/CONTEXT_MANAGEMENT.md` defines a non-compressed state-checkpoint layer and immutable `ContextSnapshot` artifacts.
- `specs/FILE_SYSTEM.md` defines file-scoped version history and restore.
- `docs/SANDBOX_DEPTH.md` defines workspace snapshots and rollback.
- `architecture/MEMORY_SYSTEM.md` assigns separate ownership to file versions, workspace snapshots, context snapshots, and memory artifacts.
- `docs/CANONICAL_SOURCES.md` requires one canonical owner per concept.

## Alternatives

### A — Transcript boundary only

A checkpoint would identify a message/turn boundary and conversation metadata. This preserves subsystem ownership and is the narrowest meaning.

### B — Transcript plus logical metadata

A checkpoint would additionally capture conversation-local metadata, but not execution, file, workspace, or memory state.

### C — Conversation plus plan/context

A checkpoint would include plan and context state. This overlaps with execution checkpoint and context snapshot ownership.

### D — Composite cross-domain snapshot

A checkpoint would contain conversation, execution, context, memory, and workspace state. This would create cross-subsystem ownership and make external side-effect semantics ambiguous.

## Decision

Nexora selects **B: transcript plus logical conversation metadata**.

A conversation checkpoint is a durable, immutable boundary over one conversation's ordered user/agent conversation record and conversation-local metadata. It is not an execution checkpoint, context snapshot, file version, workspace snapshot, or memory snapshot.

A conversation checkpoint MAY reference related execution, task, plan, context, memory, file, or workspace artifacts for inspection and lineage. References do not transfer ownership or imply restoration.

The checkpoint captures:

- the conversation identity;
- the ordered conversation record boundary;
- conversation-local metadata required to interpret that boundary;
- creation provenance and integrity information;
- parent/lineage information when the checkpoint is created from another checkpoint.

The checkpoint does not capture or own task state, execution state, provider state, context snapshots, memory artifacts, file versions, workspace snapshots, Git state, or external side effects.

## Consequences

- Conversation rollback can preserve historical conversation records without claiming to undo execution or external actions.
- Related subsystem state must be handled by its own canonical operation.
- A future implementation must not use a conversation checkpoint as a substitute for an execution checkpoint or workspace snapshot.

## Non-decisions

This decision does not select a storage schema, API shape, UI layout, identifier encoding, retention value, or roadmap implementation date. Those are governed by the specification and roadmap artifacts below.
