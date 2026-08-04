# Provider SDK — Nexora

The Provider SDK defines the contract surface for provider adapters.

## Lifecycle Alignment

Provider SDK implementations SHOULD preserve durable execution outcome semantics rather than inferring completion from stream closure alone.

## Notes

Streaming, retry, resume, usage accounting, and canonical error-envelope preservation are core SDK responsibilities.
