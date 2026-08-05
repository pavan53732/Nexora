> **Status: DERIVED** for Plugin API.
> This document describes the API surface for the Plugin System. Canonical behavior is defined in the owning state-machine (`state-machines/PluginLifecycle.md`) and architecture (`architecture/PLUGIN_SYSTEM.md`) documents.
>
> Depends on: the canonical architecture document for Plugin System (`architecture/PLUGIN_SYSTEM.md`).
> Referenced by: upstream architecture, models, protocols, and registries.

# Plugin API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/PLUGIN_SYSTEM.md](../../architecture/PLUGIN_SYSTEM.md)

---

## Normative Operation Contract

The Plugin API governs plugin packaging, installation, cryptographic integrity verification, activation, deactivation, and rollback. Activation is transactional: a failure to register any exported capability (tool, provider, agent, or skill) MUST trigger a complete rollback of the activation pass to ensure no partial registrations leak.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `installPlugin` | Plugin `Discovered → Downloading → Installed` | Stable plugin projection with signature details | Extract failed (`NXR-6001`), verification failed (`NXR-6002`), invalid signature (`NXR-6009`) | Safe (Idempotent) | Signature and checksum verified against Release Key before extraction; deletes temp files on fail | Registry and cryptographic verification tests |
| `activatePlugin` | Plugin `Installed → Activating → Active` | Projection and list of exported capabilities | Load failed (`NXR-6003`), missing dependency (`NXR-6007`), incompatible SDK (`NXR-6005`) | Safe to retry | Restricts classloader to private namespaces; rolls back cleanly if duplicate capability exists | Transactional registration and lifecycle tests |
| `deactivatePlugin`| Plugin `Active → Deactivating → Inactive` | Projection in `Inactive` state | Teardown exception, reference leak | Safe (Idempotent) | Unregisters all exported capabilities; terminates active sandboxes for plugin tools | Lifecycle and teardown tests |
| `uninstallPlugin` | Plugin `Installed/Inactive → Uninstalling → Uninstalled` | Uninstalled confirmation projection | Delete failed (`NXR-6006`), plugin active | Safe (Idempotent) | Purges all plugin files from storage; cannot uninstall while active or in-use | Cleanup and file purging tests |

Every response and emitted event MUST propagate a `correlationId`.

## Contract Shapes

### Install Request

```kotlin
data class InstallPluginRequest(
    val correlationId: String,
    val sourceUri: String,
    val checksumSha256: String,
    val expectedSignatureAuthor: String? = null
)
```

### Plugin Activation Output

```kotlin
data class ActivationOutput(
    val pluginId: String,
    val version: String,
    val status: PluginStatus,
    val activePermissions: List<String>,
    val registeredTools: List<String>,
    val registeredProviders: List<String>,
    val registeredAgents: List<String>,
    val registeredSkills: List<String>
)
```

### Plugin API Interface

```kotlin
package com.nexora.app.runtime.plugin

interface PluginApi {
    suspend fun installPlugin(request: InstallPluginRequest): PluginProjection
    suspend fun activatePlugin(pluginId: String, correlationId: String): ActivationOutput
    suspend fun deactivatePlugin(pluginId: String, correlationId: String): PluginProjection
    suspend fun uninstallPlugin(pluginId: String, correlationId: String): Boolean
    suspend fun listPlugins(): List<PluginProjection>
}
```

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes | Recovery & Lifecycle Effects |
|---|---|---|
| `installPlugin` | `NXR-6001` (Install Failed) | Clean up temp files; state remains `Discovered`. |
| | `NXR-6002` (Verification Failed) | Reject installation; alert user of integrity mismatch. |
| | `NXR-6009` (Signing Invalid) | Block classloader integration; raise security warning. |
| `activatePlugin` | `NXR-6003` (Load Failed) | Fail activation; roll back state to `Installed`. |
| | `NXR-6005` (Incompatible) | Reject activation; notify user to upgrade Nexora runtime. |
| | `NXR-6007` (Dependency Missing) | Prompt user to install required dependencies. |
| `deactivatePlugin`| `NXR-6008` (Sandbox Violation) | Kill classloader; force disable plugin. |
