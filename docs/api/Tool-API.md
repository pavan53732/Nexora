# Tool API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/TOOL_SYSTEM.md](../architecture/TOOL_SYSTEM.md)

---

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
    IMPORT_EXPORT, PLUGIN_SYSTEM, MULTI_AGENT, WORKFLOW
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
