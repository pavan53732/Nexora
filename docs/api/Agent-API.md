> **Status: DERIVED** for Agent-API API.
> This document describes the api surface for Agent-API. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Agent-API.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Agent API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/AGENT_RUNTIME.md](../../architecture/AGENT_RUNTIME.md)

---

## Overview

The Agent API defines how agents are created, configured, and executed. Each agent type (Planner, Coder, etc.) implements this API.

## Agent Interface

```kotlin
package com.nexora.app.runtime.agents

interface Agent {
    val id: String
    val type: AgentType
    val name: String
    val description: String
    val capabilities: List<String>
    val defaultTools: List<String>  // Tool IDs this agent uses by default
    val systemPrompt: String  // Agent-specific system prompt

    suspend fun execute(task: AgentTask, context: AgentContext): AgentResult
}

enum class AgentType {
    PLANNER, RESEARCHER, CODER, REVIEWER, TESTER, DEBUGGER,
    DOCUMENTATION_WRITER, REFACTORING, DEPLOYMENT, SECURITY_AUDITOR,
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR,
    ARCHITECT, CUSTOM  // ARCHITECT = AGT-016; CUSTOM = user-defined agents (not a built-in type)
}

data class AgentContext(
    val workspaceId: String,
    val agentId: String,
    val memoryManager: MemoryManager,
    val eventBus: EventBus,
    val sessionId: String? = null
)

data class AgentTask(
    val id: String,
    val goal: String,
    val workspaceId: String,
    val parentTaskId: String?,
    val assignedAgentType: AgentType,
    val context: Map<String, Any>
)

data class AgentResult(
    val taskId: String,
    val success: Boolean,
    val output: String,
    val artifacts: List<Artifact>,
    val steps: List<AgentStep>
)
```

## Agent Registry API

```kotlin
// Register a built-in agent
agentRegistry.register(PlannerAgent())

// Create an instance for a specific workspace
val planner = agentRegistry.create(
    type = AgentType.PLANNER,
    workspaceId = "ws-001"
)

// Execute a task
val result = planner.execute(task, agentContext)
```

See [registry/AGENTS.md](../../registry/AGENTS.md) for the complete agent registry with stable IDs.
