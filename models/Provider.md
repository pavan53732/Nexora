> **Status: DERIVED** for Provider domain model.
> This document defines the shape and semantics of Provider in the data model.
>
> Depends on: the canonical architecture document for Provider.
> Referenced by: protocols, APIs, SDKs, registries, and runtime implementations.

# Domain Model: Provider

```kotlin
data class Provider(
    val id: String,
    val version: String,
    val name: String,
    val capabilities: List<String>,
    val supportedModels: List<String>,
    val supportsStreaming: Boolean,
    val supportsResume: Boolean,
    val status: ProviderStatus,
    val health: ProviderHealth,
    val createdAt: Instant,
    val updatedAt: Instant
)
```

## Lifecycle and Health Semantics

Provider request execution is correlated by `correlationId` and provider-scoped request ID. Usage accounting, terminal markers, and canonical error envelopes are part of the durable contract even when the upstream provider omits optional fields.
