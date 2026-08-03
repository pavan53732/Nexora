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
    val stopSequences: List<String>? = null
)

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

## Phase Mapping

- **Phase 1**: Define `AIProvider` interface, `ProviderRegistry`, configuration models.
- **Phase 5**: Implement all 9 providers. Streaming. Health checks.
- **Phase 8**: Providers as plugins. Custom provider SDK.
