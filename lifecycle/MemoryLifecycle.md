# Memory Lifecycle Authority — Nexora

## States

`Recorded`, `Indexed`, `Retrieved`, `Retained`, `Expired`, `Deleted`

## Rules

Memory lifecycle governs durable memory fact handling and retention semantics. Scoring, ranking, and context projection are derived behaviors and MUST NOT replace durable memory lifecycle state.

## Transition Minimums

Transitions SHOULD emit memory identity, scope, provenance/correlation reference when available, prior state, new state, version, and timestamp.

## Expanded Lifecycle Specification (S3 — Option A)

### States
`Created`, `Active`, `Summarized`, `Archived`, `Restored`, `Pruned`

### Transitions
- `Created → Active`: Memory entry written; trust tag applied (`FR-M001`).
- `Active → Summarized`: Token budget exceeded (`FR-CM-002`); progressive summarization triggered (`FR-CM-003`).
- `Summarized → Archived`: Entry retained but compressed; retrieval requires reconstruction (`FR-CM-007`).
- `Archived → Restored`: Full entry reconstructed from checkpoint + retrieval layer (`FR-AS-013`).
- `Active/Archived → Pruned`: Entry deleted (stale, low relevance, or user-requested); audit logged (`FR-M010`).

### Dependencies
- `specs/CONTEXT_MANAGEMENT.md` (§memory, summarization, resume).
- `models/Memory.md` — memory model (`MemoryScope`, `MemoryEntry`).
- `protocols/Memory-Protocol.md` — memory protocol operations.
