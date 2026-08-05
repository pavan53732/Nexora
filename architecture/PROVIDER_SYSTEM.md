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
    fun stream(request: CompletionRequest): Flow<StreamChunk>
    suspend fun embed(request: EmbeddingRequest): EmbeddingResponse
    suspend fun listModels(): List<Model>
    suspend fun healthCheck(): HealthStatus
}

enum class ProviderType {
    OPENAI_COMPATIBLE,  // OpenAI, DeepSeek, Together, Fireworks
    ANTHROPIC,           // Claude family
    GEMINI,              // Google AI
    GROQ,                // Fast inference
    OPENROUTER,           // Unified gateway
    OLLAMA,              // Local model server
    LM_STUDIO,           // Local model server
    LOCAL_GGUF,          // Direct GGUF loading
    CUSTOM               // User-defined endpoints
}

enum class ProviderCapability {
    CHAT_COMPLETION,
    STREAMING,
    TOOL_CALLING,
    VISION,
    EMBEDDINGS,
    FUNCTION_CALLING,
    REASONING   // multi-step internal reasoning (e.g. o-series, Claude thinking, Gemini thinking, DeepSeek-R1)
}
```

## Request/Response Models

```kotlin
data class CompletionRequest(
    val model: String,
    val messages: List<Message>,
    val tools: List<ToolDefinition>?,
    val temperature: Double = 0.7,
    val maxTokens: Int = 4096,
    val stopSequences: List<String>? = null,
    val reasoningEffort: ReasoningEffort? = null  // null = omit reasoning params entirely (OFF)
)

enum class ReasoningEffort { LOW, MEDIUM, HIGH, X_HIGH, MAX }

data class CompletionResponse(
    val content: String,
    val toolCalls: List<ToolCall>?,
    val usage: TokenUsage,
    val model: String,
    val finishReason: FinishReason
)

data class StreamChunk(
    val content: String?,
    val toolCalls: List<ToolCall>?,
    val usage: TokenUsage?,
    val finishReason: FinishReason?
)
```

## Initial Providers

| Provider | Protocol | Capabilities |
|----------|----------|-------------|
| **OpenAI** | REST API | Chat, Streaming, Tool Calling, Vision, Embeddings |
| **Anthropic** | REST API | Chat, Streaming, Tool Calling, Vision |
| **Gemini** | Google AI REST | Chat, Streaming, Tool Calling, Vision, Embeddings |
| **Groq** | REST API | Chat, Streaming, Tool Calling |
| **OpenRouter** | Unified API | Chat, Streaming, Tool Calling, Vision |
| **Ollama** | Local REST | Chat, Streaming, Tool Calling, Vision, Embeddings |
| **LM Studio** | Local REST | Chat, Streaming, Tool Calling |
| **Local GGUF** | Direct loading | Chat, Streaming |
| **Custom** | User-defined | Varies |

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
- **Phase 5**: Implement all 9 providers. Streaming. Health checks.
- **Phase 8**: Providers as plugins. Custom provider SDK.
