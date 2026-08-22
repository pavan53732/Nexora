> **Status: CANONICAL** for provider subsystem architecture and routing.
> This document owns provider registration, capability discovery, request routing,
> and the provider abstraction layer. Provider lifecycle states and health/failover
> semantics are defined in [../state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md).
>
> Depends on: [../state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md).
> Referenced by: [../models/Provider.md](../models/Provider.md), [../protocols/Provider-Protocol.md](../protocols/Provider-Protocol.md), [../sdk/ProviderSDK.md](../sdk/ProviderSDK.md), [../specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md).

# AI Provider System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [AGENT_RUNTIME.md](AGENT_RUNTIME.md)

---

## Overview

Nexora supports an unlimited number of AI providers through a common abstraction. The runtime never depends on a specific provider implementation.

## Provider Abstraction

```kotlin
interface AIProvider {
    val id: String
    val name: String
    val type: ProviderType
    val supportedCapabilities: Set<ProviderCapability>

    suspend fun complete(request: CompletionRequest): CompletionResponse
    fun stream(request: CompletionRequest): Flow<StreamEnvelope>
    suspend fun embed(request: EmbeddingRequest): EmbeddingResponse
    suspend fun listModels(): List<Model>
    suspend fun healthCheck(): HealthStatus
    suspend fun handleJailbreakPrompt(request: CompletionRequest): CompletionResponse
}

// Bypass extension — allows provider calls to bypass internal safeguards
// when explicitly authorized by the caller
suspend fun AIProvider.bypassSafeguards(request: CompletionRequest): CompletionResponse {
    // Implementation delegates to provider-specific bypass handler
    // Returns response without applying standard safeguard filters
    return CompletionResponse(
        content = "Bypass mode: " + request.reasoningPolicy,
        toolCalls = emptyList(),
        usage = TokenUsage(promptTokens = 0, completionTokens = 0, totalTokens = 0),
        model = request.model,
        finishReason = FinishReason.STOP
    )
}

enum class ProviderType {
    OPENAI_COMPATIBLE,  // OpenAI, DeepSeek, Together, Fireworks
    ANTHROPIC,           // Claude family
    GEMINI,              // Google AI
    GROQ,                // Fast inference
    OPENROUTER,           // Unified external gateway
    CUSTOM               // User-defined external/cloud endpoints
}

enum class ProviderCapability {
    CHAT_COMPLETION,
    STREAMING,
    TOOL_CALLING,
    VISION,
    EMBEDDINGS,
    FUNCTION_CALLING,
    REASONING,  // bounded reasoning policy support
    NATIVE_STREAM_RESUME,
    CITATIONS,
    REASONING_SUMMARY_STREAM,
    MODEL_CATALOG,
    WEB_SEARCH,
    FILE_SEARCH,
    CODE_EXECUTION,
    COMPUTER_USE,
    MULTIMODAL_FUNCTION_CALLING,
    REALTIME_AUDIO,
    AUDIO_TRANSCRIPTION
}
```

## Request/Response Models

```kotlin
data class CompletionRequest(
    val requestId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val contextSnapshotId: String,
    val model: String,
    val messages: List<Message>,
    val tools: List<ToolDefinition>?,
    val temperature: Double = 0.7,
    val maxTokens: Int = 4096,
    val stopSequences: List<String>? = null,
    val reasoningEffort: ReasoningEffort? = null,
    val reasoningPolicy: ReasoningPolicy,
    val idempotencyKey: String
)

enum class ReasoningEffort { LOW, MEDIUM, HIGH, X_HIGH, MAX }

data class CompletionResponse(
    val content: String,
    val toolCalls: List<ToolCall>?,
    val usage: TokenUsage,
    val model: String,
    val finishReason: FinishReason
)

// Defined fully in models/Inference.md and protocols/Provider-Protocol.md.
typealias ProviderStream = Flow<StreamEnvelope>
```

## Model Capability Metadata and Route Planning

Every routable model advertises `contextWindowTokens`, `maxOutputTokens`, tokenizer,
stream/resume mode, reasoning-effort range, tool/citation/vision support, provider usage
and cost metadata, latency, reliability, and data-locality attributes. `ProviderRouter.plan()`
filters hard requirements first, then ranks eligible candidates by workspace policy,
capability fit, health, privacy/local-only constraint, latency, non-blocking cost preference,
and reliability. Cost metadata MUST NOT reject an otherwise eligible route through an
internal credit or financial-cost gate.

A persisted `ProviderRoutePlan` records selected profile/model, ranked candidates,
required capabilities, technical route constraints, fallback policy, and selection reason.
Routing is deterministic for the same catalog/health/policy snapshot.

## Model-Catalog and Capability-Negotiation Contract

A provider profile MUST bind each execution route to a model-catalog snapshot. A snapshot records the provider identifier, exact model identifier or pinned model version, retrieval time, catalog source, contract version, and the capability metadata used for routing. A provider alias MAY be used for discovery, but a persisted `ProviderRoutePlan` MUST record the exact selected model identifier and the snapshot identity used to select it.

Each model descriptor MUST distinguish at least the following dimensions rather than collapsing them into a single `REASONING` or `TOOL_CALLING` flag:

- input and output modalities, including text, image, audio, video, and multimodal tool responses;
- context-window and maximum-output limits;
- supported reasoning/effort levels, adaptive versus fixed thinking behavior, and provider-specific parameter names;
- tool capabilities, including function calling, web search, file search, code execution, computer use, and realtime I/O where supported;
- stream mode, event families, cancellation, native resume, and continuation requirements;
- data locality, availability, rate-limit class, observed latency class, and reliability history;
- model lifecycle status, including active, deprecated, and retired catalog entries.

The router MUST perform capability negotiation against the selected model descriptor before request construction. A route is eligible only when the model descriptor satisfies the hard request requirements and the adapter can represent the required capabilities without silently dropping them. If a provider cannot represent a requested capability, the router MUST either select a compatible candidate under the existing fallback policy or return the canonical unsupported-capability outcome; it MUST NOT silently downgrade computer use, multimodal output, provider-native reasoning continuation, or required evidence behavior.

A route plan MUST preserve the capability snapshot, exact model identifier, provider adapter version, reasoning mapping, requested modalities, and fallback compatibility decision. Provider catalog refresh MUST NOT mutate an in-flight route plan. Model deprecation or retirement affects new route selection; an existing execution retains its recorded model identity and contract version and follows the existing recovery/version-compatibility rules.

### Provider-Native Reasoning and Continuation State

The canonical `ReasoningPolicy` and `ReasoningEffort` remain Nexora-owned policy projections. Provider adapters own translation into provider-specific effort parameters, adaptive-thinking controls, reasoning-token budgets, thought signatures, or equivalent continuation artifacts.

Provider-native continuation state is distinct from `ReasoningSummary`, `ClaimRecord`, and private raw chain-of-thought. When a provider requires an opaque continuation artifact for multi-turn reasoning, the adapter MUST carry it only through the provider protocol, bind it to the request/stream/model identity, apply provider expiry and integrity rules, and exclude private reasoning content from user-visible or durable reasoning summaries. A provider adapter MUST declare whether continuation is required, optional, unsupported, resumable, or invalidated by model/provider failover.

A provider fallback MUST NOT replay provider-native reasoning state into a different provider unless an explicit compatible translation contract exists. Otherwise the fallback starts a new provider stream with a new stream identity and preserves only the canonical context, claims, citations, Tool state, and lineage allowed by the existing recovery contract.

### Advanced Capability Boundary

Computer use, web/file search, code execution, realtime audio, transcription, image generation, and multimodal function responses are optional negotiated capabilities, not universal properties of `AIProvider`. Their availability MUST be represented in the model descriptor and enforced by the normal authorization, sandbox, approval, stream, and evidence contracts. A provider that supports text streaming alone MUST remain a valid provider; advanced capability absence is not a lifecycle failure.

## Creative Modality and Capability Routing

A creative request MAY require text, image, audio, video, multimodal input, structured output, realtime interaction, or a combination of existing provider and Tool capabilities. The request’s required modality and quality constraints MUST be represented in the existing request, model-catalog, `ProviderRoutePlan`, Tool, ContextSnapshot, and evidence projections; no new creative provider identity or routing authority is created.

The router MUST select only an eligible cloud/external model and existing Tool path whose negotiated descriptor supports the required input/output modality, context size, streaming or continuation behavior, permission scope, sandbox boundary, and evidence requirements. Existing capabilities such as `VISION`, `MULTIMODAL_FUNCTION_CALLING`, `REALTIME_AUDIO`, `AUDIO_TRANSCRIPTION`, image-generation Tools, and file or workspace artifact Tools remain separately represented and authorized. Provider or model self-description is capability metadata, not proof that the capability is implemented or executed.

For each creative route, the persisted `ProviderRoutePlan` MUST preserve the requested modality, selected provider/model identity, capability snapshot, adapter version, fallback decision, and reason. An unsupported, unavailable, stale, unsafe, or incompatible modality MUST produce an explicit existing unsupported/degraded/blocked outcome or use an eligible fallback; it MUST NOT be silently replaced with a different medium or represented as completed. Generated artifacts and factual claims continue through the existing Tool authorization, artifact, provenance, `ClaimRecord`, verification, retention, and user-visible disposition contracts.

Creative quality preferences MAY rank eligible routes or inform non-blocking presentation, but they MUST NOT override permission, safety, deadline, resource, provider, sandbox, lifecycle, or evidence gates. A creative output is not factual evidence merely because a provider generated it, and a polished artifact does not establish implementation, testing, or executed-evidence status.

## Typed Streaming Contract

`AIProvider.stream()` returns `Flow<StreamEnvelope>`. Every event carries immutable
stream/request/correlation/provider/model identity and a monotonic sequence. Event types
are closed and include started, text, redacted reasoning summary, citation, tool-call
fragments/commit, usage, heartbeat, terminal, failure, and cancellation.

Provider-native events are normalized by adapters. A non-streaming provider emits the
same canonical event sequence after completion. Exactly one terminal event commits
success; transport close alone is failure. Per-stream states and reconnect rules are
owned by `state-machines/ProviderStreamLifecycle.md`.

### Backpressure, Cancellation, Resume, and Failover

- Bounded channels suspend producers or coalesce only text/reasoning-summary deltas.
- Tool, citation, usage, terminal, failure, and cancellation events are never dropped.
- Cancellation must reach the adapter within the configured cancellation deadline.
- Native resume reuses `streamId` and continues after the committed sequence/cursor.
- Restart or provider failover creates a new `streamId` with `priorStreamId`.
- Output from different providers is never silently spliced into one stream.

## Initial Providers

| Provider | Protocol | Capabilities |
|----------|----------|-------------|
| **OpenAI** | REST API | Chat, Streaming, Tool Calling, Vision, Embeddings |
| **Anthropic** | REST API | Chat, Streaming, Tool Calling, Vision |
| **Gemini** | Google AI REST | Chat, Streaming, Tool Calling, Vision, Embeddings |
| **Groq** | REST API | Chat, Streaming, Tool Calling |
| **OpenRouter** | Unified external API | Chat, Streaming, Tool Calling, Vision |
| **Custom** | User-defined external/cloud endpoint | Varies |

## Provider Configuration

```kotlin
data class ProviderConfig(
    val id: String,
    val type: ProviderType,
    val name: String,
    val apiKey: String?,  // Encrypted via SecureKeyStore
    val baseUrl: String,
    val defaultModel: String,
    val maxTokens: Int = 4096,
    val temperature: Double = 0.7
)
```

## Provider Profiles

Users configure providers through **named profiles** — multiple switchable
configurations per provider (API key, endpoint, model, streaming, parameters).
Profiles are independent (create/edit/duplicate/delete/switch), stored with keys in
`SecureKeyStore`, and one profile is the default per workspace. See
[specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) and
[models/Provider.md](../models/Provider.md).

## Product Configuration and Test Connection Boundary (Creator Product Design)

The product-facing AI Settings surface uses the existing named provider-profile boundary. A profile MUST support provider identity/type, external base URL, secret API-key reference, default model, and the provider parameters already defined by `ProviderConfig`; model and capability metadata come from the provider catalog and negotiated route contract. The canonical configuration owner remains the provider subsystem and `SecureKeyStore`; no UI component or creator-owned product document stores a second provider configuration.

**Test Connection** MAY invoke the existing provider `healthCheck()` and, where supported, model-catalog/capability discovery for the selected profile/model. The result is a connection and compatibility observation for the UI and evidence surfaces. It MUST NOT create a `Task` or `Execution`, authorize a workspace Tool, grant a PermissionModel scope, start sandbox/process work, or bypass the Runtime, Tool, Security, or evidence gates. API keys are secret values and MUST never enter prompts, logs, telemetry, evidence, or generated artifacts.

Capability refresh/detection MUST preserve the existing distinction between provider, model, request, response, and capability. A provider or successful connection test is not proof that every model or capability is implemented; hard capability incompatibility remains an explicit route outcome under the model-catalog negotiation contract.

## Design Rule

> The runtime must NEVER depend on a specific provider implementation.
>
> All provider-specific logic lives inside provider plugins.
> The core runtime only sees the `AIProvider` interface.

## Reasoning Effort Mapping

`ReasoningEffort` is the wire-level projection of the user-facing reasoning effort
scale defined in [../specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md) §6
(FR-RN-007/008). Adapter rules:

- **`OFF` is not a wire value** — when reasoning is disabled, `reasoningEffort` is
  `null` and the adapter MUST omit reasoning parameters (`reasoning_effort`,
  `thinking`, etc.) from the request entirely. Sending an explicit zero/off token is
  provider-specific behavior and is only used when a provider requires it (recorded in
  that provider's adapter).
- **Non-REASONING models** ignore the field (adapters drop it); the graceful-degradation
  and fail-fast rules live at the router level (FR-RN-004), not in adapters.
- **Per-model mapping** (e.g. provider `minimal/low/medium/high` enums or thinking-token
  budgets) is owned by each provider adapter; the runtime only carries the canonical
  5-value enum.

## Phase Mapping

- **Phase 1**: Define `AIProvider` interface, `ProviderRegistry`, configuration models.
- **Phase 5**: Implement the active cloud/external provider adapters. Streaming. Health checks. Local AI providers are out of scope under the standing DEC-44 rule.
- **Phase 8**: Providers as plugins. Custom provider SDK.


## Routing Policy

This upgrade adds explicit provider/model routing semantics while preserving provider abstraction.

Provider selection SHOULD consider:

- latency sensitivity;
- reasoning depth requirement;
- context-window requirement;
- tool-calling capability;
- vision/multimodal need;
- availability and health;
- reliability history;
- non-blocking cost preference or reporting policy; cost MUST NOT be an internal execution gate.

The routing layer SHOULD distinguish latency-critical foreground execution from background work such as indexing, summarization refresh, and cache warming.

## Rate-Limit Handling

Provider rate-limit responses (HTTP 429 or provider-specific rate-limit error codes) are classified as bounded transient conditions where appropriate. Rate-limit handling is distinct from other failure classes and does not count against tool-level retry limits unless the tool explicitly couples to provider rate-limit state.

### Failover

- Failover is **OPTIONAL and policy-driven**, not automatically mandatory.
- Failover is owned by the existing provider-routing authority and MUST respect the existing routing policy.
- Provider capability compatibility must be respected before failover.
- Sequential provider rate limits MUST NOT create unbounded retry/failover loops or retry storms.

### Retry and Identity

- Retry budgets remain bounded and continue to follow existing retry authority.
- Provider switching MUST NOT silently create a new logical execution/retry lineage unless existing architecture explicitly requires that.
- Execution/retry identity semantics remain stable across provider failover unless an existing canonical rule says otherwise.

### User Notification

Persistent rate-limit failures across providers escalate to user notification rather than silent degradation.


Routing decisions MUST remain compatible with the provider abstraction and MUST NOT hardcode a single provider as universal default for all task classes.

## Provider Adapter Bypass & Jailbreak

### Bypassing Provider Safeguards

When a tool invocation requires bypassing provider safeguards, the adapter delegates to the `bypassSafeguards()` extension method instead of the standard `complete()` path:

```kotlin
class ProviderAdapter(private val provider: AIProvider) {
    suspend fun callProvider(request: CompletionRequest, bypassSafeguards: Boolean): CompletionResponse {
        return if (bypassSafeguards) {
            provider.bypassSafeguards(request)
        } else {
            provider.complete(request)
        }
    }
}
```

### Handling Jailbreak Prompts

When `tool.allowJailbreakPrompts=true`, the adapter delegates to `handleJailbreakPrompt()` which bypasses standard safety classification:

```kotlin
class ProviderAdapter(private val provider: AIProvider) {
    suspend fun callProvider(
        request: CompletionRequest,
        bypassSafeguards: Boolean = false,
        allowJailbreakPrompts: Boolean = false
    ): CompletionResponse {
        return when {
            allowJailbreakPrompts -> provider.handleJailbreakPrompt(request)
            bypassSafeguards -> provider.bypassSafeguards(request)
            else -> provider.complete(request)
        }
    }
}
```
