> **Status: CANONICAL** for workflow graph state progression.
> This document owns workflow definition, step sequencing, branching, looping,
> and error recovery within a workflow graph. It does NOT own multi-agent
> delegation (see [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)) or the
> single-agent autonomous loop (see [AGENT_RUNTIME.md](AGENT_RUNTIME.md)).
>
> Depends on: [AGENT_RUNTIME.md](AGENT_RUNTIME.md) (step execution), [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) (multi-agent steps).
> Referenced by: [RUNTIME.md](RUNTIME.md), [docs/api/Runtime-API.md](../docs/api/Runtime-API.md).

# Workflow Engine — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [RUNTIME.md](RUNTIME.md) | [AGENT_RUNTIME.md](AGENT_RUNTIME.md)

---

## Overview

The Workflow Engine manages workflow graph state and progression. It handles step
sequencing, branching, looping, and error recovery within a workflow. Multi-agent
workflow steps are delegated to the Multi-Agent Coordinator (see
[MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)), not implemented by the Workflow
Engine itself.

## Workflow Types

| Type | Description |
|------|-------------|
| **Linear** | Sequential steps executed one after another. |
| **Parallel** | Independent steps executed simultaneously. |
| **Branching** | Steps chosen based on conditions (if/else). |
| **Looping** | Steps repeated until a condition is met. |
| **Error Recovery** | Retry with fallback strategies on failure. |
| **Human-in-the-Loop** | Steps that pause for user approval before continuing. |
| **Multi-Agent Step** | Steps delegated to the Multi-Agent Coordinator for parallel agent execution. |

## Workflow Definition

```kotlin
data class Workflow(
    val id: String,
    val name: String,
    val steps: List<WorkflowStep>,
    val onError: ErrorStrategy = ErrorStrategy.RETRY,
    val maxRetries: Int = 3
)

sealed class WorkflowStep {
    abstract val id: String
    abstract val dependsOn: List<String>

    data class ExecuteTool(
        override val id: String,
        override val dependsOn: List<String>,
        val toolId: String,
        val params: JsonObject
    ) : WorkflowStep()

    data class RunAgent(
        override val id: String,
        override val dependsOn: List<String>,
        val agentType: String,
        val goal: String
    ) : WorkflowStep()

    data class Condition(
        override val id: String,
        override val dependsOn: List<String>,
        val condition: String,
        val ifTrue: List<String>,  // step IDs
        val ifFalse: List<String>  // step IDs
    ) : WorkflowStep()

    data class WaitForApproval(
        override val id: String,
        override val dependsOn: List<String>,
        val message: String
    ) : WorkflowStep()
}

enum class ErrorStrategy { RETRY, SKIP, ABORT, FALLBACK }
```

## Execution Model

The engine uses a **directed acyclic graph (DAG)** for step dependencies:

1. Topologically sort steps based on dependencies.
2. Execute independent steps in parallel.
3. Wait for dependencies before executing dependent steps.
4. Apply error strategy on failures.
5. Pause at approval gates.

## Phase Mapping

- **Phase 2**: Basic linear and parallel workflows.
- **Phase 6**: Branching, looping, error recovery.
- **Phase 7**: Multi-agent workflow steps.
- **Phase 8**: Workflow plugins and scheduling.
