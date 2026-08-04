> **Status: DERIVED** for Permission entity shape.
> This document defines the data model for Permission. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Permission.
> Referenced by: APIs, SDKs, protocols, and tests that consume Permission.


# Domain Model: Permission

> Canonical domain model. See [architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md).

```kotlin
package com.nexora.app.runtime.security

data class PermissionScope(
    val domain: String,    // e.g. "sandbox", "network", "device"
    val action: String     // e.g. "read", "write", "execute", "http"
)

enum class PermissionDecision { ALLOW, ASK, DENY }

// Predefined scopes
val SANDBOX_READ = PermissionScope("sandbox", "read")
val SANDBOX_WRITE = PermissionScope("sandbox", "write")
val SANDBOX_EXECUTE = PermissionScope("sandbox", "execute")
val NETWORK_HTTP = PermissionScope("network", "http")
val NETWORK_WEBSOCKET = PermissionScope("network", "websocket")
val DEVICE_CAMERA = PermissionScope("device", "camera")
val DEVICE_STORAGE = PermissionScope("device", "storage")
val DEVICE_NOTIFICATIONS = PermissionScope("device", "notifications")
val AI_COMPLETE = PermissionScope("ai", "complete")
val AI_EMBED = PermissionScope("ai", "embed")
val MEMORY_READ = PermissionScope("memory", "read")
val MEMORY_WRITE = PermissionScope("memory", "write")
val PLUGIN_INSTALL = PermissionScope("plugin", "install")
val AGENT_CREATE = PermissionScope("agent", "create")
```
