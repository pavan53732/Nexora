# Session–Conversation Runtime and Recovery Semantics — Nexora

> **Status: SUPPORTING** runtime/recovery contract.
> Canonical authority: `state-machines/SessionLifecycle.md`, `architecture/CONVERSATION_CHECKPOINTS.md`, `decisions/DEC-20-session-conversation-association-lifecycle.md`, and `decisions/DEC-21-session-conversation-continuation-recovery.md`.

## Scope

This document defines engineering-facing runtime and recovery semantics for Session and Conversation without selecting concrete recovery algorithms, Android process-restoration mechanics, database transactions, or API transports.

## Normal active session

### Trigger
A valid nonterminal Session is associated with a valid Conversation without violating DEC-19.

### Semantic effect
The Session–Conversation association is active.

### Identity
- Session identity unchanged.
- Conversation identity unchanged.

### Checkpoint / branch effect
None unless a separate checkpoint or rollback operation occurs.

### Forbidden effects
No new relationship identity. No independent relationship lifecycle state.

## Session CLOSED

### Trigger
Canonical Session lifecycle transition to `CLOSED`.

### Preconditions
Session exists and satisfies Session lifecycle guards.

### Semantic effect
The prior active Session–Conversation association ends.

### Identity
- Session identity remains the terminal Session identity.
- Conversation identity unchanged.

### Checkpoint / branch / lineage effect
Unchanged.

### Recovery requirement
No same-identity reopen of the terminal Session.

### Forbidden effects
No Conversation deletion, no checkpoint deletion by implication, no rollback, no lineage mutation.

## Session EXPIRED

### Trigger
Canonical Session lifecycle transition to `EXPIRED`.

### Preconditions
Session lifecycle guards satisfied.

### Semantic effect
The prior active Session–Conversation association ends.

### Identity
- Session identity remains the expired Session identity.
- Conversation identity unchanged.

### Checkpoint / branch / lineage effect
Unchanged.

### Recovery requirement
If work later continues, same-identity reopen is forbidden; a new Session identity is required.

### Forbidden effects
No Conversation destruction, no branch destruction, no automatic continuation.

## Session recreation

### Trigger
A previously terminal Session is reopened through a new Session object/record.

### Semantic effect
The new Session is a distinct Session identity. Any later Conversation association is a new active association.

### Identity
- Old Session identity preserved historically.
- New Session identity distinct.
- Conversation identity depends on whether the operation is continuation (`same Conversation`) or rollback branch usage (`new branch Conversation`).

### Forbidden effects
No mutation of the prior Session identity. No preservation of the terminated Session association as if it never ended.

## Same-Session recovery

### Trigger
Recovery restores the same still-valid Session rather than recreating it.

### Semantic effect
No cross-Session continuation occurs.

### Identity
- Session identity preserved.
- Conversation identity preserved.

### Active association
Remains or is restored as the same Session–Conversation association, subject to implementation successfully restoring the same nonterminal Session.

### Implementation boundary
How same-Session recovery is detected and restored is implementation-specific.

## New-Session continuation

### Trigger
Recovery or later user/system action requires a new Session identity for a Conversation that remains valid for continuation.

### Semantic effect
DEC-21 continuation semantics apply.

### Identity
- new Session identity,
- same Conversation identity,
- new active association.

### Forbidden effects
No new Conversation identity unless a rollback branch is explicitly created.

## Rollback

### Trigger
Valid rollback request against a valid source Conversation and checkpoint.

### Semantic effect
Creates a new branch Conversation and preserves source Conversation.

### Identity
- source Conversation identity unchanged,
- branch Conversation receives a new identity,
- Session identity unchanged unless a separate Session operation occurs.

### Active association
Depends on whether the source or branch Conversation becomes the currently associated Conversation under the active-cardinality rules.

### Forbidden effects
No destructive rewind, no reversal of external side effects, no conflation with continuation.

## Branch continuation

### Trigger
A branch Conversation later becomes associated with a later Session.

### Semantic effect
Continuation applies to the branch Conversation itself.

### Identity
- new Session identity if later Session,
- same branch Conversation identity,
- preserved lineage to source Conversation and source checkpoint.

## Process death

### Trigger
Process termination or unexpected runtime loss.

### Semantic effect
No independently selected Session–Conversation semantic mutation.

### Recovery requirement
Implementation must determine whether same-Session recovery is possible or a new Session continuation path is required.

### Forbidden effects
No automatic assumption that Conversation ended. No automatic assumption that continuation occurred.

## Application restart

### Trigger
Application relaunch after previous process termination or clean stop.

### Semantic effect
No independently selected Session–Conversation semantic mutation.

### Recovery requirement
Implementation may restore same Session or require new Session continuation, but must keep the semantic distinction explicit.

### Forbidden effects
No silent creation of a new Conversation. No silent destruction of branch lineage.
