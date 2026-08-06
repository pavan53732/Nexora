# Plugin SDK — Nexora

The Plugin SDK defines the standard packaging structure, entry-point interfaces, and registration utilities for developing third-party extensions in Nexora.

---

## SDK Architecture

All Nexora plugins MUST implement the `NexoraPlugin` entry-point interface provided by the SDK. The platform's dynamic ClassLoader boundary loads the class marked as the `entry-point` in the plugin manifest and drives its activation.

```kotlin
package com.nexora.app.sdk.plugin

interface NexoraPlugin {
    /**
     * Called when the plugin is being loaded.
     * Use the registrar to export tools, providers, or agent roles.
     */
    suspend fun onActivate(context: PluginContext, registrar: CapabilityRegistrar)

    /**
     * Called when the plugin is being unloaded.
     * Clean up open sockets, file locks, or background threads.
     */
    suspend fun onDeactivate(context: PluginContext)
}

data class PluginContext(
    val pluginId: String,
    val version: String,
    val storageDirectory: String,
    val minContractVersion: String
)

interface CapabilityRegistrar {
    fun registerTool(descriptor: ToolDescriptor, tool: BaseTool)
    fun registerProvider(descriptor: ProviderDescriptor, adapter: BaseProviderAdapter)
    fun registerAgent(descriptor: AgentDescriptor, factory: BaseAgentFactory)
    fun registerSkill(descriptor: SkillDescriptor, skill: BaseSkill)
    fun registerUiScreen(descriptor: UiScreenDescriptor, screen: BaseUiScreen)
    fun registerMemoryBackend(descriptor: MemoryBackendDescriptor, backend: BaseMemoryBackend)
}
```

Every `register*` call corresponds to one `exported*` field in
[../models/Plugin.md](../models/Plugin.md) and to one capability kind in
[../architecture/PLUGIN_SYSTEM.md](../architecture/PLUGIN_SYSTEM.md) §Plugin Architecture.
Registration is transactional: partial registration is not a valid durable state and
failed activation rolls back to the prior committed plugin state.

## Security & Permission Model

Plugins operate within strict sandbox boundaries:
- **ClassLoader Isolation**: Plugins are loaded via separate `DexClassLoader` instances. A plugin CANNOT inspect or invoke host classes unless they are explicitly exposed in the SDK package (`com.nexora.app.sdk.*`).
- **Least-Privilege Declarations**: All required security permissions (e.g. `sandbox:read`, `network:http`) MUST be statically declared inside the plugin manifest. The platform validates these permissions against user-granted profiles at installation time, blocking activation if unauthorized.

## Errors & Exception Guidelines

Plugin authors MUST catch internal failures and translate them into clean, descriptive SDK outcomes. Leaking native platform exceptions triggers an unhandled crash trap, forcing the `PluginManager` to transition the plugin state to `FAILED`, disable its capabilities, and isolate its classloader for safety.
