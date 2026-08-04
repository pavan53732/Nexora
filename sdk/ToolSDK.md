> **Status: DERIVED** for ToolSDK SDK.
> This document describes the sdk surface for ToolSDK. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for ToolSDK.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Tool SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

> **Testing:** Tool tests: [testing/UnitTests.md](../testing/UnitTests.md) (Tool section), [testing/IntegrationTests.md](../testing/IntegrationTests.md) (tool execution in sandbox).

---

## Normative SDK Contract

The SDK is an adapter over the corresponding API and protocol. SDK convenience methods MUST NOT create a second lifecycle or error vocabulary. Every operation MUST preserve correlation ID, canonical error fields, lifecycle effect, cancellation outcome, and idempotency behavior from the API contract.

| SDK responsibility | Required behavior |
|---|---|
| Request construction | Validate local arguments without changing server-side lifecycle semantics. |
| Result projection | Expose durable status, execution phase, transition version, and correlation ID where the API provides them. |
| Errors | Map canonical `NXR-*` codes to typed SDK errors while preserving the original envelope and redacted details. |
| Retry | Never retry automatically unless the canonical error says retry is safe and the operation is idempotent or keyed. |
| Cancellation | Propagate cancellation to the API/protocol and expose the committed terminal outcome. |
| Events/streams | Preserve ordering metadata and deduplicate at-least-once events; do not infer success from transport closure. |
| Compatibility | SDK version changes MUST document any renamed projection or transport mapping without changing canonical meanings. |

### Required Operation Coverage

The SDK MUST expose or explicitly mark unsupported the operation contracts for agent execution, task cancellation/status, tool invocation, provider completion/streaming, and plugin install/activation. Unsupported operations MUST return a canonical capability error rather than a generic exception.

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
