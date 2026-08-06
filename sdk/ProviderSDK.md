# Provider SDK — Nexora

The Provider SDK defines provider adapter, typed-stream normalization, credentials,
cancellation, and backpressure contracts.

## Adapter Contract

```kotlin
abstract class BaseProviderAdapter(
    val descriptor: ProviderDescriptor
) {
    abstract suspend fun complete(
        request: ProviderCompletionRequest,
        credentials: ProviderCredentials
    ): ProviderCompletionResponse

    abstract fun streamComplete(
        request: ProviderCompletionRequest,
        credentials: ProviderCredentials,
        bufferPolicy: StreamBufferPolicy
    ): Flow<StreamEnvelope>

    open fun resumeStream(
        request: ResumeProviderStreamRequest,
        credentials: ProviderCredentials
    ): Flow<StreamEnvelope> = throw NexoraError("NXR-4014", "Native resume unsupported")

    abstract suspend fun cancelStream(
        request: CancelProviderStreamRequest
    ): StreamEnvelope
}

data class ProviderDescriptor(
    val providerId: String,
    val adapterVersion: String,
    val minContractVersion: String,
    val capabilities: Set<ProviderCapability>,
    val streamResumeMode: StreamResumeMode,
    val modelCatalog: List<ModelCapabilityMetadata>
)
```

## Normalization Rules

- Adapters translate native SSE/WebSocket/HTTP events into the closed canonical event set.
- `streamId`, `requestId`, identity, and sequence are assigned/validated before emission.
- Native reasoning is emitted only as provider-approved redacted reasoning summary data.
- Tool argument fragments remain isolated until complete JSON and Tool schema validation.
- Socket close without a canonical terminal event throws `NXR-4017`.
- Network loss becomes `NXR-4007` unless native cursor resume is valid.

## Backpressure and Cancellation

- Use bounded channels from `StreamBufferPolicy`; never use unbounded buffering.
- Text/reasoning-summary deltas may be coalesced; semantic/control events may not be dropped.
- Sustained overflow returns `NXR-4013`.
- Cancellation closes HTTP/SSE/WebSocket resources and emits one idempotent Cancelled terminal event.
- Coroutine cancellation is propagated and `CancellationException` is never swallowed.

## Resume

- `NATIVE_CURSOR` resumes the same stream after its last committed sequence.
- `RESTART_WITH_LINEAGE` is orchestrated by ProviderRouter as a new stream, not adapter byte-resume.
- Resume tokens are opaque, short-lived, provider/profile scoped, redacted from logs, and never persisted in exported diagnostics.

## Security

- Credentials exist only in transient memory and are never logged or persisted by adapters.
- Clients connect only to the profile `baseUrl`; TLS and pinning rules apply.
- Event sizes and schemas are validated before crossing into Agent Runtime.
