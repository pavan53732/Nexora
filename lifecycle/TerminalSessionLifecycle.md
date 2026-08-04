# Terminal Session Lifecycle Authority — Nexora

## States

`Created`, `Attached`, `Running`, `Detached`, `Closed`, `Failed`

## Rules

Terminal session lifecycle governs terminal availability inside sandboxed execution. Tool-call or task lifecycle remains the authority for business-level execution state.

## Transition Minimums

Transitions SHOULD emit terminal session identity, workspace identity, sandbox identity, correlation reference when available, prior state, new state, version, and timestamp.
