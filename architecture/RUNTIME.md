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


> **DEC-7:** Retry-attempt indexing is Execution-scoped via `retryAttempt`. RetryPending is ephemeral and does not survive process death. PATH A preserves the same Execution; PATH B after a committed terminal state creates a new Execution with `priorExecutionId`. Process-death recovery is distinct from both retry paths and is governed by [DEC-7](../decisions/DEC-7-retry-attempt-state.md) §DEC-7.7–DEC-7.12.

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

It consists of 17 tightly coordinated modules (counted as internal sub-components of the
`com.nexora.app.runtime` package — for the 14 top-level module boundaries, see
[MODULE_BOUNDARIES.md](../docs/MODULE_BOUNDARIES.md)). The Workflow Engine is listed
here as a runtime service but is owned canonically by
[WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md) as a separate module boundary.

## Module Inventory

| Module | Responsibility | Kotlin Package |
--------|---------------|----------------|
| **Planner** | Decomposes goals into tasks, creates execution plans with dependencies. | `com.nexora.app.runtime.planner` |
| **Executor** | Executes planned tasks sequentially or in parallel, manages execution state. | `com.nexora.app.runtime.executor` |
| **Workflow Engine** | Manages workflow graph state and step progression. Delegates step execution to the Executor. | `com.nexora.app.workflows` |
| **Tool Manager** | Discovers, registers, and invokes tools. Routes tool calls to the correct handler. | `com.nexora.app.tools` |
| **Context Builder** | Assembles context for AI calls: system prompt, conversation history, file contents, memory. | `com.nexora.app.runtime.context` |
| **Memory Manager** | Reads/writes to all memory stores. Manages recall and relevance scoring. | `com.nexora.app.memory` |
| **Permission Manager** | Enforces tool permission policies. Prompts user for approval when required. | `com.nexora.app.runtime.permissions` |
| **Plugin Manager** | Loads, validates, sandboxes, and manages plugin lifecycles. | `com.nexora.app.plugins` |
| **Scheduler** | Schedules deferred, recurring, and background tasks. | `com.nexora.app.runtime.scheduler` |
| **Event Bus** | Central publish/subscribe system for inter-module communication. | `com.nexora.app.runtime.events` |
| **Observability** | Collects metrics, traces, and logs for every runtime operation. | `com.nexora.app.runtime.observability` |
| **Security Manager** | Enforces sandbox boundaries, resource limits, and access controls. | `com.nexora.app.runtime.security` |
| **Background Runtime** | Manages long-running agent execution via Android foreground services. Behavior defined in [specs/BACKGROUND_EXECUTION.md](../specs/BACKGROUND_EXECUTION.md). | `com.nexora.app.runtime.background` |
| **Resource Manager** | Tracks and limits CPU, memory, disk, and network usage per agent/workspace. | `com.nexora.app.runtime.resources` |
| **Agent Manager** | Creates, configures, and manages multiple agent instances. | `com.nexora.app.agents` |
| **Skill Registry** | Maintains the skill catalog, agent–skill bindings, and skill→tool mappings; supports registration, discovery, compatibility validation, and acquisition under DEC-11. | `com.nexora.app.runtime.skills` |
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
Tool Manager ---route---> Complete Authorization Gate
    |
    v
Permission Manager + ASK Approval + explicit DENY + audit ---authorize---> Allowed/Denied
    |
    v
Executor ---execute only after Allowed---> Tool Result
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

### Bounded progression projections

The runtime composition layer MUST route, but does not replace, the canonical Task lifecycle transitions. Before queueing, task dependencies are validated as an acyclic graph; invalid references or cycles return `NXR-1014` without Task mutation. A failed dependency returns `NXR-1015` and propagates terminal failure to dependent tasks. Approval denial produces `NXR-2003` / `USER_DENIED` and a `WaitingApproval → Failed` Task transition; approval expiry produces `NXR-2003` / `POLICY_DENIAL` under DEC-36 with the same Task effect; the participating Agent may independently project `WaitingApproval → Paused` under DEC-35, while audit and activity projections preserve expiry as distinct from explicit user denial. The effective task deadline bounds `Pending`, `Blocked`, and `BlockedAwaitingInput`, whose expiry returns `NXR-1016` and transitions to `Failed`. Provider `Retry-After` waits are honored only within the parent task effective deadline; an exhausted deadline produces `NXR-1016` rather than an indefinite wait. Delegation depth is bounded at 4 by the multi-agent coordination authority. These are projections of canonical subsystem contracts, not new runtime states or a new loop owner.

### Derived Work-Group Projection (ADR-0010)

Runtime MAY compute a derived work-group view to communicate actionable work, recovery candidates, and replanning context. The view is recomputed from existing `Task`, `Execution`, `Workflow`, `PlanStep`, delegated-child, checkpoint, acceptance-progress, trace, and evidence records. It is not a persisted domain entity and does not require a new table, identity, or lifecycle.

A work-group MUST NOT substitute for `Task`, `Execution`, `Workflow`, `PlanStep`, or delegated-child identity in persistence, telemetry, correlation, authorization, recovery, checkpointing, audit, evidence, deadlines, retries, or completion. Every displayed row MUST resolve to its source identity and preserve the source owner, version, deadline, lineage, and evidence references. A cached presentation projection is non-authoritative and MUST be invalidatable after checkpoint, retry, failure, cancellation, or unknown-completion changes.

The work-group view MAY inform the Agent Runtime, Workflow Engine, coordinator, activity feed, or a replanning request. It MUST NOT transition a lifecycle, authorize a Tool, reset a deadline or retry budget, resolve `UNKNOWN_COMPLETION`, or declare completion. A request for durable work-group identity, lifecycle, scheduler, permission, recovery, or evidence ownership requires a separate ADR.

## Inference-Turn Composition

Agent Runtime owns turn orchestration; Provider System owns routing/streaming; Context
Management owns snapshots/reasoning/evidence; Tool System owns authorization/execution.
Runtime supplies references and EventBus transport only. Typed stream events pass through
sequence validation before UI, Tool assembly, usage accounting, memory, or checkpoints.
No new monolithic AI-pipeline owner is introduced (ADR-0008).

## Background Execution

Long-running tasks use Android's **Foreground Service** to survive app minimization. Under DEC-34, every autonomous background terminal session is bound to its parent `taskId`, `executionId`, `workspaceId`, `correlationId`, and immutable effective deadline. Parent cancellation, terminal state, or deadline expiry invokes the existing terminal termination/checkpoint path; an idempotent reconciliation closes or fails sessions with missing, terminal, or expired parents. Unbound autonomous background terminal requests are rejected before process creation.

Under DEC-35, runtime correlation preserves the Tool `NXR-2003` denial, Task `Failed` outcome, and independent Agent `Paused` projection without collapsing their lifecycle authorities. A later operation is a new authorization transaction, not an automatic retry.

```kotlin
class AgentExecutionService : LifecycleService() {
    // Keeps agent alive when app is backgrounded
    // Shows persistent notification with task progress
    // Restores state on service restart
}
```

## Checkpoint System

Nexora enforces a **Crash-Only Software Architecture**. Every agent action, tool invocation, and state transition is durably persisted to Room/SQLite before execution. Non-idempotent operations (e.g., network requests, database mutations) require cryptographic **idempotency guardians** (`idempotencyKey`). Agent state is periodically saved for crash recovery.

```kotlin
data class AgentCheckpoint(
    val taskId: String,
    val plan: ExecutionPlan,
    val currentStepIndex: Int,
    val memorySnapshot: Map<String, Any>,
    val acceptanceProgress: AcceptanceProgressVector,
    val failureLedger: TaskFailureLedger,
    val effectiveDeadline: Instant,
    val remainingBudget: Duration,
    val timestamp: Instant
)
```

## Correlated Agent Trace

Observability is owned by the Runtime’s existing Observability module. It MUST expose one
correlated trace projection for each execution without becoming a second owner of Task,
Execution, Provider, Tool, Agent, Permission, Context, or Evidence semantics.

The trace MUST correlate, when present, the stable `workspaceId`, `taskId`, `executionId`,
`agentId`, `correlationId`, `requestId`, `streamId`/`priorStreamId`, provider profile and
exact model identity, model-catalog snapshot, provider contract version, prompt/config
version, Tool descriptor ID/version, Tool invocation identity, approval transaction,
context snapshot/checkpoint, sub-agent graph, evidence/ClaimRecord references, reasoning
policy and provider-effort mapping, timestamps, queue/active/Tool/provider latency,
usage metadata, retry/failover lineage, canonical error envelope, and final disposition.

Trace records MUST distinguish planned, attempted, observed, verified, incomplete, and
failed outcomes. They MUST preserve plan-versus-actual and claim-to-evidence
relationships and MUST NOT persist private chain-of-thought. Provider-native continuation
artifacts are opaque adapter state and are referenced only according to the Provider Protocol privacy and
retention rules.

When task-scoped execution-capability escalation or delegation is used, the same trace MUST
also preserve the requester, delegated worker when applicable, requested capability, purpose,
affected Tool IDs or operation class, required scope decisions, approval transaction, grant
lifetime, effective deadline, resource/concurrency limits, grant use, expiry or revocation,
cancellation propagation, and final disposition. This is diagnostic and audit metadata only;
it MUST NOT become a new Task or Execution lifecycle state, mutate the static agent matrix, or
infer success from a grant or approval.


Trace correlation is diagnostic and evaluative. It MUST NOT infer lifecycle transitions
from a log message, provider category, model confidence, or latency observation. Lifecycle
changes remain owned by the canonical state machine or operation owner. Trace export MUST
respect workspace permissions, sensitive-content redaction, retention policy, and the
existing audit/security rules.

## ExecutionStatus Lifecycle

The Executor owns ExecutionStatus lifecycle semantics. The canonical state set is
defined in `models/Execution.md`:

- `CREATED` — execution record exists, not yet started.
- `RUNNING` — actively executing a task.
- `COMPLETED` — execution finished successfully; terminal.
- `FAILED` — execution terminated with an unrecoverable error; terminal.
- `CANCELLED` — execution was cancelled; terminal.

### Authoritative Transitions

| Trigger | From | To | Guard |
|---|---|---|---|
| `start` | `CREATED` | `RUNNING` | Task assigned; agent ready |
| `cancel` | `CREATED` | `CANCELLED` | None |
| `cancel` | `RUNNING` | `CANCELLED` | Active steps drained or interrupted |
| `complete` | `RUNNING` | `COMPLETED` | All acceptance criteria met; reviewer gate passed if required |
| `fail` | `RUNNING` | `FAILED` | Unrecoverable error; error strategy exhausted |

### Rules

1. ExecutionStatus is separate from TaskStatus. Task state tracks work progress; ExecutionStatus tracks the runtime execution context.
2. ExecutionPhase (`REQUIREMENT_ANALYSIS`…`COMPLETION_REPORTING`) is a transient activity label, not a lifecycle state. Phase changes do not change ExecutionStatus.
3. Checkpointing never creates a new Execution identity. A recoverable checkpoint resume retains `executionId` and `correlationId` and increments `version`. A new `executionId` is created only for an explicit retry/restart after a committed terminal state.
4. Resume from checkpoint retains the same `executionId` with `version` incremented. `ExecutionStatus` returns to `RUNNING` (from RUNNING) or transitions `CREATED → RUNNING` if the execution was created but not yet started. A new Execution identity is created only for an explicit retry/restart operation after a terminal status (`COMPLETED`, `FAILED`, `CANCELLED`). A terminal Execution is never mutated back to `RUNNING` — retry creates a new `executionId`. Correlation ID remains stable across same-identity resumes.
5. Terminal state commit precedes terminal event publication.
6. Cancellation is idempotent; cancelling an already-cancelled execution is a no-op.
7. Completion after committed cancellation is invalid and returns a canonical error.
8. Duplicate transition events are deduplicated by `(executionId, version)`.

### Failure Recovery

- **Recoverable interruption before a terminal state:** retain the same `executionId`; increment `version`; retain `correlationId`; resume `RUNNING` from checkpoint.
- **User-clarification suspension (BlockedAwaitingInput):** when `TaskLifecycle`
  transitions to `BlockedAwaitingInput` via `requestEscalation`, the executor
  commits a checkpoint capturing the full plan + `currentStepIndex` + the
  escalation payload (`clarificationQuestion`) and retains the same
  `executionId`/`correlationId`. The `resolveEscalation` trigger resumes from
  that checkpoint: `version` increments, status → `RUNNING`, and the
  user's answer is injected as the next input — same-identity resume, no
  new `executionId` (ADR-0009 Decision #5; TaskLifecycle `resolveEscalation`
  transition).
- **Committed terminal `FAILED`/`CANCELLED`/`COMPLETED`:** never transition back to `RUNNING`. Explicit retry/restart creates a new `executionId`; parent/prior execution linkage and correlation policy preserved.
- **Unrecoverable failure:** commit `FAILED`; no same-identity resume. DEC-33 uses `NXR-1014` for invalid Task dependency references/cycles, `NXR-1015` for unsatisfied terminal dependencies, and `NXR-1016` for effective-deadline expiry.
- **Android ANR (Application Not Responding):** `AgentExecutionService` MUST commit a checkpoint on the 6 s / 10 s ANR threshold (foreground / background), emit `TASK_SUSPENDED`, and suspend execution. Service restart or watchdog resumes from the checkpoint without user-visible crash data (NFR-REL-002, ADR-0009 Decision #7). The `executionId` and `correlationId` are preserved across the ANR/resume cycle; `version` increments at resume.

### Checkpoint Save and Restore Exhaustion (GAP-002/GAP-006)

Checkpoint recovery remains artifact-specific. An execution restore MAY use only a validated checkpoint candidate and the declared last-known-good fallback; it MUST preserve the `executionId`, `correlationId`, version lineage, acceptance progress, failure ledger, deadline, and evidence. If the selected checkpoint is corrupt or incompatible, `NXR-1004` MUST be persisted and the next validated fallback MAY be attempted. When no valid execution checkpoint candidate remains, the existing Execution lifecycle MUST commit `FAILED` as an unrecoverable error, dependent recovery work MUST NOT start, the last valid checkpoint reference and failure evidence MUST be preserved, and the user MUST be alerted. No new restore lifecycle is created.

A checkpoint-save failure uses the existing `NXR-1003` contract: retry once without overwriting the last valid checkpoint. If the retry fails, persist the error and checkpoint lineage, mark the affected workspace recovery path unhealthy, prevent dependent recovery work from starting, and commit the existing execution `FAILED` or explicit non-success outcome. **OWNER DECISION REQUIRED:** the Workspace owner MUST select the existing user-visible unavailable/read-only or failed projection for a workspace whose persistence remains unhealthy; this section creates no new Workspace state.

`NXR-8004` `SavedStateHandle` restoration and `NXR-9004` database-backup restoration remain separate artifact-owner contracts. `NXR-8004` reinitializes UI state from defaults and records data loss. `NXR-9004` verifies the current backup and tries an earlier backup without mutating the source until validation succeeds. If all database candidates fail, the database/workspace owner MUST preserve the source and commit its existing unavailable/read-only or failed projection. **OWNER DECISION REQUIRED:** the database/workspace owner MUST select that existing projection before implementation; no generic checkpoint authority or new restore state is introduced.

### Phase Mapping

- **Phase 1**: Define interfaces only (Task, ExecutionPlan, EventBus, NexoraEvent).
- **Phase 2**: Implement Planner, Executor, Context Builder, Event Bus, Token Budget Manager.
- **Phase 3+**: Wire Sandbox, Tools, Memory, Plugins into the runtime.