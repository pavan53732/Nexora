# DEC-18 — Session–Conversation Relationship Semantic Representation

> **Status: CANONICAL DECISION**
> This decision resolves only the semantic representation of the first-class Session–Conversation relationship. It does not select storage, persistence, schema, API, serialization, identifiers, cardinality, uniqueness, lifecycle, resumption, authorization, or implementation.

## Decision

**The first-class Session–Conversation relationship is represented semantically through the participating Session and Conversation concepts and their relationship-specific contract under DEC-15; no separate relationship representation is required by the current architecture.**

This is an explicit semantic representation decision, not a decision that the relationship is incidental. The relationship remains first-class under DEC-14, is owned by the existing Conversation/Session responsibility under DEC-15, and has no independent identity under DEC-17.

## Meaning of representation

For this decision, semantic representation means the architecture's recognized way of expressing and reasoning about the relationship. It does not mean a database structure, class, record, object, API resource, serialized form, or storage artifact.

The relationship is represented by the existing Session and Conversation concepts together with the relationship-specific semantic rules governed by DEC-15. No separate relationship-bearing concept is required merely because the relationship is first-class.

## Repository evidence

- DEC-14 explicitly establishes the relationship as first-class semantic architecture while leaving representation unresolved.
- DEC-15 assigns the canonical relationship semantic contract to the existing Conversation/Session responsibility.
- DEC-17 establishes no independent relationship identity.
- DEC-8 and DEC-9 preserve distinctions between Conversation identity, checkpoint identity, branch identity, and lineage without requiring a separately identified Session–Conversation relationship representation.
- Conversation checkpoint documentation states that references do not transfer ownership or restoration semantics.
- Session lifecycle documentation establishes Session lifecycle boundaries without defining a separate relationship representation.
- Existing repository patterns include participant references and relationship-specific semantic rules, but do not establish a universal requirement for a separate relationship concept for every first-class relationship.

## Candidate evaluation

### Candidate A — Implicit relationship through existing concepts

A purely incidental reference would be insufficient because DEC-14 expressly states that the relationship is not merely incidental. However, a semantic representation through the participating concepts and an explicit relationship contract is compatible with DEC-14. This decision selects that stronger semantic form, not incidental-reference status.

### Candidate B — Explicit semantic relationship representation without independent identity

This is the selected semantic form. The relationship is represented explicitly at the architecture level by its relationship-specific contract under DEC-15, while the participating Session and Conversation concepts remain the semantic participants. No separate identity-bearing or independently represented relationship concept is required.

### Candidate C — Representation through participant references

Participant references are compatible with the selected semantic representation as a possible future expression of the relationship. This decision does not prescribe how references are encoded or transported.

### Candidate D — Derived semantic association

A derived association remains a possible explanatory model, but selecting derived mechanics would exceed this decision and could introduce unselected uniqueness or cardinality consequences. No derived association mechanism is selected.

### Candidate E — Separate relationship concept

The repository does not require a separate relationship concept. Selecting one would add architectural structure without evidence that DEC-14, DEC-15, DEC-17, checkpoint semantics, or Session lifecycle require it. It is not selected.

## Architectural reasoning

DEC-14 requires more than an incidental reference: it gives the relationship independent semantic significance. DEC-15 supplies the authority under which relationship-specific rules may be defined. DEC-17 removes the need for a third identity-bearing concept. Together, these decisions justify an explicit semantic relationship contract expressed through the existing participants, without requiring a separate relationship representation.

This preserves boundary integrity. Session remains Session, Conversation remains Conversation, and the relationship is recognized as a first-class semantic boundary under the existing Conversation/Session responsibility. No authority is transferred to checkpoint, runtime, memory, task, execution, workspace, or file subsystems.

The selected representation is the minimum representation that preserves DEC-14's first-class meaning without creating identity, storage, lifecycle, cardinality, or implementation commitments.

## Exact semantic boundary

DEC-18 establishes only this fact:

**The Session–Conversation relationship is semantically represented by the participating Session and Conversation concepts plus the relationship-specific contract owned under DEC-15; no separate relationship representation is required by the current architecture.**

## Explicit non-decisions

DEC-18 does not select a database table, SQL schema, foreign key, ORM model, class, interface, API resource, endpoint, route, serialization format, UUID, ULID, hash, integer identifier, string identifier, composite key, identifier assignment, storage, persistence, cardinality, uniqueness, one-active constraint, attachment, detachment, rebinding, reattachment, lifecycle, creation timing, expiration, deletion, recreation, resumption, process recovery, application restart, retention, authorization, or implementation.

## Compatibility

### DEC-14

Compatible. The relationship remains first-class semantic architecture and is not reduced to an incidental reference.

### DEC-15

Compatible. The existing Conversation/Session responsibility remains the owner of the relationship-specific semantic contract. DEC-18 does not create a second authority.

### DEC-17

Compatible. No independent relationship identity is introduced. Semantic representation does not imply identity.

### DEC-8 and DEC-9

Compatible. Checkpoint, branch, source, and lineage semantics remain unchanged. No relationship representation is converted into checkpoint or branch identity.

### DEC-13

Compatible. Durable immutable Conversation identity remains distinct and authoritative. The relationship representation does not absorb Conversation identity.

## Remaining unresolved decisions

Reference encoding, participant association mechanics, cardinality, uniqueness, lifecycle, attachment, detachment, rebinding, reattachment, resumption, Session effects, Conversation lifecycle, persistence, storage, schema, API exposure, authorization, retention, deletion, quota, cleanup, archive semantics, and implementation remain unresolved.
