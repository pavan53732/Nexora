> **Status: DERIVED** for Tool API.
> This document describes the API surface for the Tool System. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Tool System (`architecture/TOOL_SYSTEM.md`).
> Referenced by: upstream architecture, models, protocols, and implementation consumers.

# Tool API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/TOOL_SYSTEM.md](../../architecture/TOOL_SYSTEM.md)

---

## Normative Operation Contract

The Tool API defines the boundaries for registering tools, executing tools in the sandbox, verifying permissions, and enforcing execution constraints. It delegates low-level sandbox execution to the Sandbox module, and credential storage to the Keystore.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `registerTool` | Tool `Discovered → Registered` | Stable validated descriptor | Duplicate ID (`NXR-2006`), invalid schema/risk/scope declaration (`NXR-2005`), storage failure | Safe (Idempotent) | Validates unique known permission IDs and risk level before registry exposure | `SEC-PERM-055/066`, `IT-TOOL-010` |
| `executeTool` | No ToolStatus change; backing terminal may run | Standardized output envelope | Not found (`NXR-2001`), timeout (`NXR-2002`), authorization denied (`NXR-2003`), exception (`NXR-2004`), validation (`NXR-2005`), OOM (`NXR-7004`) | Idempotency key required for retry-sensitive calls | Runs the complete PermissionModel authorization gate before any side effect; preserves denial subreason, toolCallId, and correlationId | `SEC-PERM-001..066`, `IT-TOOL-001..014` |
| `getToolDescriptor`| No lifecycle change | Dynamic tool schema and metadata | Not found (`NXR-2001`) | Safe to retry; side-effect free | Open access; sanitizes internal implementation details | API contract tests |
| `listTools` | No lifecycle change | Paged list of registered tool descriptors | Storage failure, invalid page parameters | Safe to retry; side-effect free | Filters out internal-only tools based on client credentials | API contract tests |

Every tool call MUST include a `correlationId` and `toolCallId`. Long-running tool executions MUST support timeout and cancellation.

## Contract Shapes

### Execute Tool Request

```kotlin
data class ExecuteToolRequest(
    val toolId: String,
    val toolCallId: String,
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val parameters: JsonObject,
    val timeoutMs: Long = 300_000,
    val bypassCache: Boolean = false
)
```

### Tool Output Envelope

```kotlin
data class ToolOutputEnvelope(
    val toolCallId: String,
    val correlationId: String,
    val workspaceId: String,
    val success: Boolean,
    val result: JsonObject?,
    val error: CanonicalErrorEnvelope?,
    val durationMs: Long,
    val isCached: Boolean = false
)
```

### Tool Descriptor

```kotlin
enum class ToolRiskLevel { LOW, MEDIUM, HIGH, CRITICAL }

data class ToolDescriptor(
    val toolId: String,
    val version: String,
    val name: String,
    val description: String,
    val category: String,
    val riskLevel: ToolRiskLevel,
    val parameterSchema: JsonObject,
    val requiredPermissions: List<String>,
    val requiresSandbox: Boolean,
    val supportsStreaming: Boolean,
    val isIdempotent: Boolean
)
```

## Tool API Interface

```kotlin
package com.nexora.app.runtime.tool

interface ToolApi {
    suspend fun registerTool(descriptor: ToolDescriptor): ToolDescriptor
    suspend fun executeTool(request: ExecuteToolRequest): ToolOutputEnvelope
    suspend fun getToolDescriptor(toolId: String): ToolDescriptor
    suspend fun listTools(category: String?, pageRequest: PageRequest): Page<ToolDescriptor>
}
```

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes | Recovery & Lifecycle Effects |
|---|---|---|
| `registerTool` | `NXR-2005` (Invalid descriptor), `NXR-2006` (Not Registered), `NXR-2010` (Incompatible) | Reject registration; state remains `DISCOVERED`; never prompt for descriptor repair. |
| `executeTool` | `NXR-2001` (Not Found) | Reject call; no lifecycle change. |
| | `NXR-2002` (Timeout) | Kill process; return partial outputs; trigger exponential backoff retry. |
| | `NXR-2003` (Authorization Denied) | Enter `WaitingApproval` only for effective `ASK`; unknown, policy, malformed, user, or classifier denial returns without side effects according to the canonical subreason. |
| | `NXR-2004` (Execution Failed) | Log exception; run agent bounded self-correction loop. |
| | `NXR-2005` (Invalid Parameters) | Return schema validation errors back to agent for repair. |
| | `NXR-7004` (OOM) | Terminate sandbox process; transition task status to `FAILED`. |
| `getToolDescriptor`| `NXR-2001` (Not Found) | Safe to retry; no state mutation. |
