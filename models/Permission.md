> **Status: DERIVED** for Permission entity shape.
> This model projects canonical permission semantics from `security/PermissionModel.md`.
> The canonical scope defaults and permission evaluation algorithm are authoritative there.
>
> Depends on: `security/PermissionModel.md` for scope defaults and semantics.
> Referenced by: APIs, SDKs, protocols, and tests that consume Permission.

# Domain Model: Permission

> This model projects canonical permission semantics. See [architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md) for security architecture and [security/PermissionModel.md](../security/PermissionModel.md) for the canonical scope table and evaluation algorithm.
> Canonical scope defaults are authoritative in [security/PermissionModel.md](../security/PermissionModel.md).

```kotlin
package com.nexora.app.runtime.security

data class PermissionScope(
    val id: String,                          // e.g. "sandbox:read", "instance:delegate"
    val domain: String,                      // e.g. "sandbox", "network", "device"
    val action: String,                      // e.g. "read", "write", "execute", "http"
    val defaultDecision: PermissionDecision  // ALLOW, ASK, or DENY
)

enum class PermissionDecision { ALLOW, ASK, DENY }

interface PermissionScopeRegistry {
    /** Resolves a scope by its string ID. Returns null for unknown scopes. */
    fun resolve(scopeId: String): PermissionScope?
}

// Predefined scopes — all 18 canonical scopes
val SANDBOX_READ = PermissionScope("sandbox:read", "sandbox", "read", PermissionDecision.ALLOW)
val SANDBOX_WRITE = PermissionScope("sandbox:write", "sandbox", "write", PermissionDecision.ALLOW)
val SANDBOX_EXECUTE = PermissionScope("sandbox:execute", "sandbox", "execute", PermissionDecision.ALLOW)
val NETWORK_HTTP = PermissionScope("network:http", "network", "http", PermissionDecision.ASK)
val NETWORK_WEBSOCKET = PermissionScope("network:websocket", "network", "websocket", PermissionDecision.ASK)
val DEVICE_CAMERA = PermissionScope("device:camera", "device", "camera", PermissionDecision.DENY)
val DEVICE_STORAGE = PermissionScope("device:storage", "device", "storage", PermissionDecision.DENY)
val DEVICE_NOTIFICATIONS = PermissionScope("device:notifications", "device", "notifications", PermissionDecision.ASK)
val AI_COMPLETE = PermissionScope("ai:complete", "ai", "complete", PermissionDecision.ALLOW)
val AI_EMBED = PermissionScope("ai:embed", "ai", "embed", PermissionDecision.ALLOW)
val MEMORY_READ = PermissionScope("memory:read", "memory", "read", PermissionDecision.ALLOW)
val MEMORY_WRITE = PermissionScope("memory:write", "memory", "write", PermissionDecision.ALLOW)
val PLUGIN_INSTALL = PermissionScope("plugin:install", "plugin", "install", PermissionDecision.ASK)
val AGENT_CREATE = PermissionScope("agent:create", "agent", "create", PermissionDecision.ASK)
val INSTANCE_PAIR = PermissionScope("instance:pair", "instance", "pair", PermissionDecision.ASK)
val INSTANCE_CONNECT = PermissionScope("instance:connect", "instance", "connect", PermissionDecision.ASK)
val INSTANCE_BROADCAST = PermissionScope("instance:broadcast", "instance", "broadcast", PermissionDecision.DENY)
val INSTANCE_DELEGATE = PermissionScope("instance:delegate", "instance", "delegate", PermissionDecision.ASK)
```
