# DEC-16 — Session–Conversation Relationship Identity

> **Status: CANONICAL DECISION**
> This decision resolves only the identity semantics of the first-class Session–Conversation relationship. It preserves DEC-15 ownership and does not select representation, cardinality, lifecycle, resumption, persistence, storage, schema, API, or implementation.

## Decision

**The first-class Session–Conversation relationship has an independently meaningful semantic identity.**

This identity is a distinct architectural concept from Session identity, Conversation identity, and Checkpoint identity. It identifies the relationship semantic itself, not either participating concept and not a checkpoint or branch.

The concrete representation of relationship identity is intentionally unresolved.

## Context

DEC-14 established that the Session–Conversation relationship is first-class semantic architecture. DEC-15 assigned ownership of its canonical semantic contract to the existing Conversation/Session responsibility established by DEC-10. DEC-16 now resolves only whether the relationship itself has identity semantics.

## Repository-supported facts

- Session has its own identity and independently canonical lifecycle authority in `state-machines/SessionLifecycle.md`.
- DEC-13 establishes durable immutable Conversation identity and keeps it distinct from Session identity.
- DEC-8 and DEC-9 distinguish Conversation identity, checkpoint identity, and new branch identity; rollback preserves the source and creates a new Conversation branch identity.
- DEC-10 establishes the Conversation/Session responsibility for Conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branch construction.
- DEC-14 establishes first-class relationship semantic status without selecting identity.
- DEC-15 assigns the relationship semantic contract to the existing Conversation/Session responsibility.
- Existing repository identity patterns do not establish that an identity-bearing relationship must use a particular representation or storage mechanism.

## Identity candidates

### No independent relationship identity

This would preserve first-class semantics but make the relationship semantically addressable only through the participating identities. The repository does not require that a first-class relationship have independent identity, but this option weakens distinction between the relationship semantic and its references.

### Independent semantic identity

This gives the relationship its own architectural identity while leaving all representation and mechanics open. It preserves the distinction established by DEC-14 and avoids collapsing the relationship into Session or Conversation.

### Derived identity from Session and Conversation

This treats the relationship identity as a derived pair. It is not selected because it would constrain identity semantics toward a pair identity and could imply uniqueness or cardinality that this decision must not establish.

### Independently assigned concrete identifier

This is a possible future representation, but selecting it now would exceed DEC-16. Independent semantic identity does not select assignment, format, storage, or transport.

### Semantic identity without concrete identifier mechanism

This is the selected form: the relationship is independently meaningful as an identity-bearing architectural concept, while its concrete identifier mechanism remains unresolved.

## Architectural reasoning

The repository does not mechanically force independent relationship identity. The selection is therefore an architecture-owner judgment.

Independent semantic identity best preserves semantic distinguishability: Session identity remains Session identity, Conversation identity remains the durable immutable identity selected by DEC-13, Checkpoint identity remains checkpoint identity, and the relationship remains a separate first-class concept under DEC-15.

It also preserves future extensibility. Later decisions may determine whether identity is represented, derived, assigned, persisted, exposed, or used by another contract without retroactively collapsing the relationship into a Session–Conversation pair or assigning cardinality.

The decision is lifecycle-neutral, cardinality-neutral, resumption-neutral, representation-neutral, and storage-neutral because it establishes only that the relationship itself is semantically distinguishable and may be referred to by future architecture decisions as its own concept.

## Exact semantic boundary

DEC-16 establishes only this fact:

The Session–Conversation relationship is an identity-bearing semantic concept distinct from Session, Conversation, and Checkpoint identities.

This does not mean that a concrete identifier exists in the implementation, that the relationship is persisted, that it is addressable through an API, or that an association record/object is required.

## Explicit non-decisions

DEC-16 does not select a UUID, ULID, integer, string, hash, composite key, database primary key, foreign key, URI, path, object identifier, database identifier, API identifier, or serialization format.

It does not select Session-to-Conversation cardinality, one-active constraints, uniqueness of a Session–Conversation pair, automatic association creation, attachment, detachment, rebinding, reattachment, creation timing, expiration, closure, deletion, recreation, persistence, process recovery, application-restart recovery, resumption, restoration, relationship lifecycle, Conversation lifecycle, storage, database structure, schema, files, serialization, repositories, ORM, API endpoints, events, services, authorization, retention, quota, cleanup, archive behavior, or implementation.

## Compatibility

### DEC-8

Compatible. Checkpoint and rollback semantics remain unchanged. Checkpoint identity remains distinct from relationship identity.

### DEC-9

Compatible. Non-destructive branching, new Conversation identity, source preservation, and parent/source-checkpoint lineage remain unchanged. DEC-16 does not assign lineage ownership.

### DEC-10

Compatible. DEC-16 operates within the Conversation/Session responsibility selected by DEC-15. It does not rewrite DEC-10 or expand Session lifecycle ownership.

### DEC-13

Compatible. Durable immutable Conversation identity remains governed by DEC-13. Relationship identity is distinct and does not replace or absorb Conversation identity.

### DEC-14

Compatible. First-class relationship semantic status is preserved. DEC-16 adds only the relationship’s semantic identity status.

### DEC-15

Compatible. The existing Conversation/Session responsibility remains the canonical owner of the relationship semantic contract. DEC-16 is a subordinate identity decision and creates no competing authority.

## Consequences

Future architecture decisions may determine whether relationship identity requires a concrete identifier, representation, persistence, transport, authorization subject, or other mechanism. None of those mechanisms is selected by DEC-16.

The relationship must not be treated as identical to Session, Conversation, or Checkpoint merely because those concepts participate in or reference it.

## Remaining unresolved decisions

Relationship identifier representation, assignment, derivation mechanics, storage, persistence, schema, API exposure, authorization semantics, cardinality, lifecycle, attachment, detachment, rebinding, reattachment, resumption, Session effects, Conversation lifecycle, retention, deletion, quota, cleanup, archive semantics, and implementation remain unresolved.
