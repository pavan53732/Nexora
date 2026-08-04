# Provider SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [../docs/api/Provider-API.md](../docs/api/Provider-API.md)

---

## Normative SDK Contract

The Provider SDK MUST preserve the contract defined by [Provider-API.md](../docs/api/Provider-API.md). Convenience abstractions MUST NOT hide usage records, correlation IDs, provider request IDs, stream sequence ordering, terminal markers, resume tokens, or canonical error envelopes.

### Required Operation Coverage

A conforming SDK implementation MUST provide typed support for:

- provider registration
- capability declaration
- completion and streaming request envelopes
- cancellation
- usage accounting
- resumable-stream metadata where supported
- canonical error-envelope creation and propagation

## Overview

The Provider SDK helps adapter authors implement providers that conform to the canonical provider contract.

## Creating a Provider

```kotlin
interface ProviderAdapter {
    val descriptor: ProviderDescriptor
    suspend fun complete(request: ProviderRequest): ProviderResponse
    fun stream(request: ProviderRequest): Flow<ProviderStreamEvent>
    suspend fun cancel(providerRequestId: String, correlationId: String, cancellationKey: String?): ProviderResponse
}
```

## Adapter Pattern

Provider adapters MAY normalize vendor-specific payloads internally, but the exported SDK types MUST remain canonical.

## Compatibility Rules

SDKs MUST expose compatibility metadata for API contract version, supported model capability families, streaming/resume support, and manifest/schema version.
