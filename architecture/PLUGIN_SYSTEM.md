> **Status: CANONICAL** for plugin subsystem architecture and responsibility.
> This document owns how plugins are loaded, sandboxed, and integrated. Plugin
> lifecycle states are defined in [../state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md).
> Plugin identity catalog lives in [../registry/PLUGINS.md](../registry/PLUGINS.md).
>
> Depends on: [../state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md).
> Referenced by: [../registry/PLUGINS.md](../registry/PLUGINS.md), [../sdk/PluginSDK.md](../sdk/PluginSDK.md).

# Plugin System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [TOOL_SYSTEM.md](TOOL_SYSTEM.md)

---

## Overview

Every capability in Nexora should be installable as a plugin. The core runtime is minimal; plugins provide all extended functionality.

## Plugin Architecture

Plugins can register:

- **Tools** — New tool implementations added to the Tool Registry.
- **Agents** — New agent types added to the Agent Registry.
- **AI Providers** — New provider implementations.
- **UI Screens** — Custom screens embedded in the app.
- **Memory Backends** — Alternative memory storage.

## Plugin Interface

```kotlin
interface NexoraPlugin {
    val id: String
    val name: String
    val version: String
    val description: String
    val requiredPermissions: List<PermissionScope>
    val dependencies: List<String>  // Other plugin IDs

    fun onInstall(context: PluginContext)
    fun onActivate(context: PluginContext)
    fun onDeactivate(context: PluginContext)
    fun onUninstall(context: PluginContext)
}

class PluginContext(
    val toolRegistry: ToolRegistry,
    val agentRegistry: AgentRegistry,
    val providerRegistry: ProviderRegistry,
    val sandbox: Sandbox,
    val eventBus: EventBus
)
```

## Plugin Lifecycle

```
Discovery -> Browse marketplace or install from URL/file
    |
    v
Install -> Download, validate, store plugin
    |
    v
Load -> Initialize plugin in isolated context
    |
    v
Register -> Plugin registers its tools, agents, providers
    |
    v
Activate -> Plugin is available for use
    |
    v
Update -> Check for updates, apply seamlessly
    |
    v
Disable/Enable -> User can toggle plugins
    |
    v
Uninstall -> Remove plugin and clean up data
```

## Example Plugins

| Plugin | Registers |
--------|----------|
| **Browser** | Browser tools (open_url, screenshot, extract_page) |
| **Git** | Git tools (clone, commit, push, pull) |
| **Python** | Python runtime extension, pip tools |
| **Node** | Node runtime extension, npm tools |
| **SQLite** | Database tools |
| **OCR** | Image-to-text tool |
| **PDF** | PDF generation and parsing tools |
| **Camera** | Camera access tool |
| **Email** | Email send/receive tools |
| **Calendar** | Calendar integration tools |
| **Maps** | Location and mapping tools |
| **Speech** | TTS and STT tools |
| **Translation** | Multi-language translation tool |
| **Weather** | Weather data tool |

## Phase Mapping

- **Phase 1**: Plugin interface definition, registration system.
- **Phase 8**: Full marketplace, plugin SDK, community plugins.
