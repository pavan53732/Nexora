> **Status: DERIVED** for Tool-API API.
> This document describes the api surface for Tool-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Tool-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Tool API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/TOOL_SYSTEM.md](../../architecture/TOOL_SYSTEM.md)

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

The Tool API defines how tools are discovered, registered, invoked, and how results are returned. Every tool in Nexora implements this API.

## Core Interface

```kotlin
package com.nexora.app.runtime.tools

/**
 * Every capability in Nexora implements this interface.
 * Tools are registered in the ToolRegistry and invoked by the ToolManager.
 */
interface Tool {
    val id: String           // Unique identifier, e.g. "file_read"
    val name: String         // Human-readable name
    val description: String  // Description for AI discovery
    val category: ToolCategory
    val parameters: JsonSchema  // Input parameter schema
    val requiredPermissions: List<PermissionScope>
    val timeout: Duration    // Max execution time
    val requiresSandbox: Boolean  // Must execute in sandbox?
    val version: String

    suspend fun execute(params: JsonObject, context: ToolContext): ToolResult
}

enum class ToolCategory {
    FILE_SYSTEM, WORKSPACE, CODE_INTELLIGENCE, SEARCH, TERMINAL,
    GIT, PACKAGE_MANAGER, BUILD, TEST, DEBUGGING, FORMATTING,
    DOCUMENTATION, BROWSER, NETWORK, DATABASE, MEMORY, AI,
    ANDROID_DEVICE, PROJECT_MANAGEMENT, SECURITY, OBSERVABILITY,
    IMPORT_EXPORT, PLUGIN_SYSTEM, MULTI_AGENT, WORKFLOW, SKILLS
}
```

## Request/Response

```kotlin
data class ToolContext(
    val workspaceId: String,
    val sandbox: Sandbox,
    val memoryManager: MemoryManager,
    val eventBus: EventBus
)

sealed class ToolResult {
    data class Success(
        val output: JsonObject,
        val metadata: ToolMetadata
    ) : ToolResult()

    data class Error(
        val message: String,
        val code: String,
        val recoverable: Boolean
    ) : ToolResult()

    data class NeedsApproval(
        val toolCall: ToolCall,
        val reason: String
    ) : ToolResult()
}

// Example usage by the runtime
toolManager.invoke(
    toolId = "file_read",
    params = jsonObjectOf("path" to "/src/main.kt"),
    context = toolContext
)
```

## Registration API

```kotlin
// Built-in registration (at app startup)
toolRegistry.register(FileReadTool())

// Plugin registration (at plugin activation)
pluginContext.toolRegistry.register(MyCustomTool())
```

See [registry/TOOLS.md](../../registry/TOOLS.md) for the complete tool registry with stable IDs.

## Canonical Error Mapping

The following mapping is normative. Adapters MUST preserve these codes and the canonical error-envelope fields; message text MUST NOT be used as a compatibility key.

| Operation | Canonical `NXR-*` codes |
|---|---|
| invoke | NXR-2001, NXR-2002, NXR-2003, NXR-2004, NXR-2005, NXR-2009 |
| result/cleanup | NXR-2008, NXR-7007 |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for identity, retryability, idempotency, lifecycle effect, recovery owner, and redaction requirements.
