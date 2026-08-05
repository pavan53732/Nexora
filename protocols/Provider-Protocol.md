> **Status: DERIVED** for Provider message contract.
> This document defines protocol messages for Provider operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical provider architecture document (`architecture/PROVIDER_SYSTEM.md`).
> Referenced by: APIs, SDKs, adapters, and tests.

# Provider Protocol — Nexora

> Wire and communication contract between the ProviderRouter, TokenAccountingEngine, and remote AI endpoint adapters.

## Streaming Execution Flow

```text
ProviderRouter            Accounting Engine            Provider Adapter
      │                           │                           │
      ├─────── request() ────────>│                           │
      │                           │                           │
      │<─────── VALIDATED ────────┤                           │
      │                                                       │
      ├────────────────── executeStream() ───────────────────>│
      │                                                       │
      │<─────────────── StreamChunk (Token) ──────────────────┤
      │                                                       │
      │<─────────────── StreamTerminal (Usage) ───────────────┤
```

1. **Pre-flight Validation**: The `ProviderRouter` passes the request to the `TokenAccountingEngine` to verify the token budget has not been exhausted (`NXR-1007`).
2. **Stream Execution**: The router routes the request to the correct active `BaseProviderAdapter` instance. The adapter establishes an encrypted TLS 1.3 socket to the endpoint and initiates Server-Sent Events (SSE).
3. **Token Accumulation**: The adapter streams tokens in real-time, feeding chunks into the agent's context pipeline.
4. **Durable Terminal Signaling**: The stream MUST cleanly close with a termination chunk carrying explicit token count metadata (`prompt_tokens`, `completion_tokens`). This chunk is persisted in Room, the budget is decremented, and the final completion event is published.

## Protocol Messages

### SSE Chunk Format

```kotlin
data class ProviderStreamChunk(
    val correlationId: String,
    val chunkId: String,
    val textDelta: String,
    val toolCallDelta: List<ToolCallDelta> = emptyList(),
    val isTerminal: Boolean = false,
    val usage: TokenUsage? = null
)
```

### Usage Audit Record

```kotlin
data class TokenUsageRecord(
    val recordId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val modelId: String,
    val inputTokens: Int,
    val outputTokens: Int,
    val totalTokens: Int,
    val occurredAt: Instant
)
```

## Conformance Rules

- **Stream Integrity**: In contrast to standard HTTP closures, success MUST NOT be inferred solely from socket closure. If the TCP stream disconnects before the explicit SSE terminal JSON chunk carrying metadata is received, the adapter MUST convert the disconnect into `NXR-4007` (Streaming Failed) and propagate a partial failure to prevent truncation hallucinations.
- **Budget Lock**: Requests exceeding the remaining session token budget MUST be rejected at the boundary (`NXR-1007`) before reaching the network adapter.
