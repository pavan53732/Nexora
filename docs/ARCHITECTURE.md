# Architecture Overview — Nexora

Nexora uses a workspace-first, agent-driven architecture that coordinates runtime, tools, providers, memory, plugins, and sandboxed execution.

## Lifecycle Authorities

Where lifecycle semantics are durable first-class concerns, the repository uses explicit
lifecycle authorities with canonical state-machine definitions in `state-machines/`:

- Workspace — [../state-machines/WorkspaceLifecycle.md](../state-machines/WorkspaceLifecycle.md)
  (narrative: [../lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md))
- Session — [../lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md) (no state-machine companion)
- Memory — [../state-machines/MemoryLifecycle.md](../state-machines/MemoryLifecycle.md)
  (narrative: [../lifecycle/MemoryLifecycle.md](../lifecycle/MemoryLifecycle.md))
- Terminal session — [../state-machines/TerminalSessionLifecycle.md](../state-machines/TerminalSessionLifecycle.md)
  (narrative: [../lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md))

## Notes

Derived models, APIs, protocols, SDKs, registries, and tests SHOULD align to these lifecycle authorities instead of redefining state semantics locally.
