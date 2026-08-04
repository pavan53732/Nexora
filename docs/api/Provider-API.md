# Provider API — Nexora

The Provider API governs normalized provider completion, streaming, and usage-accounting behavior.

## Lifecycle Alignment

Provider operations participate in higher-level execution lifecycle handling and MUST preserve durable terminal semantics rather than inferring outcome from transport closure.

## Contract Notes

Streaming, resume, canonical error mapping, and usage accounting should remain consistent with the provider protocol and runtime execution semantics.
