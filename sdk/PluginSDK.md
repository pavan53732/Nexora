# Plugin SDK — Nexora

The Plugin SDK defines the standard packaging structure, entry-point interfaces, and registration utilities for developing third-party extensions in Nexora. Canonical Plugin lifecycle semantics are owned by [../state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md).

---

## SDK Architecture

All Nexora plugins MUST implement the `NexoraPlugin` entry-point interface provided by the SDK. The application's dynamic ClassLoader boundary loads the class marked as the `entry-point` in the plugin manifest and drives its activation.

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
Registration is transactional: partial registration is not a valid durable state. When activation fails, successful compensation and verified cleanup MUST restore the exact prior committed Plugin lifecycle state (`Installed` or `Inactive`, matching the activation origin). Failed or unproven cleanup MUST preserve `Failed`, disable or isolate affected capabilities, and prevent their execution until cleanup is verified. Retry remains governed by the existing retryability rules.

## Security & Permission Model

Plugins operate within strict sandbox boundaries:
- **ClassLoader Isolation**: Plugins are loaded via separate `DexClassLoader` instances. A plugin CANNOT inspect or invoke host classes unless they are explicitly exposed in the SDK package (`com.nexora.app.sdk.*`).
- **Least-Privilege Declarations**: All required security permissions (e.g. `sandbox:read`, `network:http`) MUST be statically declared inside the plugin manifest. Plugin permissions are validated against the applicable user-granted permission profiles at installation time, and activation is blocked when required permissions are unauthorized.

## Errors & Exception Guidelines

Plugin authors MUST catch internal failures and translate them into clean, descriptive SDK outcomes. Leaking native application exceptions or failing to prove activation compensation triggers the `PluginManager` to transition the plugin state to `FAILED`, disable or isolate affected capabilities, and prevent their execution for safety. Successful compensation does not produce `Failed`; it restores the activation-origin prior committed state after cleanup is verified.
