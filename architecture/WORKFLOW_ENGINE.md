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
| **Iterative** | Steps repeated with a bounded iteration count or convergence condition; modeled as a cycle in the step graph with explicit iteration metadata. |
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

    data class Iterative(
        override val id: String,
        override val dependsOn: List<String>,
        val bodySteps: List<String>,  // step IDs forming the loop body
        val maxIterations: Int,
        val convergenceCondition: String?
    ) : WorkflowStep()
}

enum class ErrorStrategy { RETRY, SKIP, ABORT, FALLBACK }
```

## Execution Model

The engine uses a **step dependency graph** that supports bounded cycles for iterative workflows:

1. Topologically sort steps based on dependencies (treating iteration edges specially).
2. Execute independent steps in parallel.
3. Wait for dependencies before executing dependent steps.
4. Apply error strategy on failures.
5. Pause at approval gates.
6. **Iteration control**: `Iterative` steps carry `maxIterations` and optional `convergenceCondition`. The engine increments the counter and re-evaluates downstream readiness only when the convergence condition is met or the iteration limit is reached.
7. **File Write Synchronization (Race Mitigation)**: When independent branches execute in parallel lanes, steps are prohibited from conflicting writes. The engine enforces per-file write locks (matching multi-agent SA-3): if a second parallel step attempts to write to a locked file, it suspends until the lock is released, or is assigned a private workspace overlay copy to be merged at join points.

> **Concurrency cap inheritance:** Parallel lanes inherit the dynamic resource-budgeted cap defined in `MULTI_AGENT_SYSTEM.md` SA-3 (`min(memory_budget/per_agent_est, cpu_cores, configurable_max)`, default 3, high-end 8–16). The Workflow Engine does not enforce the cap directly; it relies on the `ResourceManager` (`RUNTIME.md`) and the Multi-Agent Coordinator (`MULTI_AGENT_SYSTEM.md`) to limit active sub-agent count per workspace.

## Phase Mapping

- **Phase 2**: Basic linear and parallel workflows.
- **Phase 6**: Branching, looping, error recovery.
- **Phase 7**: Multi-agent workflow steps.
- **Phase 8**: Workflow plugins and scheduling.
