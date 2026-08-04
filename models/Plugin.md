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
    val integrityState: IntegrityState,
    val status: PluginStatus,
    val createdAt: Instant,
    val updatedAt: Instant
)
```

## Lifecycle and Operation Semantics

Plugin activation is transactional across exported capability registration. Partial registration is not a valid durable state; failed activation must roll back to the prior committed plugin state.
