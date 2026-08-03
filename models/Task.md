# Domain Model: Task

> **Status: DERIVED.** This document defines the persisted shape of a Task. The
> `TaskStatus` enum below MUST exactly match the canonical state set defined in
> [state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md). Do not add,
> remove, or rename states here without updating the canonical state machine first.
>
> See also [architecture/RUNTIME.md](../architecture/RUNTIME.md).

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

/**
 * Canonical source: state-machines/TaskLifecycle.md.
 * Do not redefine this enum's members anywhere else in the codebase or docs.
 */
enum class TaskStatus {
    DRAFT, PENDING, QUEUED, RUNNING, BLOCKED,
    WAITING_APPROVAL, COMPLETED, FAILED, CANCELLED, RETRY_PENDING
}
```
