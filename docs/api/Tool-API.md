# Tool API — Nexora

The Tool API governs normalized tool invocation, execution, and result envelopes.

## Lifecycle Alignment

Terminal-backed tool execution that opens or reuses shell contexts SHOULD align with [lifecycle/TerminalSessionLifecycle.md](../../lifecycle/TerminalSessionLifecycle.md) where terminal session state is material to execution handling.

## Contract Notes

Tool invocation MUST preserve permission mediation, canonical error-envelope behavior, and lifecycle-safe ordering of side effects.
