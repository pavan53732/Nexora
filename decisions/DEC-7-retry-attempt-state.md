# Decision #7 — Retry Attempt State and Durability

> **Status: CANONICAL** for retry attempt state ownership, durability, and reconstruction semantics.
> This document resolves the open architecture decisions identified in the retry-lifecycle audit (NEXORA #7).
> All other documents (models, schemas, state machines, protocols, APIs) MUST align with the decisions below.
>
> Depends on: [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md), [../models/Task.md](../models/Task.md), [../models/Execution.md](../models/Execution.md), [../specs/DATABASE_SCHEMA.md](../specs/DATABASE_SCHEMA.md), [../specs/BACKGROUND_EXECUTION.md](../specs/BACKGROUND_EXECUTION.md).
> Referenced by: retry implementation, BootReceiver, TaskScheduler, persistence layer.

---

## DEC-1 — Retry Attempt Index Ownership

**Decision:** The authoritative retry-attempt index (`retryAttempt`, 0-based) is stored on the **Execution** model.

**Rationale:**
- Execution is the canonical unit of retry lineage (`priorExecutionId` field). [cite:1]
- Task identity remains stable across retries; Execution identity encodes retry attempts. [cite:1]
- Aligns with `version` and `checkpointId` fields, which are already Execution-scoped. [cite:1]

**Required schema update:** Add `retryAttempt INTEGER NOT NULL DEFAULT 0` to the `execution` table in `specs/DATABASE_SCHEMA.md`. [cite:1]

**Required model update:** Add `val retryAttempt: Int` to the `Execution` data class in `models/Execution.md`. [cite:1]

**Scope:** `retryAttempt` is scoped per-Execution, not per-Task. Each retry that creates a new Execution increments this counter. [cite:1]

---

## DEC-2A — RetryPending State Durability

**Decision:** RetryPending state is **EPHEMERAL** — it does not survive process death.

**Rationale:**
- `BACKGROUND_EXECUTION.md` explicitly distinguishes checkpoint resume (durable) from retry (unspecified). [cite:1]
- No `retryDueAt`, `nextRetryAt`, or `backoff_until` field exists in the schema. [cite:1]
- Treating RetryPending as ephemeral simplifies persistence and aligns with the checkpoint-vs-retry distinction. [cite:1]

**Required behavior:** On process death, any Task in `RetryPending` state must transition to a defined post-crash state (see GAP-2 clarification below). [cite:1]

---

## DEC-2B — Retry Scheduling on Reconstruction (Conditional: Not Applicable)

**Decision:** Not applicable — DEC-2A = Ephemeral, so no retry-scheduling state is persisted or reconstructed. [cite:1]

**Implication:** BootReceiver does not reconstruct RetryPending state. Tasks in RetryPending at crash time are handled via the post-crash transition path defined in GAP-2. [cite:1]

---

## GAP-2 — Execution Identity Clarification

**Clarification:**
1. **PATH A (RetryPending retry):** Preserves `executionId`. No new Execution is created; the same Execution continues after backoff. [cite:1]
2. **PATH B (terminal retry via `retryExecution`):** Creates a new `executionId` with `priorExecutionId` referencing the terminal predecessor. [cite:1]
3. **retryAttempt numbering:** Scoped per-Execution (DEC-1). PATH A does not increment `retryAttempt`; PATH B increments `retryAttempt` on the new Execution. [cite:1]

---

## GAP-4 — TaskScheduler Authority Boundary

**Clarification:** TaskScheduler owns:
- Policy decision ("should retry?") — CANONICAL. [cite:1]
- Transition `RetryPending → Queued` — CANONICAL. [cite:1]
- Enforce `retries < max` — CANONICAL. [cite:1]

TaskScheduler does **not** own:
- Compute retry delay — UNSPECIFIED (deferred to implementation). [cite:1]
- Create/start/cancel retry timer — UNSPECIFIED (deferred to implementation). [cite:1]
- Persist/restore retry state — UNSPECIFIED (DEC-2A = Ephemeral makes this moot). [cite:1]

---

## GAP-5 — Idempotency Scope

**Clarification:**
- **PATH A (RetryPending retry):** Preserves the same `idempotencyKey` and `executionId`. No new idempotency boundary is created. [cite:1]
- **PATH B (terminal retry via `retryExecution`):** Creates a new `executionId` and a new idempotency boundary. The new Execution may carry a new `idempotencyKey` or inherit the prior one, depending on client semantics. [cite:1]
- **Idempotency scope:** Per-Execution, not per-Task or per-retry-attempt. [cite:1]

---

## Retry-After Interaction

**Finding:** No canonical interaction between `Retry-After` (Provider Layer) and Task `RetryPending` is specified. [cite:1]

**Status:** No precedence decision is justified. Provider Layer handles `Retry-After` independently; Task retry semantics are unchanged. [cite:1]

---

## Affected Artifacts

- `models/Execution.md` — add `retryAttempt: Int`. [cite:1]
- `specs/DATABASE_SCHEMA.md` — add `retryAttempt INTEGER NOT NULL DEFAULT 0` to `execution` table. [cite:1]
- `state-machines/TaskLifecycle.md` — clarify RetryPending durability (EPHEMERAL) and post-crash transition path. [cite:1]
- `specs/BACKGROUND_EXECUTION.md` — clarify BootReceiver does not reconstruct RetryPending state. [cite:1]
- `protocols/Execution-Protocol.md` — clarify PATH A vs PATH B executionId semantics. [cite:1]
- `docs/api/Runtime-API.md` — clarify idempotencyKey behavior for PATH A vs PATH B. [cite:1]

---

## Implementation Impact

- Determines which table/column stores the attempt counter (`execution.retryAttempt`). [cite:1]
- Affects whether attempt number is scoped per-Task or per-Execution (per-Execution). [cite:1]
- Constrains API shape for retry operations (PATH A vs PATH B). [cite:1]
- BootReceiver reconstruction logic is simplified (no RetryPending state to restore). [cite:1]

---

## Dependencies

- DEC-1 → DEC-2B (not applicable, DEC-2A = Ephemeral). [cite:1]
- DEC-2A → DEC-2B (conditional, not applicable). [cite:1]
- GAP-2 → GAP-5 (execution identity affects idempotency boundary). [cite:1]

---

## Decision Record Metadata

- **Decision ID:** DEC-7
- **Date:** 2026-08-11
- **Status:** CANONICAL
- **Owners:** Architecture Owner (retry lifecycle)
- **Related Audit:** NEXORA #7 — Corrected Architecture Decision Package
