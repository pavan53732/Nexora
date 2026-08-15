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
    val capabilities: Set<ProviderCapability>,
    val supportedModels: List<ModelDescriptor>,
    val modelCatalogSnapshotId: String,
    val modelCatalogRetrievedAt: Instant,
    val providerContractVersion: String,
    val supportsStreaming: Boolean,
    val streamResumeMode: StreamResumeMode,
    val supportedInputModalities: Set<String>,
    val supportedOutputModalities: Set<String>,
    val contextWindowTokens: Int,
    val maxOutputTokens: Int,
    val tokenizerId: String,
    val reasoningEfforts: Set<String>,
    val supportsAdaptiveThinking: Boolean,
    val supportsProviderReasoningContinuation: Boolean,
    val supportsTools: Boolean,
    val supportsCitations: Boolean,
    val observedLatencyClass: LatencyClass,
    val inputCostPerMillion: Double?,
    val outputCostPerMillion: Double?,
    val dataLocality: DataLocality,
    val status: ProviderStatus,
    val health: ProviderHealth,
    val createdAt: Instant,
    val updatedAt: Instant
)

// StreamResumeMode is defined in models/Inference.md.
// ProviderCapability is owned by architecture/PROVIDER_SYSTEM.md.
data class ModelDescriptor(
    val modelId: String,
    val pinnedVersion: String?,
    val contextWindowTokens: Int,
    val maxOutputTokens: Int,
    val reasoningEfforts: Set<String>,
    val supportsAdaptiveThinking: Boolean,
    val capabilities: Set<ProviderCapability>,
    val streamResumeMode: StreamResumeMode,
    val contractVersion: String,
    val lifecycleStatus: ModelLifecycleStatus
)

enum class ModelLifecycleStatus { ACTIVE, DEPRECATED, RETIRED }
enum class LatencyClass { ULTRA_LOW, LOW, BALANCED, HIGH, UNKNOWN }
enum class DataLocality { EXTERNAL } // DEC-41: active AI providers are external/cloud only

enum class ProviderStatus {
    REGISTERED,
    CONFIGURING,
    CONFIGURED,
    TESTING,
    ACTIVE,
    DISABLED,
    REMOVED
}

enum class ProviderHealth {
    UNKNOWN,
    HEALTHY,
    DEGRADED,
    UNHEALTHY
}
```

## Lifecycle and Health Semantics

Provider request execution is correlated by `correlationId` and provider-scoped request ID. Each execution also records the model-catalog snapshot, exact model descriptor, provider contract version, requested modalities, reasoning-effort mapping, and any opaque provider-native continuation reference used by the adapter. Usage accounting, terminal markers, and canonical error envelopes are part of the durable contract even when the upstream provider omits optional fields. Provider-native continuation state is not raw private chain-of-thought and is not replayed across incompatible provider failover.

### Administrative Status vs. Operational Health

To eliminate responsibility gaps and resolve High Finding 6, the Provider domain model separates administrative lifecycle status (`ProviderStatus`) from periodic operational health checks (`ProviderHealth`):
- `status: ProviderStatus` tracks manual configuration, registration, enablement, and removal states.
- `health: ProviderHealth` tracks runtime reachability, latency thresholds, and consecutive error rates handled automatically by the background `HealthMonitor` coroutine.
- Administrative lifecycle `From` and `To` values are `ProviderStatus` only. A `ProviderHealth` value is a predicate only when an explicit lifecycle guard requires it; it is not an administrative state.
- `disable()` is `ACTIVE → DISABLED`; `remove()` is `DISABLED → REMOVED`. An `ACTIVE` provider, including one whose health is `UNHEALTHY`, cannot be removed directly.
- After `DISABLED`, persisted health is retained but no longer actively evaluated. After `REMOVED`, health has no operational effect.

### Failover and Routing Constraints

- Only providers with `status = ACTIVE` and `health = HEALTHY` are eligible for primary request routing.
- Degraded providers may be used if no healthy alternative is configured (emitting warning events).
- Unhealthy providers are immediately excluded from active routing tables and put on a connection re-probe cycle while their status remains eligible for health evaluation.
