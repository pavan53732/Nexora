> **Status: DERIVED** for Runtime API.
> This document describes the API surface for the Core Runtime. Canonical behavior is defined in the owning architecture document (`architecture/RUNTIME.md`).
>
> Depends on: the canonical architecture document for Core Runtime (`architecture/RUNTIME.md`).
> Referenced by: upstream architecture, models, protocols, and implementation consumers.

# Runtime API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/RUNTIME.md](../../architecture/RUNTIME.md)

---

## Normative Operation Contract

The Runtime API exposes workspace orchestration, session isolation, transactionally-safe task execution, checkpoint save/restore, and background execution services backed by the Android WorkManager. It does not acquire ownership of the single-agent loop, multi-agent delegation, or workflow graph semantics; those remain governed by `architecture/AGENT_RUNTIME.md`, `architecture/MULTI_AGENT_SYSTEM.md`, and `architecture/WORKFLOW_ENGINE.md` respectively.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `createWorkspace`| Workspace `Created` | Stable workspace projection | Initialization failed (`NXR-7001`), database corrupt (`NXR-9001`) | Safe (Idempotent) | Validates unique owner scope; establishes isolated directory structure | Storage and folder isolation tests |
| `startExecution` | Execution `Created → Running` | Execution projection with correlation ID | Checkpoint failed (`NXR-1003`), service denied (`NXR-1012`), not initialized (`NXR-1013`) | Safe (Idempotent Key) | Spawns foreground CPU wake locks inside isolated processes; validates target task | Foreground service and task-start tests |
| `checkpoint` | No lifecycle change | Confirmed checkpoint ID with timestamp | Serialization failed (`NXR-1003`), disk full (`NXR-7003`) | Safe to retry | Performs transactional WAL commit of execution snapshot variables | Checkpoint and rollback tests |
| `resumeExecution` | Interrupted nonterminal Execution remains/returns `RUNNING` | Same-ID projection with higher version | Corrupt checkpoint (`NXR-1004`), stale version, terminal target | Idempotency key required | Same `executionId`/`correlationId`; checkpoint required | `IT-LC-001..005`, `IT-LC-018/020` |
| `retryExecution` | New `CREATED → RUNNING` Execution; predecessor unchanged | New-ID projection with `priorExecutionId` | Missing/nonterminal predecessor, cyclic lineage, idempotency conflict | Idempotency key required | Terminal predecessor remains terminal | `IT-LC-006..010`, `IT-LC-016/017/019` |

Every API call MUST carry a `correlationId`.

### Background terminal binding (DEC-34)

Autonomous background terminal work is not an unbound Runtime operation. The created TerminalSession projection MUST carry the parent `taskId`, `executionId`, `workspaceId`, `correlationId`, and immutable effective deadline. Parent cancellation, terminal state, or deadline expiry invokes the existing terminal termination/checkpoint path; requests without a parent Task/Execution are rejected before process creation. Reconciliation closes or fails sessions whose parent is missing, terminal, or expired.

### Adaptive orchestration projection

`startExecution`, checkpoint, resume, and terminal projections participate in the existing adaptive orchestration chain: objective and constraints are compiled into a plan; the plan is decomposed and dependency-checked; eligible work is allocated sequentially or in parallel; observations and evidence are aggregated; conflicts or failed verification return to the owning bounded repair/re-plan path; and only the existing completion gates may produce a successful terminal outcome. The Runtime API exposes the resulting Task/Execution/checkpoint projections and correlation/version data; it does not create a second orchestration state machine or replace the ownership of Agent Runtime, Multi-Agent, Workflow, Tool, Provider, Context, Evidence, or lifecycle authorities.

The reconstructable state needed for long-running or delegated work is assembled from the existing Task, Workflow, Execution, ContextSnapshot, checkpoint, Memory, ClaimRecord, and artifact records as specified by `specs/CONTEXT_MANAGEMENT.md` §3. The API MUST preserve the source identity and provenance of those projections when returning or restoring execution state.

## Contract Shapes

### Workspace Creation Request

```kotlin
data class CreateWorkspaceRequest(
    val name: String,
    val description: String,
    val ownerId: String,
    val templateName: String? = null
)
```

### Execution Checkpoint Shape

```kotlin
data class CheckpointState(
    val checkpointId: String,
    val executionId: String,
    val correlationId: String,
    val stepIndex: Int,
    val variables: JsonObject,
    val historyLog: List<String>,
    val tokenBudgetUsed: Int,
    val phase: ExecutionPhase,
    val occurredAt: Instant
)
```

The `historyLog` field is an execution-recovery and audit projection. It MUST NOT be interpreted as unrestricted model reasoning, hidden system prompts, raw untrusted content, or provider-native private continuation state. User-visible reasoning remains limited to the existing redacted `ReasoningSummary` contract.

### Execution Recovery Shapes

```kotlin
data class ExecutionProjection(
    val executionId: String,
    val priorExecutionId: String?,
    val checkpointId: String?,
    val correlationId: String,
    val status: ExecutionStatus,
    val phase: ExecutionPhase,
    val version: Long
)

data class 

> **DEC-7 (2026-08-11):** PATH A (RetryPending retry) preserves the same `idempotencyKey` and `executionId`. PATH B (terminal retry via `retryExecution`) creates a new `executionId` and a new idempotency boundary. See `decisions/DEC-7-retry-attempt-state.md`.

ResumeExecutionRequest(
    val executionId: String,
    val checkpointId: String,
    val correlationId: String,
    val expectedVersion: Long,
    val idempotencyKey: String,
    val escalationAnswer: JsonObject? = null  // set when resuming from BlockedAwaitingInput
)

data class RetryExecutionRequest(
    val priorExecutionId: String,
    val correlationId: String,
    val idempotencyKey: String
)
```

### Runtime API Interface

```kotlin
package com.nexora.app.runtime.core

interface RuntimeApi {
    suspend fun createWorkspace(request: CreateWorkspaceRequest): WorkspaceProjection
    suspend fun startExecution(taskId: String, correlationId: String): ExecutionProjection
    suspend fun checkpoint(executionId: String, state: CheckpointState): Boolean
    suspend fun resumeExecution(request: ResumeExecutionRequest): ExecutionProjection
    suspend fun retryExecution(request: RetryExecutionRequest): ExecutionProjection
    suspend fun terminateExecution(executionId: String, correlationId: String): Boolean
}
```

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes | Recovery & Lifecycle Effects |
|---|---|---|
| `createWorkspace` | `NXR-7001` (Creation Failed) | Terminate directory allocation; state remains uncreated. |
| `startExecution` | `NXR-1012` (FGS Denied) | Log warning; request notification permissions; fallback to in-process execution. |
| | `NXR-1013` (Not Initialized) | Fail startup; wait for `NexoraRuntime.init()` to complete. |
| `checkpoint` | `NXR-1003` (Save Failed) | Retry once; if persistent, preserve the prior valid checkpoint, mark the workspace unhealthy as specified by the canonical error recovery, and make no Workspace lifecycle transition. |
| `resumeExecution` | `NXR-1004` (Restore Failed) | Keep identity stable; reject terminal/stale targets; fall back only to a valid checkpoint. |
| `retryExecution` | Canonical validation/conflict envelope | Require terminal predecessor, create new ID once per idempotency key, preserve acyclic lineage. |
| Task queue/dependency/deadline validation | `NXR-1014` (Task dependency invalid), `NXR-1015` (Task dependency unsatisfied), `NXR-1016` (Task deadline expired) | Scheduler rejects invalid dependency graphs without Task mutation; TaskLifecycle fails dependent Tasks or deadline-expired waits through the existing `Failed` effect; no automatic retry or deadline renewal. |
| Task timeout identity | No canonical Task-specific `NXR-*` identity is established by the error catalog; preserve the Task deadline contract through `NXR-1016` where applicable and do not reuse the Agent-specific `NXR-3004`. | No additional Task-timeout error mapping is asserted here. |
