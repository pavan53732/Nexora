> **Status: DERIVED** for Provider API.
> This document describes the API surface for the AI Provider System. Canonical behavior is defined in the owning state-machine (`state-machines/ProviderLifecycle.md`) and architecture (`architecture/PROVIDER_SYSTEM.md`) documents.
>
> Depends on: the canonical architecture document for Provider System (`architecture/PROVIDER_SYSTEM.md`).
> Referenced by: upstream architecture, models, protocols, and registries.

# Provider API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/PROVIDER_SYSTEM.md](../../architecture/PROVIDER_SYSTEM.md)

---

## Normative Operation Contract

The Provider API governs AI provider registration, model configuration, structured text completion, streaming, embedding generation, and token usage tracking. Sensitive keys are encrypted via Android Keystore-backed transience and are never stored in plain text.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `registerProfile`| Provider `Registered → Configured` | Confirmed provider metadata with encrypted key handle | Invalid key (`NXR-4011`), validation error (`NXR-1010`) | Safe (Idempotent) | Encrypts API keys inside Android Keystore; credentials never logged or leaked in memory dumps | Keystore and configuration tests |
| `complete` | No lifecycle change | Complete response text + detailed token metadata | Auth failed (`NXR-4003`), rate limit (`NXR-4004`), model not found (`NXR-4005`), malformed JSON (`NXR-4006`) | Safe (Idempotent Key) | Confinements: HTTP clients connect only to configured `baseUrl`; TLS 1.3 with pinned certs | Request routing and accuracy tests |
| `streamComplete` | No lifecycle change | Real-time text token chunks + final token usage | Network break (`NXR-4007`), timeout (`NXR-4002`), quota exceeded (`NXR-4012`) | Safe (Idempotent Key) | Outbound payload scanned for leak of keys or secrets; cancels stream on backpressure | Streaming and low-latency tests |
| `embed` | No lifecycle change | Normalized vector array (FloatArray) | Empty vector (`NXR-4008`) | Safe (Idempotent) | Scoped per-workspace; cannot bleed training data cross-workspace | Vector Database and search tests |
| `checkHealth` | Provider status updates based on health latency | Status updated to `HEALTHY`, `DEGRADED`, or `UNHEALTHY` | Host unreachable (`NXR-4001`), check failed (`NXR-4009`) | Safe to retry | Periodic FixedDelayRouter probes; automatic failover to fallback on Unhealthy | Failover and degradation ladder tests |

Every API request MUST carry a `correlationId`.

## Contract Shapes

### Completion Request

```kotlin
data class ProviderCompletionRequest(
    val correlationId: String,
    val providerProfileId: String,
    val modelId: String,
    val messages: List<ChatMessage>,
    val temperature: Float = 0.7f,
    val maxTokens: Int = 4096,
    val systemPrompt: String? = null,
    val tools: List<ToolDescriptor> = emptyList()
)
```

### Chat Message

```kotlin
data class ChatMessage(
    val role: MessageRole,
    val content: String,
    val toolCalls: List<ToolCall> = emptyList()
)

enum class MessageRole { SYSTEM, USER, ASSISTANT, TOOL }
```

### Usage Metadata

```kotlin
data class TokenUsage(
    val promptTokens: Int,
    val completionTokens: Int,
    val totalTokens: Int,
    val estimatedCostUsd: Double
)
```

### Completion Response

```kotlin
data class ProviderCompletionResponse(
    val correlationId: String,
    val message: ChatMessage,
    val usage: TokenUsage,
    val modelId: String,
    val finishReason: String
)
```

## Provider API Interface

```kotlin
package com.nexora.app.runtime.provider

interface ProviderApi {
    suspend fun registerProfile(profile: ProviderProfileDescriptor): ProviderProjection
    suspend fun complete(request: ProviderCompletionRequest): ProviderCompletionResponse
    suspend fun streamComplete(request: ProviderCompletionRequest): Flow<ProviderCompletionResponse>
    suspend fun embed(text: String, profileId: String, correlationId: String): FloatArray
    suspend fun checkHealth(profileId: String): ProviderHealth
}
```

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes | Recovery & Lifecycle Effects |
|---|---|---|
| `registerProfile` | `NXR-4011` (Invalid Key) | Block registry write; prompt user for correction. |
| `complete` / `stream` | `NXR-4003` (Auth Failed) | Prompt user to re-configure key; halt generation. |
| | `NXR-4004` (Rate Limited) | Parse `Retry-After` header; wait and delay retry. |
| | `NXR-4005` (Model Not Found) | Suggest alternative model; fallback to default. |
| | `NXR-4006` (Invalid Response)| Re-prompt or trigger automatic retry. |
| | `NXR-4002` (Timeout) | Halt execution; try fallback provider; trigger degradation. |
| | `NXR-4012` (Quota Exceeded) | Pause task; notify user; halt generation. |
| `embed` | `NXR-4008` (Embedding Failed) | Log failure; try fallback model. |
| `checkHealth` | `NXR-4001` (Connection Failed) | Log exception; retry with backoff. |
| | `NXR-4009` (Health Failed) | Transition status to `UNHEALTHY`; exclude from router. |
