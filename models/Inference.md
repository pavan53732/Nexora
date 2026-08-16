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
    val maxWallClockMs: Long
)

// Non-overridable provider, device, and resource-class ceilings are evaluated by
// the Context Management / Agent Runtime policy boundary before this policy is
// accepted. Cost and usage metadata remain observable outside this execution policy;
// no internal credit or financial-cost gate is represented here.
```

**Per-effort-level ceilings (non-overridable).** The table below selects the maximum `ReasoningPolicy` values for each effort level (`specs/CONTEXT_MANAGEMENT.md` §Reasoning Effort Scale). Task, agent, workspace, and global settings MAY reduce any value but MUST NOT increase it; over-ceiling policies are rejected before execution. `maxRepairCycles` never exceeds 3 (FR-AS-003). `maxReasoningTokens` is bounded by `TokenBudget.maxTokensPerRequest` (`architecture/AGENT_RUNTIME.md` §Token Budgeting).

| Effort | maxProviderCalls | maxReasoningTokens | maxToolCalls | maxRepairCycles | verifierPasses | maxWallClockMs |
|---|---:|---:|---:|---:|---:|---:|
| `OFF` | 20 | 0 | 50 | 1 | 0 | 600 000 (10 min) |
| `LOW` | 30 | 2 048 | 75 | 2 | 1 | 1 200 000 (20 min) |
| `MEDIUM` | 50 | 4 096 | 100 | 3 | 1 | 1 800 000 (30 min) |
| `HIGH` | 75 | 8 192 | 150 | 3 | 2 | 2 700 000 (45 min) |
| `X_HIGH` | 100 | 16 384 | 200 | 3 | 2 | 3 600 000 (60 min) |
| `MAX` | 150 | 32 768 | 300 | 3 | 3 | 5 400 000 (90 min) |

```kotlin

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

/**
 * Claim-level evidence binding required by Context Management §7 and NFR-CI-003.
 * This is a semantic projection; persistence and transport remain downstream.
 */
data class ClaimRecord(
    val claimId: String,
    val claimText: String,
    val evidenceRefs: List<String>,
    val evidenceClass: EvidenceClass,
    val sourceAuthority: String,
    val freshnessStatus: FreshnessStatus,
    val contradictionStatus: ContradictionStatus,
    val verifierResult: VerifierResult,
    val confidence: ConfidenceClass,
    val disposition: ClaimDisposition
)

enum class EvidenceClass { VERIFIED, DERIVED, ESTIMATED, UNKNOWN }
enum class FreshnessStatus { FRESH, STALE, UNAVAILABLE }
enum class ContradictionStatus { NONE, DETECTED, UNRESOLVED }
enum class VerifierResult { PASSED, FAILED, NOT_RUN }
enum class ConfidenceClass { HIGH, MEDIUM, LOW }
enum class ClaimDisposition { PRESENT_AS_FACT, PRESENT_AS_UNCERTAIN, CLARIFY, WITHHOLD }

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
    val createdAt: Instant,
    val progressSignal: ProgressSignal,
    val effectiveReasoningPolicy: ReasoningPolicy,
    val ceilingDecision: CeilingDecision
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

data class ProgressSignal(
    val testSuitePassCountDelta: Int,
    val workspaceFileChangeDelta: Int,
    val newEvidenceArtifactCountDelta: Int,
    val errorCategoryShift: Boolean
)

data class CeilingDecision(
    val accepted: Boolean,
    val policyBoundary: String,
    val evidenceRefs: List<String>
)

```

## Model Rules

- Raw private chain-of-thought is not required or persisted; `ReasoningSummary` is the durable user/audit artifact.
- `StreamEnvelope` ordering is validated before its event mutates UI, tool assembly, usage, or memory.
- `ContextSnapshot` is immutable and reproducible for its tokenizer/model contract.
- `ProgressSignal` records the state-delta dimensions required by ADR-0009 for semantic progress evaluation; it does not itself change lifecycle state.
- Effective ceiling validation and rejection follow `specs/CONTEXT_MANAGEMENT.md` §6.1; `effectiveReasoningPolicy` and `ceilingDecision` are recorded in the immutable ContextSnapshot, while provider/device/resource-class ceiling values remain policy-boundary inputs rather than user-overridable settings.
- `ClaimRecord` is the claim-level evidence projection required by `specs/CONTEXT_MANAGEMENT.md` §7. Every significant user-facing factual claim is dispositioned from its evidence, authority, freshness, contradiction, verifier, and confidence metadata before crossing the user boundary.
- Failover/restart creates a new `streamId`; `priorStreamId` preserves lineage.
