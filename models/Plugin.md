> **Status: DERIVED** for Plugin domain model.
> This document defines the shape and semantics of Plugin in the data model.
>
> Depends on: the canonical architecture document for Plugin.
> Referenced by: protocols, APIs, SDKs, registries, and storage implementations.

# Domain Model: Plugin

```kotlin
data class Plugin(
    val id: String,
    val version: String,
    val compatibilityRange: String,
    val requiredPermissions: List<String>,
    val dependencies: List<PluginDependency>,
    val exportedAgents: List<String>,
    val exportedTools: List<String>,
    val exportedProviders: List<String>,
    val exportedSkills: List<String>,
    val exportedUiScreens: List<String>,
    val exportedMemoryBackends: List<String>,
    val integrityState: IntegrityState,
    val status: PluginStatus,
    val createdAt: Instant,
    val updatedAt: Instant
)

data class PluginDependency(
    val pluginId: String,
    val versionRange: String
)

enum class IntegrityState {
    PENDING,
    VERIFYING,
    VERIFIED,
    FAILED_INVALID_SIGNATURE,
    FAILED_INCOMPATIBLE_SDK,
    FAILED_TAMPERED
}

enum class PluginStatus {
    DISCOVERED,
    DOWNLOADING,
    DOWNLOADED,
    VERIFYING,
    INSTALLING,
    INSTALLED,
    ACTIVATING,
    ACTIVE,
    DEACTIVATING,
    INACTIVE,
    UNINSTALLING,
    UNINSTALLED,
    FAILED,
    CANCELLED
}
```

## Lifecycle and Operation Semantics

Plugin activation is transactional across exported capability registration. Partial registration is not a valid durable state; failed activation must roll back to the prior committed plugin state.

### State Transitions & Error Recovery

Plugin status changes are governed canonically by [state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md). 
- An interrupted installation or download (e.g. process termination) MUST recover by returning to `DISCOVERED` or starting the download transition again.
- Active plugins can be dynamically deactivated, returning to the `INACTIVE` state, which releases classloader resources but preserves local storage.
