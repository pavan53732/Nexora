# DEC-20 — Session–Conversation Association Lifecycle and Session-Termination Effects

> **Status: CANONICAL DECISION**
> This decision resolves only the semantic association lifecycle requirements for the Session–Conversation relationship, including Session termination effects and recovery boundaries. It does not select storage, schema, API, identifier formats, authorization, or implementation.

## Decision

**The Session–Conversation relationship has no independent lifecycle of its own. Its semantics are expressed through participant state and association rules under the DEC-15 contract.**

**Session `CLOSED` and `EXPIRED` terminate the active association but do not alter Conversation identity, Conversation record integrity, checkpoint lineage, or branch history.**

**Process death and application restart do not themselves redefine the relationship; they are recovery conditions governed by participant authorities and any future resumption decisions.**

## Context

DEC-19 selected one active Session ↔ one active Conversation at a point in time. The remaining question is whether the relationship itself requires a separate lifecycle and what Session termination and recovery events mean semantically for the association.

## Repository-supported facts

- Session lifecycle defines `CLOSED` and `EXPIRED` as terminal Session states and states that reopening a terminal Session creates a new Session identity.
- Session lifecycle distinguishes Session state from Task and Execution state.
- DEC-13 establishes durable immutable Conversation identity distinct from Session identity.
- DEC-8 and DEC-9 preserve Conversation checkpoint, branch identity, source preservation, and lineage semantics independently of Session terminal state.
- No repository source defines a separate Session–Conversation lifecycle state machine.
- Conversation resumption through a later Session remained unresolved prior to this decision.

## Candidate evaluation

### Independent relationship lifecycle

Rejected. DEC-17 already removes independent relationship identity, and the repository does not require a third lifecycle authority for the association.

### Participant-driven association semantics without independent lifecycle

Selected. Association semantics can be expressed through Session state, Conversation continuity, and DEC-15 relationship rules without inventing independent lifecycle states.

## Architectural reasoning

A first-class relationship can require semantic rules without requiring a separate lifecycle state machine. The Session lifecycle already provides terminal Session conditions. Conversation identity and checkpoint/branch semantics already preserve Conversation continuity independently. The minimum coherent architecture is therefore participant-driven association semantics.

Session termination must end active association because DEC-19 permits at most one active Conversation per active Session. But Session termination does not imply Conversation deletion, Conversation mutation, lineage change, or checkpoint invalidation. Reopening a terminal Session creates a new Session identity, so any later association with the same Conversation would be a new active association under a new Session, not a continuation of the terminated Session.

Process death and application restart are not semantic relationship events by themselves. They may trigger recovery behavior under Session, Execution, or future resumption decisions, but DEC-20 does not select recovery mechanics.

## Exact semantic boundary

DEC-20 establishes only these facts:

- The relationship has no independent lifecycle.
- Session `CLOSED` and `EXPIRED` end active association.
- Session recreation creates a new Session identity; any later association is not the same active association.
- Process death and application restart do not by themselves alter Conversation identity or create new relationship semantics.

## Explicit non-decisions

DEC-20 does not select resumption, reattachment mechanics, restoration, persistence technology, storage, schema, API exposure, authorization, retention, deletion, cleanup, archive semantics, or implementation.

## Compatibility

### DEC-19

Compatible. Ending active association on terminal Session state preserves the one-active association constraint.

### DEC-17 and DEC-18

Compatible. No independent relationship identity or separate relationship representation is introduced.

### DEC-8, DEC-9, DEC-13

Compatible. Conversation identity, checkpoint semantics, branch identity, source preservation, and lineage remain unchanged.

## Remaining unresolved decisions

Continuation across Sessions, conversation resumption, participant reference encoding, persistence semantics, storage, schema, API exposure, authorization, retention, deletion, cleanup, archive semantics, and implementation remain unresolved.
