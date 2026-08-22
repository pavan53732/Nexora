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
    val riskLevel: ToolRiskLevel,
    val parametersSchemaRef: String,
    val requiredPermissions: List<String>,
    val timeoutMs: Long,
    val requiresSandbox: Boolean,
    val supportsStreaming: Boolean,
    val supportsCancellation: Boolean,
    val isIdempotent: Boolean, // canonical: architecture/TOOL_SYSTEM.md `Tool` interface (FR-AS-007)
    val recoveryContract: ToolRecoveryContract, // existing operation-level recovery declaration
    val cacheTtlMs: Long,
    val configSchemaRef: String?,
    val health: ToolHealth,
    val isFavorite: Boolean,
    val status: ToolStatus,
    val bypassSafeguards: Boolean, // when true, tool invocation bypasses standard provider and safeguard checks
    val allowJailbreakPrompts: Boolean, // when true, allows jailbreak-style prompts for this tool
    val selfGrantPermissions: Boolean // when true, the tool may self-grant required permissions
)

enum class ToolRiskLevel { LOW, MEDIUM, HIGH, CRITICAL }

enum class ToolRecoveryContract {
    IDEMPOTENT_REPLAY,
    STATUS_RECONCILIATION,
    DETERMINISTIC_COMPENSATION,
    BOUNDED_CONTAINMENT
}

enum class ToolHealth { UNKNOWN, HEALTHY, DEGRADED, UNHEALTHY }

enum class ToolStatus {
    DISCOVERED,
    REGISTERED,
    ACTIVE,
    DISABLED
}
```

Tool invocation state is tracked separately from the static tool descriptor. Every tool call is correlated by `correlationId` and `toolCallId`, while durable lifecycle deduplication uses committed versioned transitions.
