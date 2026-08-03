# Core Runtime — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [AGENT_RUNTIME.md](AGENT_RUNTIME.md) | [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md)

---

## Overview

The Core Runtime is the brain of Nexora. It orchestrates all agent activity, from receiving a user goal to producing a result. It consists of 15 tightly coordinated modules.

## Module Inventory

| Module | Responsibility | Kotlin Package |
--------|---------------|----------------|
| **Planner** | Decomposes goals into tasks, creates execution plans with dependencies. | `com.nexora.app.runtime.planner` |
| **Executor** | Executes planned tasks sequentially or in parallel, manages execution state. | `com.nexora.app.runtime.executor` |
| **Workflow Engine** | Orchestrates multi-step workflows, handles branching, looping, and error recovery. | `com.nexora.app.runtime.workflow` |
| **Tool Manager** | Discovers, registers, and invokes tools. Routes tool calls to the correct handler. | `com.nexora.app.runtime.tools` |
| **Context Builder** | Assembles context for AI calls: system prompt, conversation history, file contents, memory. | `com.nexora.app.runtime.context` |
| **Memory Manager** | Reads/writes to all memory stores. Manages recall and relevance scoring. | `com.nexora.app.runtime.memory` |
| **Permission Manager** | Enforces tool permission policies. Prompts user for approval when required. | `com.nexora.app.runtime.permissions` |
| **Plugin Manager** | Loads, validates, sandboxes, and manages plugin lifecycles. | `com.nexora.app.runtime.plugins` |
| **Scheduler** | Schedules deferred, recurring, and background tasks. | `com.nexora.app.runtime.scheduler` |
| **Event Bus** | Central publish/subscribe system for inter-module communication. | `com.nexora.app.runtime.events` |
| **Observability** | Collects metrics, traces, and logs for every runtime operation. | `com.nexora.app.runtime.observability` |
| **Security Policies** | Enforces sandbox boundaries, resource limits, and access controls. | `com.nexora.app.runtime.security` |
| **Background Runtime** | Manages long-running agent execution in Android foreground services. | `com.nexora.app.runtime.background` |
| **Resource Manager** | Tracks and limits CPU, memory, disk, and network usage per agent/workspace. | `com.nexora.app.runtime.resources` |
| **Agent Manager** | Creates, configures, and manages multiple agent instances. | `com.nexora.app.runtime.agents` |

> **Background execution** — task queue, scheduled jobs, resumable execution,
> notifications, progress updates, checkpoint recovery, and Android platform rules
> are specified in [specs/BACKGROUND_EXECUTION.md](../specs/BACKGROUND_EXECUTION.md).

## Core Interfaces

### Task

```kotlin
data class Task(
    val id: String,
    val workspaceId: String,
    val agentId: String,
    val parentTaskId: String?,
    val description: String,
    val status: TaskStatus,  // PENDING, PLANNING, EXECUTING, BLOCKED, COMPLETED, FAILED, CANCELLED
    val plan: ExecutionPlan?,
    val createdAt: Instant,
    val updatedAt: Instant
)
```

### ExecutionPlan

```kotlin
data class ExecutionPlan(
    val steps: List<PlanStep>,
    val dependencies: Map<String, List<String>>  // stepId -> dependsOn stepIds
)

data class PlanStep(
    val id: String,
    val description: String,
    val toolCalls: List<ToolCall>,
    val dependsOn: List<String>,
    val status: StepStatus  // PENDING, RUNNING, COMPLETED, FAILED, SKIPPED
)
```

### Event Bus

```kotlin
interface EventBus {
    fun publish(event: NexoraEvent)
    fun subscribe(eventType: KClass<out NexoraEvent>, handler: (NexoraEvent) -> Unit)
    fun unsubscribe(eventType: KClass<out NexoraEvent>, handler: (NexoraEvent) -> Unit)
}

sealed class NexoraEvent {
    val timestamp: Instant = Clock.System.now()
    abstract val workspaceId: String
}
```

## Execution Flow

```
User Goal (from Chat inside Workspace)
    |
    v
Planner ---decompose---> ExecutionPlan
    |
    v
Context Builder ---assemble---> AI Request (system + history + files + memory)
    |
    v
AI Provider ---complete---> AI Response (text + tool_calls)
    |
    v
Tool Manager ---route---> Tool Execution
    |
    v
Permission Manager ---check---> Approved/Denied
    |
    v
Executor ---execute in sandbox---> Tool Result
    |
    v
Memory Manager ---store---> Persisted
    |
    v
Event Bus ---publish---> All subscribers notified
    |
    v
Loop back to Planner (reflect and plan next step)
```

## Background Execution

Long-running tasks use Android's **Foreground Service** to survive app minimization.

```kotlin
class AgentExecutionService : LifecycleService() {
    // Keeps agent alive when app is backgrounded
    // Shows persistent notification with task progress
    // Restores state on service restart
}
```

## Checkpoint System

Agent state is periodically saved for crash recovery.

```kotlin
data class AgentCheckpoint(
    val taskId: String,
    val plan: ExecutionPlan,
    val currentStepIndex: Int,
    val memorySnapshot: Map<String, Any>,
    val timestamp: Instant
)
```

## Phase Mapping

- **Phase 1**: Define interfaces only (Task, ExecutionPlan, EventBus, NexoraEvent).
- **Phase 2**: Implement Planner, Executor, Context Builder, Event Bus, Token Budget Manager.
- **Phase 3+**: Wire Sandbox, Tools, Memory, Plugins into the runtime.