# Session Lifecycle Authority — Nexora

## States

`Created`, `Active`, `Idle`, `Closed`, `Expired`

## Rules

Session lifecycle is the durable authority for session context availability. Active task or agent references are subordinate runtime associations and MUST NOT replace session lifecycle state.

## Transition Minimums

Transitions SHOULD emit session identity, workspace identity, prior state, new state, version, and timestamp.
