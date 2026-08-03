# Domain Model: Execution

> Canonical domain model. See [architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md).

```kotlin
package com.nexora.app.runtime.models

/**
 * Records a single execution step within a task.
 */
data class ExecutionEvent(
    val id: String,
    val timestamp: Instant,
    val taskId: String,
    val agentId: String,
    val eventType: EventType,
    val data: JsonObject,
    val durationMs: Long?,
    val tokenUsage: TokenUsage?,
    val status: EventStatus
)

enum class EventType {
    TOOL_CALL, AI_RESPONSE, REFLECTION, PLANNING,
    ERROR, PERMISSION_REQUESTED, CHECKPOINT_SAVED
}

enum class EventStatus { SUCCESS, ERROR, CANCELLED }

data class TokenUsage(
    val promptTokens: Int,
    val completionTokens: Int,
    val totalTokens: Int
)
```
