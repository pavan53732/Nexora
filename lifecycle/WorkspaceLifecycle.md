# Workspace Lifecycle Authority — Nexora

## States

`Created`, `Active`, `Suspended`, `Archived`, `Deleted`

## Rules

Workspace lifecycle is the durable authority for workspace availability and ownership context. Task, session, execution, and terminal activity may occur within a workspace but MUST NOT replace workspace lifecycle state.

## Transition Minimums

Every durable transition SHOULD emit workspace identity, prior state, new state, correlation reference when applicable, version, and timestamp.
