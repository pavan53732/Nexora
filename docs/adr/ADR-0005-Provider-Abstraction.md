# ADR-0005: Provider Abstraction Layer

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect

## Context

Nexora must support multiple external/cloud AI providers (OpenAI-compatible APIs, Anthropic, Gemini, Groq, OpenRouter, and Custom external endpoints). Each has a different API format, authentication method, and capability set. Local AI providers are out of scope under DEC-41.

Two approaches:

1. **Provider-specific code in runtime**: The runtime contains `if (provider == "openai") ... else if (provider == "anthropic") ...`. This creates tight coupling and makes adding providers require modifying the runtime.

2. **Abstraction layer**: Define a common `AIProvider` interface. Each provider is an implementation of this interface. The runtime only sees the interface.

## Decision

Nexora uses a **provider abstraction layer**. The `AIProvider` interface is defined in the `providers` module (`com.nexora.app.providers`, per `docs/MODULE_BOUNDARIES.md`):

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
    suspend fun handleJailbreakPrompt(request: CompletionRequest): CompletionResponse
}
```

**Design rule**: The runtime must NEVER depend on a specific provider implementation. All provider-specific logic lives in `providers/` as plugins.

## Consequences

### Positive
- **Loose coupling**: Runtime is independent of any provider.
- **Easy to add providers**: Implement the interface, register it.
- **Testable**: Mock providers for testing without real API calls.
- **Swappable**: Users can switch providers mid-conversation.

### Negative
- **Lowest common denominator**: The interface must be generic enough for all providers, potentially missing provider-specific features.
- **Adapter complexity**: Providers with very different APIs (e.g., Anthropic's tool format vs OpenAI's) need non-trivial adapters.

### Mitigation
- Allow providers to expose provider-specific options through a generic `metadata: Map<String, Any>` field.
- Support both OpenAI-format and Anthropic-format tool calling in the adapter layer.
- Provider plugins can add custom UI for provider-specific configuration.
