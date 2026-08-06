> **Status: DERIVED** for Provider request, routing, and typed stream messages.
> Canonical provider behavior is defined in `architecture/PROVIDER_SYSTEM.md`; per-stream
> lifecycle is defined in `state-machines/ProviderStreamLifecycle.md`.

# Provider Protocol — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## Streaming Execution Flow

```text
Agent Runtime       ProviderRouter       Accounting       Provider Adapter       UI/EventBus
     │                    │                  │                    │                    │
     ├─ route request ───>│                  │                    │                    │
     │                    ├─ reserve budget >│                    │                    │
     │                    │<─ validated ─────┤                    │                    │
     │                    ├─ open stream ────────────────────────>│                    │
     │                    │<─ native events ──────────────────────┤                    │
     │                    ├─ normalize, sequence, validate         │                    │
     │<─ StreamEnvelope ──┤───────────────────────────────────────────────────────────>│
     │                    ├─ usage reconcile >│                    │                    │
     │                    └─ exactly one Terminal / Failed / Cancelled                │
```

## Stream Envelope

```kotlin
data class StreamEnvelope(
    val streamId: String,
    val priorStreamId: String?,
    val requestId: String,
    val correlationId: String,
    val providerProfileId: String,
    val modelId: String,
    val sequence: Long,
    val emittedAt: Instant,
    val resumeToken: String?,
    val event: StreamEvent
)

sealed interface StreamEvent {
    data class Started(val contextTokens: Int) : StreamEvent
    data class TextDelta(val text: String) : StreamEvent
    data class ReasoningSummaryDelta(val text: String) : StreamEvent
    data class CitationDelta(val citations: List<Citation>) : StreamEvent
    data class ToolCallStarted(val toolCallId: String, val toolName: String) : StreamEvent
    data class ToolArgumentsDelta(val toolCallId: String, val jsonFragment: String) : StreamEvent
    data class ToolCallCommitted(val toolCall: ToolCall) : StreamEvent
    data class UsageDelta(val usage: TokenUsage) : StreamEvent
    data class Heartbeat(val providerTimestamp: Instant?) : StreamEvent
    data class Terminal(val finishReason: FinishReason, val usage: TokenUsage) : StreamEvent
    data class Failed(val error: CanonicalErrorEnvelope, val partialOutput: Boolean) : StreamEvent
    data class Cancelled(val actor: String, val reason: String?) : StreamEvent
}
```

## Ordering and Integrity

1. `sequence` starts at zero and increases by one for every committed event.
2. Consumers deduplicate at-least-once delivery by `(streamId, sequence)`.
3. A sequence gap pauses consumption and initiates bounded recovery; it never guesses missing content.
4. Exactly one terminal event (`Terminal`, `Failed`, or `Cancelled`) commits.
5. Socket/HTTP/SSE closure without a canonical terminal event is `NXR-4017`.
6. Every event is size-limited, UTF-8 validated, schema validated, and tied to the authenticated stream identity.
7. Terminal usage is authoritative; accumulated deltas are reconciled and mismatch is audited.

## Tool-Call Assembly

- `ToolCallStarted` allocates assembly state by `toolCallId`.
- `ToolArgumentsDelta` appends in sequence and is never executable by itself.
- Multiple tool calls may interleave; fragments are isolated by ID.
- `ToolCallCommitted` requires complete JSON, canonical Tool lookup, and parameter-schema validation.
- Failure, cancellation, sequence gap, or terminal with incomplete assembly discards fragments and returns `NXR-4016` where surfaced.
- Only committed Tool calls enter the Tool authorization gate.

## Backpressure

```kotlin
data class StreamBufferPolicy(
    val capacity: Int,
    val highWaterMark: Int,
    val lowWaterMark: Int,
    val overflowDeadlineMs: Long,
    val maxEventBytes: Int,
    val uiCoalesceWindowMs: Long
)
```

- Adapter collection uses a bounded channel.
- Text and reasoning-summary deltas may be coalesced while preserving order.
- Tool, citation, usage, heartbeat, error, cancellation, and terminal events are never dropped.
- Producers suspend above the high-water mark and resume below the low-water mark.
- Sustained overflow fails with `NXR-4013`; memory growth is never unbounded.
- UI throttling changes rendering frequency, not the durable event order.

## Cancellation

Cancellation carries `streamId`, `requestId`, `correlationId`, actor, and idempotency key.
It propagates Agent Runtime → ProviderRouter → adapter. Repeated cancellation returns the
committed result. The adapter must close network resources and emit one `Cancelled`
terminal event within the cancellation performance budget.

## Resume and Failover

| Mode | Behavior |
|---|---|
| `NATIVE_CURSOR` | Same `streamId`; provider cursor resumes after last committed sequence. |
| `RESTART_WITH_LINEAGE` | New request/stream with `priorStreamId`; committed context may be supplied, but output is a new attempt. |
| `NONE` | Commit `Failed` with partial output; no automatic continuation claim. |

A different provider always uses `RESTART_WITH_LINEAGE`. Replacement output is never
appended to the prior stream as if it were byte-continuation. Invalid/expired cursors
return `NXR-4014`; sequence gaps that cannot be recovered return `NXR-4015`.

## Usage Audit Record

```kotlin
data class TokenUsageRecord(
    val recordId: String,
    val requestId: String,
    val streamId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val providerProfileId: String,
    val modelId: String,
    val inputTokens: Int,
    val reasoningTokens: Int?,
    val outputTokens: Int,
    val totalTokens: Int,
    val estimatedCostUsd: Double?,
    val terminalSequence: Long,
    val occurredAt: Instant
)
```

## Conformance Rules

- Budget is reserved before transport opens and reconciled only from a committed terminal or canonical failure record.
- Provider adapters map native event formats to this contract without exposing provider-specific logic to Agent Runtime.
- Private chain-of-thought is not emitted; only provider-approved, redacted `ReasoningSummaryDelta` may cross the boundary.
- `NXR-4007` represents general stream transport failure; `NXR-4013..4017` identify canonical stream-contract failures.
