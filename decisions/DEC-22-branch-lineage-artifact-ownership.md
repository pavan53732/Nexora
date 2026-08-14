# DEC-22 — BranchLineage Artifact Ownership

> **Status: CANONICAL DECISION**
> This decision selects a distinct BranchLineage artifact boundary for rollback branch lineage. It does not select the artifact's identifier format, field list, schema, lifecycle states or transitions, storage, API, retention, deletion, quotas, cleanup, or implementation.

## Problem

DEC-9 requires non-destructive rollback to create a new Conversation identity and preserve parent-Conversation and source-checkpoint lineage. DEC-13 and DEC-15 explicitly leave ownership of that lineage unresolved. A separate owner decision is required without transferring Conversation identity ownership, checkpoint lifecycle ownership, or Session–Conversation relationship ownership.

## Repository evidence

- DEC-9 requires rollback lineage to be recorded and preserved while the source Conversation remains unchanged and addressable.
- DEC-10 establishes the Conversation/Session responsibility for Conversation identity, conversation-local records, checkpoint creation, checkpoint lineage, and non-destructive branch construction, but does not establish an exclusive owner for the lineage artifact.
- DEC-13 explicitly leaves branch-lineage ownership unresolved among a durable Conversation record, the ConversationCheckpoint artifact, or a separate lineage structure.
- DEC-15 assigns the Session–Conversation relationship semantic contract to the existing Conversation/Session responsibility and explicitly does not select branch-lineage ownership.
- `architecture/CONVERSATION_CHECKPOINTS.md` preserves lineage recording and source preservation while identifying precise lineage ownership as unresolved.

## Candidates considered

### Conversation-owned lineage

Rejected as the exclusive owner. Conversation retains durable immutable Conversation identity and ordered-record semantics, but selecting Conversation alone would collapse a distinct lineage artifact boundary into Conversation ownership.

### ConversationCheckpoint-owned lineage

Rejected as the exclusive owner. ConversationCheckpoint owns checkpoint boundary lifecycle and rollback-source semantics, but selecting it alone would collapse branch-lineage ownership into checkpoint lifecycle ownership.

### Distinct BranchLineage artifact

Selected. This preserves the distinction between Conversation identity, checkpoint identity, and the parent/source lineage relationship created by rollback without assigning the Session–Conversation relationship or checkpoint lifecycle to the new artifact.

## Decision

Nexora selects a distinct **BranchLineage** artifact boundary, separate from Conversation and ConversationCheckpoint, as the owner of rollback branch-lineage semantics and the parent/source lineage relationship between a rollback-created branch Conversation, its source Conversation, and its source checkpoint.

The BranchLineage decision does not change DEC-9: rollback remains non-destructive, creates a new Conversation identity, and preserves the source Conversation. It does not create an independent Session–Conversation relationship identity or lifecycle, and it does not transfer Conversation identity ownership, checkpoint lifecycle ownership, or Session–Conversation relationship ownership.

## Semantic boundary

BranchLineage owns the semantic lineage relationship required to record and preserve rollback ancestry. Conversation owns Conversation identity and ordered conversation records. ConversationCheckpoint owns checkpoint boundary lifecycle and checkpoint availability. References between these artifacts do not transfer ownership.

## Explicit non-decisions

This decision does not select a BranchLineage identifier format; field list; parent/source key encoding; schema; lifecycle states; lifecycle transitions; persistence technology; transaction mechanism; API; transport; authorization subject; retention; expiration; deletion; quota; cleanup; archive behavior; recovery mechanism; or implementation. These remain separate downstream or owner decisions where not selected by another canonical source.

## Compatibility

- DEC-8 and DEC-9 remain unchanged: checkpoint boundaries and non-destructive rollback semantics are preserved.
- DEC-13 remains unchanged: Conversation identity is durable and immutable, and branch-lineage ownership was not selected by DEC-13 itself.
- DEC-15 remains unchanged: the existing Conversation/Session responsibility owns the Session–Conversation relationship semantic contract only.
- `architecture/CONVERSATION_CHECKPOINTS.md` remains canonical for checkpoint and rollback semantics; it now projects the BranchLineage ownership boundary selected here.

## Downstream work remaining

A future canonical or implementation-facing document may define BranchLineage lifecycle, identity, persistence, schema, API, retention, deletion, quota, cleanup, and testing only after those decisions are separately established. This decision alone does not create those mechanisms or claim implementation evidence.
