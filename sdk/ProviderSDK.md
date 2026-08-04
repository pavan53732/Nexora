> **Status: DERIVED** for ProviderSDK SDK.
> This document describes the sdk surface for ProviderSDK. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for ProviderSDK.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Provider SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

> **Testing:** Provider tests: [testing/UnitTests.md](../testing/UnitTests.md) (Provider section), [testing/IntegrationTests.md](../testing/IntegrationTests.md) (mocked provider server).

---

## Normative SDK Contract

The SDK is an adapter over the corresponding API and protocol. SDK convenience methods MUST NOT create a second lifecycle or error vocabulary. Every operation MUST preserve correlation ID, canonical error fields, lifecycle effect, cancellation outcome, and idempotency behavior from the API contract.

| SDK responsibility | Required behavior |
|---|---|
| Request construction | Validate local arguments without changing server-side lifecycle semantics. |
| Result projection | Expose durable status, execution phase, transition version, and correlation ID where the API provides them. |
| Errors | Map canonical `NXR-*` codes to typed SDK errors while preserving the original envelope and redacted details. |
| Retry | Never retry automatically unless the canonical error says retry is safe and the operation is idempotent or keyed. |
| Cancellation | Propagate cancellation to the API/protocol and expose the committed terminal outcome. |
| Events/streams | Preserve ordering metadata and deduplicate at-least-once events; do not infer success from transport closure. |
| Compatibility | SDK version changes MUST document any renamed projection or transport mapping without changing canonical meanings. |

### Required Operation Coverage

The SDK MUST expose or explicitly mark unsupported the operation contracts for agent execution, task cancellation/status, tool invocation, provider completion/streaming, and plugin install/activation. Unsupported operations MUST return a canonical capability error rather than a generic exception.

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
