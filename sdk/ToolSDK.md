# Tool SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [../docs/api/Tool-API.md](../docs/api/Tool-API.md)

---

## Normative SDK Contract

The Tool SDK MUST preserve the contract defined by [Tool-API.md](../docs/api/Tool-API.md). SDK helpers MAY simplify registration or request handling, but they MUST NOT erase required fields such as `correlationId`, `idempotencyKey`, `toolCallId`, canonical error envelopes, pagination cursors, or resume tokens.

### Required Operation Coverage

A conforming SDK implementation MUST provide typed support for:

- tool registration
- tool invocation request/response envelopes
- cancellation
- capability metadata
- approval-required responses
- canonical error-envelope creation and propagation
- event emission metadata
- schema validation hooks

## Overview

The Tool SDK helps authors build tools that remain compliant with the canonical Tool API.

## Creating a Tool

```kotlin
abstract class BaseTool : Tool {
    abstract override val id: String
    abstract override val name: String
    abstract override val description: String
    abstract override val category: ToolCategory
    abstract override val parameters: JsonSchema
    abstract override val requiredPermissions: List<PermissionScope>
    abstract override val timeout: Duration
    abstract override val requiresSandbox: Boolean
    abstract override val supportsStreaming: Boolean
    abstract override val supportsCancellation: Boolean
    abstract override val isIdempotent: Boolean
    abstract override val version: String

    final override suspend fun execute(
        request: ToolInvokeRequest,
        context: ToolContext
    ): ToolInvokeResponse {
        validateEnvelope(request)
        validateSchema(request.input, parameters)
        return executeValidated(request, context)
    }

    protected abstract suspend fun executeValidated(
        request: ToolInvokeRequest,
        context: ToolContext
    ): ToolInvokeResponse
}
```

## Registering

```kotlin
toolRegistry.registerTool(myTool.toDescriptor(), registryContext)
```

## Tool ID Convention

Tool IDs MUST be stable, lowercase, and registry-compatible. SDK helpers MUST reject IDs that would violate [registry/TOOLS.md](../registry/TOOLS.md).

## Compatibility Rules

SDKs MUST expose compatibility metadata for:

- minimum supported API contract version
- supported feature flags, such as streaming or resumable invocation
- manifest/schema version
- declared transport bindings, if any

A tool compiled against the SDK but missing required contract fields is **not** considered conforming.
