> **Status: DERIVED** for PluginSDK SDK.
> This document describes the sdk surface for PluginSDK. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for PluginSDK.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Plugin SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

> **Testing:** Plugin tests: [testing/UnitTests.md](../testing/UnitTests.md) (Plugin section), [testing/IntegrationTests.md](../testing/IntegrationTests.md) (plugin loading).

---

## Overview

The Plugin SDK enables developers to create plugins that extend Nexora. Plugins can register tools, agents, providers, and UI screens.

## Plugin Structure

```
my-plugin/
├── plugin.json          # Manifest
├── build.gradle.kts     # Build config (depends on nexora-plugin-api)
└── src/
    └── main/kotlin/
        └── MyPlugin.kt   # Plugin implementation
```

## Plugin Manifest

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "minAppVersion": "0.1.0",
  "permissions": ["sandbox:read", "sandbox:write"],
  "dependencies": [],
  "registers": {
    "tools": ["my_tool_1", "my_tool_2"],
    "agents": [],
    "providers": [],
    "screens": []
  }
}
```

## Plugin Implementation

```kotlin
class MyPlugin : NexoraPlugin {
    override val id = "my-plugin"
    override val name = "My Plugin"
    override val version = "1.0.0"
    override val description = "A custom plugin."
    override val requiredPermissions = listOf(PermissionScope.SANDBOX_READ)
    override val dependencies = emptyList()
    override val minAppVersion = "0.1.0"

    override fun onActivate(context: PluginContext) {
        context.toolRegistry.register(MyTool1())
        context.toolRegistry.register(MyTool2())
    }

    override fun onDeactivate(context: PluginContext) {
        context.toolRegistry.unregister("my_tool_1")
        context.toolRegistry.unregister("my_tool_2")
    }

    override fun onInstall(context: PluginContext) {}
    override fun onUninstall(context: PluginContext) {}
}
```

## Distribution

Plugins are distributed as `.nexora-plugin` files (ZIP archives with the manifest and compiled code).

See [docs/api/Plugin-API.md](../docs/api/Plugin-API.md) for the full Plugin API reference.
