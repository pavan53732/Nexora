> **Status: DERIVED** for Execution message contract.
> This document defines protocol messages for Execution operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical runtime and execution lifecycle sources.
> Referenced by: APIs, SDKs, tasks, workflows, and tests.

# Execution Protocol — Nexora

> Communication and wire contract between the Orchestration Engine, CheckpointManager, and TaskScheduler.

## Execution Lifecycle Flow

```text
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

1. **Instantiation**: The Orchestration Engine initializes a new `Execution` session, assigns a stable `correlationId`, and requests a CPU wake lock from the Android OS.
2. **Periodic Checkpointing**: During the running loop, the engine serializes execution frames every 30s. The `CheckpointManager` commits these frames using ACID SQLite writes, returning a `CheckpointCommitted` event.
3. **Automatic Re-scheduling**: If the device loses network or runs low on battery, the `TaskScheduler` registers a WorkManager job, suspends FGS execution, and waits for charging/wifi constraints before re-triggering resume.
4. **Outcome Roll-up**: Upon final step validation, the engine commits terminal outcomes (`COMPLETED` or `FAILED`) and publishes the final event.

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
