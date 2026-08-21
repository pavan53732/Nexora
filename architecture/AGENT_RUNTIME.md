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

## Execution Modes

The single-agent runtime supports **mode-selected execution**. These modes are established runtime behavior within the canonical single-agent loop and do not change multi-agent ownership.

| Mode | Purpose | Typical use | Required controls |
|---|---|---|---|
| FAST | Lowest-latency path with minimal planning | Direct requests with low ambiguity and low risk | Small plan budget, direct tool/model execution, explicit termination gate |
| NORMAL | Default balanced path | Typical multi-step requests | Structured planning, bounded evidence gathering, validation before completion |
| DEEP | Deeper bounded reasoning for ambiguity, contradiction, or high-stakes work | Complex debugging, architectural analysis, conflict resolution | Bounded decomposition, competing hypotheses, contradiction checks, uncertainty tracking |
| VERIFY | Independent validation path | Important outputs, compliance-sensitive tasks, user-requested verification | Requirement/constraint re-check, provenance validation, output verification |
| RECOVER | Failure-handling path | Retryable failure, context reconstruction, checkpoint restore | Retry policy, fallback routing, checkpoint recovery, bounded escalation |

### Mode selection

The runtime MUST select the **minimum sufficient mode** for the task and the applicable autonomy mode automatically from the existing scoped trust score and thresholds. FAST is preferred when requirement coverage, risk, and evidence needs permit. DEEP MUST NOT be the default path for all requests.

The existing autonomy thresholds are `MANUAL` 0–39, `ASSISTED` 40–74, and `AUTOPILOT` 75–100. The effective autonomy mode MUST be recorded through existing execution, audit, activity, and evidence projections. The user does not confirm the mode per session or per action. An existing user override MAY only downgrade the effective mode, takes effect immediately, and MUST NOT silently upgrade the mode or bypass PermissionModel, sandbox, safety, or evidence gates. Android degraded mode may force `MANUAL` independently of trust.

Mode selection SHOULD consider:

- task criticality;
- ambiguity level;
- conflict or contradiction presence;
- evidence sufficiency;
- trust score and its scoped provenance;
- user-requested rigor;
- failure history;
- provider/tool latency sensitivity.

### Bounded reasoning contract

Regardless of mode, each agent iteration MUST have:

- an iteration identifier;
- a declared objective;
- a bounded step/iteration budget;
- a progress signal evaluation;
- a termination condition;
- an escalation condition when bounded progress is not achieved.

### Hierarchical Deadline Contract

Every task or execution MUST establish an end-to-end deadline before the first provider, tool, repair, verifier, or delegation call. Child operations receive the remaining parent budget; they MUST NOT receive a fresh full timeout that can outlive the parent execution.

The remaining budget MUST reserve time for cancellation propagation, checkpoint persistence, result classification, and user-visible completion. When the remaining budget cannot safely cover a new operation, the runtime MUST stop starting new work, cancel descendants, persist recoverable state, and return an explicit `INCOMPLETE`, `ESCALATED`, or equivalent non-success disposition. Deadline exhaustion MUST never become an unbounded retry, repair, or verification loop.

The effective deadline and remaining budget are immutable inputs to each nested operation and are recorded in execution history and checkpoints for recovery and audit.

**DEC-30 projection:** Task dependency, approval, clarification, provider-wait, and delegated-child waits consume the existing effective deadline and cannot renew it. When an Agent runtime incarnation fails, retry does not reactivate the committed failed incarnation; it creates a new incarnation/version and execution identity while preserving the stable registered `agentId` and predecessor linkage. Task/Execution retry rules remain owned by their canonical lifecycle contracts.

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
→ execution checkpoint + memory curation

> The checkpoint in this execution loop is an execution checkpoint for recovery. Conversation checkpoint and rollback semantics are owned by `architecture/CONVERSATION_CHECKPOINTS.md`; the two artifacts are not interchangeable.
```

A partial `ToolArgumentsDelta` is data, never executable. Only a schema-valid
`ToolCallCommitted` enters the Tool authorization gate. Stream failure leaves displayed
text marked partial; failover starts a new stream identity with lineage.

## Progress and Loop Guards

This upgrade adds an explicit bounded-progress contract to the single-agent loop.

### Progress signals

Progress is established only when one or more of the following occurs:

- new evidence is collected;
- execution state changes;
- a task acceptance criterion is satisfied;
- unresolved requirements or contradictions are reduced;
- a plan is materially revised;
- a tool result succeeds where it previously failed;
- verification confidence increases through independent checks.

Repeated activity without meaningful progress MUST NOT continue indefinitely.

### Acceptance-Criterion Progress Vector

Semantic progress MUST be evaluated against the task's declared acceptance criteria. Each criterion has a monotonic status of `UNASSESSED`, `IN_PROGRESS`, `PASSED`, or `FAILED`. A progress signal is substantive only when it improves a criterion status, produces evidence directly relevant to a criterion, changes the plan to address a verified failure, or records an explicit user-directed scope change.

File changes, additional evidence, or error-category changes that are unrelated to acceptance criteria MUST NOT by themselves reset the bounded-progress detector. The vector and its evidence references are persisted with the execution checkpoint.

### ProgressSignal computation boundary

The `ProgressSignal` model is a derived observation of the acceptance-criterion progress vector and the current execution lineage; it is not an independent lifecycle state. Before comparing iterations, the runtime MUST establish a baseline from the latest valid checkpoint or the initial execution snapshot. Each delta MUST be computed against that baseline for the same logical execution identity. `testSuitePassCountDelta`, `workspaceFileChangeDelta`, and `newEvidenceArtifactCountDelta` are diagnostic deltas only and count as substantive progress only when they are relevant to a declared acceptance criterion. `errorCategoryShift` is true only when the canonical error category or recovery classification changes for the same logical operation; a repeated error with a different message does not qualify. The runtime MUST evaluate the signal together with criterion-status improvement, relevant evidence, plan repair, verification improvement, and failure-ledger state. The N=3 zero-progress/escalation rule remains the existing bounded policy; no new threshold, lifecycle state, or error identity is created by this computation boundary.

### Loop-prevention requirements

The runtime MUST detect and react to:

- repeated identical tool calls with materially identical inputs and no new state;
- repeated searches or reads that return no new evidence;
- planner/executor oscillation without plan advancement;
- repeated self-correction attempts that do not improve validation state;
- verification loops that restate the same failure without new evidence;
- retry storms after repeated transient failure beyond policy bounds.

When a bounded-progress violation is detected, the runtime MUST first determine whether the next action represents ordinary advancing progress and remains within existing permission, safety, capability, deadline, resource, and evidence gates. If so, it MUST surface an existing user-visible notification/status update and continue through the existing execution path. Otherwise it MUST use the existing recovery or escalation contract, including:

1. switch to RECOVER mode,
2. escalate for explicit clarification, capability input, or required approval,
3. fall back to a different provider/tool strategy, or
4. terminate with explicit incomplete/blocked/failed status.

A notification is observability, not approval. High-risk, denied, unsafe, unverified, deadline-exhausted, resource-exhausted, and unresolved non-idempotent operations remain blocking or non-successful under their existing owners.

An exhausted reconciliation budget or effective deadline for a non-idempotent Tool is an automatic bounded-recovery exhaustion case. The runtime MUST preserve the child `UNKNOWN_COMPLETION`, retain the reconciliation evidence and existing checkpoint context, prohibit replay or further Tool execution of the unresolved child, and apply the existing non-success effects through TaskLifecycle and the Execution lifecycle: parent Task `Running → Failed` and associated Execution `RUNNING → FAILED`. No human clarification or `requestEscalation(question)` is required for this exhaustion path. Any later eligible retry/restart uses existing idempotency and new-Execution lineage rules; it MUST NOT replay the unresolved child merely because recovery continued. No new state or ExecutionStatus is introduced.

## Metric-Driven Execution and Evidence Projection (ADR-0010)

The Agent Runtime MUST expose a derived execution/progress/verification projection over the existing `Agent`, `Task`, `Execution`, `Workflow`, `PlanStep`, `AcceptanceProgressVector`, `ProgressSignal`, `ClaimRecord`, checkpoint, trace, and evidence references. The projection MUST make the current objective, actionable next work, acceptance-criterion status, progress reason, verification state, blocked reason, recovery/replan candidate, and completion disposition explainable without creating a second lifecycle owner.

A metric is a derived evaluation over existing acceptance criteria, `ProgressSignal`, Task/Execution/Workflow state, and evidence. Nexora MUST NOT persist a `GoalMetric` identity, metric lifecycle, metric-owned scheduler, metric-owned authorization, or metric-owned completion authority. Metric output MAY recommend continue, recover, replan, escalate, or report incomplete; only the existing lifecycle and authorization owners may transition state or authorize side effects.

Every projection observation MUST retain the existing execution lineage and evidence references needed to distinguish `CANONICAL REQUIREMENT`, `IMPLEMENTED`, `TEST DEFINED`, `TESTED`, and `EXECUTED EVIDENCE`. A metric MUST NOT infer lifecycle success from confidence, latency, logs, file-change count, or provider output alone. It MUST NOT reset a deadline, retry budget, failure ledger, checkpoint, or unknown-completion classification.

The execution trace MUST preserve the existing Planner → ExecutionPlan → ContextSnapshot → ProviderRoutePlan → typed stream → Tool authorization → Executor → result/memory/EventBus → verification → bounded repair/replan → claim/evidence validation path. This is an explicit composition and observability contract; it does not create an Execution Kernel or replace the ownership boundaries declared by `RUNTIME.md`, `TOOL_SYSTEM.md`, `WORKFLOW_ENGINE.md`, `MULTI_AGENT_SYSTEM.md`, or `specs/CONTEXT_MANAGEMENT.md`.

### Operational Progress and Recovery Projection (ADR-0010)

Whenever the Agent Runtime exposes progress or recovery information, the projection MUST resolve to the existing `agentId`, `taskId`, `executionId`, `workflowId`/`planStepId` when applicable, `workspaceId`, `correlationId`, checkpoint/version, and evidence references. It MUST report the current objective and phase, actionable step or Tool operation, elapsed time, immutable effective deadline and remaining budget, latest heartbeat/freshness observation, applicable resource/concurrency condition, blocker or uncertainty, next safe action, verification/evidence state, and final non-authoritative disposition. A missing value MUST be reported as unknown or unavailable rather than inferred.

The projection MUST report the applicable existing recovery ladder without creating a recovery owner. The reporting sequence is: preserve the current checkpoint, lineage, failure classification, and evidence; consider retry only when the owning Tool, Provider, Task, or Execution contract permits it; run bounded diagnostics or context refresh when those existing paths can add relevant evidence; apply bounded repair or re-plan; change provider/strategy or delegate to an eligible specialist/read-only investigator; when ordinary advancing progress remains within all existing gates, notify through the existing user-visible status boundary and continue; restore a validated checkpoint through the existing same-identity recovery path; then escalate to the user or return the existing safe read-only, degraded, incomplete, cancelled, or failed disposition.
 The sequence is a projection of existing authorities, not a promise that every rung is available or ordered identically for every failure. Candidate selection remains bounded by the existing deadline, retry budget, failure ledger, resource limits, permission/sandbox rules, and lifecycle owners. This projection is observational and coordinating only: it MUST NOT adopt or reparent work, reset a deadline or budget, authorize a Tool or permission escalation, replay an uncertain operation, trigger autonomous side effects, or create a recovery manager, supervisor identity, worker identity, lease, lifecycle, or state. The existing recovery and degradation contracts remain authoritative.

## Controlled Execution-Capability Escalation

The static capability matrix remains authoritative for ordinary dispatch. An agent MUST NOT acquire Terminal, Background, Delegate, or any other capability merely because the shared runtime can perform that operation. When a task requires a capability not granted to the current agent type, the runtime has only two permitted paths: delegate the work to an eligible agent, or create a task-scoped capability-escalation request through the existing authorization and approval flow.

A capability-escalation request is a bounded execution projection, not a new agent type, Tool identity, permission scope, lifecycle state, or permanent matrix mutation. It MUST include the requesting `agentId`, `taskId`, `workspaceId`, requested capability, stated purpose, affected Tool IDs or operation class, required permission scopes, effective deadline, maximum execution/concurrency limits, cancellation policy, and revocation condition. The request MUST be rejected when the requested capability is outside the task's declared acceptance criteria, workspace policy, sandbox limits, or applicable autonomy mode.

The orchestrator MUST evaluate the request against the current agent capability matrix before any escalation path is considered. Delegation to an eligible agent is preferred when the work can remain within the existing role boundary. A direct temporary grant requires the existing PermissionModel permission resolution, approval, sandbox, resource, and audit gates; it MUST NOT bypass any of them. A grant is valid only for the identified task and execution lineage, expires at the earliest of task completion, cancellation, effective deadline, explicit revocation, or terminal failure, and cannot be reused by another task or agent.

Terminal escalation MUST continue to use the existing `sandbox:execute` and applicable `sandbox:read`/`sandbox:write` scopes. Background escalation MUST additionally satisfy the existing background-runtime requirements for checkpointing, cancellation, progress notification, resource limits, Android lifecycle handling, and degraded-mode behavior. A capability grant does not authorize host filesystem, unrestricted device, network, plugin, MCP, browser, or sensitive-app access; those remain separately governed by their existing permissions, sandbox rules, and blocked-list authorization contract. No local classifier is invoked.

Every request, decision, approval, delegation, grant, denial, use, cancellation, expiry, and revocation MUST be represented in the existing execution history, permission audit trail, and correlated agent trace. The user-visible activity feed MUST distinguish requested, approved, denied, delegated, active, expired, revoked, and completed outcomes without presenting a temporary grant as a permanent role capability. Unsupported capability requests MUST fail closed or be delegated; the agent MUST NOT invent a Tool, scope, approval, or successful execution result.

The escalation path MUST preserve the existing bounded-progress and deadline contracts. It MUST NOT restart a task's full deadline, reset the failure ledger, clear acceptance progress, or bypass unknown-completion reconciliation. If the grant expires or is revoked while a child operation is active, cancellation propagates through the existing Agent → ProviderRouter → Tool children path, recoverable state is checkpointed, and the final outcome remains incomplete, cancelled, failed, or otherwise non-successful unless the existing completion gate is satisfied.

This section defines execution authorization behavior only. The static per-agent capability inventory remains owned by `registry/AGENT_MATRIX.md`; Tool identity and execution remain owned by `architecture/TOOL_SYSTEM.md`; permission decisions remain owned by `security/PermissionModel.md`; containment remains owned by `security/SandboxPolicy.md`; background lifecycle behavior remains owned by `specs/BACKGROUND_EXECUTION.md`; and multi-agent delegation remains owned by `architecture/MULTI_AGENT_SYSTEM.md`.

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
    val finalClaims = evidenceEngine.bindAndValidateClaims(answer, snapshot)
    completionGate.requireSatisfied(
        answer = answer,
        acceptanceProgress = state.acceptanceProgress,
        claimRecords = finalClaims
    )
    saveCheckpoint(state.withTurn(answer, finalClaims))
    return TurnResult(answer)
}
```

The pseudocode above is a successful-turn path, not permission to continue after an
unsuccessful stream or Tool call. If the stream reaches `Failed` or `Cancelled`, the
runtime MUST route to the existing failure/cancellation effect, preserve partial output
and checkpoint state as applicable, and MUST NOT call `requireCommittedDraft()` or the
completion gate as if a successful draft existed. If authorization is not `Allowed`, the
runtime MUST apply the existing denial/approval/escalation contract and MUST NOT execute
the Tool or treat the absent Tool result as progress. If a committed draft is unavailable,
verification or synthesis fails, or the completion gate is unsatisfied, the runtime MUST
use the existing bounded recovery, escalation, or terminal failure path before returning.

### Turn Invariants

- Cancellation propagates Agent → ProviderRouter → adapter → Tool children.
- Exactly one terminal stream outcome is accepted per `streamId`.
- Provider failover never silently concatenates output from distinct streams.
- Reasoning and repair remain inside explicit technical token/call/time and safety ceilings; usage and cost telemetry do not impose an internal credit or financial stop.
- Durable reasoning output is a redacted `ReasoningSummary`, not unrestricted private chain-of-thought.
- Final acceptance-criterion status and claim-to-evidence bindings are revalidated after bounded repair and final answer synthesis; an earlier draft verification does not authorize a changed final answer.

### Semantic Progress & Anti-Replay (mandated by ADR-0009; mirrored in AUTONOMY_STABILITY.md §9.5)

- Syntactic loop detection (n=2 identical action+argument repeat) is a **floor**, not a ceiling.
- Each iteration, before `saveCheckpoint`, Agent Runtime MUST compute a semantic `ProgressSignal`
  over the `ContextSnapshot` working-state lineage (test delta, file-change delta,
  new-evidence delta, error-category shift). If `ProgressSignal == 0` over N=3
  consecutive iterations, the turn is escalated via §3's escalation path.
- Each task carries a task-scoped **failure ledger** `{toolId, errorSignature, count, firstSeenAt, blacklistedUntilTaskEnd}`.
  After K=3 identical signatures on a single tool within the task, Agent Runtime **MUST**
  enforce **strategy mutation**: the next invocation **MUST select a different `toolId`**
  (not merely different arguments); the blocked `toolId` is recorded in the ledger as
  `BLACKLISTED_UNTIL_TASK_END`. It is **forbidden** to re-issue the blacklisted tool
  (regardless of parameter changes) on any subsequent turn within the same task. The
  ledger is **task-scoped only**; global `Tool` registry descriptors and `ToolStatus` are
  never mutated (`TOOL_SYSTEM.md` §ToolStatus Lifecycle owns descriptor health, explicitly
  excluding per-call failures — see NXR-2004 recovery).
- `ToolReplaced` (old: `blockedToolId`, `replacementToolId`, `newSignature`) is logged in
  `AgentStep` history when a blacklisted tool is substituted with an alternative selection.


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
    val acceptanceProgress: AcceptanceProgressVector,
    val failureLedger: TaskFailureLedger,
    val effectiveDeadline: Instant,
    val remainingBudget: Duration,
    val checkpoint: AgentCheckpoint?,
    val isComplete: Boolean = false,
    val startedAt: Instant = Clock.System.now()
)

data class AcceptanceProgressVector(
    val criteria: List<AcceptanceCriterionProgress>
)

data class AcceptanceCriterionProgress(
    val criterionId: String,
    val status: CriterionStatus,
    val evidenceRefs: List<String>
)

enum class CriterionStatus { UNASSESSED, IN_PROGRESS, PASSED, FAILED }

data class TaskFailureLedger(
    val entries: List<TaskFailureEntry>
)

data class TaskFailureEntry(
    val toolId: String,
    val errorSignature: String,
    val count: Int,
    val firstSeenAt: Instant,
    val blacklistedUntilTaskEnd: Boolean
)

sealed class AgentStep {
    data class Thinking(val reflection: String) : AgentStep()
    data class Planning(val plan: ExecutionPlan) : AgentStep()
    data class ToolExecution(val call: ToolCall, val result: ToolResult) : AgentStep()
    data class ToolReplaced(
        val blockedToolId: String,
        val replacementToolId: String,
        val newSignature: String
    ) : AgentStep()
    data class Error(val message: String, val recoverable: Boolean) : AgentStep()
}
```

`AgentStep.Thinking` and its `reflection` value are in-memory control-flow placeholders in this pseudocode, not a persistence schema, protocol field, API response, export field, or user-visible history artifact. Implementations MUST NOT serialize unrestricted internal reasoning, hidden prompts, raw provider continuation state, or raw untrusted content from this step into `AgentCheckpoint`, execution history, or UI. Durable and user-visible reasoning remains limited to the existing redacted `ReasoningSummary` and structured evidence, decision, uncertainty, and verification artifacts defined by [../specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md) §6.2.

## Token Budgeting

```kotlin
// Technical request/session ceilings for correctness, liveness, provider safety, and
// resource protection. These are not user credits, spending quotas, or financial gates
// under DEC-45; usage/cost telemetry remains informational.
data class TokenBudget(
    val maxTokensPerRequest: Int = 4096,
    val maxTokensPerSession: Int = 100_000,
    val usedTokens: Int = 0,
    val reservedForResponse: Int = 1024
) {
    fun remainingContextTokens(): Int =
        maxTokensPerRequest - reservedForResponse

    // Exhaustion may stop or degrade execution only because a technical ceiling was
    // reached; it must not be presented as user credit/token-budget refusal.
    fun isExhausted(): Boolean = usedTokens >= maxTokensPerSession
}
```

## Phase Mapping

- **Phase 2**: Agent loop, state management, token budgeting, checkpointing.
- **Phase 5**: Streaming integration, provider switching.
- **Phase 6**: Context management with memory retrieval.
- **Phase 7**: Multi-agent coordination and delegation.
