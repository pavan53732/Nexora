# Session–Conversation Implementation Handoff — Nexora

> **Status: SUPPORTING** implementation handoff document.
> Canonical authority: DEC-8 through DEC-21, `architecture/CONVERSATION_CHECKPOINTS.md`, `state-machines/SessionLifecycle.md`, `models/Session.md`, and `models/Conversation.md`.

## Purpose

This document is the bridge between the closed Session–Conversation semantic architecture and future implementation work. An engineer should be able to begin persistence, runtime, API, validation, and test design without inventing Session/Conversation semantics.

## Authoritative sources

- Conversation checkpoint and rollback semantics: `architecture/CONVERSATION_CHECKPOINTS.md`
- Session lifecycle: `state-machines/SessionLifecycle.md`
- Session model projection: `models/Session.md`
- Conversation model projection: `models/Conversation.md`
- Engineering contract: `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`
- Runtime/recovery contract: `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md`
- Error/validation contract: `specs/SESSION_CONVERSATION_ERRORS.md`
- Test matrix: `testing/SESSION_CONVERSATION_TEST_MATRIX.md`

## Semantic invariants

1. Session and Conversation are distinct concepts.
2. Session–Conversation is first-class semantic architecture.
3. The relationship semantic contract is owned by the existing Conversation/Session responsibility.
4. No independent relationship identity exists.
5. No independent relationship lifecycle exists.
6. At most one active Session ↔ one active Conversation exists at a point in time.
7. No all-time uniqueness exists.
8. Session `CLOSED`/`EXPIRED` end the active association only.
9. Session recreation produces a new Session identity.
10. Continuation preserves Conversation identity and creates a new active association.
11. Rollback creates a new Conversation identity and preserves the source Conversation.
12. A rollback branch may later continue through another Session.

## Identity rules

- Session identity exists and is distinct from Conversation identity.
- Conversation identity is durable and immutable.
- Checkpoint identity exists and is distinct from Conversation identity.
- Branch Conversation identity exists and is distinct from the source Conversation identity.
- Relationship identity does not exist as a semantic class.

## Association rules

- Active association is derived from participant state and the current association condition.
- A Session cannot have two active Conversations at the same time.
- A Conversation cannot have two active Sessions at the same time.
- Sequential historical reuse in either direction is allowed.

## Lifecycle and continuation rules

- Session lifecycle remains governed by `state-machines/SessionLifecycle.md`.
- Conversation does not gain an independently selected lifecycle from this handoff.
- Session `CLOSED`/`EXPIRED` end active association without changing Conversation identity/records/checkpoints/lineage.
- Same-identity reopen of a terminal Session is forbidden.
- Later Session continuation of the same Conversation is allowed and preserves Conversation identity.

## Rollback and branch rules

- Rollback is non-destructive branch creation.
- Source Conversation remains preserved.
- Branch receives a new Conversation identity.
- Branch lineage to source Conversation and source checkpoint must be preserved.
- Rollback is never described or implemented as continuation.

## Persistence contract

Implementation must preserve:
- Session identity,
- Conversation identity,
- ordered Conversation record continuity,
- checkpoint references,
- branch lineage,
- enough association history/current state to enforce active cardinality and continuation semantics.

## API boundary

The architecture does not require a dedicated relationship API. Future APIs may expose Session, Conversation, checkpoint, continue, or rollback operations, but they must preserve the semantic rules above.

Implementation-specific choices that remain open:
- endpoint naming,
- transport shape,
- database encoding,
- table layout,
- serialization,
- idempotency-token transport,
- event schema.

## Runtime and recovery contract

- Process death and application restart are not by themselves relationship mutation events.
- Recovery must explicitly distinguish same-Session recovery from new-Session continuation.
- If a new Session is required, continuation semantics apply.
- Concrete Android/process recovery mechanics are implementation-specific.

## Validation/error contract

Reject at minimum:
- simultaneous dual active association in either direction,
- same-identity reopen of terminal Session,
- invalid continuation,
- invalid rollback,
- source-muting rollback,
- invalid lineage,
- identity mutation,
- unauthorized ownership transfer.

## Cross-domain ownership boundaries

- Runtime references Session/Conversation but does not own their relationship semantics.
- Task/Execution remain separate lifecycle authorities.
- Memory references conversation data but does not own the relationship.
- Checkpoint lifecycle remains checkpoint-owned.
- Authorization, retention, cleanup, and deletion policies remain with their own authorities unless a canonical persistence/security source selects them.

## Prohibited architectural assumptions

Do not assume:
- relationship ID,
- relationship entity,
- relationship service as semantic owner,
- relationship lifecycle/state machine,
- all-time uniqueness,
- Session termination destroys a Conversation,
- continuation creates new Conversation,
- rollback preserves source Conversation identity as the active branch identity.
