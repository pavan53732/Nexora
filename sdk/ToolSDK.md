# Tool SDK — Nexora

The Tool SDK defines the contract surface for tool implementations.

## Lifecycle Alignment

Tool SDK implementations that interact with shell or terminal contexts SHOULD preserve terminal session semantics as defined by [lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md).

## Notes

Schema validation, permission mediation, error-envelope preservation, and idempotent retry behavior are core SDK responsibilities.
