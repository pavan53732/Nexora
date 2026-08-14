# DEC-24 — Conversation-Local Metadata Boundary

> **Status: CANONICAL DECISION**
> This decision closes the minimum semantic content boundary for Conversation-local metadata. It does not select concrete field names, types, encoding, schema, storage, API, or implementation.

## Problem

DEC-8 requires conversation-local metadata needed to interpret an ordered conversation-record boundary. DEC-13 explicitly left the complete content/field boundary unresolved. The repository now needs a minimum semantic boundary that preserves Conversation identity, ordering, checkpoint semantics, and BranchLineage separation without absorbing unrelated subsystem state.

## Repository evidence

- DEC-8 defines the checkpoint boundary over one Conversation’s ordered record and conversation-local metadata.
- DEC-13 selects durable immutable Conversation identity and ordered-record semantics while explicitly leaving the metadata schema and field list unresolved.
- `architecture/CONVERSATION_CHECKPOINTS.md` identifies creation provenance, integrity information, and parent/lineage information as checkpoint-relevant information, while excluding task, execution, provider, context, memory, file, workspace, permission, and external-side-effect state.
- DEC-22 assigns rollback parent/source lineage to the distinct BranchLineage artifact.
- `models/Conversation.md` distinguishes Conversation-local data from Session, Task, Execution, Context, Memory, file, workspace, authorization, and provider state.

## Decision

Conversation-local metadata is limited to the semantic categories required to interpret and validate a Conversation record boundary:

1. **Creation provenance:** information identifying the origin of the Conversation record and the operation that established it.
2. **Integrity information:** information required to validate that the Conversation identity and ordered-record boundary have not been corrupted or invalidly altered.

Conversation identity, ordered-record content, and checkpoint-addressable boundaries remain separate Conversation and ConversationCheckpoint semantics rather than metadata categories. Rollback parent/source lineage is owned by BranchLineage under DEC-22 and is not reclassified as Conversation-local metadata. Session, Task, Execution, Provider, ContextSnapshot, Memory, file, workspace, authorization, and external-side-effect state remain outside the Conversation-local metadata boundary.

The two categories are semantic obligations only. Concrete fields, field names, types, values, encodings, schemas, storage, APIs, and transport are implementation or downstream specification choices subject to the selected invariants.

## Explicit non-decisions

This decision does not select a field list; identifier format; timestamp representation; actor representation; checksum or hash algorithm; schema; storage technology; serialization; API; transport; retention; deletion; quota; cleanup; authorization workflow; or implementation.

## Compatibility

- DEC-8 and DEC-13 remain unchanged: Conversation identity, ordered records, and checkpoint boundaries retain their existing semantics.
- DEC-22 remains unchanged: BranchLineage owns rollback parent/source lineage.
- The checkpoint lifecycle and retention/deletion policy remain governed by their existing canonical sources and DEC-23.

## Validation obligations

Future model, persistence, API, and test documents must demonstrate provenance and integrity coverage while rejecting accidental inclusion of unrelated subsystem lifecycle or side-effect state. Concrete field and schema decisions must remain within this semantic boundary.
