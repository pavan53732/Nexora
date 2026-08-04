> **Status: DERIVED** for Tool-API API.
> This document describes the api surface for Tool-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Tool-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Tool API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/TOOL_SYSTEM.md](../../architecture/TOOL_SYSTEM.md)

---

## Normative Operation Contract

The operations below define the **wire-level contract boundary** for tool discovery, registration, and invocation. They are not merely Kotlin convenience methods. Implementations MUST preserve lifecycle, authorization, event ordering, error-envelope, retry, cancellation, redaction, and idempotency semantics. Transport-specific names MAY differ only when the mapping is documented, lossless, and test-covered.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `registerTool` | Tool `Discovered → Registered` | Durable tool projection with version | Duplicate ID, invalid manifest/schema, incompatible SDK/version, permission failure, storage failure | Duplicate `(toolId, version)` is idempotent and returns committed projection | Registration MUST validate ownership, permissions, and declared capabilities before visibility | Registry and SDK conformance tests |
| `getTool` / `listTools` | No lifecycle change | Stable projection(s), filter metadata, pagination cursor | Not found, invalid filter, unauthorized, storage failure | Safe to retry; reads are side-effect free and versioned | Results MUST redact hidden/internal capabilities based on caller scope | API contract tests |
| `invoke` | ToolCall `Pending → Approved/Denied → Executing → Completed/Error` | Tool result envelope, ordered events, correlation ID | Permission denied, approval required, timeout, cancellation, invalid parameters, sandbox/provider failure | Client retries require idempotency key for side-effecting tools; duplicate key MUST return original committed outcome | Authorization, permission, sandbox, and policy checks MUST occur before side effects; cancellation releases resources and emits terminal event after commit | Protocol, security, and integration tests |
| `cancelToolCall` | Active ToolCall → `Cancelled` | Committed cancellation projection | Not found, already terminal, conflict, cleanup failure | Idempotent for same `toolCallId` and cancellation key | Caller MUST own workspace or delegated execution scope; cancellation propagates to child processes/resources | Lifecycle and cancellation tests |

Every request and every emitted event MUST include `correlationId`. Side-effecting requests MUST include `idempotencyKey`. Durable state MUST commit before lifecycle events are published. Duplicate events MUST be deduplicated by `(entityId, version, transition)`. Errors MUST preserve canonical envelope fields from [ERROR_CODES.md](../../errors/ERROR_CODES.md): `code`, `category`, `retryability`, `idempotency`, `lifecycleEffect`, `recoveryOwner`, and redacted `details`.

## Contract Shapes

The following envelope fields are **normative across transports**. JSON, protobuf, IPC, or in-process adapters MAY rename fields only when the mapping is exact, documented, and reversible.

### Request Envelope

```kotlin
data class ToolInvokeRequest(
    val requestId: String,
    val correlationId: String,
    val idempotencyKey: String?,
    val workspaceId: String,
    val agentId: String?,
    val taskId: String?,
    val toolCallId: String,
    val toolId: String,
    val toolVersion: String?,
    val input: JsonObject,
    val caller: CallerRef,
    val approvals: List<ApprovalRef> = emptyList(),
    val timeoutMs: Long?,
    val resumeToken: String? = null,
    val metadata: Map<String, String> = emptyMap()
)
```

### Response Envelope

```kotlin
data class ToolInvokeResponse(
    val correlationId: String,
    val toolCallId: String,
    val status: ToolCallStatus,
    val version: Long,
    val startedAt: Instant?,
    val completedAt: Instant?,
    val output: JsonObject?,
    val artifacts: List<ArtifactRef> = emptyList(),
    val usage: ToolUsage?,
    val approvalsRequired: List<ApprovalRequirement> = emptyList(),
    val error: CanonicalErrorEnvelope? = null,
    val nextPageCursor: String? = null,
    val resumeToken: String? = null
)
```

### Event Envelope

```kotlin
data class ToolEvent(
    val eventId: String,
    val correlationId: String,
    val entityId: String,
    val entityType: String,
    val transition: String,
    val version: Long,
    val publishedAt: Instant,
    val workspaceId: String,
    val taskId: String?,
    val toolCallId: String,
    val payload: JsonObject,
    val terminal: Boolean
)
```

### Required Rules

- `requestId` identifies the transport request; `correlationId` groups all work spawned by the same logical operation.
- `toolCallId` is client- or runtime-generated and stable across retries.
- `version` is a monotonically increasing durable entity version used for deduplication and optimistic reads.
- `resumeToken` is REQUIRED for resumable streams or long-running invocations and MUST be opaque to clients.
- Pagination MUST use opaque cursors rather than offset-based scanning for registry reads.

## Overview

The Tool API defines how tools are discovered, registered, invoked, cancelled, and how results, artifacts, approvals, and events are returned. Every tool in Nexora implements this contract either directly or through an adapter.

## Core Interface

```kotlin
package com.nexora.app.runtime.tools

interface Tool {
    val id: String
    val name: String
    val description: String
    val category: ToolCategory
    val parameters: JsonSchema
    val requiredPermissions: List<PermissionScope>
    val timeout: Duration
    val requiresSandbox: Boolean
    val supportsStreaming: Boolean
    val supportsCancellation: Boolean
    val isIdempotent: Boolean
    val version: String

    suspend fun execute(request: ToolInvokeRequest, context: ToolContext): ToolInvokeResponse
}

enum class ToolCategory {
    FILE_SYSTEM, WORKSPACE, CODE_INTELLIGENCE, SEARCH, TERMINAL,
    GIT, PACKAGE_MANAGER, BUILD, TEST, DEBUGGING, FORMATTING,
    DOCUMENTATION, BROWSER, NETWORK, DATABASE, MEMORY, AI,
    ANDROID_DEVICE, PROJECT_MANAGEMENT, SECURITY, OBSERVABILITY,
    IMPORT_EXPORT, PLUGIN_SYSTEM, MULTI_AGENT, WORKFLOW, SKILLS
}
```

## Request/Response Context

```kotlin
data class ToolContext(
    val workspaceId: String,
    val sandbox: Sandbox,
    val memoryManager: MemoryManager,
    val eventBus: EventBus,
    val logger: StructuredLogger,
    val cancellation: CancellationToken,
    val clock: Clock
)
```

`Map<String, Any>`, free-form strings, or transport-specific exception types MUST NOT be treated as the normative contract shape. Generated SDKs and adapters SHOULD derive from a machine-readable schema source (OpenAPI, JSON Schema, or protobuf) that preserves these envelope semantics.

## Registration API

```kotlin
interface ToolRegistryApi {
    suspend fun registerTool(tool: ToolDescriptor, context: RegistryContext): ToolProjection
    suspend fun getTool(toolId: String, version: String? = null): ToolProjection
    suspend fun listTools(filter: ToolFilter, page: PageRequest): Page<ToolProjection>
}
```

Built-in tools register at runtime startup. Plugin tools register only after plugin verification and activation succeed. Stable IDs are governed by [registry/TOOLS.md](../../registry/TOOLS.md).

## Ownership Boundaries

This specification covers tool registration, discovery, invocation, and tool-call lifecycle only.

- Agent planning, task ownership, and delegation semantics belong to [Agent-API.md](./Agent-API.md).
- Provider completion and streaming semantics belong to [Provider-API.md](./Provider-API.md).
- Plugin package verification and activation semantics belong to [Plugin-API.md](./Plugin-API.md).
- Runtime orchestration, background work, and global event bus guarantees belong to [Runtime-API.md](./Runtime-API.md).

Cross-domain behavior MUST be referenced, not redefined, to avoid contract drift.

## Canonical Error Mapping

The following mapping is normative. Adapters MUST preserve these codes and the canonical error-envelope fields; message text MUST NOT be used as a compatibility key.

| Operation | Canonical `NXR-*` codes |
|---|---|
| registerTool | NXR-5001, NXR-5002, NXR-5004, NXR-5007 |
| getTool / listTools | NXR-2001, NXR-7001 |
| invoke | NXR-2001, NXR-2002, NXR-2003, NXR-2004, NXR-2005, NXR-2009 |
| cancelToolCall | NXR-2010, NXR-7007 |
| result/cleanup | NXR-2008, NXR-7007 |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for identity, retryability, idempotency, lifecycle effect, recovery owner, and redaction requirements.
