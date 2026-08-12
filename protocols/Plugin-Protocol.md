> **Status: DERIVED** for Plugin message contract.
> This document defines protocol messages for Plugin lifecycle operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Plugin (`architecture/PLUGIN_SYSTEM.md`).
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

- **Transactional Registration**: Capability registration is atomic. If any exported tool or provider registration fails (e.g. duplicate key or naming collision), the registration engine MUST throw an exception, triggering the `PluginManager` to immediately call `onDeactivate` and roll back state to `INACTIVE`.
- **Deduplication**: Plugin lifecycle events MUST carry a monotonically increasing entity version and be deduplicated by `(pluginId, version, transition)`.
