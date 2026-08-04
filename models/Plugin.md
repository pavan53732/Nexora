> **Status: DERIVED** for Plugin entity shape.
> This document defines the data model for Plugin. The explicit lifecycle/behavior authority is [state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md).
>
> Depends on: the canonical architecture and lifecycle sources for Plugin.
> Referenced by: APIs, SDKs, protocols, and tests that consume Plugin.


# Domain Model: Plugin

> Canonical domain model. See [architecture/PLUGIN_SYSTEM.md](../architecture/PLUGIN_SYSTEM.md).

```kotlin
package com.nexora.app.runtime.plugins

data class Plugin(
    val id: String,
    val name: String,
    val version: String,
    val description: String,
    val status: PluginStatus,
    val requiredPermissions: List<PermissionScope>,
    val minAppVersion: String,
    val dependencies: List<String>,
    val installedAt: Instant,
    val lastActiveAt: Instant
)

enum class PluginStatus { INSTALLED, ACTIVE, DISABLED, ERROR }
```
