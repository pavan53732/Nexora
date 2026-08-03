# Runtime API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/RUNTIME.md](../../architecture/RUNTIME.md)

---

## Overview

The Runtime API is the central coordination point. It connects the planner, executor, tool manager, and provider system into the agent loop.

## Core API

```kotlin
package com.nexora.app.runtime

/**
 * Main entry point for executing agent tasks.
 */
interface NexoraRuntime {
    // Execute a goal within a workspace
    suspend fun execute(goal: String, workspaceId: String): Task

    // Cancel a running task
    suspend fun cancel(taskId: String)

    // Get task status
    suspend fun getTaskStatus(taskId: String): Task

    // List running tasks
    suspend fun getRunningTasks(workspaceId: String): List<Task>

    // Get execution history
    suspend fun getHistory(workspaceId: String, limit: Int): List<ExecutionEvent>
}
```

## Event Bus API

```kotlin
interface EventBus {
    fun publish(event: NexoraEvent)
    fun subscribe(eventType: KClass<out NexoraEvent>, handler: (NexoraEvent) -> Unit)
    fun unsubscribe(eventType: KClass<out NexoraEvent>, handler: (NexoraEvent) -> Unit)
}

// Usage
eventBus.subscribe(TaskProgress::class) { event ->
    updateUI(event)
}
```

## Background Service API

```kotlin
/**
 * Android Foreground Service for long-running agent execution.
 * Survives app minimize and device restart.
 */
class AgentExecutionService : LifecycleService() {
    fun startTask(taskId: String, goal: String, workspaceId: String)
    fun cancelTask(taskId: String)
    fun getActiveTasks(): List<String>
}
```
