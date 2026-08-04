> **Status: DERIVED** for Provider-API API.
> This document describes the api surface for Provider-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Provider-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Provider API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/PROVIDER_SYSTEM.md](../../architecture/PROVIDER_SYSTEM.md)

---

## Normative Operation Contract

The operation below is a contract boundary, not merely a Kotlin convenience method. Implementations MUST preserve the lifecycle, event, error, security, retry, cancellation, and idempotency semantics shown here. Transport-specific names MAY differ only when the mapping is documented and lossless.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `execute` / `startTask` | Task `Draft/Pending → Queued → Running`; Agent `Ready → Running` | Task projection plus correlation ID | Invalid input, unavailable agent/provider, permission/approval, timeout, cancellation, internal fault; use `NXR-*` envelope | Client retries require idempotency key; duplicate key returns original task; execution retry is lifecycle-controlled | Workspace authorization and tool policy checked before side effects; cancellation emits lifecycle event and performs cleanup | Runtime integration and end-to-end tests |
| `cancel` / `cancelTask` | Active task/agent → `Cancelled` | Committed cancellation projection | Not found, already terminal, conflict, cleanup failure | Idempotent for same task and cancellation key; repeated request returns committed result | Caller must own workspace/task; cancellation propagates to child jobs and sandbox operations | Lifecycle and cancellation tests |
| `getTaskStatus` | No lifecycle change | Durable status, execution phase, version, latest error | Not found, unauthorized, storage failure | Safe to retry; read is versioned | Redact sensitive error details according to caller scope | API contract tests |
| `invoke` | ToolCall `Pending → Approved/Denied → Executing → Completed/Error` | Tool result, event sequence, correlation ID | Permission denied, approval required, timeout, cancellation, invalid parameters, sandbox/provider failure | Re-execution requires tool idempotency declaration; duplicate call key MUST NOT repeat non-idempotent effects | Permission and sandbox checks precede execution; cancellation releases resources | Tool protocol and security tests |
| `complete` / `stream` | Provider remains lifecycle-authorized; request execution gets committed result or canonical failure | Completion response or ordered stream with terminal marker | Provider unavailable, rate limit, timeout, invalid request, capability mismatch | Retry follows error envelope; non-idempotent external effects require key; stream reconnect must declare resume policy | Provider credentials never cross boundary; cancellation closes stream and records outcome | Provider protocol and integration tests |
| `install` / `activate` | Plugin lifecycle follows verification/install/activation transitions | Plugin projection and registered capabilities | Integrity failure, incompatibility, dependency, permission, timeout, cancellation | Install keyed by plugin/version; duplicate operation returns existing result; activation is not repeated after commit | Signature, compatibility, permission, and sandbox checks precede activation; cancellation rolls back partial artifacts | Plugin lifecycle and security tests |

Every operation MUST return or emit a correlation ID. Errors MUST preserve `code`, `category`, `retryability`, `idempotency`, `lifecycleEffect`, `recoveryOwner`, and redacted `details` from [ERROR_CODES.md](../../errors/ERROR_CODES.md). Lifecycle events are published only after durable state commit and are deduplicated by entity plus transition version.

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
    CHAT_COMPLETION, STREAMING, TOOL_CALLING, VISION, EMBEDDINGS,
    FUNCTION_CALLING, REASONING
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
