> **Status: DERIVED** for Plugin message contract.
> This document defines protocol messages for Plugin lifecycle operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Plugin (`architecture/PLUGIN_SYSTEM.md`) and [../state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md) for Plugin lifecycle transitions.
> Referenced by: models, APIs, SDKs, registries, security, and tests.

# Plugin Protocol — Nexora

> Communication contract between the PluginManager, Registry, and application ClassLoader boundary.

## Installation Flow

```text
PluginManager             Security Engine             ClassLoader
      │                          │                         │
      ├─────── verify() ────────>│                         │
      │                          │                         │
      │<─────── VERIFIED ────────┤                         │
      │                                                    │
      ├────────────────── load() ─────────────────────────>│
      │                                                    │
      │<───────────── PluginLoaded ────────────────────────┤
```

1. **Verification**: The `PluginManager` downloads the plugin archive, computes the SHA-256 hash, and passes the archive handle to the `SecurityEngine` for Release-Key cryptographic signature verification.
2. **Mount & Load**: On success, the `PluginManager` extracts dynamic DEX/JAR binaries to `/data/data/com.nexora.app/plugins/{id}/{version}/` and instantiates a private, isolated `DexClassLoader`.
3. **Activation Command**: The engine invokes `onActivate` on the plugin's entry point interface. The plugin registers its exported capabilities via core APIs.
4. **Outcome Publication**: The `PluginManager` commits the new status (`ACTIVE`) and emits the `PluginActivated` transition event.

## Protocol Messages

### Plugin Loading Command

```kotlin
data class LoadPluginMessage(
    val correlationId: String,
    val pluginId: String,
    val version: String,
    val binaryPath: String,
    val permissions: List<String>,
    val classloaderIsolationEnabled: Boolean = true
)
```

### Plugin State Changed Event

```kotlin
data class PluginStateChangedEvent(
    val eventId: String,
    val correlationId: String,
    val pluginId: String,
    val fromStatus: PluginStatus,
    val toStatus: PluginStatus,
    val version: Long,
    val occurredAt: Instant,
    val errorEnvelope: CanonicalErrorEnvelope? = null
)
```

## Conformance Rules

- **Transactional Registration**: Capability registration is atomic. If any exported capability registration fails (e.g. duplicate key or naming collision), the registration engine MUST throw an exception and the `PluginManager` MUST immediately attempt compensation through `onDeactivate`. If activation began from `Installed` or `Inactive` and every registered capability is unregistered and cleanup is verified, the Plugin MUST return to that activation-origin state. If cleanup fails or completion cannot be proven, the Plugin MUST remain `Failed`, affected capabilities MUST NOT be executable, and retry MUST require the existing retryability rule plus verified cleanup.
- **Deduplication**: Plugin lifecycle events MUST carry a monotonically increasing entity version and be deduplicated by `(pluginId, version, transition)`.
