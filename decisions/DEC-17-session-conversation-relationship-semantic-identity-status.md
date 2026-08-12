# DEC-17 — Session–Conversation Relationship Semantic Identity Status

> **Status: CANONICAL DECISION**
> This decision resolves only whether the first-class Session–Conversation relationship has independent semantic identity. It does not select a concrete identifier, representation, cardinality, lifecycle, resumption, persistence, storage, schema, API, authorization, or implementation.

## Decision

**The first-class Session–Conversation relationship has no independent semantic identity.**

The relationship remains first-class semantic architecture under DEC-14 and remains governed by the existing Conversation/Session responsibility under DEC-15. “No independent semantic identity” means the relationship is meaningful as architecture, but is not a third identity-bearing concept alongside Session and Conversation.

This decision does not weaken the relationship to an incidental reference. Relationship-specific semantic rules may still be defined under DEC-15 without introducing an independently identified relationship concept.

## Context

DEC-14 established first-class semantic status. DEC-15 assigned ownership of the relationship semantic contract. Corrected DEC-16 preserved the identity question as unresolved and explicitly kept three outcomes open: no independent identity, identity derived from participating concepts, or independently meaningful identity.

DEC-17 now selects the minimum identity commitment justified by the repository and architectural reasoning.

## Repository-supported facts

- Session identity is distinct from durable immutable Conversation identity established by DEC-13.
- Checkpoint identity and branch Conversation identity are distinct concepts under DEC-8 and DEC-9.
- DEC-14 does not require relationship identity.
- DEC-15 provides a semantic authority for relationship rules without requiring an additional identity-bearing concept.
- The repository does not establish an invariant requiring every first-class semantic relationship to have independent identity.
- Repository identity precedents do not establish a universal first-class-to-identity rule.

## Candidate evaluation

### Candidate A — No independent relationship identity

This preserves the first-class semantic relationship while avoiding a third identity concept. It is compatible with DEC-14, DEC-15, DEC-13, checkpoint identity, and branch identity. It does not select any concrete representation and leaves future relationship-specific rules available under DEC-15.

### Candidate B — Identity derived from participating concepts

This could provide a future way to refer to a relationship, but selecting it would require additional decisions about derivation semantics and could create uniqueness or cardinality implications. No such implications are selected here. Candidate B is therefore not required and is rejected as a premature identity-mechanics commitment.

### Candidate C — Independently meaningful relationship identity

This would preserve a distinct relationship concept, but it would add a third identity-bearing architectural concept without a repository invariant requiring one. DEC-14’s first-class semantic status can be preserved without this additional commitment. Candidate C is therefore rejected as unnecessary architectural expansion.

## Architectural reasoning

Candidate A is the strongest minimum-commitment outcome. The relationship’s semantic importance is already established by DEC-14, and its semantic authority is already established by DEC-15. Independent identity is not necessary to make the relationship first-class, and derived identity would introduce identity mechanics that could affect future cardinality or uniqueness decisions.

Selecting no independent relationship identity preserves the distinction between Session identity and Conversation identity while avoiding unnecessary authority and identity coupling. It also preserves future extensibility for relationship semantics without creating an independently identified relationship concept.

This decision is representation-neutral, lifecycle-neutral, cardinality-neutral, resumption-neutral, persistence-neutral, storage-neutral, API-neutral, and implementation-neutral.

## Exact semantic boundary

DEC-17 establishes only this fact:

**The Session–Conversation relationship has no independent semantic identity.**

The relationship remains first-class semantic architecture and may have relationship-specific semantic rules. Those rules must not be interpreted as creating a separate relationship identity, representation, lifecycle, storage object, or API resource.

## Explicit non-decisions

DEC-17 does not select identity derived from participating concepts, pair identity, uniqueness, cardinality, one-active constraints, a concrete identifier, identifier assignment, identifier format, relationship key, composite key, association entity, record, object, table, foreign key, persistence identity, API identity, storage identity, creation, attachment, detachment, rebinding, reattachment, activation, closure, expiration, deletion, recreation, restoration, resumption, process-death behavior, application-restart behavior, durable relationship state, stored relationship state, database structure, schema, file, repository, ORM, API endpoint, route, request field, response field, authorization, retention, quota, cleanup, archive behavior, or implementation.

## Compatibility

### DEC-8

Compatible. Checkpoint and rollback semantics remain unchanged. Checkpoint identity remains distinct from Session and Conversation identities; no relationship identity is introduced.

### DEC-9

Compatible. Non-destructive branching, new Conversation identity, source preservation, and parent/source-checkpoint lineage remain unchanged. Branch identity is not relationship identity.

### DEC-10

Compatible. The Conversation/Session responsibility continues to own the relationship semantic contract under DEC-15. No new identity authority is created.

### DEC-13

Compatible. Durable immutable Conversation identity remains governed by DEC-13 and remains distinct from Session identity. No relationship identity absorbs either concept.

### DEC-14

Compatible. The relationship remains first-class semantic architecture. This decision separates first-class semantic status from independent identity rather than weakening the relationship.

### DEC-15

Compatible. DEC-15 remains the canonical ownership decision for relationship semantics. DEC-17 does not create a competing authority or expand ownership into representation, storage, lifecycle, or implementation.

### DEC-16

Compatible. Corrected DEC-16 deferred identity status. DEC-17 now resolves that deferred question by selecting no independent semantic identity.

## Consequences

Relationship-specific semantics may be defined in future decisions under DEC-15 without introducing a separate identity-bearing relationship concept. Any future representation of references between Session and Conversation must not be interpreted as an independent relationship identity unless a later architecture decision explicitly changes this decision.

## Remaining unresolved decisions

Derived identity mechanics, relationship representation, cardinality, lifecycle, attachment, detachment, rebinding, reattachment, resumption, Session effects, Conversation lifecycle, persistence, storage, schema, API exposure, authorization, retention, deletion, quota, cleanup, archive semantics, and implementation remain unresolved.
