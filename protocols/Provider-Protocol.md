> **Status: DERIVED** for Provider message contract.
> This document defines protocol messages for Provider operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical provider architecture document.
> Referenced by: APIs, SDKs, adapters, and tests.

# Provider Protocol — Nexora

## Lifecycle Alignment

Provider messages participate in higher-level execution lifecycles and MUST NOT infer success solely from transport or stream closure. Provider adapters SHOULD preserve durable terminal semantics compatible with the execution contract path.

## Envelope Rules

Requests and events SHOULD preserve correlation, resume behavior where supported, canonical error mapping, and ordered terminal signaling.
