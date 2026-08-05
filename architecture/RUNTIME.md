# Core Runtime Architecture — Nexora

> **Status: CANONICAL** for system-wide runtime service composition and boundaries.
> This document owns how runtime services are composed and coordinated. It does NOT
> own the internal autonomous agent loop (see [AGENT_RUNTIME.md](AGENT_RUNTIME.md)),
> multi-agent coordination algorithm (see [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)),
> or workflow state machine progression (see [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md)).
>
> Depends on: [state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md) (task states).
> Referenced by: AGENT_RUNTIME.md, MULTI_AGENT_SYSTEM.md, WORKFLOW_ENGINE.md.

---

## Overview

The Core Runtime is the composition layer of Nexora. It coordinates runtime services
(agent loop, multi-agent coordinator, workflow engine, tool manager, memory system,
provider router) and manages their lifecycle, but it does NOT implement the internal
logic of any subsystem. Service boundaries:

| Service | Owned By | Runtime Role |
|---------|----------|--------------|
| Agent loop (plan→execute→reflect) | [AGENT_RUNTIME.md](AGENT_RUNTIME.md) | Runtime starts/stops the loop service |
| Multi-agent coordination | [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) | Runtime provides the coordinator service reference |
| Workflow state progression | [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md) | Runtime invokes workflow engine for graph execution |
| Tool execution | [TOOL_SYSTEM.md](TOOL_SYSTEM.md) | Runtime routes tool calls through ToolManager |
| Memory/context | [MEMORY_SYSTEM.md](MEMORY_SYSTEM.md) | Runtime requests memory services |
| Provider routing | [PROVIDER_SYSTEM.md](PROVIDER_SYSTEM.md) | Runtime holds the provider registry |

It consists of 17 tightly coordinated modules.

## Module Inventory

| Module | Responsibility | Kotlin Package |
--------|---------------|----------------|
| **Planner** | Decomposes goals into tasks, creates execution plans with dependencies. | `com.nexora.app.runtime.planner` |
| **Executor** | Executes planned tasks sequentially or in parallel, manages execution state. | `com.nexora.app.runtime.executor` |
| **Workflow Engine** | Manages workflow graph state and step progression. Delegates step execution to the Executor. | `com.nexora.app.runtime.workflow` |
| **Tool Manager** | Discovers, registers, and invokes tools. Routes tool calls to the correct handler. | `com.nexora.app.runtime.tools` |
| **Context Builder** | Assembles context for AI calls: system prompt, conversation history, file contents, memory. | `com.nexora.app.runtime.context` |
| **Memory Manager** | Reads/writes to all memory stores. Manages recall and relevance scoring. | `com.nexora.app.runtime.memory` |
| **Permission Manager** | Enforces tool permission policies. Prompts user for approval when required. | `com.nexora.app.runtime.permissions` |
| **Plugin Manager** | Loads, validates, sandboxes, and manages plugin lifecycles. | `com.nexora.app.runtime.plugins` |
| **Scheduler** | Schedules deferred, recurring, and background tasks. | `com.nexora.app.runtime.scheduler` |
| **Event Bus** | Central publish/subscribe system for inter-module communication. | `com.nexora.app.runtime.events` |
| **Observability** | Collects metrics, traces, and logs for every runtime operation. | `com.nexora.app.runtime.observability` |
| **Security Manager** | Enforces sandbox boundaries, resource limits, and access controls. | `com.nexora.app.runtime.security` |
| **Background Runtime** | Manages long-running agent execution via Android foreground services. Behavior defined in [specs/BACKGROUND_EXECUTION.md](../specs/BACKGROUND_EXECUTION.md). | `com.nexora.app.runtime.background` |
| **Resource Manager** | Tracks and limits CPU, memory, disk, and network usage per agent/workspace. | `com.nexora.app.runtime.resources` |
| **Agent Manager** | Creates, configures, and manages multiple agent instances. | `com.nexora.app.runtime.agents` |
| **Skill Registry** | Maintains the skill catalog, agent–skill bindings, and skill→tool mappings; supports skill acquisition (ADR-0007). | `com.nexora.app.runtime.skills` |
| **Evidence & Validation Engine** | Owns anti-hallucination mechanics as a runtime policy, not a prompt: evidence collection, source attribution, statement classification (verified/derived/estimated/unknown/user-provided), confidence scoring, assumption detection, plan validation, output verification, self-review, completion validation, audit logging (RG/RB rules, FR-EV). | `com.nexora.app.runtime.evidence` |

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
    val correlationId: String,
    val parentTaskId: String?,
    val status: TaskStatus,
    val phase: ExecutionPhase,
    val priority: TaskPriority = TaskPriority.NORMAL,
    val version: Long,
    val goal: String,
    val input: JsonObject,
    val output: JsonObject?,
    val childTaskIds: List<String>,
    val delegatedAgentIds: List<String>,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null,
    val latestError: CanonicalErrorEnvelope? = null
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