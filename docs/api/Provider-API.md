> **Status: DERIVED** for Provider API.
> This document describes the api surface for Provider. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Provider.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Provider API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/PROVIDER_SYSTEM.md](../../architecture/PROVIDER_SYSTEM.md)

---

## Normative Operation Contract

The Provider API owns model capability discovery, request validation, completion, streaming, cancellation, and usage accounting. Credential loading and redaction are part of the contract boundary; raw credentials MUST NOT cross into caller-visible payloads.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `registerProvider` | Provider `Discovered → Registered → Available` | Durable provider projection | Duplicate provider, incompatible adapter/API version, invalid capabilities, storage failure | Duplicate `(providerId, version)` is idempotent | Registration validates capability declaration and compatibility before visibility | Registry and SDK conformance tests |
| `getProvider` / `listProviders` | No lifecycle change | Stable projection(s), capabilities, pagination cursor | Not found, invalid filter, unauthorized, storage failure | Safe to retry; reads are side-effect free | Secret material and internal routing metadata MUST be redacted | API contract tests |
| `complete` | Request execution committed with terminal result | Completion payload, usage, correlation ID | Provider unavailable, rate limit, timeout, invalid request, capability mismatch | Side-effect-free completion retries SHOULD use same idempotency key and return equivalent terminal outcome where supported | Credentials never cross boundary; cancellation closes external request and records terminal outcome | Provider protocol and integration tests |
| `stream` | Request execution emits ordered stream and terminal marker | Ordered chunks plus terminal event and usage | Disconnect, timeout, provider unavailable, capability mismatch, invalid request | Resume support REQUIRES opaque `resumeToken`; if unsupported, provider MUST declare non-resumable streams | Cancellation closes stream, emits terminal event after durable commit, and frees external resources | Streaming and lifecycle tests |
| `cancelRequest` | Active provider request → `Cancelled` | Committed cancellation projection | Not found, already terminal, conflict, cleanup failure | Idempotent for same request and cancellation key | Caller must own workspace/request scope | Cancellation tests |

## Contract Shapes

```kotlin
data class ProviderRequest(
    val requestId: String,
    val correlationId: String,
    val idempotencyKey: String?,
    val workspaceId: String,
    val providerRequestId: String,
    val providerId: String,
    val model: String,
    val messages: List<MessagePart>,
    val toolsOffered: List<ToolDescriptorRef> = emptyList(),
    val responseFormat: ResponseFormat?,
    val temperature: Double?,
    val maxTokens: Int?,
    val timeoutMs: Long?,
    val caller: CallerRef,
    val metadata: Map<String, String> = emptyMap(),
    val resumeToken: String? = null
)

data class ProviderResponse(
    val correlationId: String,
    val providerRequestId: String,
    val status: ProviderRequestStatus,
    val version: Long,
    val output: ProviderOutput?,
    val usage: UsageRecord?,
    val error: CanonicalErrorEnvelope? = null,
    val resumeToken: String? = null
)
```

Streaming chunks MUST carry monotonically increasing sequence numbers and a terminal marker. Clients MUST NOT infer completion from socket closure alone.

## Overview

The Provider API defines how AI providers are registered, discovered, invoked, streamed, cancelled, and metered.

## Provider Interface

```kotlin
interface ProviderApi {
    suspend fun registerProvider(descriptor: ProviderDescriptor): ProviderProjection
    suspend fun getProvider(providerId: String): ProviderProjection
    suspend fun listProviders(filter: ProviderFilter, page: PageRequest): Page<ProviderProjection>
    suspend fun complete(request: ProviderRequest): ProviderResponse
    fun stream(request: ProviderRequest): Flow<ProviderStreamEvent>
    suspend fun cancelRequest(providerRequestId: String, correlationId: String, cancellationKey: String?): ProviderResponse
}
```

## Usage API

Usage accounting MUST be part of the success and terminal-failure contract where the upstream provider exposes billable units. Missing usage data MUST be represented explicitly as unknown, not silently omitted.

## Design Rule

Provider-specific response formats MAY vary internally, but the exported contract MUST normalize capabilities, usage, errors, cancellation outcome, and streaming terminal semantics.

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| registerProvider | NXR-4001, NXR-4002, NXR-5007 |
| getProvider / listProviders | NXR-4001, NXR-7001 |
| complete / stream | NXR-4003, NXR-4004, NXR-4005, NXR-4006, NXR-4007 |
| cancelRequest | NXR-4008, NXR-7007 |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for canonical envelope requirements.
