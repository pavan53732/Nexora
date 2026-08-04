> **Status: DERIVED** for Plugin-API API.
> This document describes the api surface for Plugin-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Plugin-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Plugin API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/PLUGIN_SYSTEM.md](../../architecture/PLUGIN_SYSTEM.md)

---

## Normative Operation Contract

The operation below is a contract boundary, not merely a Kotlin convenience method. Implementations MUST preserve the lifecycle, event, error, security, retry, cancellation, and idempotency semantics shown here. Transport-specific names MAY differ only when the mapping is documented and lossless.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `execute` / `startTask` | Task `Draft/Pending → Queued → Running`; Agent `Ready → Running` | Task projection plus correlation ID | Invalid input, unavailable agent/provider, permission/approval, timeout, cancellation, internal fault; use `NXR-*` envelope | Client retries require idempotency key; duplicate key returns original task; execution retry is lifecycle-controlled | Workspace authorization and tool policy checked before side effects; cancellation emits lifecycle event and performs cleanup | Runtime integration and end-to-end tests |
| `cancel` / `cancelTask` | Active task/agent → `Cancelled` | Committed cancellation projection | Not found, already terminal, conflict, cleanup failure | Idempotent for same task and cancellation key; repeated request returns committed result | Caller must own workspace/task; cancellation propagates to child jobs and sandbox operations | Lifecycle and cancellation tests |
| `getTaskStatus` | No lifecycle change | Durable status, execution phase, version, latest error | Not found, unauthorized, storage failure | Safe to retry; read is versioned | Redact sensitive error details according to caller scope | API contract tests |
| `invoke` | ToolCall `Pending → Approved/Denied → Executing → Completed/Error` | Tool result, event sequence, correlation ID | Permission denied, approval required, timeout, cancellation, invalid parameters, sandbox/provider failure | Re-execution requires tool idempotency declaration; duplicate call key MUST NOT repeat non-idempotent effects | Permission and sandbox checks precede execution; cancellation releases resources | Tool protocol and security tests |
| `complete` / `stream` | Provider remains lifecycle-authorized; request execution gets committed result or canonical failure | Completion response or ordered stream with terminal marker | Provider unavailable, rate limit, timeout, invalid request, capability mismatch | Retry follows error envelope; non-idempotent external effects require key; stream reconnect must declare resume policy | Provider credentials never cross boundary; cancellation closes stream and records outcome | Provider protocol and integration tests |
| `install` / `activate` | Plugin lifecycle follows verification/install/activation transitions | Plugin projection and registered capabilities | Integrity failure, incompatibility, dependency, permission, timeout, cancellation | Install keyed by plugin/version; duplicate operation returns existing result; activation is not repeated after commit | Signature, compatibility, permission, and sandbox checks precede activation; cancellation rolls back partial artifacts | Plugin lifecycle and security tests |

Every operation MUST return or emit a correlation ID. Errors MUST preserve `code`, `category`, `retryability`, `idempotency`, `lifecycleEffect`, `recoveryOwner`, and redacted `details` from [ERROR_CODES.md](../../errors/ERROR_CODES.md). Lifecycle events are published only after durable state commit and are deduplicated by entity plus transition version.

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
