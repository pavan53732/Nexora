# DEC-15 — Session–Conversation Relationship Ownership

> **Status: CANONICAL DECISION**
> This decision assigns ownership of the semantic contract for the first-class Session–Conversation relationship only. It does not select relationship identity, representation, lifecycle, cardinality, resumption, persistence, storage, API, authorization, retention, cleanup, or implementation.

## Problem

DEC-14 establishes the Session–Conversation relationship as a first-class semantic relationship but leaves its semantic authority unresolved. A canonical owner is required so later decisions can define relationship-specific rules without silently expanding Session, Conversation, Runtime, checkpoint, or Memory authority.

## Repository evidence

- DEC-10 establishes a bounded Conversation/Session responsibility for conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branch construction.
- DEC-10 states that Runtime requests checkpoint or rollback operations but does not own conversation semantics.
- DEC-10 states that Memory and other subsystems retain ownership of their own artifacts and lifecycles.
- DEC-10 states that cross-subsystem references remain references and do not transfer ownership.
- DEC-13 assigns durable immutable Conversation identity while preserving independent Session lifecycle authority.
- DEC-14 establishes first-class semantic relationship status while explicitly leaving ownership unresolved.
- `architecture/CONVERSATION_CHECKPOINTS.md` identifies the Conversation/Session responsibility as the existing boundary for Conversation checkpoint semantics and preserves relationship ownership as unresolved.
- `state-machines/SessionLifecycle.md` is canonical for Session lifecycle and does not own Conversation relationship semantics.
- `architecture/MEMORY_SYSTEM.md` is canonical for memory storage, retention, promotion, and summarization; its scope terminology does not assign Conversation/Session relationship ownership.

## Candidates considered

### Session

Session is a participant and owns Session lifecycle semantics, but no repository authority assigns it ownership of Conversation relationship semantics. Selecting Session would risk expanding Session lifecycle authority.

### Conversation

Conversation identity and conversation-local records are governed through the Conversation/Session responsibility and DEC-13, but no authority assigns exclusive relationship ownership to Conversation. Selecting Conversation could absorb Session-related semantics.

### Existing Conversation/Session responsibility

DEC-10 provides the closest existing semantic boundary. Its listed responsibility covers Conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branching. It does not explicitly include the first-class relationship established later by DEC-14, so this option requires a narrow scope extension rather than a claim that DEC-10 already decided it.

### Runtime

Rejected. DEC-10 explicitly states that Runtime does not own conversation semantics.

### Checkpoint authority

Rejected as exclusive owner. Checkpoint authority owns checkpoint and rollback semantics. References to Session or Conversation do not transfer ownership of the broader relationship.

### Memory authority

Rejected. Memory owns memory artifacts and their lifecycles. Session and Conversation memory scopes are memory terminology, not ownership of product-level relationship semantics.

### New dedicated relationship authority

Architecturally compatible, but not selected. The repository already provides a Conversation/Session semantic boundary, and introducing a parallel authority would duplicate ownership unless the existing boundary proves insufficient.

### Other existing authority

No other repository-supported owner was identified.

## Decision

**The existing Conversation/Session responsibility established by DEC-10 owns the canonical semantic contract of the first-class Session–Conversation relationship.**

This is a narrow scope extension made by DEC-15. It does not mean DEC-10 previously selected first-class relationship status, and it does not retroactively alter DEC-10.

The owner is the existing Conversation/Session responsibility as a canonical semantic boundary. DEC-15 does not assign ownership to Session alone, Conversation alone, Runtime, Checkpoint, Memory, or implementation components.

## Rationale

The existing Conversation/Session responsibility is the most local repository-supported boundary: it already governs Conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branch construction. It preserves the distinction between Session and Conversation without assigning Session lifecycle to Conversation or assigning Conversation semantics to Runtime, Memory, or checkpoint consumers.

Using this existing boundary avoids authority duplication while allowing later decisions to define relationship-specific rules. A new dedicated authority remains architecturally possible in principle, but current repository evidence does not establish that the existing Conversation/Session responsibility is inadequate.

## Semantic boundary

The selected owner defines and maintains the canonical architectural contract for the meaning and scope of the first-class Session–Conversation relationship. Later decisions may define relationship-specific rules under this authority without treating them as accidental extensions of Session or Conversation.

Ownership does not imply an association entity, record, object, identifier, key, table, foreign key, API, service, repository, storage mechanism, event, UI construct, or implementation.

## Explicit non-decisions

This decision does not select relationship identity or identifier format; representation; schema; entity/object design; cardinality; one-active constraints; attachment; detachment; rebinding; reattachment; resumption; Session `CLOSED` effects; Session `EXPIRED` effects; Session recreation; process-death behavior; application-restart behavior; Conversation lifecycle; relationship-specific lifecycle; branch-lineage ownership; conversation-local metadata; message/turn ordering; persistence; storage; database design; API; authorization; retention; deletion; quota; cleanup; archive semantics; or implementation.

## Compatibility

### DEC-8

Compatible. Conversation checkpoint and rollback semantics remain unchanged.

### DEC-9

Compatible. Non-destructive branching, new Conversation identity, source preservation, and lineage requirements remain unchanged.

### DEC-10

Compatible. DEC-15 makes a narrow explicit scope extension to the Conversation/Session responsibility. It does not rewrite DEC-10 or claim that DEC-10 previously selected ownership of the first-class relationship.

### DEC-13

Compatible. Durable immutable Conversation identity remains governed by DEC-13. Relationship ownership does not transfer Conversation identity ownership or select persistence mechanics.

### DEC-14

Compatible. DEC-14’s first-class semantic status is preserved. DEC-15 resolves only the owner of that semantic contract.

## Downstream decisions remaining unresolved

Relationship identity, representation, lifecycle, cardinality, resumption, attachment, detachment, rebinding, Session effects, Conversation lifecycle, persistence, storage, schema, API, authorization, retention, deletion, quota, cleanup, archive semantics, and implementation remain separate future decisions.
