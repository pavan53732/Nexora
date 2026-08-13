> **Status: DERIVATIVE** for memory lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/MemoryLifecycle.md](../state-machines/MemoryLifecycle.md).**
> This file describes the memory lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/MemoryLifecycle.md](../state-machines/MemoryLifecycle.md).

# Memory Lifecycle Authority — Nexora

## States

`Recorded`, `Indexed`, `Retrieved`, `Retained`, `Expired`, `Deleted`

## Rules

Memory lifecycle governs durable memory fact handling and retention semantics. Scoring, ranking, and context projection are derived behaviors and MUST NOT replace durable memory lifecycle state.

## Transition Minimums

Transitions SHOULD emit memory identity, scope, provenance/correlation reference when available, prior state, new state, version, and timestamp.

## Expanded Lifecycle Specification (S3 — Option A)

Narrative reference for the canonical state machine at
[../state-machines/MemoryLifecycle.md](../state-machines/MemoryLifecycle.md).
States defined there: `Recorded`, `Indexed`, `Retrieved`, `Retained`, `Expired`, `Deleted`.

### Canonical State Alignment

The states and transitions below are descriptive prose mirroring the canonical
state machine. In case of discrepancy, `state-machines/MemoryLifecycle.md` wins.

#### States (from canonical source)
`Recorded`, `Indexed`, `Retrieved`, `Retained`, `Expired`, `Deleted`

### Transitions
- `Recorded → Indexed`: Embedding/vector generated; searchable.
- `Indexed → Retrieved`: Surfaced into a context/recall segment.
- `Indexed / Retrieved → Retained`: Within retention policy; durable.
- `Retrieved → Indexed`: Content changed; reindexed.
- `Retained → Expired`: Lifetime/quota reached; non-revivable, no longer searchable, and pending eviction.
- `Expired → Deleted`: Physical removal from store. `Expired → Indexed` is invalid; an expired record cannot be reindexed.
- `Recorded / Indexed / Retrieved / Expired → Deleted`: Deleted at any non-terminal point.

### Dependencies
- `specs/CONTEXT_MANAGEMENT.md` (§memory, summarization, resume).
- `models/Memory.md` — memory model (`MemoryScope`, `MemoryEntry`).
- `protocols/Memory-Protocol.md` — memory protocol operations.
