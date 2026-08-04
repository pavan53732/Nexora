# Context Management Specification — Nexora

## Scope

Defines how session, memory, and contextual retrieval state is preserved and applied.

## Lifecycle Alignment

Session lifecycle semantics are governed by [../lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md). Durable memory fact handling and retention semantics are governed by [../lifecycle/MemoryLifecycle.md](../lifecycle/MemoryLifecycle.md).

## Notes

Derived context projections MUST NOT overwrite authoritative session or memory lifecycle state.
