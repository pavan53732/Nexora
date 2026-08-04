# Agent SDK — Nexora

The Agent SDK defines the contract surface for agent implementations.

## Lifecycle Alignment

Agent SDK helpers that create or observe task, session, workflow, or execution state SHOULD treat lifecycle authorities as canonical rather than inferring lifecycle from incidental transport behavior.

## Notes

Delegation, streaming, retry, and cancellation helpers SHOULD preserve correlation and durable outcome semantics.
