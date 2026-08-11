# Decision #7 — Retry Attempt State and Durability

> **Status: CANONICAL** for retry attempt state ownership, durability, and reconstruction semantics.
> This document resolves the open architecture decisions identified in the retry-lifecycle audit (NEXORA #7).
> All other documents (models, schemas, state machines, protocols, APIs) MUST align with the decisions below.

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

## DEC-2 — RetryPending State Durability

**Decision:** RetryPending state is **EPHEMERAL** — it does not survive process death.

**Rationale:**
- `BACKGROUND_EXECUTION.md` explicitly distinguishes checkpoint resume (durable) from retry (unspecified). [cite:1]
- No `retryDueAt`, `nextRetryAt`, or `backoff_until` field exists in the schema. [cite:1]
- Treating RetryPending as ephemeral simplifies persistence and aligns with the checkpoint-vs-retry distinction. [cite:1]

**Required behavior:** On process death, any Task in `RetryPending` state must transition to a defined post-crash state (see GAP-2 clarification below). [cite:1]

---

## DEC-2A — RetryPending State Durability (Conditional: Not Applicable)

**Decision:** Not applicable — DEC-2 = Ephemeral, so no retry-scheduling state is persisted or reconstructed. [cite:1]

**Implication:** BootReceiver does not reconstruct RetryPending state. Tasks in RetryPending at crash time are handled via the post-crash transition path defined in GAP-2. [cite:1]

---

## DEC-3 — Post-Recovery Execution Projection

**Decision:** After process-death recovery reconciliation, the preserved existing Execution semantically fits `ExecutionStatus.CREATED` because:
- The Execution identity (`executionId`, `correlationId`) is durably preserved via R4 evidence.
- The Execution is not currently running and is awaiting future start from `Queued` state.
- `CREATED` is the canonical ExecutionStatus for an execution record that exists but is not currently executing and is awaiting future start from Queued. [cite:models/Execution.md]
- Selecting `CREATED` does not create a new Execution; it designates the existing preserved Execution's status.
- `retryAttempt` is unchanged (per DEC-1, scoped per-Execution, no increment on post-death recovery). [cite:1]
- `version` is unchanged (no checkpoint resume occurs; per RUNTIME.md §ExecutionStatus Lifecycle, only explicit checkpoint/resume transitions increment version).
- `priorExecutionId` is unchanged (the preserved Execution retains its identity).
- No new Execution is created (the existing Execution's status is designated as CREATED).
- Identity is preserved: same `executionId`, `correlationId` across the recovery boundary.

**What CREATED does not mean**:
- It does not mean the Execution is ready to run immediately without transitioning through QUEUED and start().
- It does not mutate `retryAttempt` or consume retry budget.
- It does not signal a terminal retry (PATH B).

**Identity behavior**:
- Same `executionId` retained across the recovery boundary.
- Same `correlationId` retained (stable tracing across same-identity resumes).
- Same `taskId` retained; the Execution remains scoped to its original Task.

**Version behavior**:
- `version` is unchanged at reconciliation.
- Version increments only on explicit checkpoint/resume transitions, not on status designation.

**retryAttempt behavior**:
- Unchanged from pre-crash value.
- Per DEC-1, `retryAttempt` is scoped per-Execution and does not increment on post-death recovery.

**No new Execution**:
- The existing Execution is designated `CREATED`; no new `executionId` is generated.

**Compatible schema state**:
- `execution.status = CREATED` [cite:models/Execution.md]
- `execution.retryAttempt = <unchanged value>` [cite:DEC-1]
- `execution.version = <unchanged value>` [cite:RUNTIME.md]
- `execution.priorExecutionId = <unchanged or null>` [cite:DEC-1]
- `task.status = QUEUED` (the Task transitions to QUEUED after recovery reconciliation). [cite:state-machines/TaskLifecycle.md]

---

## DEC-4 — Process-Death Recovery Ownership

**Decision:** Process-death recovery responsibility is separated as follows:
- **BootReceiver** = startup trigger: detects process death / device reboot and initiates recovery. [cite:specs/BACKGROUND_EXECUTION.md §5.7]
- **Explicit recovery reconciliation responsibility** = detection + reconciliation: identifies affected Tasks, validates R4 evidence, and designates post-recovery Execution status. [cite:decisions/DEC-7-retry-attempt-state.md DEC-7.3]
- **TaskScheduler** = ordinary scheduling owner after Task returns to Queued: schedules Tasks back into the execution queue after reconciliation commits them to QUEUED. [cite:architecture/RUNTIME.md §Service Inventory]
- **Executor** = ExecutionStatus lifecycle owner: manages ExecutionStatus transitions (CREATED→RUNNING→COMPLETED/FAILED) per RUNTIME.md §ExecutionStatus Lifecycle. [cite:architecture/RUNTIME.md §ExecutionStatus Lifecycle]
- **WorkManager** = infrastructure: provides scheduled/periodic job mechanisms; does not own retry policy or Execution lifecycle decisions. [cite:specs/BACKGROUND_EXECUTION.md §1-8]

---

## DEC-5 — Startup Eligibility + Duplicate/Idempotency Semantics

**Decision:** The semantic eligibility predicate for process-death recovery is defined in terms of durable R4 evidence:

**Eligible iff** all of the following are durably true:
- R4 evidence identifies the affected Task [cite:specs/DATABASE_SCHEMA.md `execution` table + R4 convention]
- R4 evidence identifies the preserved existing Execution [cite:models/Execution.md `execution` row]
- R4 evidence proves the relevant RetryPending provenance [cite:decisions/DEC-7-retry-attempt-state.md GAP-2]
- R4 evidence represents process-death recovery (not ordinary retry or checkpoint resume) [cite:specs/BACKGROUND_EXECUTION.md GAP-2]
- R4 evidence is unreconciled (has not yet been committed to the reconciliation result) [cite:protocol-level idempotency guards]
- R4 evidence is not stale or conflicting with current persisted state [cite:protocol-level version checks]
- R4 evidence is compatible with current persisted state (no newer authoritative lifecycle/version boundary invalidates it) [cite:RUNTIME.md §ExecutionStatus Lifecycle versioning]
- R4 evidence is not invalidated by a newer checkpoint or transition [cite:protocol-level expectedVersion guards]

**Explicitly excluded** (ineligible, reconciliation rejected):
- ordinary `Queued` — no R4 evidence present; task is in normal lifecycle flow [cite:state-machines/TaskLifecycle.md]
- `Running` — Execution is actively in progress; recovery does not apply mid-execution [cite:models/Execution.md]
- `checkpoint recovery` — checkpoint resume is a distinct path (different from process-death recovery); R4 evidence from checkpoint resume is handled per RUNTIME.md §ExecutionStatus Lifecycle [cite:architecture/RUNTIME.md]
- `terminal retry` — PATH B explicit retry after committed terminal state; creates new executionId [cite:decisions/DEC-7-retry-attempt-state.md GAP-2]
- `ordinary retry` — RetryPending → Queued → start() path; not process-death recovery [cite:state-machines/TaskLifecycle.md RETRY_PENDING→Queued→start]
- already reconciled evidence — if R4 evidence was already committed as reconciliation result, it is not eligible for re-reconciliation [cite:protocol-level idempotency guards]
- `stale` or `conflicting` evidence — R4 evidence contradicted by newer persisted state (status, version, retryAttempt) [cite:protocol-level conflict detection]
- `unrelated` Execution records — R4 evidence from a different Execution/scoped per-Execution [cite:DEC-1 per-Execution scoping]

**Duplicate handling guarantee**:
- First valid reconciliation commits recovery: the first durable R4 evidence observation that passes all eligibility checks commits the recovery result atomically. [cite:protocol-level atomic commit]
- Later observations converge to committed result or are rejected as stale/already reconciled: subsequent observations that fail eligibility checks are rejected without side effects; they do not create a new Execution, do not increment `retryAttempt`, do not consume retry budget, and do not mutate `priorExecutionId`. [cite:protocol-level idempotency guards + version checks]
- No new Execution: the committed result designates the existing preserved Execution's status; no new `executionId` is generated. [cite:DEC-7.3]
- No `retryAttempt` increment: the existing Execution's `retryAttempt` is unchanged. [cite:DEC-1]
- No budget consumption: retry budget is not consumed for already-committed recovery. [cite:DEC-7 retry budget semantics]
- No `priorExecutionId` mutation: the existing Execution retains its identity. [cite:DEC-1]
- No second semantic Task transition: the Task moves once to QUEUED (if not already there); no duplicate Task state change occurs. [cite:state-machines/TaskLifecycle.md]
- No duplicated non-idempotent side effect: the reconciliation is designed to be idempotent; repeated observations produce the same committed result. [cite:specs/DATABASE_SCHEMA.md append-only + idempotency guards]

---

## DEC-6 — Post-Recovery Scheduling

**Decision:** After process-death recovery reconciliation commits the result (Execution designated CREATED, Task designated QUEUED), the following is the post-recovery scheduling flow:
- **Recovery → Queued → TaskScheduler**: After reconciliation, the Task is in QUEUED state and re-enters the normal TaskScheduler scheduling lifecycle. [cite:state-machines/TaskLifecycle.md QUEUED→start()]
- **no retryAttempt increment**: the existing Execution's `retryAttempt` is unchanged through the recovery boundary. [cite:DEC-1]
- **no budget consumption**: retry budget is not consumed; the recovery is not an ordinary retry. [cite:DEC-7 retry budget semantics]
- **no restoration of RetryPending deadline**: RetryPending is EPHEMERAL and does not survive process death; no deadline is restored. [cite:decisions/DEC-7-retry-attempt-state.md DEC-2]
- **no PATH A retry**: PATH A (RetryPending retry) preserves `executionId` and applies backoff — this is inapplicable because RetryPending is ephemeral and lost on process death. [cite:decisions/DEC-7-retry-attempt-state.md DEC-2A]
- **no PATH B retry**: PATH B (terminal retry via `retryExecution`) creates a new `executionId` — this is inapplicable because the recovery designates the existing Execution's status, not a new Execution. [cite:decisions/DEC-7-retry-attempt-state.md GAP-2]
- **recovered queued task re-enters normal scheduling lifecycle only after reconciliation**: the TaskScheduler schedules the Task from QUEUED via ordinary `start()` transition when the agent loop is available. [cite:state-machines/TaskLifecycle.md QUEUED→start()]

---

## DEC-7 — Recovery Evidence Retention

**Decision:** The minimum correctness requirement for R4 (recovery evidence) retention is:
- R4 evidence must survive until the recovery outcome is durably established.
- Minimum lifetime is until durable reconciliation: R4 evidence must be retained at least through the point where the recovery result (Execution CREATED, Task QUEUED) is durably persisted in the Room database. [cite:specs/DATABASE_SCHEMA.md Room persistence durability]
- Post-reconciliation retention remains independently unspecified unless the repository explicitly defines it: after the recovery outcome is durably established, whether R4 evidence continues to be retained is not defined by this decision and would require a separate architectural decision. [cite:no broader rule exists in repository]
- It is acceptable to document: "minimum lifetime is until durable reconciliation; post-reconciliation retention remains independently unspecified unless the repository explicitly defines it." [cite:decision rationale]

---

## DEC-8 — Concrete R4 Persistence Placement

**Decision:** After DEC-7.1 through DEC-7.7 are closed, the repository supports a concrete persistence placement for R4 (recovery evidence) as a dedicated Room artifact:
- R4 is represented as a dedicated Room recovery-evidence persistence artifact, stored in a dedicated schema location.
- R4 is **separate from**: `task` table, `execution` table, `execution_checkpoint` table, `execution_replay` table, lifecycle-history storage, and durable `RetryPending` state. [cite:specs/DATABASE_SCHEMA.md table isolation]
- R4 persistence placement is documented in `specs/DATABASE_SCHEMA.md` as a dedicated recovery-evidence table/column arrangement, separate from the core execution/task lifecycle tables. [cite:specs/DATABASE_SCHEMA.md documentation update]
- The narrowest compatible option is chosen: a dedicated recovery-evidence artifact that satisfies the eligibility predicate (DEC-7.5) without altering core lifecycle tables. [cite:architectural minimalism]
- R4 is not implemented as a new entity/DAO/migration code: this decision is documentation-only, updating the schema description to identify the R4 placement. [cite:editing rules — do not implement schema code]

---

## Decision Record Metadata

- **Decision ID:** DEC-7
- **Date:** 2026-08-11
- **Status:** CANONICAL
- **Owners:** Architecture Owner (retry lifecycle)
- **Related Audit:** NEXORA #7 — Corrected Architecture Decision Package