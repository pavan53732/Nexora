# Tool SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

The Tool SDK enables developers to create custom tools that agents can use. Tools are the primary way to extend Nexora's capabilities.

## Creating a Tool

```kotlin
class MyCustomTool : Tool {
    override val id = "my_custom_tool"
    override val name = "My Custom Tool"
    override val description = "Does something useful."
    override val category = ToolCategory.CUSTOM
    override val parameters = JsonSchema.parse("""
        {
            "type": "object",
            "properties": {
                "input": { "type": "string", "description": "The input" }
            },
            "required": ["input"]
        }
    """)
    override val requiredPermissions = listOf(PermissionScope.SANDBOX_READ)
    override val timeout = Duration.seconds(30)
    override val requiresSandbox = false
    override val version = "1.0.0"

    override suspend fun execute(
        params: JsonObject,
        context: ToolContext
    ): ToolResult {
        val input = params["input"].jsonPrimitive.content
        // Do work
        return ToolResult.Success(
            output = jsonObjectOf("result" to "done"),
            metadata = ToolMetadata(durationMs = 42)
        )
    }
}
```

## Registering

In a plugin's `onActivate()`:

```kotlin
context.toolRegistry.register(MyCustomTool())
```

## Tool ID Convention

Format: `{category}_{action}`, e.g. `file_read`, `git_commit`, `http_post`.

See [registry/TOOLS.md](../registry/TOOLS.md) for assigned IDs.
