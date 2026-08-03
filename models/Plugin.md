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
    val permissions: List<PermissionScope>,
    val dependencies: List<String>,
    val installedAt: Instant,
    val lastActiveAt: Instant
)

enum class PluginStatus { INSTALLED, ACTIVE, DISABLED, ERROR }
```
