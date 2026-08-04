> **Status: DERIVED** for Memory message contract.
> This document defines protocol messages for Memory operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical memory architecture document and [lifecycle/MemoryLifecycle.md](../lifecycle/MemoryLifecycle.md).
> Referenced by: models, context management, ranking, and tests.

# Memory Protocol — Nexora

## Operations

Memory protocol messages cover write, fetch, score, update, and retention operations across session, project, and long-term memory tiers. Messages SHOULD preserve `correlationId` when memory entries originate from a concrete execution or tool/provider interaction. Lifecycle-sensitive writes and retention changes SHOULD remain consistent with [lifecycle/MemoryLifecycle.md](../lifecycle/MemoryLifecycle.md).

### Tool History (FR-M011)

Tool history entries SHOULD store tool identity, tool-call identity, correlation reference, normalized result metadata, and retention scope.

### File History (FR-M012)

File history entries SHOULD preserve workspace, path reference, operation type, and originating correlation reference when applicable.

### User Preferences (FR-M013)

Preference writes MUST be scoped and durable. Preference retrieval SHOULD expose provenance metadata when available.

### Knowledge Graph (FR-M014 / FR-M015)

Entity and relationship writes SHOULD preserve source provenance, timestamp metadata, and retrievability semantics suitable for ranking and replay.

## Backing Stores

Backing store implementations MAY vary, but they MUST preserve durable write semantics and retrieval provenance needed by the memory system.

## Scoring

Scoring and ranking are derived computations and MUST NOT overwrite the underlying durable memory fact without explicit write semantics.
