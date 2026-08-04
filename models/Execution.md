> **Status: DERIVED** for Execution entity shape.
> This document defines the data model for Execution. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Execution.
> Referenced by: APIs, SDKs, protocols, and tests that consume Execution.


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

## Execution Phase Semantics

`EventType` identifies an immutable execution record; it is not a lifecycle state. Runtime phase is represented by the event stream and current execution projection. Each event MUST preserve task ID, agent ID, correlation ID, sequence/version, phase or event type, status, and canonical error information when applicable.

Execution events are append-only and at-least-once. Consumers MUST deduplicate by execution ID and sequence/version. A checkpoint event is durable only after the referenced checkpoint has been committed.
