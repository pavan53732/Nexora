> **Status: DERIVED** for Plugin message contract.
> This document defines protocol messages for Plugin. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Plugin.
> Referenced by: models, APIs, SDKs, and tests.


# Plugin Protocol — Nexora

> Communication contract between the plugin manager and plugins.

## Lifecycle Messages

| Message | Direction | Description |
|---------|-----------|-------------|
| `INSTALL` | Manager → Plugin | Plugin should initialize persistent storage. |
| `ACTIVATE` | Manager → Plugin | Plugin should register capabilities. |
| `DEACTIVATE` | Manager → Plugin | Plugin should unregister capabilities. |
| `UNINSTALL` | Manager → Plugin | Plugin should clean up all data. |

## Registration

During `ACTIVATE`, the plugin calls registration methods on `PluginContext`:
- `toolRegistry.register(tool)`
- `agentRegistry.register(agent)`
- `providerRegistry.register(provider)`

## Isolation

Plugins run in the same process but are logically isolated. A misbehaving plugin should not crash the app. The plugin manager wraps each plugin call in try/catch.
