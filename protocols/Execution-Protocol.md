> **Status: DERIVED** for Execution message contract.
> This document defines protocol messages for Execution operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: [../architecture/RUNTIME.md](../architecture/RUNTIME.md) for the canonical Runtime and ExecutionStatus lifecycle sources.
> Referenced by: APIs, SDKs, tasks, workflows, and tests.

# Execution Protocol — Nexora

> Communication and wire contract between the Orchestration Engine, CheckpointManager, and TaskScheduler.



> **DEC-7 (2026-08-11):** PATH A (RetryPending retry) preserves `executionId`. PATH B (terminal retry via `retryExecution`) creates a new `executionId` with `priorExecutionId` referencing the terminal predecessor. See `decisions/DEC-7-retry-attempt-state.md`.

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
5. **ESCALATION**: User answer injected via `resolveEscalation` resumes nonterminal `BlockedAwaitingInput`; `executionId`/`correlationId` retained, `version` incremented. `escalationPayload` (stored on checkpoint) is cleared after resume.
6. **Outcome Roll-up**: Terminal outcomes (`COMPLETED`, `FAILED`, `CANCELLED`) are committed and final; no terminal-to-RUNNING transition.

### Recovery Operations

```kotlin
enum class ExecutionRecoveryOperation { RESUME, RETRY_AFTER_TERMINAL, ESCALATION }

data class EscalationRecoveryCommand(
    val executionId: String,
    val checkpointId: String,
    val correlationId: String,
    val expectedVersion: Long,
    val idempotencyKey: String,
    val escalationAnswer: JsonObject  // populated: user's response to resolveEscalation
)

data class ExecutionRecoveryCommand(
    val operation: ExecutionRecoveryOperation,
    val executionId: String,
    val priorExecutionId: String?,
    val checkpointId: String?,
    val correlationId: String,
    val expectedVersion: Long,
    val idempotencyKey: String,
    val escalationAnswer: JsonObject? = null  // populated for ESCALATION recovery; deprecated overload field (see Note below)
)

> **Note (deprecated Option A):** The `escalationAnswer` field on `ExecutionRecoveryCommand`
> exists for backward-compatible `RESUME` overloading. New implementations MUST use the dedicated
> `ESCALATION` operation and `EscalationRecoveryCommand` data class instead. `RESUME` with a
> non-null `escalationAnswer` is retained for legacy wire compatibility only.

data class ExecutionRecoveryCommitted(
    val operation: ExecutionRecoveryOperation,
    val executionId: String,
    val priorExecutionId: String?,
    val checkpointId: String?,
    val correlationId: String,
    val previousVersion: Long,
    val committedVersion: Long,
    val status: ExecutionStatus,
    val occurredAt: Instant
)
```

`RESUME` targets an existing interrupted nonterminal Execution: `executionId`,
`correlationId`, and lineage remain stable; `checkpointId` and `expectedVersion` are
required; the committed version increases. `RETRY_AFTER_TERMINAL` carries a new
`executionId`, requires `priorExecutionId` to reference the immediate terminal
predecessor, leaves that predecessor terminal, and preserves acyclic lineage.

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

data class TaskSuspendedEvent(
    val eventId: String,
    val correlationId: String,
    val taskId: String,
    val executionId: String,
    val checkpointId: String,
    val version: Long,
    val cause: String,
    val occurredAt: Instant
)

data class CheckpointSavedEvent(
    val eventId: String,
    val correlationId: String,
    val executionId: String,
    val checkpointId: String,
    val version: Long,
    val occurredAt: Instant
)
```

`TaskSuspendedEvent` is an execution/checkpoint event, not a new Task or Execution lifecycle state. `cause` records the existing platform/runtime trigger (for example, ANR safeguard or service handoff). `CheckpointSavedEvent` is emitted only after the checkpoint transaction commits. Both events are at-least-once and deduplicated by `(executionId, version, event type)`.

## Protocol Conformance Rules

- **ACID Integrity**: A checkpoint write MUST complete transactionally. Partial or fragmented checkpoint frames are invalid; any serialization exception MUST throw `NXR-1003` and preserve the prior valid checkpoint intact on disk.
- **Deduplication**: Execution events MUST be deduplicated by consumers using `(executionId, version, transition)`.
- **Idempotency Replay**: Checkpoints MUST store whether in-progress tool executions were declared idempotent. Non-idempotent calls MUST be reconciled from durable transaction history; safe incomplete idempotent calls MAY replay.
- **Recovery guards**: Reject terminal `RESUME`, nonterminal retry predecessors, missing checkpoint/prior ID, cyclic lineage, stale `expectedVersion`, and idempotency conflicts.
- **Versioning**: A successful recovery commit has `committedVersion > previousVersion`; consumers deduplicate by `(executionId, committedVersion, operation)`.


## Upgrade Notes

This protocol participates in the architecture upgrade for bounded progress, provenance-aware execution, and explicit failure classification. Implementations conforming to this protocol SHOULD preserve enough metadata to support retry policy, conflict handling, and verification.
