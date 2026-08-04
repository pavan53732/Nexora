> **Status: DERIVED** for Tool message contract.
> This document defines protocol messages for Tool operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical tool architecture document.
> Referenced by: APIs, SDKs, sandbox, and tests.

# Tool Protocol — Nexora

## Lifecycle Alignment

Tool protocol operations that create or attach terminal execution contexts SHOULD align with [../lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md). Tool-side effects MUST respect permission ordering and durable lifecycle-safe outcome semantics.

## Envelope Rules

Requests and events SHOULD preserve `correlationId`, canonical error semantics, idempotency behavior where declared, and durable ordering of externally visible outcomes.
