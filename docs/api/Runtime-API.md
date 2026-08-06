> **Status: DERIVED** for Runtime API.
> This document describes the API surface for the Core Runtime. Canonical behavior is defined in the owning architecture document (`architecture/RUNTIME.md`).
>
> Depends on: the canonical architecture document for Core Runtime (`architecture/RUNTIME.md`).
> Referenced by: upstream architecture, models, protocols, and implementation consumers.

# Runtime API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../../architecture/RUNTIME.md](../../architecture/RUNTIME.md)

---

## Normative Operation Contract

The Runtime API governs workspace orchestration, session isolation, transactionally-safe task execution, checkpoint save/restore, and background execution services backed by the Android WorkManager.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `createWorkspace`| Workspace `Created` | Stable workspace projection | Initialization failed (`NXR-7001`), database corrupt (`NXR-9001`) | Safe (Idempotent) | Validates unique owner scope; establishes isolated directory structure | Storage and folder isolation tests |
| `startExecution` | Execution `Created → Running` | Execution projection with correlation ID | Checkpoint failed (`NXR-1003`), service denied (`NXR-1012`), not initialized (`NXR-1013`) | Safe (Idempotent Key) | Spawns foreground CPU wake locks inside isolated processes; validates target task | Foreground service and task start tests |
| `checkpoint` | No lifecycle change | Confirmed checkpoint ID with timestamp | Serialization failed (`NXR-1003`), disk full (`NXR-7003`) | Safe to retry | Performs transactional WAL commit of execution snapshot variables | Checkpoint and rollback tests |
| `resume` | Execution `Running` (re-hydrated) | Restored execution projection | Corrupt checkpoint (`NXR-1004`), task timeout (`NXR-3004`) | Safe to retry | Rebuilds loop memory, token budget, and step history from the latest snapshot | Restore and crash recovery tests |

Every API call MUST carry a `correlationId`.

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

### Runtime API Interface

```kotlin
package com.nexora.app.runtime.core

interface RuntimeApi {
    suspend fun createWorkspace(request: CreateWorkspaceRequest): WorkspaceProjection
    suspend fun startExecution(taskId: String, correlationId: String): ExecutionProjection
    suspend fun checkpoint(executionId: String, state: CheckpointState): Boolean
    suspend fun resume(executionId: String, correlationId: String): ExecutionProjection
    suspend fun terminateExecution(executionId: String, correlationId: String): Boolean
}
```

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes | Recovery & Lifecycle Effects |
|---|---|---|
| `createWorkspace` | `NXR-7001` (Creation Failed) | Terminate directory allocation; state remains uncreated. |
| `startExecution` | `NXR-1012` (FGS Denied) | Log warning; request notification permissions; fallback to in-process execution. |
| | `NXR-1013` (Not Initialized) | Fail startup; wait for `NexoraRuntime.init()` to complete. |
| `checkpoint` | `NXR-1003` (Save Failed) | Retry once; if persistent, transition workspace to `SUSPENDED` status. |
| `resume` | `NXR-1004` (Restore Failed) | Purge corrupt checkpoint; fall back to prior valid checkpoint; notify user. |
| | `NXR-3004` (Task Timeout) | Gracefully abort active runner; capture partial log outputs. |
