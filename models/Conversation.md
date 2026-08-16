> **Status: DERIVED** for Conversation domain model.
> This document defines the shape and semantics of Conversation as required by DEC-8 through DEC-21.
>
> Canonical authority remains distributed: `architecture/CONVERSATION_CHECKPOINTS.md` owns checkpoint/rollback semantics, `decisions/DEC-13-conversation-identity-persistence.md` owns durable immutable Conversation identity, and `decisions/DEC-14-session-conversation-relationship-semantic-status.md` through `decisions/DEC-21-session-conversation-continuation-recovery.md` own the Session–Conversation relationship semantics.
> Referenced by: persistence, runtime, API, testing, and future implementation documents.

# Domain Model: Conversation

```kotlin
data class Conversation(
    val id: String,
    val workspaceId: String,
    val sourceConversationId: String? = null,
    val sourceCheckpointId: String? = null,
    val recordVersion: Long,
    val status: ConversationStatus,
    val createdAt: Instant,
    val updatedAt: Instant,
    val latestCheckpointId: String? = null
)

enum class ConversationStatus {
    ACTIVE,
    ARCHIVED,
    DELETED
}
```

`ConversationStatus` lifecycle is canonically owned by `state-machines/ConversationLifecycle.md`; the `conversation` table in `specs/DATABASE_SCHEMA.md` persists it.

## Purpose

A Conversation is the durable, ordered record boundary for interaction history and conversation-local metadata. It is distinct from Session, Task, Execution, Memory, ContextSnapshot, FileVersion, and WorkspaceSnapshot.

## Ownership

The Conversation/Session responsibility established by DEC-10 owns Conversation identity, conversation-local records, checkpoint creation, rollback branch construction, and the semantic contract of the Session–Conversation relationship under DEC-15. The distinct BranchLineage artifact selected by DEC-22 owns rollback parent/source lineage; ConversationCheckpoint remains the checkpoint boundary and lifecycle artifact.

Runtime, Memory, Context, Task, Execution, File, Workspace, Agent, Workflow, Tool, and Permission authorities may reference conversation data but do not own Conversation semantics merely by reference.

## Identity

Conversation identity is durable and immutable under DEC-13.

Conversation identity is distinct from:
- Session identity,
- checkpoint identity,
- branch lineage,
- ordered-record content,
- retention/deletion policy,
- any transport, database, or API encoding.

No independent Session–Conversation relationship identity exists under DEC-17.

## Record boundary and ordering

A Conversation owns one ordered conversation record and conversation-local metadata.

The ordered conversation record is the semantic history boundary used by checkpoints, continuation, and rollback branching. Ordering must remain stable enough to identify a checkpoint boundary and to preserve post-rollback lineage semantics, but the concrete storage representation of messages, turns, or records remains an implementation choice and is not architecturally fixed here.

Conversation identity does not equal Conversation lifecycle. Conversation records do not equal checkpoint lineage. Branch lineage does not replace the current ordered record.

## Conversation-local data

Conversation-local data includes the ordered record, checkpoint-addressable boundaries, and the creation-provenance and integrity-information categories selected by DEC-24. Concrete fields and schema remain downstream. Metadata semantically belongs to the Conversation rather than to Session, Task, Execution, Context, or Memory.

Conversation-local data does not include:
- Task lifecycle state,
- Execution lifecycle state,
- provider stream state,
- file/workspace snapshot state,
- external side effects,
- authorization policy state,
- Session lifecycle state.

## Checkpoint relationship

A conversation checkpoint is an immutable boundary over one Conversation's ordered record and conversation-local metadata. Checkpoint identity is not Conversation identity. A checkpoint references a Conversation; it does not become the Conversation.

Checkpoint lifecycle remains independently owned by `state-machines/ConversationCheckpointLifecycle.md` and does not create a Conversation lifecycle.

## Branch semantics

Rollback is the non-destructive branch operation selected by DEC-9.

When rollback is requested from source Conversation `C1` at a valid checkpoint, the result is a new Conversation `C2` with its own Conversation identity. `C1` remains preserved and addressable. `C2` records lineage to its source Conversation and source checkpoint.

Rollback is not continuation.

## Lineage

BranchLineage records parent/source relationships between distinct Conversations created by rollback. This derived model projects the semantic BranchLineage boundary selected by DEC-22 and the operational identity/lifecycle policy selected by DEC-31; its stable identifier, `RECORDED`/`ACTIVE`/`DETACHED`/`DELETED` status, dependency protection, and retention/cleanup behavior are governed by those canonical sources.

Lineage does not:
- mutate the source Conversation identity,
- collapse branch identity into the source Conversation,
- create an independent relationship identity,
- replace checkpoint identity,
- imply destructive rewind.

## Session relationship

Session and Conversation are distinct concepts. Their relationship is first-class semantic architecture under DEC-14 and is owned semantically by the existing Conversation/Session responsibility under DEC-15.

The relationship:
- has no independent identity under DEC-17,
- has no separate semantic representation requirement under DEC-18,
- permits at most one active Session ↔ one active Conversation at a point in time under DEC-19,
- has no independent lifecycle under DEC-20,
- permits later-Session continuation with preserved Conversation identity and a new active association under DEC-21.

## Session CLOSED / EXPIRED effects

When an associated Session reaches `CLOSED` or `EXPIRED`, the active Session–Conversation association ends under DEC-20.

Those Session terminal states do not by themselves:
- mutate Conversation identity,
- delete Conversation records,
- rewrite checkpoints,
- destroy branch lineage,
- transform rollback into continuation.

## Session recreation

Reopening a terminal Session creates a new Session identity under the canonical Session lifecycle.

Therefore, a later Conversation association after Session recreation is a new active association. Conversation identity is preserved only if the later operation is continuation of the same Conversation under DEC-21; rollback still creates a new Conversation identity.

## Continuation

A Conversation may continue through a later Session under DEC-21.

Example semantic effect:
- `S1 ↔ C1` active,
- `S1` terminates,
- later `S2 ↔ C1` is allowed,
- Conversation identity remains `C1`,
- Session identity is `S2`,
- the active association is new.

Continuation does not create a new Conversation identity.

## Process death, application restart, and recovery

Process death and application restart are not independently selected Conversation mutation events in the Session–Conversation semantic contract.

If recovery restores the same still-valid Session, that is same-Session recovery. If recovery requires a new Session identity, Session–Conversation continuation semantics apply. The concrete recovery mechanism, persistence technology, restoration trigger, and transport/API shape remain implementation choices and are not architecturally fixed here.

## Persistence boundary

Conversation identity, ordered-record continuity, checkpoint references, and branch lineage are required semantic persistence concerns.

Concrete storage mapping, table layout, blob layout, serialization, and reference encoding are implementation choices unless selected elsewhere by a canonical persistence document.

## Retention, deletion, and cleanup boundary

Retention, deletion, and cleanup policy are not determined by Conversation identity alone and are not changed by Session closure, Session expiration, or Session recreation.

DEC-31 selects the checkpoint operational policy: superseded checkpoints use a default 30-day retention window, each workspace has a default retained-checkpoint quota of 100, and an idempotent daily cleanup job rechecks lineage/dependency protection before deletion and records protected skips. DEC-23 and DEC-31 continue to govern deletion safety and branch/source dependency protection. Concrete persistence, DAO, transaction, scheduling, and physical cleanup mechanisms remain downstream implementation choices.

## Authorization boundary

Authorization for reading, continuing, checkpointing, or rollback branching a Conversation is governed by the applicable conversation-data authorization boundary. This document does not establish a new authorization subject or relationship-specific authorization authority.

## Invariants

1. Conversation identity is durable and immutable.
2. Rollback creates a new Conversation identity.
3. Source Conversation remains preserved after rollback.
4. Continuation preserves Conversation identity.
5. Session termination ends only the active association, not the Conversation identity.
6. No independent relationship identity, lifecycle, or state machine is implied.
7. Ordered-record continuity and branch lineage remain distinct concepts.

## Forbidden behavior

Implementation must not infer that:
- Session identity equals Conversation identity,
- rollback is destructive rewind of the source Conversation,
- continuation creates a new Conversation,
- Session closure or expiration deletes the Conversation,
- process death automatically creates a new Conversation,
- application restart automatically creates cross-Session continuation,
- checkpoint lifecycle owns Conversation semantics,
- Runtime or Memory owns the Session–Conversation semantic contract.
