> **Status: DERIVED** for Session domain model.
> This document defines the shape and semantics of Session in the data model.
>
> Canonical lifecycle authority: `../state-machines/SessionLifecycle.md`.
> Canonical runtime boundary: `../architecture/RUNTIME.md`.
> Session–Conversation semantic authority: `../architecture/CONVERSATION_CHECKPOINTS.md` and DEC-14 through DEC-21.
> Referenced by: runtime, persistence, memory, execution, orchestration, and future implementation documents.

# Domain Model: Session

```kotlin
data class Session(
    val id: String,
    val workspaceId: String,
    val correlationId: String?,
    val status: SessionStatus,
    val activeTaskId: String?,
    val activeAgentId: String?,
    val createdAt: Instant,
    val updatedAt: Instant,
    val closedAt: Instant? = null
)

enum class SessionStatus {
    CREATED,
    ACTIVE,
    IDLE,
    CLOSED,
    EXPIRED
}
```

## Purpose

A Session is a durable runtime-context container inside a Workspace. It tracks the current runtime interaction boundary and remains distinct from Task, Execution, Conversation, Checkpoint, Memory, and ContextSnapshot.

## Ownership

Session lifecycle is canonically owned by `../state-machines/SessionLifecycle.md`.

Session does not own Conversation identity, checkpoint lineage, rollback semantics, or the semantic contract of Task or Execution lifecycle. The Session–Conversation relationship semantic contract is owned by the existing Conversation/Session responsibility under DEC-15, not by Session alone.

## Identity semantics

Session identity is durable for the lifetime of that Session record. A Session identity is not a Conversation identity, checkpoint identity, branch identity, task identity, or execution identity.

Reopening a terminal Session does not preserve the same Session identity; recreation produces a new Session identity.

## Creation

A Session is created as a durable runtime record within a Workspace. This document does not select the concrete API, persistence transaction, or UI flow that creates it.

## Lifecycle

Canonical lifecycle authority is defined in `../state-machines/SessionLifecycle.md`. The prose lifecycle narrative in `../lifecycle/SessionLifecycle.md` is supporting only.

Session states are:
- `CREATED`
- `ACTIVE`
- `IDLE`
- `CLOSED`
- `EXPIRED`

`CLOSED` and `EXPIRED` are terminal.

## ACTIVE and terminal behavior

`ACTIVE` means the Session currently has active interaction or runtime context. `IDLE` means the Session remains available without active task/agent interaction. `CLOSED` and `EXPIRED` are terminal Session states and end any active Session–Conversation association under DEC-20.

Terminal Session states do not by themselves delete a Conversation, mutate Conversation identity, destroy checkpoints, or rewrite branch lineage.

## Recreation

A terminal Session cannot simply become active again as the same Session identity. Reopening after terminal closure/expiration requires a new Session identity. Any later Conversation association is therefore a new active association.

## Relationship to Conversation

Session and Conversation are distinct concepts.

The Session–Conversation relationship:
- is first-class semantic architecture,
- has no independent relationship identity,
- has no independent lifecycle,
- allows at most one active Conversation per Session at a point in time,
- ends active association when the Session becomes `CLOSED` or `EXPIRED`,
- may later continue the same Conversation through a new Session identity under DEC-21.

Session must not be documented or implemented as permanently equal to Conversation.

## Relationship to Runtime

Runtime may create, load, close, or recover Sessions as part of execution flow, but Runtime does not own the Session–Conversation semantic contract merely because it coordinates Session use.

## Relationship to Task and Execution

Session is not a substitute for Task lifecycle or Execution lifecycle.

Task completion/failure does not imply Session closure. Execution checkpoint/recovery does not by itself define Conversation rollback semantics. A Session may retain `correlationId` alignment with active execution for observability, but Session identity remains separate from Execution identity.

## Relationship to Context and Memory

Context and Memory may reference Session-scoped data, but they do not own Session lifecycle or the Session–Conversation relationship semantics. Session expiration/closure does not automatically redefine memory retention or context snapshot ownership.

## Process death and application restart

Process death and application restart are not by themselves Session–Conversation semantic decisions. They are recovery contexts.

If the same nonterminal Session is restored, that is same-Session recovery. If a new Session is required, recreation/continuation semantics apply. The concrete recovery mechanism remains an implementation choice.

## Recovery boundary

This model distinguishes semantic effect from implementation mechanism:
- semantic effect: whether the same Session survives or a new Session is required,
- implementation mechanism: how Android/runtime restoration actually loads or recreates it.

## Persistence boundary

Session identity, workspace ownership, lifecycle state, timestamps, and any current runtime references that the implementation selects to persist belong to the Session persistence boundary.

This document does not mandate a concrete Room schema, API envelope, or serialization format.

## Cleanup boundary

Cleanup, retention, archival, and physical deletion policy are not selected by this model. Session terminal state is not equivalent to immediate deletion.

## Invariants

1. Session identity is distinct from Conversation identity.
2. Session state does not replace Task state.
3. Session state does not replace Execution state.
4. A terminal Session cannot be reopened as the same identity.
5. Session terminality ends active Session–Conversation association but does not mutate Conversation identity.

## Forbidden operations

Implementation/documentation must not infer that:
- Session equals Conversation,
- reopening terminal Session preserves the same Session identity,
- Session closure deletes a Conversation,
- Session expiration deletes a Conversation,
- Runtime, Memory, or Checkpoint owns the Session–Conversation semantic contract.
