> **Status: DERIVED** for inference-turn, routing, stream, context, and reasoning artifact shapes.
> Canonical behavior is owned by Agent Runtime, Provider System, ProviderStreamLifecycle,
> and Context Management.

# Domain Model: Inference Pipeline

```kotlin
data class InferenceRequest(
    val requestId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val contextSnapshotId: String,
    val routePlan: ProviderRoutePlan,
    val reasoningPolicy: ReasoningPolicy,
    val idempotencyKey: String
)

data class ProviderRoutePlan(
    val selectedProfileId: String,
    val selectedModelId: String,
    val candidates: List<RouteCandidate>,
    val requiredCapabilities: Set<ProviderCapability>,
    val maxLatencyMs: Long?,
    val maxCostUsd: Double?,
    val localOnly: Boolean,
    val fallbackPolicy: StreamFallbackPolicy,
    val reason: String
)

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

enum class StreamResumeMode { NATIVE_CURSOR, RESTART_WITH_LINEAGE, NONE }
enum class StreamFallbackPolicy { FAIL_PARTIAL, RESTART_SAME_PROVIDER, RESTART_NEXT_PROVIDER }

data class ReasoningPolicy(
    val effort: ReasoningEffort,
    val maxProviderCalls: Int,
    val maxReasoningTokens: Int,
    val maxToolCalls: Int,
    val maxRepairCycles: Int,
    val verifierPasses: Int,
    val useIndependentCritic: Boolean,
    val requireReviewer: Boolean,
    val maxWallClockMs: Long,
    val maxCostUsd: Double?
)

data class ReasoningSummary(
    val summaryId: String,
    val approach: String,
    val evidenceRefs: List<String>,
    val decisions: List<String>,
    val alternatives: List<String>,
    val uncertainty: List<String>,
    val verificationResults: List<String>,
    val tokenUsage: TokenUsage,
    val redacted: Boolean
)

data class ContextSnapshot(
    val snapshotId: String,
    val correlationId: String,
    val modelId: String,
    val tokenizerId: String,
    val maxContextTokens: Int,
    val reservedOutputTokens: Int,
    val reservedReasoningTokens: Int,
    val segments: List<ContextSegmentRef>,
    val excludedSegments: List<ExcludedContextSegment>,
    val totalTokens: Int,
    val createdAt: Instant
)

data class ContextSegmentRef(
    val segmentId: String,
    val source: String,
    val scope: String,
    val trust: String,
    val freshness: String,
    val tokenCount: Int,
    val relevanceScore: Double,
    val diversityScore: Double,
    val evidenceClass: String,
    val contentHash: String,
    val compactionParentId: String?
)
```

## Model Rules

- Raw private chain-of-thought is not required or persisted; `ReasoningSummary` is the durable user/audit artifact.
- `StreamEnvelope` ordering is validated before its event mutates UI, tool assembly, usage, or memory.
- `ContextSnapshot` is immutable and reproducible for its tokenizer/model contract.
- Failover/restart creates a new `streamId`; `priorStreamId` preserves lineage.
