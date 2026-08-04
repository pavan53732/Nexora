> **Status: DERIVED** for Plugin API.
> This document describes the api surface for Plugin. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Plugin.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Plugin API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/PLUGIN_SYSTEM.md](../../architecture/PLUGIN_SYSTEM.md)

---

## Normative Operation Contract

The Plugin API owns package verification, dependency resolution, installation, activation, deactivation, and removal. Capability registration by plugins is delegated to the owning Agent, Tool, and Provider APIs after plugin activation succeeds.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `installPlugin` | Plugin `Discovered → Verified → Installed` | Durable plugin projection | Integrity failure, incompatibility, dependency failure, storage failure, timeout | Duplicate `(pluginId, version)` install is idempotent | Signature, compatibility, dependency, and permission checks MUST precede install | Lifecycle and security tests |
| `activatePlugin` | Installed plugin `Installed → Activated` | Activated projection plus registered capability references | Permission denied, dependency inactive, capability registration failure, timeout | Duplicate activation after durable commit returns active projection | Activation MUST be transactional; partial capability registration requires rollback | Activation and rollback tests |
| `deactivatePlugin` | Active plugin `Activated → Deactivated` | Durable deactivation projection | Not found, already inactive, dependency conflict, cleanup failure | Idempotent for same plugin and operation key | Deactivation MUST unregister exposed capabilities before final commit | Lifecycle tests |
| `removePlugin` | Plugin `Deactivated/Installed → Removed` | Durable removal projection | Not found, dependency conflict, cleanup/storage failure | Idempotent after commit | Caller must have administrative scope; removal clears stored artifacts after commit-safe point | Removal tests |
| `getPlugin` / `listPlugins` | No lifecycle change | Stable projection(s), dependency and capability metadata, pagination cursor | Not found, invalid filter, unauthorized, storage failure | Safe to retry | Internal verification data may be redacted by caller scope | API contract tests |

## Overview

The Plugin API defines package-level lifecycle management only. Plugin-exposed tools, agents, and providers must register through their own canonical APIs after activation.

## Plugin Interface

```kotlin
interface PluginApi {
    suspend fun installPlugin(request: PluginInstallRequest): PluginProjection
    suspend fun activatePlugin(pluginId: String, correlationId: String, operationKey: String?): PluginProjection
    suspend fun deactivatePlugin(pluginId: String, correlationId: String, operationKey: String?): PluginProjection
    suspend fun removePlugin(pluginId: String, correlationId: String, operationKey: String?): PluginProjection
    suspend fun getPlugin(pluginId: String): PluginProjection
    suspend fun listPlugins(filter: PluginFilter, page: PageRequest): Page<PluginProjection>
}
```

## Plugin Manifest

The manifest is a normative contract artifact and MUST declare:

- `pluginId`
- `version`
- compatibility range
- required permissions
- exported capabilities by type (`agents`, `tools`, `providers`, `skills`)
- dependency list and minimum versions
- signature/integrity metadata

Free-form manifest blobs are not sufficient for compatibility checking.

## Lifecycle

Activation MUST be transactional across capability registration. If any exported capability fails registration, the plugin returns to the prior durable state and no partial registration remains visible.

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| installPlugin | NXR-5001, NXR-5002, NXR-5003, NXR-5004 |
| activatePlugin | NXR-5005, NXR-5006, NXR-5007 |
| deactivatePlugin / removePlugin | NXR-5008, NXR-5009, NXR-7007 |
| getPlugin / listPlugins | NXR-5001, NXR-7001 |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for canonical envelope requirements.
