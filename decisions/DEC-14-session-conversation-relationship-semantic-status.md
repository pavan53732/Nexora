# DEC-14 — Session–Conversation Relationship Semantic Status

> **Status: CANONICAL DECISION**
> This decision establishes only the semantic status of the Session–Conversation relationship. It does not select ownership, identity, representation, lifecycle, cardinality, resumption, persistence, or implementation.

## Problem

The repository establishes Session and Conversation as distinct concepts, but previously left the semantic status of their relationship unresolved. A normative boundary is required without deciding downstream relationship mechanics.

## Existing repository evidence

- `architecture/CONVERSATION_CHECKPOINTS.md` distinguishes Session from Conversation and identifies their relationship as unresolved.
- DEC-10 establishes bounded Conversation and checkpoint responsibilities without classifying the relationship itself.
- DEC-13 establishes durable immutable Conversation identity while explicitly leaving the Conversation-to-Session relationship unresolved.
- `state-machines/SessionLifecycle.md` remains canonical for Session lifecycle and does not transfer that lifecycle to the relationship.
- DEC-8 and DEC-9 establish checkpoint and non-destructive branching semantics that remain unchanged by this decision.

These statements are repository-supported facts. They do not retroactively establish this decision.

## Scope

This decision resolves only whether the Session–Conversation relationship is a first-class semantic relationship at the architecture level.

## Explicit non-scope

This decision does not select association ownership, relationship identity, representation, schema, cardinality, one-active constraints, attachment, detachment, rebinding, reattachment, resumption, Session `CLOSED` effects, Session `EXPIRED` effects, Session recreation, process death, application restart, Conversation lifecycle, relationship-specific lifecycle, branch-lineage ownership, conversation-local metadata schema, message/turn ordering representation, storage technology, database schema, API contract, authorization semantics, retention, deletion, quota, cleanup, archive semantics, or implementation.

## Candidate A: relationship-only / implicit

Candidate A would treat the relationship as having no independent semantic status beyond an incidental reference between Session and Conversation. It would constrain future relationship-specific rules to the existing Session or Conversation authorities.

Candidate A was a viable proposal during analysis, but the repository did not establish it as a pre-existing constraint.

## Candidate B: first-class semantic relationship

Candidate B recognizes the relationship itself as independently meaningful architectural semantics. This means future decisions may define relationship-specific rules without treating them as accidental extensions of Session or Conversation.

First-class semantic status does not by itself require a separate association entity, record, identifier, key, object, state machine, lifecycle, service, API, storage mechanism, schema, event, message, UI construct, authorization subject, or persistence record.

## Evidence for Candidate A

The repository supports distinct Session and Conversation concepts and independent authority boundaries. That evidence is compatible with Candidate A but does not require it.

No repository rule prohibits a future relationship authority, relationship-specific semantics, or a separate semantic boundary. Candidate A is therefore not selected.

## Evidence for Candidate B

The repository treats the Session–Conversation relationship as an explicit unresolved architecture dependency rather than an incidental reference. Session and Conversation are independently meaningful concepts with separate identity/lifecycle boundaries. This supports recognizing their relationship as a semantic boundary, but does not select any downstream representation or ownership.

The decision to classify the relationship as first-class is an owner decision made here. It is not presented as a fact that existed in earlier decisions.

## Rejected interpretations

- The relationship is not automatically identical to either Session or Conversation.
- The absence of an association model does not establish relationship-only semantics.
- First-class semantic status does not imply a separate association entity or database record.
- First-class semantic status does not imply relationship identity.
- First-class semantic status does not imply a relationship lifecycle.
- First-class semantic status does not select cardinality, resumption, storage, schema, API, authorization, retention, deletion, quota, cleanup, or implementation.

## Decision

**Nexora selects Candidate B: the Session–Conversation relationship is a first-class semantic relationship at the architecture level.**

The relationship is not merely an incidental reference between two otherwise unrelated records. Its semantics are sufficiently meaningful that future architecture decisions may define relationship-specific rules without treating those rules as accidental extensions of either Session or Conversation.

No relationship owner is selected by this decision.

## Rationale

Session and Conversation are distinct architectural concepts. Conversation has a durable immutable identity under DEC-13, while Session has an independently canonical lifecycle. The repository therefore provides separate semantic boundaries whose relationship is architecturally meaningful, while leaving all relationship mechanics to later decisions.

This decision preserves the distinction between semantic status and implementation. It creates a canonical boundary for future decisions without collapsing Session into Conversation, transferring Conversation identity ownership, or expanding DEC-10.

## Architectural consequences

- Future relationship-specific rules may be defined by separately scoped architecture decisions.
- Session lifecycle remains solely governed by `state-machines/SessionLifecycle.md`.
- Conversation identity remains governed by DEC-13.
- DEC-8 checkpoint/rollback semantics remain unchanged.
- DEC-9 non-destructive branching, new Conversation identity, source preservation, and lineage requirements remain unchanged.
- DEC-10 responsibility remains unchanged and is not silently expanded.

## Explicit non-decisions

Relationship identity, relationship representation, association ownership, relationship lifecycle, cardinality, one-active constraints, attachment, detachment, rebinding, reattachment, resumption, Session termination effects, Conversation lifecycle, persistence, storage, schema, API, authorization, retention, deletion, quota, cleanup, and archive semantics remain OWNER DECISION REQUIRED / UNRESOLVED.

## Open downstream decisions

The unresolved decisions listed in the explicit non-scope and explicit non-decisions sections remain independent future architecture work. First-class semantic status does not select their outcomes.

## Compatibility

### DEC-8

Compatible. Conversation checkpoint and rollback semantics are unchanged.

### DEC-9

Compatible. Non-destructive branching, new Conversation identity, source preservation, and lineage requirements are unchanged.

### DEC-10

Compatible. Existing Conversation/Session responsibility remains intact. This decision does not assign relationship ownership to the Conversation/Session subsystem, Session, Conversation, Runtime, or checkpoint subsystem.

### DEC-13

Compatible. Durable immutable Conversation identity remains intact. DEC-13 previously left the Conversation-to-Session relationship unresolved; this decision resolves only its semantic status and does not reinterpret DEC-13 retroactively.

## Traceability implications

This decision is documentation-only and not implemented. `docs/CANONICAL_SOURCES.md`, `docs/TRACEABILITY.md`, `docs/DECISION_LOG.md`, and `architecture/CONVERSATION_CHECKPOINTS.md` may reference this decision as the authority for semantic status while preserving all downstream unresolved boundaries.
