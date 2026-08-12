# Session–Conversation Engineering Contract — Nexora

> **Status: SUPPORTING** implementation-facing semantic contract.
> Canonical decision authority: `decisions/DEC-8-conversation-checkpoint-rollback.md`, `decisions/DEC-9-conversation-rollback-operation.md`, `decisions/DEC-10-conversation-checkpoint-ownership.md`, `decisions/DEC-13-conversation-identity-persistence.md`, and `decisions/DEC-14-session-conversation-relationship-semantic-status.md` through `decisions/DEC-21-session-conversation-continuation-recovery.md`.
> Canonical semantic projection: `architecture/CONVERSATION_CHECKPOINTS.md`.
>
> This document translates the closed Session–Conversation semantic architecture into engineering handoff rules. It does not create a new architecture decision, relationship entity, relationship identity, relationship lifecycle, or implementation mandate beyond the existing decisions.

## Purpose

This specification exists so implementers can build Session/Conversation persistence, runtime integration, API surfaces, validation, and tests without inventing semantics already decided by DEC-8 through DEC-21.

## Authority classification

- **DECIDED** — explicit in DEC-8 through DEC-21 or another canonical source.
- **DERIVED** — direct projection from those decisions.
- **IMPLEMENTATION CHOICE** — required for implementation but not architecturally fixed.
- **DOWNSTREAM** — outside the semantic contract; handled by a later engineering layer.
- **NOT APPLICABLE** — no contract needed at this level.

## Ownership

**DECIDED:** The existing Conversation/Session responsibility established by DEC-10 owns the semantic contract of the Session–Conversation relationship under DEC-15.

**DERIVED:** Session lifecycle remains Session-owned. Conversation identity, ordered records, checkpoint semantics, and rollback branch construction remain Conversation/Session-owned. Runtime, Memory, Context, Task, Execution, Agent, Workflow, Tool, and Workspace may reference the relationship but do not own its semantics.

## Identity

**DECIDED:**
- Session identity exists.
- Conversation identity exists and is durable/immutable under DEC-13.
- Checkpoint identity exists.
- Branch Conversation identity exists when rollback creates a new Conversation.
- No independent Session–Conversation relationship identity exists under DEC-17.

**FORBIDDEN INFERENCE:**
- deriving a canonical relationship ID,
- treating `(sessionId, conversationId)` as a semantic relationship identity,
- introducing an association entity as a new semantic authority.

## Semantic representation

**DECIDED:** Under DEC-18 the relationship is represented semantically through Session, Conversation, and the DEC-15 relationship contract; no separate semantic relationship representation is required.

**IMPLEMENTATION CHOICE:** Internal objects, rows, join fields, caches, or projections may temporarily hold both `sessionId` and `conversationId` so long as they are treated as implementation mechanisms rather than a new semantic authority.

## Active cardinality

**DECIDED:** At most one active Conversation per Session and at most one active Session per Conversation at a point in time under DEC-19.

**DECIDED:** No all-time uniqueness is selected.

**DERIVED historical multiplicity:**
- One Session may be associated with different Conversations sequentially, if not simultaneously active.
- One Conversation may be associated with different Sessions sequentially, if not simultaneously active.

## Active association

An association is semantically active only when:
- the Session exists,
- the Session is not terminal,
- the Conversation is the current associated Conversation for that Session,
- no competing active association violates DEC-19.

This document does not define a separate relationship state machine. Active/inactive is derived from participant state and the current association condition.

## Session CLOSED

**DECIDED semantic effect:**
- prior active association ends,
- Conversation identity unchanged,
- Conversation records unchanged,
- checkpoint semantics unchanged,
- branch lineage unchanged.

**FORBIDDEN:** inferring Conversation deletion, branch destruction, or rollback semantics from Session closure.

## Session EXPIRED

**DECIDED semantic effect:** same relationship effect as `CLOSED` under DEC-20.

Expiration ends the active association without mutating Conversation identity, records, checkpoints, or branch lineage.

## Session recreation

**DECIDED:** A terminal Session cannot resume as the same Session identity. Reopening creates a new Session identity under the canonical Session lifecycle.

**DERIVED:** any later Conversation association after recreation is a new active association.

## Continuation

**DECIDED:** A Conversation may continue through a later Session under DEC-21.

Example:
- `S1 ↔ C1` active,
- `S1` terminates,
- later `S2 ↔ C1`.

Semantic result:
- Session identity = `S2`,
- Conversation identity = `C1`,
- association = new active association,
- ordered Conversation record continuity preserved.

## Rollback

**DECIDED:** Rollback is the non-destructive branch operation selected by DEC-9.

If `C1` rolls back to a valid checkpoint, the result is a new Conversation `C2`:
- `C1` preserved,
- `C2` receives a new Conversation identity,
- lineage to source Conversation and source checkpoint preserved.

Rollback is not continuation.

## Branch continuation

**DERIVED from DEC-9 and DEC-21:** A rollback branch `C2` may later continue through a later Session `S3`. In that case Conversation identity remains `C2`; it does not collapse into `C1`.

## Process death and application restart

**DECIDED:** Process death and application restart are not independently selected relationship mutation events.

**DERIVED:** Their effects depend on recovery behavior chosen by implementation. They do not by themselves end a Conversation, create a new Conversation, or force continuation.

## Recovery

Separate the following:
- **Semantic continuation** — the DEC-21 rule allowing later Session continuation with preserved Conversation identity and a new active association.
- **Concrete recovery mechanism** — process restore, persistence reload, same-Session recovery, or creation of a new Session during recovery.

**IMPLEMENTATION CHOICE:** how recovery determines whether the same Session survives or a new Session is required.

## Persistence contract

Implementation must preserve semantically:
- Session identity,
- Conversation identity,
- ordered Conversation record continuity,
- checkpoint identity and checkpoint-to-Conversation reference,
- rollback branch lineage,
- enough association information to enforce active cardinality and continuation semantics.

Not a relationship-owned persistence concern:
- independent relationship identity,
- relationship lifecycle records as a separate semantic authority,
- all-time uniqueness enforcement.

## API and protocol boundary

This architecture does not require a specific Session API, Conversation API, or relationship API surface.

If implementation exposes operations for continue, rollback, checkpoint, close, or expire, those operations must preserve the semantics in this document. Concrete endpoints, method names, request/response shapes, transport semantics, and idempotency tokens are implementation choices unless selected by a canonical API document.

## Validation and error contract

At minimum, implementation must reject:
- one Session with two active Conversations,
- one Conversation with two active Sessions,
- continuation of a nonexistent or unauthorized Conversation,
- reopening a terminal Session as the same identity,
- rollback that mutates the source Conversation,
- invalid checkpoint or lineage references,
- Conversation identity mutation,
- Session identity mutation,
- unauthorized ownership transfer.

Concrete numeric error codes are downstream unless selected by `errors/ERROR_CODES.md` or a later canonical API source.

## Observability and audit expectations

Audit/event trails should make the following distinguishable:
- Session terminal transition,
- continuation using later Session,
- rollback branch creation,
- source Conversation preservation,
- checkpoint/lineage reference used,
- rejected cardinality conflict,
- rejected identity mutation.

Concrete event shapes are implementation choices.

## Migration and versioning implications

Future implementation must treat these semantic rules as stable architecture. Storage layout, API shape, and persistence encoding may evolve under normal versioning so long as they preserve:
- durable Conversation identity,
- Session recreation semantics,
- active cardinality,
- non-destructive rollback,
- cross-Session continuation semantics.

## Forbidden behavior

Implementation MUST NOT infer that:
- the relationship has its own identity,
- the relationship has its own lifecycle/state machine,
- all-time uniqueness exists,
- Session closure/expiration destroys a Conversation,
- rollback equals continuation,
- continuation creates a new Conversation,
- process death automatically mutates Conversation semantics,
- application restart automatically creates continuation,
- Runtime, Memory, or Checkpoint owns the relationship semantics.
