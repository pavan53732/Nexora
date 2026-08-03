# Provider API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md)

---

## Overview

The Provider API defines how AI providers are integrated. The runtime interacts with providers exclusively through this API.

## Provider Interface

```kotlin
package com.nexora.app.core.providers

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
    OPENAI_COMPATIBLE, ANTHROPIC, GEMINI, GROQ,
    OPENROUTER, OLLAMA, LM_STUDIO, LOCAL_GGUF, CUSTOM
}

enum class ProviderCapability {
    CHAT_COMPLETION, STREAMING, TOOL_CALLING, VISION, EMBEDDINGS, FUNCTION_CALLING
}
```

## Usage API

```kotlin
// Get a provider instance
val provider = providerRegistry.get("openai")

// Synchronous completion
val response = provider.complete(CompletionRequest(
    model = "gpt-4o",
    messages = listOf(Message(role = "user", content = "Build a todo app")),
    tools = toolRegistry.toToolDefinitions()
))

// Streaming
provider.stream(request).collect { chunk ->
    // Handle each chunk
}

// Health check
val health = provider.healthCheck()
```

## Design Rule

> The runtime must NEVER depend on a specific provider implementation.
> All provider-specific logic lives in `providers/` as plugins.

See [registry/PROVIDERS.md](../../registry/PROVIDERS.md) for the complete provider registry.
