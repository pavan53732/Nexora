> **Status: DERIVED** for Tool domain model.
> This document defines the shape and semantics of Tool in the data model.
>
> Depends on: the canonical architecture document for Tool.
> Referenced by: protocols, APIs, SDKs, registries, and runtime implementations.

# Domain Model: Tool

```kotlin
data class Tool(
    val id: String,
    val version: String,
    val name: String,
    val description: String,
    val category: String,
    val parametersSchemaRef: String,
    val requiredPermissions: List<String>,
    val timeoutMs: Long,
    val requiresSandbox: Boolean,
    val supportsStreaming: Boolean,
    val supportsCancellation: Boolean,
    val isIdempotent: Boolean,
    val status: ToolStatus
)

enum class ToolStatus {
    DISCOVERED,
    REGISTERED,
    ACTIVE,
    DISABLED
}
```

Tool invocation state is tracked separately from the static tool descriptor. Every tool call is correlated by `correlationId` and `toolCallId`, while durable lifecycle deduplication uses committed versioned transitions.
