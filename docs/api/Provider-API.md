> **Status: DERIVED** for Provider API.
> Canonical routing/streaming behavior is owned by
> [Provider System](../../architecture/PROVIDER_SYSTEM.md) and
> [ProviderStreamLifecycle](../../state-machines/ProviderStreamLifecycle.md).

# Provider API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md)

## Normative Operation Contract

| Operation | Success | Canonical failures | Retry/idempotency | Security/cancellation | Evidence |
|---|---|---|---|---|---|
| `registerProfile` | Provider profile projection | NXR-4011, NXR-1010 | Idempotent | Keys remain in SecureKeyStore | Provider contract tests |
| `planRoute` | Persistable ranked `ProviderRoutePlan` | No eligible model, technical capability/context/privacy conflict | Safe read for same snapshot | Profile isolation; redacted reason | Routing tests |
| `complete` | Committed completion response | NXR-4002..4006, NXR-4012 | Idempotency key required | Endpoint confinement | Completion tests |
| `streamComplete` | `Flow<StreamEnvelope>` ending in one terminal | NXR-4007, NXR-4013..4017 | Request/stream IDs and cursor rules | Cancellation propagates; bounded backpressure | Streaming tests |
| `cancelStream` | Committed Cancelled event | Already terminal, not found | Idempotent | Caller owns workspace/request | Cancellation tests |
| `resumeStream` | Same-ID native resume or new lineage stream | NXR-4014/4015 | Resume key required | Resume token opaque/redacted | Resume tests |
| `embed` | Normalized vector | NXR-4008 | Idempotent | Workspace scoped | Vector tests |
| `checkHealth` | Updated provider health | NXR-4001/4009 | Safe | Does not expose credentials | Health/failover tests |

Every request carries `requestId`, `correlationId`, workspace identity, profile/model
identity, the model-catalog snapshot and provider contract version used for negotiation,
requested modalities, and an idempotency key where the operation can create or resume work.
A provider-native reasoning continuation reference is opaque adapter state: it is bound to
the provider/model/request/stream identity, is not raw private chain-of-thought, and MUST
NOT be replayed across provider failover without a compatible translation contract.

## Request and Routing Shapes

```kotlin
data class ProviderCompletionRequest(
    val requestId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val providerProfileId: String?,
    val modelId: String?,
    val modelCatalogSnapshotId: String,
    val providerContractVersion: String,
    val contextSnapshotId: String,
    val requiredCapabilities: Set<ProviderCapability>,
    val requestedModalities: Set<String>,
    val reasoningPolicy: ReasoningPolicy,
    val bypassProviderSafety: Boolean = false,
    val providerReasoningContinuationRef: String?,
    val maxTokens: Int,
    val tools: List<ToolDescriptor> = emptyList(),
    val idempotencyKey: String
)

data class RouteConstraints(
    val requiredCapabilities: Set<ProviderCapability>,
    val requestedModalities: Set<String>,
    val requiredReasoningEffort: ReasoningEffort?,
    val maxLatencyMs: Long?,
    val localOnly: Boolean,
    val fallbackPolicy: StreamFallbackPolicy
)
```

## Completion Response

```kotlin
data class ProviderCompletionResponse(
    val requestId: String,
    val correlationId: String,
    val providerProfileId: String,
    val modelId: String,
    val content: String,
    val toolCalls: List<ToolCall>,
    val usage: TokenUsage,
    val finishReason: FinishReason
)
```

## Stream Operations

```kotlin
data class CancelProviderStreamRequest(
    val requestId: String,
    val streamId: String,
    val correlationId: String,
    val actor: String,
    val idempotencyKey: String
)

data class ResumeProviderStreamRequest(
    val requestId: String,
    val streamId: String,
    val correlationId: String,
    val lastCommittedSequence: Long,
    val resumeToken: String,
    val idempotencyKey: String
)

interface ProviderApi {
    suspend fun registerProfile(profile: ProviderProfileDescriptor): ProviderProjection
    suspend fun planRoute(request: ProviderCompletionRequest, constraints: RouteConstraints): ProviderRoutePlan
    suspend fun complete(request: ProviderCompletionRequest): ProviderCompletionResponse
    fun streamComplete(request: ProviderCompletionRequest): Flow<StreamEnvelope>
    suspend fun cancelStream(request: CancelProviderStreamRequest): StreamEnvelope
    fun resumeStream(request: ResumeProviderStreamRequest): Flow<StreamEnvelope>
    suspend fun embed(text: String, profileId: String, correlationId: String): FloatArray
    suspend fun checkHealth(profileId: String): ProviderHealth
}
```

## Stream Rules

- API consumers validate monotonic sequence and deduplicate `(streamId, sequence)`.
- UI text is provisional until a successful `Terminal` event.
- `ToolArgumentsDelta` is never executable; only `ToolCallCommitted` crosses to Tool API.
- `resumeStream` is exposed only for `NATIVE_CURSOR`; emulated restart uses a new request and `priorStreamId`.
- Mid-stream failover never silently combines provider outputs.
- Provider-native continuation artifacts are adapter-owned and are not exposed as
  `ReasoningSummary` or `ClaimRecord` content.
- A requested advanced capability that is unavailable or unrepresentable is an explicit
  route incompatibility or policy-approved fallback; it is never silently discarded.
- Backpressure is bounded; overflow returns `NXR-4013`.

## Error Mapping

| Code | Meaning | API effect |
|---|---|---|
| `NXR-4007` | Stream transport failed | Commit Failed with partial-output flag. |
| `NXR-4013` | Stream backpressure overflow | Cancel transport; commit Failed. |
| `NXR-4014` | Resume rejected | Preserve partial stream; optionally restart with lineage. |
| `NXR-4015` | Sequence gap unrecoverable | Commit Failed; never synthesize missing deltas. |
| `NXR-4016` | Incomplete/invalid streamed Tool call | Discard fragments; no Tool execution. |
| `NXR-4017` | Missing terminal event | Treat socket close as failure. |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for canonical envelopes.
