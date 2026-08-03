> **Status: CANONICAL** for single-agent autonomous loop behavior.
> This document owns the per-agent execution loop: reflect → plan → build context →
> call provider → parse → execute tools → store results → evaluate → checkpoint.
> It does NOT own multi-agent coordination (see [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)),
> workflow graph progression (see [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md)), or
> system-wide service composition (see [RUNTIME.md](RUNTIME.md)).
>
> Depends on: [RUNTIME.md](RUNTIME.md) (service composition), [TOOL_SYSTEM.md](TOOL_SYSTEM.md) (tool execution), [MEMORY_SYSTEM.md](MEMORY_SYSTEM.md) (context/memory).
> Referenced by: [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md), [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md), [docs/api/Agent-API.md](../docs/api/Agent-API.md).

# Autonomous Agent Runtime — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [RUNTIME.md](RUNTIME.md) | [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)

---

## Overview

The Agent Runtime defines how individual AI agents behave autonomously. Each agent instance runs the agent loop, makes decisions, and executes tools within a workspace.

## Capabilities

| Capability | Description | Phase |
-----------|-------------|-------|
| **Goal-based execution** | Agent receives a high-level goal and autonomously determines steps. | 2 |
| **Task planning** | Breaks goals into ordered subtasks with dependencies. | 2 |
| **Reflection** | After each step, evaluates whether the goal is being achieved. | 2 |
| **Retry strategies** | On failure, retries with different approaches. | 2 |
| **Self-correction** | Detects errors in its own output and fixes them. | 2 |
| **Long-running execution** | Tasks run for minutes or hours, surviving app restarts. | 2 |
| **Parallel execution** | Independent subtasks execute concurrently. | 2 |
| **Checkpoint saving** | Execution state periodically persisted for crash recovery. | 2 |
| **Resume after restart** | Agent picks up where it left off after app/device restart. | 2 |
| **Background execution** | Agent continues when app is minimized. | 2 |
| **Streaming responses** | AI responses stream in real-time. | 5 |
| **Cancellation** | User can cancel any running task. | 2 |
| **Human approval gates** | Sensitive operations require user confirmation. | 2 |
| **Automatic tool selection** | AI chooses tools based on task context. | 4 |
| **Automatic agent selection** | AI assigns the best-suited specialized agent per task. | 7 |
| **Automatic skill selection** | AI selects required skills (expertise) per task via the SkillRegistry. | 4 |
| **Per-step validation criteria** | Every step declares pass/fail criteria; validated before proceeding. | 2 |
| **Objective verification** | Acceptance criteria re-checked before reporting completion. | 2 |
| **Follow-up identification** | Possible improvements and follow-up tasks listed before completion. | 2 |
| **Grounded responses** | Claims trace to tool results or context segments; citations and uncertainty disclosure (RG-1..RG-6, FR-GND). | 2 |
| **Code-claim verification** | Codebase claims verified via code-intelligence tools before being stated (RG-5). | 4 |
| **Deliberate-then-answer** | Classification gate (answer now / reasoning pass / clarify first) with effort levels fast/balanced/thorough (RB-1..RB-3). | 2 |
| **Reasoning-capable routing** | Per-task selection of REASONING-capable models (RB-4, FR-EL-005); reasoning traces in the activity feed (RB-5). | 5 |
| **Answer-quality gates** | Grounded/complete/consistent/confident checks before sending; self-consistency for critical answers (RB-6). | 2 |
| **Automatic workflow generation** | Complex goals auto-generate multi-step workflows. | 6 |
| **Context management** | Intelligent context window management with summarization. | 2 |
| **Token budgeting** | Tracks token usage per request and per session. | 2 |
| **Execution history** | Full history of every action, persisted across sessions. | 6 |

## Agent Loop

```kotlin
class AgentLoop(
    private val planner: Planner,
    private val executor: Executor,
    private val contextBuilder: ContextBuilder,
    private val memoryManager: MemoryManager,
    private val eventBus: EventBus,
    private val permissionManager: PermissionManager
) {
    suspend fun run(goal: String, workspace: Workspace) {
        var state = AgentState(goal = goal, workspace = workspace)

        while (!state.isComplete) {
            // 1. Reflect on current state
            val reflection = planner.reflect(state)

            // 2. Plan next actions
            val plan = planner.planNext(state, reflection)

            // 3. Build context for AI
            val context = contextBuilder.build(state, plan)

            // 4. Call AI provider
            val response = state.provider.complete(context)

            // 5. Parse response (text + tool calls)
            val parsed = parseResponse(response)

            // 6. Execute each tool call
            for (toolCall in parsed.toolCalls) {
                // Check permissions
                val approved = permissionManager.check(toolCall, state)
                if (!approved) continue

                // Execute in sandbox
                val result = executor.execute(toolCall, workspace.sandbox)

                // Store in memory
                memoryManager.storeToolResult(toolCall, result, state)

                // Publish event
                eventBus.publish(ToolExecuted(toolCall, result))
            }

            // 7. Evaluate completion
            state = state.copy(
                history = state.history + parsed,
                isComplete = plan.isComplete(parsed)
            )

            // 8. Save checkpoint
            saveCheckpoint(state)

            // 9. Notify user
            eventBus.publish(TaskProgress(state))
        }
    }
}
```

## Agent State

```kotlin
data class AgentState(
    val goal: String,
    val workspace: Workspace,
    val provider: AIProvider,
    val history: List<AgentStep>,
    val tokenBudget: TokenBudget,
    val checkpoint: AgentCheckpoint?,
    val isComplete: Boolean = false,
    val startedAt: Instant = Clock.System.now()
)

sealed class AgentStep {
    data class Thinking(val reflection: String) : AgentStep()
    data class Planning(val plan: ExecutionPlan) : AgentStep()
    data class ToolExecution(val call: ToolCall, val result: ToolResult) : AgentStep()
    data class Error(val message: String, val recoverable: Boolean) : AgentStep()
}
```

## Token Budgeting

```kotlin
data class TokenBudget(
    val maxTokensPerRequest: Int = 4096,
    val maxTokensPerSession: Int = 100_000,
    val usedTokens: Int = 0,
    val reservedForResponse: Int = 1024
) {
    fun remainingContextTokens(): Int =
        maxTokensPerRequest - reservedForResponse

    fun isExhausted(): Boolean = usedTokens >= maxTokensPerSession
}
```

## Phase Mapping

- **Phase 2**: Agent loop, state management, token budgeting, checkpointing.
- **Phase 5**: Streaming integration, provider switching.
- **Phase 6**: Context management with memory retrieval.
- **Phase 7**: Multi-agent coordination and delegation.
