# DEC-21 — Session–Conversation Continuation and Recovery Semantics

> **Status: CANONICAL DECISION**
> This decision resolves only continuation, resumption, and recovery semantics for the Session–Conversation relationship. It does not select storage, schema, API, identifier formats, authorization, or implementation.

## Decision

**A Conversation may continue through a later Session, but such continuation creates a new active association rather than preserving the terminated Session association.**

**Conversation continuation across Sessions preserves Conversation identity and ordered conversation record continuity.**

**Rollback branch creation creates a new Conversation identity and therefore cannot be a continuation of the source Conversation relationship.**

## Context

DEC-20 left continuation and resumption unresolved. Session recreation creates a new Session identity. Conversation identity remains durable and immutable under DEC-13. The remaining question is whether a Conversation may be resumed through a later Session and how that interacts with branching and recovery.

## Repository-supported facts

- DEC-13 establishes durable immutable Conversation identity.
- Session lifecycle states that reopening a terminal Session creates a new Session identity.
- DEC-9 states that rollback creates a new Conversation branch identity while preserving the source Conversation.
- DEC-19 constrains active association to one active Session ↔ one active Conversation at a point in time.
- No decision prohibits continuation of the same Conversation through a later Session.

## Candidate evaluation

### No continuation across Sessions

Rejected. It would make Session termination artificially stronger than Conversation identity and ordered-record continuity, without repository evidence requiring that break.

### Continuation across Sessions with preserved Conversation identity and new active association

Selected. It preserves durable Conversation identity, respects new Session identity after Session recreation, and remains compatible with DEC-19 active cardinality.

### Continuation across Sessions while preserving the original Session association

Rejected. It would contradict Session lifecycle semantics once a terminal Session is recreated under a new Session identity.

## Architectural reasoning

Conversation is the durable ordered-record boundary. Session is the runtime interaction context. When a Session ends, the active association ends under DEC-20. But durable Conversation identity does not need to end with it. The minimum coherent architecture is to allow later continuation of the same Conversation through a new Session while treating that as a new active association.

This preserves locality: Session lifecycle remains Session-specific, while Conversation continuity remains Conversation-specific. It also preserves DEC-19 because only one active Session ↔ one active Conversation may exist at a time. A later Session may resume the same Conversation only by becoming the new active association.

Rollback branching cannot preserve the same relationship because DEC-9 creates a new Conversation identity. The source Conversation and the new branch are distinct Conversations, even if their histories overlap.

Process death and application restart remain recovery contexts rather than distinct relationship events. If recovery restores the same Session before terminal closure, that is Session recovery, not cross-Session continuation. If recovery requires a new Session, continuation semantics apply.

## Exact semantic boundary

DEC-21 establishes only these facts:

- A Conversation may continue through a later Session.
- Continuation across Sessions preserves Conversation identity and ordered conversation record continuity.
- Such continuation creates a new active association because the later Session has a distinct Session identity.
- Rollback branching creates a new Conversation identity and therefore is not continuation of the same Conversation relationship.

## Explicit non-decisions

DEC-21 does not select reference encoding, restoration mechanics, persistence technology, storage, schema, API exposure, authorization, retention, deletion, cleanup, archive semantics, or implementation.

## Compatibility

### DEC-13

Compatible. Durable immutable Conversation identity remains authoritative and is preserved across continuation.

### DEC-19 and DEC-20

Compatible. Only one active association exists at a time, and Session termination still ends the prior active association.

### DEC-8 and DEC-9

Compatible. Source preservation, checkpoint identity, and branch identity remain unchanged.

## Remaining unresolved decisions

Reference encoding, persistence semantics, storage, schema, API exposure, authorization, retention, deletion, cleanup, archive semantics, and implementation remain unresolved.
