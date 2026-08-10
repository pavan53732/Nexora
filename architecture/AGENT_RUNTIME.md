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
|---|---|---|
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
| **Reasoning-capable routing** | Per-task selection of REASONING-capable models under bounded ReasoningPolicy; redacted ReasoningSummary in the activity feed. | 5 |
| **Answer-quality gates** | Grounded/complete/consistent/confident checks before sending; self-consistency for critical answers (RB-6). | 2 |
| **Automatic workflow generation** | Complex goals auto-generate multi-step workflows. | 6 |
| **Context management** | Intelligent context window management with summarization. | 2 |
| **Token budgeting** | Tracks token usage per request and per session. | 2 |
| **Execution history** | Full history of every action, persisted across sessions. | 6 |

## Agent Inference-Turn Pipeline

The canonical provider path is typed streaming. Providers without native streaming are
adapted into `Started → TextDelta/ToolCallCommitted → Terminal` events. One turn runs:

```text
Inbound message
→ Deliberation/clarification gate
→ Freshness + project introspection
→ Evidence retrieval plan
→ immutable ContextSnapshot
→ bounded ReasoningPolicy
→ ProviderRoutePlan
→ typed ProviderStreamLifecycle
→ text/citation/reasoning-summary/tool-call assembly
→ complete Tool authorization and execution
→ critic/verifier pass
→ bounded repair or re-plan
→ answer synthesis + claim/evidence validation
→ completion gate
→ checkpoint + memory curation
```

A partial `ToolArgumentsDelta` is data, never executable. Only a schema-valid
`ToolCallCommitted` enters the Tool authorization gate. Stream failure leaves displayed
text marked partial; failover starts a new stream identity with lineage.

## Agent Loop

```kotlin
suspend fun runTurn(message: UserMessage, state: AgentState): TurnResult {
    val deliberation = deliberationGate.classify(message, state)
    if (deliberation.requiresClarification) return askForClarification(deliberation)

    val projectContext = projectIntrospector.inspect(state.workspace)
    val evidencePlan = evidenceEngine.planRetrieval(message, projectContext)
    val snapshot = contextBuilder.compileSnapshot(state, evidencePlan)
    val reasoningPolicy = reasoningPolicyResolver.resolve(state, deliberation)
    val routePlan = providerRouter.plan(snapshot, reasoningPolicy)

    val assembler = InferenceAssembler(snapshot, reasoningPolicy)
    providerRouter.stream(routePlan, snapshot).collect { envelope ->
        streamValidator.accept(envelope) // identity, sequence, terminal, size
        eventBus.publish(InferenceStreamEvent(envelope))
        when (val event = envelope.event) {
            is StreamEvent.TextDelta -> assembler.appendText(event)
            is StreamEvent.ReasoningSummaryDelta -> assembler.appendReasoningSummary(event)
            is StreamEvent.CitationDelta -> assembler.appendCitations(event)
            is StreamEvent.ToolCallStarted,
            is StreamEvent.ToolArgumentsDelta -> assembler.appendToolFragment(event)
            is StreamEvent.ToolCallCommitted -> {
                val authorization = permissionManager.authorizeToolCall(event.toolCall, state)
                if (authorization is PermissionResult.Allowed) {
                    val result = executor.execute(event.toolCall, state.workspace.sandbox)
                    memoryManager.storeToolResult(event.toolCall, result, state)
                    assembler.observe(result)
                }
            }
            is StreamEvent.Terminal -> assembler.commit(event)
            is StreamEvent.Failed -> assembler.failPartial(event)
            is StreamEvent.Cancelled -> assembler.cancel(event)
            else -> assembler.observeStreamControl(event)
        }
        saveStreamCheckpoint(state, envelope, assembler.snapshot())
    }

    val draft = assembler.requireCommittedDraft()
    val verified = evidenceEngine.verify(draft, reasoningPolicy)
    val repaired = boundedRepairIfNeeded(verified, reasoningPolicy)
    val answer = answerSynthesizer.create(repaired)
    completionGate.requireSatisfied(answer)
    saveCheckpoint(state.withTurn(answer))
    return TurnResult(answer)
}
```

### Turn Invariants

- Cancellation propagates Agent → ProviderRouter → adapter → Tool children.
- Exactly one terminal stream outcome is accepted per `streamId`.
- Provider failover never silently concatenates output from distinct streams.
- Reasoning and repair remain inside explicit token/call/time/cost budgets.
- Durable reasoning output is a redacted `ReasoningSummary`, not unrestricted private chain-of-thought.

### Semantic Progress & Anti-Replay (mandated by ADR-0009; mirrored in AUTONOMY_STABILITY.md §9.5)

- Syntactic loop detection (n=2 identical action+argument repeat) is a **floor**, not a ceiling.
- Each iteration, before `saveCheckpoint`, Agent Runtime MUST compute a semantic `ProgressSignal`
  over the `ContextSnapshot` working-state lineage (test delta, file-change delta,
  new-evidence delta, error-category shift). If `ProgressSignal == 0` over N=3
  consecutive iterations, the turn is escalated via §3's escalation path.
- Each task carries a task-scoped **failure ledger** `{toolId, errorSignature, count}`.
  After K=3 identical signatures on a single tool within the task, Agent Runtime
  MUST NOT re-issue that tool with the same arguments on the next turn. The ledger
  is **task-scoped only**; global `Tool` registry descriptors are never mutated.


## Agent State

```kotlin
data class AgentState(
    val goal: String,
    val workspace: Workspace,
    val provider: AIProvider,
    val history: List<AgentStep>,
    val tokenBudget: TokenBudget,
    val activeContextSnapshotId: String?,
    val activeStreamId: String?,
    val lastCommittedStreamSequence: Long?,
    val reasoningPolicy: ReasoningPolicy?,
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
