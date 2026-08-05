# Provider SDK — Nexora

The Provider SDK defines the interface contracts, credentials retrieval utilities, and streaming base classes required to implement custom model providers in Nexora.

---

## SDK Architecture

To implement a new AI provider (e.g. customized enterprise LLM or local specialized model), authors MUST extend the `BaseProviderAdapter` class. The SDK handles TLS 1.3 socket pinning, credential decryption, and rate-limit backoffs natively.

```kotlin
package com.nexora.app.sdk.provider

abstract class BaseProviderAdapter(
    val descriptor: ProviderDescriptor
) {
    /**
     * Executes a text completion call.
     */
    abstract suspend fun complete(
        request: ProviderCompletionRequest,
        credentials: ProviderCredentials
    ): ProviderCompletionResponse

    /**
     * Initiates a Server-Sent Events (SSE) streaming call.
     */
    abstract suspend fun streamComplete(
        request: ProviderCompletionRequest,
        credentials: ProviderCredentials
    ): Flow<ProviderStreamChunk>
}

data class ProviderCredentials(
    val apiKey: String,
    val endpointUrl: String,
    val orgId: String? = null
)
```

## Security & Confinement Constraints

Custom adapters operate under strict network security profiles:
- **Credential Confinement**: Stored credentials are encrypted via Keystore-backed AES ciphers. The SDK provides credentials strictly in transient memory during request dispatch; custom adapters are forbidden from logging or storing these keys on disk.
- **Network Confinement**: Network requests can connect *only* to the `baseUrl` declared in the static descriptor. Connection attempts to other hosts are intercepted and blocked by the platform egress engine (`NXR-2003` / `NXR-7005`).

## Streaming & Failure Rules

- **Force-No-Truncation**: Stream adapters MUST catch network dropouts and translate them into a formal `NXR-4007` (Streaming Failed) exception. Letting a partial stream finish successfully is forbidden, as it introduces severe truncation hallucinations in autonomous planning.
- **Memory Redaction**: Headers and response logs MUST sanitize keys and BEARER tokens. The SDK provides standard `SanitizingHttpClient` structures to wrap outgoing HTTP sessions.
