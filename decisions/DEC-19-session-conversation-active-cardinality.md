# DEC-19 — Session–Conversation Relationship Cardinality and Active Association Semantics

> **Status: CANONICAL DECISION**
> This decision resolves only the semantic cardinality and active-association constraints of the first-class Session–Conversation relationship. It does not select identifiers, storage, schema, API, serialization, lifecycle mechanics beyond active association semantics, authorization, or implementation.

## Decision

**At any given time, a Session is associated with at most one active Conversation, and a Conversation is associated with at most one active Session.**

This is an active-association semantic constraint, not a global historical uniqueness rule. The architecture does not require that either participant have only one relationship across all time.

## Context

DEC-14 established the relationship as first-class semantic architecture. DEC-15 assigned its semantic contract to the existing Conversation/Session responsibility. DEC-17 established that the relationship has no independent identity. DEC-18 established that the relationship is represented semantically through the participating Session and Conversation concepts plus the DEC-15 contract. Cardinality and active-association constraints remained unresolved.

## Repository-supported facts

- Session lifecycle defines `ACTIVE`, `IDLE`, `CLOSED`, and `EXPIRED` states and states that reopening a terminal Session creates a new Session identity.
- Session lifecycle requires that closing an `ACTIVE` Session must detach or complete active Task and Execution references.
- DEC-13 establishes durable immutable Conversation identity distinct from Session identity.
- DEC-8 and DEC-9 establish conversation checkpoint and branch semantics where rollback creates a new Conversation identity while preserving the source Conversation.
- The repository does not establish many-conversation simultaneous activity within a single Session.
- The repository does not establish simultaneous multi-Session activity for a single Conversation.

## Candidate evaluation

### Unconstrained many-to-many

Rejected. It would maximize theoretical flexibility but would weaken semantic locality and make Session activity, Conversation continuation, and branch interaction less coherent without any repository need for that breadth.

### One Session to many simultaneous Conversations

Rejected. A Session is modeled as a durable runtime context container for active interaction, not as a semantic multiplexor of independent simultaneously active Conversations.

### Many simultaneous Sessions to one Conversation

Rejected. It would blur Session-local runtime context and complicate active interaction semantics without repository support.

### One active Session ↔ one active Conversation

Selected. It is the minimum coherent active-association constraint that preserves Session locality, Conversation continuity, and rollback/branch reasoning while avoiding a global uniqueness rule.

## Architectural reasoning

The repository distinguishes Session and Conversation but consistently treats each active interaction context as singular rather than multiplexed. The Session lifecycle describes one durable runtime context with one active interaction context. Conversation rollback and branching create a new Conversation identity rather than preserving one Conversation as simultaneously active across multiple branches or runtime contexts.

Selecting an active one-to-one constraint is the smallest semantic cardinality that preserves locality without creating unnecessary historical uniqueness. A Session may, across time, be associated with different Conversations, and a Conversation may, across time, be associated with different Sessions if later decisions permit continuation or resumption. DEC-19 does not decide those temporal questions; it constrains only concurrent active association.

## Exact semantic boundary

DEC-19 establishes only this fact:

**The Session–Conversation relationship is semantically one-to-one for active association at a point in time.**

This does not establish all-time uniqueness, attachment timing, rebinding rules, resumption rules, persistence, or representation mechanics.

## Explicit non-decisions

DEC-19 does not select historical uniqueness, identifier assignment, reference encoding, storage, persistence, schema, API, authorization, attachment, detachment, rebinding, reattachment, resumption, lifecycle completion rules, deletion semantics, or implementation.

## Compatibility

### DEC-14

Compatible. The relationship remains first-class and gains a bounded active cardinality constraint.

### DEC-15

Compatible. The existing Conversation/Session responsibility remains the canonical owner of the relationship semantic contract.

### DEC-17

Compatible. No independent relationship identity is introduced.

### DEC-18

Compatible. The selected active cardinality works with semantic representation through the participants and the DEC-15 contract.

### DEC-8, DEC-9, DEC-13

Compatible. Checkpoint identity, branch identity, source preservation, and durable immutable Conversation identity remain unchanged.

## Remaining unresolved decisions

Attachment semantics, detachment semantics, rebinding, reattachment, continuation across Sessions, resumption, persistence, storage, schema, API exposure, authorization, retention, deletion, cleanup, archive semantics, and implementation remain unresolved.
