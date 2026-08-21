> **Status: CANONICAL** for ProviderStream domain model.
> Per-stream inference state is owned by [../state-machines/ProviderStreamLifecycle.md](../state-machines/ProviderStreamLifecycle.md).

# Domain Model: ProviderStream

```kotlin
data class ProviderStream(
    val streamId: String,
    val requestId: String,
    val correlationId: String,
    val providerProfileId: String,
    val modelId: String,
    val sequence: Long,
    val emittedAt: Instant,
    val resumeToken: String?,
    val status: StreamStatus,
    val priorStreamId: String?
)
```

```kotlin
enum class StreamStatus {
    CREATED,
    CONNECTING,
    OPEN,
    BACKPRESSURED,
    RECONNECTING,
    COMPLETED,
    FAILED,
    CANCELLED
}
```
