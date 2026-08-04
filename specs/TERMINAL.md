# Terminal Specification — Nexora

## Scope

Defines terminal execution behavior inside the sandboxed environment.

## Lifecycle Alignment

Terminal session lifecycle semantics are governed by [../lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md).

## Notes

Terminal process activity may support tool or task execution, but terminal session state MUST NOT replace higher-level execution lifecycle authority.
