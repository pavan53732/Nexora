> **Status: DERIVED** for Tool entity shape.
> This document defines the data model for Tool. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Tool.
> Referenced by: APIs, SDKs, protocols, and tests that consume Tool.


# Domain Model: Tool

> Canonical domain model. See [architecture/TOOL_SYSTEM.md](../architecture/TOOL_SYSTEM.md).

```kotlin
package com.nexora.app.runtime.tools

data class ToolCall(
    val id: String,
    val toolId: String,
    val parameters: JsonObject,
    val status: ToolCallStatus,
    val result: ToolResult?,
    val durationMs: Long?,
    val timestamp: Instant
)

enum class ToolCallStatus { PENDING, APPROVED, EXECUTING, COMPLETED, DENIED, ERROR }
```
