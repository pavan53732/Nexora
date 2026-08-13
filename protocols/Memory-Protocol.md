> **Status: DERIVED** for Memory message contract.
> This document defines protocol messages for Memory operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical memory architecture document.
> Referenced by: models, context management, ranking, and tests.
> This protocol is the externally visible contract for Memory operations within the repository; no separate docs/api/Memory-API.md artifact exists or is required by current repository evidence.

# Memory Protocol — Nexora

## Operations

Memory protocol messages cover write, fetch, score, update, and retention operations across session, project, and long-term memory tiers. Messages SHOULD preserve `correlationId` when memory entries originate from a concrete execution or tool/provider interaction. Durable lifecycle semantics for retained memory records are governed by the canonical [state-machines/MemoryLifecycle.md](../state-machines/MemoryLifecycle.md). An `EXPIRED` record cannot be reindexed, return to `INDEXED`, or become searchable again.

Every `MemoryKind` declared in [../models/Memory.md](../models/Memory.md) has a
corresponding protocol section below.

### Conversation (FR-M001..003)

Conversation entries SHOULD preserve session identity, turn ordering, role attribution, and embedding reference when indexed.

### Execution History (FR-M005)

Execution history entries SHOULD preserve execution identity, version, phase, terminal outcome, and correlation reference. Records are append-only.

### Tool History (FR-M011)

Tool history entries SHOULD store tool identity, tool-call identity, correlation reference, normalized result metadata, and retention scope.

### File History (FR-M012)

File history entries SHOULD preserve workspace, path reference, operation type, and originating correlation reference when applicable.

### User Preferences (FR-M013)

Preference writes MUST be scoped and durable. Preference retrieval SHOULD expose provenance metadata when available.

### Knowledge Graph (FR-M014 / FR-M015)

Entity and relationship writes SHOULD preserve source provenance, timestamp metadata, and retrievability semantics suitable for ranking and replay.

### Context Snapshots (FR-CM-010..012)

`ContextSnapshot` records are immutable once written. Writes MUST preserve snapshot identity, model/tokenizer contract, included and excluded segment references, content hashes, and compaction lineage. Retention follows the task/execution evidence window ([../specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md)).

### Reasoning Summaries (FR-RN-011 / FR-RN-012)

`ReasoningSummary` writes MUST be redacted before persistence. Raw private chain-of-thought MUST NOT be stored or transmitted. Retention follows workspace execution-history retention.

### Stream Lineage (FR-P014..019)

Stream records persist stream identity, `priorStreamId` lineage, last committed sequence, terminal outcome, usage, and sanitized error. Coalesced UI rendering deltas are not retained indefinitely. Resume tokens MUST NOT be persisted in retrievable form.

## Backing Stores

Backing store implementations MAY vary, but they MUST preserve durable write semantics and retrieval provenance needed by the memory system.

## Scoring

Scoring and ranking are derived computations and MUST NOT overwrite the underlying durable memory fact without explicit write semantics.
