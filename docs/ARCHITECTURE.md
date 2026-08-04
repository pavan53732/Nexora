# Architecture Overview — Nexora

Nexora uses a workspace-first, agent-driven architecture that coordinates runtime, tools, providers, memory, plugins, and sandboxed execution.

## Lifecycle Authorities

Where lifecycle semantics are durable first-class concerns, the repository uses explicit lifecycle authorities:

- Workspace — [../lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md)
- Session — [../lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md)
- Memory — [../lifecycle/MemoryLifecycle.md](../lifecycle/MemoryLifecycle.md)
- Terminal session — [../lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md)

## Notes

Derived models, APIs, protocols, SDKs, registries, and tests SHOULD align to these lifecycle authorities instead of redefining state semantics locally.
