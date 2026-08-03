# Domain Model: Task

> Canonical domain model. See [architecture/RUNTIME.md](../architecture/RUNTIME.md).

```kotlin
package com.nexora.app.runtime.models

/**
 * A task represents a unit of work assigned to an agent.
 */
data class Task(
    val id: String,                // UUID
    val workspaceId: String,
    val agentId: String,
    val parentTaskId: String?,     // For subtasks
    val goal: String,               // What the task should achieve
    val status: TaskStatus,
    val plan: ExecutionPlan?,
    val result: TaskResult?,
    val error: String?,
    val createdAt: Instant,
    val startedAt: Instant?,
    val completedAt: Instant?,
    val updatedAt: Instant
)

enum class TaskStatus {
    PENDING, PLANNING, EXECUTING, BLOCKED,
    COMPLETED, FAILED, CANCELLED
}
```
