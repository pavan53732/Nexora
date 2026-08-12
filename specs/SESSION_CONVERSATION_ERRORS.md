# Session–Conversation Validation and Error Contract — Nexora

> **Status: SUPPORTING** validation/error specification.
> Canonical authority: `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`, `architecture/CONVERSATION_CHECKPOINTS.md`, `state-machines/SessionLifecycle.md`, and DEC-8 through DEC-21.

## Scope

This document defines invalid semantic operations and the expected semantic result. It does not assign numeric error codes unless another canonical error source does so later.

## Error cases

### 1. Session associated with two active Conversations
- Error condition: one Session is made simultaneously active with more than one Conversation.
- Why invalid: violates DEC-19 active cardinality.
- Expected semantic result: reject the conflicting operation.
- Identity effect: none.
- Association effect: pre-existing valid active association unchanged.
- Conversation effect: none.
- Session effect: none beyond failure reporting.
- Checkpoint effect: none.
- Lineage effect: none.
- Recovery expectation: caller must retry only after the active conflict is resolved.

### 2. Conversation associated with two active Sessions
- Error condition: one Conversation is made simultaneously active with more than one Session.
- Why invalid: violates DEC-19 active cardinality.
- Expected semantic result: reject the conflicting operation.
- Identity/association/conversation/session/checkpoint/lineage effects: none except failure.
- Recovery expectation: resolve the active conflict first.

### 3. Attempt to continue nonexistent Conversation
- Error condition: continuation references a Conversation that does not exist or is not addressable.
- Why invalid: continuation requires an addressable source Conversation.
- Expected semantic result: no new association created.
- Identity effect: no Session/Conversation identity mutation.
- Recovery expectation: caller must provide a valid source Conversation or choose another operation.

### 4. Attempt to continue using invalid Session
- Error condition: continuation attempts to use a terminal or otherwise invalid Session contrary to Session lifecycle rules.
- Why invalid: terminal Session cannot be reused as the same active Session.
- Expected semantic result: reject continuation on that Session.
- Identity effect: no mutation of the invalid Session identity; if continuation is later allowed, it must use a valid Session identity.

### 5. Attempt to reopen terminal Session as same identity
- Error condition: implementation treats a terminal Session as reopened without creating a new Session identity.
- Why invalid: canonical Session lifecycle forbids transition out of terminal states and requires recreation as a new identity.
- Expected semantic result: reject same-identity reopen.
- Identity effect: old Session identity remains historical only.

### 6. Invalid checkpoint rollback
- Error condition: rollback references nonexistent, unauthorized, stale, expired, or integrity-invalid checkpoint data.
- Why invalid: rollback requires valid checkpoint lineage and authorization.
- Expected semantic result: no branch created; source Conversation unchanged.

### 7. Rollback that mutates source Conversation
- Error condition: rollback rewrites or truncates the source Conversation instead of creating a branch.
- Why invalid: DEC-9 requires non-destructive branching.
- Expected semantic result: reject or recover without claiming success.
- Conversation effect: source Conversation remains preserved.

### 8. Invalid branch lineage
- Error condition: branch creation omits or corrupts parent/source lineage.
- Why invalid: rollback branch must preserve lineage to source Conversation and source checkpoint.
- Expected semantic result: reject creation or recover to no branch.

### 9. Invalid checkpoint lineage
- Error condition: lineage points to a checkpoint not belonging to the claimed source Conversation.
- Why invalid: checkpoint reference must match the source Conversation lineage.
- Expected semantic result: reject rollback/branch creation.

### 10. Conversation identity mutation
- Error condition: implementation rewrites an existing Conversation identity during continuation, persistence repair, or branch processing.
- Why invalid: DEC-13 makes Conversation identity durable and immutable.
- Expected semantic result: reject the mutation and preserve existing Conversation identity.

### 11. Session identity mutation
- Error condition: implementation rewrites Session identity during recovery or recreation.
- Why invalid: Session recreation creates a new Session identity rather than mutating the old one.
- Expected semantic result: preserve historical Session identity and require a new Session when needed.

### 12. Invalid ordered-record mutation
- Error condition: implementation claims continuation or rollback while corrupting or reordering the Conversation record boundary inconsistently with checkpoint/lineage semantics.
- Why invalid: checkpoints and continuation depend on stable ordered-record semantics.
- Expected semantic result: reject or recover without claiming semantic success.

### 13. Unauthorized ownership transfer
- Error condition: Runtime, Memory, Checkpoint, or another subsystem is treated as the semantic owner of the Session–Conversation relationship without canonical authority.
- Why invalid: DEC-15 fixes ownership in the existing Conversation/Session responsibility.
- Expected semantic result: reject the conflicting authoritative interpretation in implementation/docs; no semantic ownership transfer occurs.
