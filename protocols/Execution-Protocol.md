> **Status: DERIVED** for Execution message contract.
> This document defines protocol messages for Execution operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical runtime and execution lifecycle sources.
> Referenced by: APIs, SDKs, tasks, workflows, and tests.

# Execution Protocol — Nexora

> Communication and wire contract between the Orchestration Engine, CheckpointManager, and TaskScheduler.

## Execution Lifecycle Flow

```
Orchestration Engine         CheckpointManager          TaskScheduler
         │                           │                        │
         ├─────── start() ──────────>│                        │
         │                           │                        │
         ├────────────────── checkpoint() ───────────────────>│
         │                           │                        │
         │<─────────────── CheckpointCommitted ───────────────┤
         │                                                    │
         ├────────────────── complete() ─────────────────────>│
```

1. **Instantiation**: Creates a new `Execution` with stable `correlationId`.
2. **Periodic Checkpointing**: Every 30s, serializes execution frames; `CheckpointManager` commits via ACID SQLite.
3. **RESUME**: Recoverable interruption resumes same `executionId` with `correlationId` unchanged and `version` incremented.
4. **RETRY_AFTER_TERMINAL**: Explicit retry after terminal (`FAILED`/`CANCELLED`/`COMPLETED`) creates new `executionId` with `priorExecutionId` linking the terminal predecessor.
5. **Outcome Roll-up**: Terminal outcomes (`COMPLETED`, `FAILED`, `CANCELLED`) are committed and final; no terminal-to-RUNNING transition.

### Recovery Operations

```kotlin
enum class ExecutionRecoveryOperation { RESUME, RETRY_AFTER_TERMINAL }

data class ExecutionRecoveryCommand(
    val operation: ExecutionRecoveryOperation,
    val executionId: String,
    val priorExecutionId: String?,
    val checkpointId: String?,
    val correlationId: String,
    val expectedVersion: Long,
    val idempotencyKey: String
)
```

RESUME: same `executionId`, `priorExecutionId` unchanged, `correlationId` unchanged, `version` increases.
RETRY_AFTER_TERMINAL: new `executionId`, `priorExecutionId` = terminal predecessor, predecessor remains terminal, lineage acyclic.

## Protocol Messages

### Checkpoint Write Command

```kotlin
data class SaveCheckpointMessage(
    val correlationId: String,
    val executionId: String,
    val checkpointId: String,
    val version: Long,
    val frame: JsonObject,
    val isIdempotentReplaySafe: Boolean
)
```

### Execution Status Changed Event

```kotlin
data class ExecutionStatusChangedEvent(
    val eventId: String,
    val correlationId: String,
    val executionId: String,
    val fromStatus: ExecutionStatus,
    val toStatus: ExecutionStatus,
    val currentPhase: ExecutionPhase,
    val version: Long,
    val occurredAt: Instant,
    val errorEnvelope: CanonicalErrorEnvelope? = null
)
```

## Protocol Conformance Rules

- **ACID Integrity**: A checkpoint write MUST complete transactionally. Partial or fragmented checkpoint frames are invalid; any serialization exception MUST throw `NXR-1003` and preserve the prior valid checkpoint intact on disk.
- **Deduplication**: Execution events MUST be deduplicated by consumers using `(executionId, version, transition)`.
- **Idempotency Replay**: Checkpoints MUST store whether in-progress tool executions were declared idempotent. Non-idempotent tool calls in progress MUST NOT be replayed on resume; they must be reconciled using their stored transaction histories.
