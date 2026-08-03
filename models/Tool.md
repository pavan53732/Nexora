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

enum class ToolCallStatus { PENDING, APPROVED, executing, COMPLETED, DENIED, ERROR }
```
