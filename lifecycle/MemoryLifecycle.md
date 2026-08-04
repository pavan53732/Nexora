# Memory Lifecycle Authority — Nexora

## States

`Recorded`, `Indexed`, `Retrieved`, `Retained`, `Expired`, `Deleted`

## Rules

Memory lifecycle governs durable memory fact handling and retention semantics. Scoring, ranking, and context projection are derived behaviors and MUST NOT replace durable memory lifecycle state.

## Transition Minimums

Transitions SHOULD emit memory identity, scope, provenance/correlation reference when available, prior state, new state, version, and timestamp.
