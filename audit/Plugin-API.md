# Plugin API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/PLUGIN_SYSTEM.md](../../architecture/PLUGIN_SYSTEM.md)

---

## Overview

The Plugin API defines how plugins are loaded, registered, and managed. Plugins can register tools, agents, providers, and UI screens.

## Plugin Interface

```kotlin
package com.nexora.app.runtime.plugins

interface NexoraPlugin {
    val id: String
    val name: String
    val version: String
    val description: String
    val requiredPermissions: List<PermissionScope>
    val dependencies: List<String>  // Other plugin IDs
    val minAppVersion: String

    fun onInstall(context: PluginContext)
    fun onActivate(context: PluginContext)
    fun onDeactivate(context: PluginContext)
    fun onUninstall(context: PluginContext)
}

/**
 * PluginContext gives plugins access to Nexora's core systems.
 * Plugins should ONLY interact with the system through this context.
 */
class PluginContext(
    val toolRegistry: ToolRegistry,
    val agentRegistry: AgentRegistry,
    val providerRegistry: ProviderRegistry,
    val sandbox: Sandbox,
    val eventBus: EventBus,
    val memoryManager: MemoryManager
)
```

## Plugin Manifest

Each plugin includes a `plugin.json` manifest:

```json
{
  "id": "nexora-browser",
  "name": "Browser Automation",
  "version": "1.0.0",
  "minAppVersion": "0.1.0",
  "permissions": ["network:http", "sandbox:execute"],
  "dependencies": [],
  "registers": {
    "tools": ["browser_navigate", "browser_screenshot", "browser_extract"],
    "agents": [],
    "providers": [],
    "screens": []
  }
}
```

## Lifecycle

1. **Install** — Download, validate manifest, check permissions, store.
2. **Load** — Instantiate plugin class, call `onInstall()`.
3. **Activate** — Call `onActivate()`. Plugin registers its capabilities.
4. **Use** — Registered capabilities available to the runtime.
5. **Deactivate** — Call `onDeactivate()`. Unregister capabilities.
6. **Uninstall** — Call `onUninstall()`. Delete plugin data.

See [sdk/PluginSDK.md](../../sdk/PluginSDK.md) for the full plugin development guide.
