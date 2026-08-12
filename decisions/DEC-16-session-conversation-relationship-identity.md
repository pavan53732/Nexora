# DEC-16 — Session–Conversation Relationship Identity Status

> **Status: CANONICAL DECISION**
> This decision resolves only the current semantic status of Session–Conversation relationship identity. It preserves DEC-14 first-class relationship semantics and DEC-15 ownership while deferring identity selection, representation, cardinality, lifecycle, resumption, persistence, storage, schema, API, and implementation.

## Decision

**The Session–Conversation relationship identity status remains unresolved.**

DEC-14 establishes that the relationship is first-class semantic architecture. DEC-15 assigns ownership of its canonical semantic contract to the existing Conversation/Session responsibility. DEC-16 does not decide whether the relationship itself has an independent identity.

First-class semantic status does not imply the existence or absence of an independent relationship identity.

## Context

The previous DEC-16 formulation selected independently meaningful relationship identity. That formulation overcommitted identity semantics because DEC-14 did not require independent identity and the repository does not establish a universal rule that every first-class semantic relationship must have one. This corrected DEC-16 preserves the identity question as a separately scoped future architecture decision.

## Repository-supported facts

- Session identity is distinct from Conversation identity and Session lifecycle remains independently canonical.
- DEC-13 establishes durable immutable Conversation identity.
- DEC-8 and DEC-9 distinguish Conversation identity, checkpoint identity, branch identity, and parent/source-checkpoint lineage.
- DEC-14 establishes first-class Session–Conversation relationship semantic status without selecting relationship identity.
- DEC-15 assigns ownership of the relationship semantic contract to the existing Conversation/Session responsibility.
- The repository does not establish that first-class semantic status requires independent relationship identity.
- The repository does not establish a concrete relationship identifier, representation, persistence identity, API identity, or storage identity.

## Preserved identity candidates

The following identity outcomes remain open for a future, separately scoped decision:

### No independent relationship identity

The relationship may remain first-class semantic architecture without having an independent identity distinct from its participating concepts.

### Identity derived from participating concepts

A future decision may examine whether relationship identity is derived from Session and Conversation identities. Any resulting uniqueness or cardinality consequences must be decided separately and are not selected here.

### Independently meaningful relationship identity

A future decision may examine whether the relationship itself has independent semantic identity. That outcome is not selected here.

DEC-16 selects none of these candidates.

## Architectural reasoning

The minimum commitment required after DEC-14 and DEC-15 is to preserve relationship identity as an independently scoped architecture question. Selecting no identity, derived identity, or independent identity now would exceed that minimum commitment.

Keeping the candidates open preserves the distinction between first-class semantic status, ownership, identity, representation, cardinality, lifecycle, resumption, persistence, and implementation. It also preserves reversibility without weakening DEC-14 or reopening DEC-15.

The relationship remains first-class regardless of which future identity outcome is selected. First-class status is not downgraded to an incidental reference.

## Exact semantic boundary

DEC-16 establishes only this fact:

**Relationship identity status is unresolved and deferred to a future architecture decision.**

The future decision may select no independent identity, derived identity, or independently meaningful identity. DEC-16 does not select among them.

## Explicit non-decisions

DEC-16 does not select independent relationship identity, no relationship identity, derived Session–Conversation identity, pair identity, uniqueness, cardinality, one-active constraints, an identifier, identifier assignment, identifier format, relationship key, composite key, association entity, record, object, table, foreign key, persistence identity, API identity, storage identity, lifecycle, creation, attachment, detachment, rebinding, reattachment, activation, closure, expiration, deletion, recreation, restoration, resumption, process-death behavior, application-restart behavior, durable relationship state, stored relationship state, database structure, schema, file, repository, ORM, API endpoint, route, request field, response field, authorization, retention, quota, cleanup, archive behavior, or implementation.

## Compatibility

### DEC-8

Compatible. Checkpoint and rollback semantics remain unchanged. Checkpoint identity remains distinct from the unresolved relationship identity question.

### DEC-9

Compatible. Non-destructive branching, new Conversation identity, source preservation, and parent/source-checkpoint lineage remain unchanged. DEC-16 does not assign lineage ownership.

### DEC-10

Compatible. DEC-16 remains within the Conversation/Session responsibility selected by DEC-15 and does not expand Session lifecycle ownership.

### DEC-13

Compatible. Durable immutable Conversation identity remains governed by DEC-13. Conversation identity is not replaced, redefined, or absorbed by the unresolved relationship identity question.

### DEC-14

Compatible. First-class relationship semantic status remains established. DEC-16 explicitly prevents the invalid inference that first-class status implies independent identity.

### DEC-15

Compatible. The existing Conversation/Session responsibility remains the canonical owner of the relationship semantic contract. DEC-16 creates no competing authority and does not assign representation, storage, lifecycle, or implementation ownership.

## Remaining unresolved decisions

Whether relationship identity is absent, derived from participating concepts, or independently meaningful; concrete identifier representation; assignment; relationship representation; persistence; storage; schema; API exposure; authorization; cardinality; lifecycle; attachment; detachment; rebinding; reattachment; resumption; Session effects; Conversation lifecycle; retention; deletion; quota; cleanup; archive semantics; and implementation remain unresolved.
