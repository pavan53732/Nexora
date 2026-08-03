# Provider SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

> **Testing:** Provider tests: [testing/UnitTests.md](../testing/UnitTests.md) (Provider section), [testing/IntegrationTests.md](../testing/IntegrationTests.md) (mocked provider server).

---

## Overview

The Provider SDK enables developers to add new AI provider integrations. Each provider implements the `AIProvider` interface.

## Creating a Provider

```kotlin
class MyProvider(
    private val config: ProviderConfig
) : AIProvider {
    override val id = config.id
    override val name = config.name
    override val type = ProviderType.CUSTOM
    override val supportedCapabilities = setOf(
        ProviderCapability.CHAT_COMPLETION,
        ProviderCapability.STREAMING,
        ProviderCapability.TOOL_CALLING
    )

    override suspend fun complete(request: CompletionRequest): CompletionResponse {
        // Translate request to provider-specific format
        // Make HTTP call
        // Translate response back to Nexora format
    }

    override fun stream(request: CompletionRequest): Flow<StreamChunk> {
        // Return a flow of streaming chunks
    }

    override suspend fun embed(request: EmbeddingRequest): EmbeddingResponse {
        throw UnsupportedOperationException("Embeddings not supported")
    }

    override suspend fun listModels(): List<Model> {
        // Return available models
    }

    override suspend fun healthCheck(): HealthStatus {
        // Check if the provider is reachable
    }
}
```

## Adapter Pattern

For providers with non-standard APIs, use an adapter to translate between Nexora's format and the provider's format. The runtime should never see provider-specific data structures.

See [docs/api/Provider-API.md](../docs/api/Provider-API.md) for the full Provider API reference.
