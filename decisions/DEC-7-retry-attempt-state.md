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
- Execution is the canonical unit of retry lineage (`priorExecutionId` field). [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]
- Task identity remains stable across retries; Execution identity encodes retry attempts. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]
- Aligns with `version` and `checkpointId` fields, which are already Execution-scoped. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]

**Required schema update:** Add `retryAttempt INTEGER NOT NULL DEFAULT 0` to the `execution` table in `specs/DATABASE_SCHEMA.md`. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]
**Required model update:** Add `val retryAttempt: Int` to the `Execution` data class in `models/Execution.md`. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]
**Scope:** `retryAttempt` is scoped per-Execution, not per-Task. Each retry that creates a new Execution increments this counter. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]

---

## DEC-2 — RetryPending State Durability

**Decision:** RetryPending state is **EPHEMERAL** — it does not survive process death.

**Rationale:**
- `BACKGROUND_EXECUTION.md` explicitly distinguishes checkpoint resume (durable) from retry (unspecified). [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]
- No `retryDueAt`, `nextRetryAt`, or `backoff_until` field exists in the schema. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]
- Treating RetryPending as ephemeral simplifies persistence and aligns with the checkpoint-vs-retry distinction. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]

**Required behavior:** On process death, any Task in `RetryPending` state must transition to a defined post-crash state (see DEC-7.7–DEC-7.12 below). [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]

---

## DEC-2A — RetryPending State Durability (Conditional: Not Applicable)

**Decision:** Not applicable — DEC-2 = Ephemeral, so no retry-scheduling state is persisted or reconstructed. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]

**Implication:** BootReceiver does not reconstruct RetryPending state. Tasks in RetryPending at crash time are handled via the post-crash transition path defined in DEC-7.7–DEC-7.12. [repository evidence: models/Execution.md; specs/DATABASE_SCHEMA.md; state-machines/TaskLifecycle.md]

---

## DEC-7 Secondary Decisions — Process-Death Recovery Closure

This section closes the secondary decisions requested by the DEC-7 recovery audit. The labels below are the authoritative labels for this closure: DEC-7.7 through DEC-7.12. The earlier DEC-3 through DEC-8 headings in the prior record were descriptive placeholders and are superseded by these labels.

### DEC-7.7 — Post-Recovery Execution Projection

**Question:** Which `ExecutionStatus` represents the preserved Execution after process-death recovery reconciliation?

**Repository evidence:**
- `models/Execution.md` defines the status set `CREATED`, `RUNNING`, `COMPLETED`, `FAILED`, and `CANCELLED`.
- `architecture/RUNTIME.md` §ExecutionStatus Lifecycle defines `CREATED` as an execution record that exists and has not yet started; it separately defines `RUNNING` as active execution and the other statuses as completed, failed, or cancelled outcomes.
- `architecture/RUNTIME.md` §ExecutionStatus Lifecycle states that checkpoint resume is a distinct path and increments `version`; terminal retry creates a new Execution.
- `state-machines/TaskLifecycle.md` defines `Queued → Running` through `start()` and identifies `RetryPending → Queued` as the ordinary retry transition.

**Candidates and analysis:** `RUNNING` is excluded because reconciliation does not execute the Task. Terminal statuses are excluded because recovery is not a terminal outcome. A checkpoint-resume projection is excluded by the locked DEC-7 invariant that no checkpoint resume occurs. `CREATED` is therefore the narrowest compatible projection for an existing Execution awaiting future start after the Task is returned to `Queued`.

**Selected decision:** After successful process-death recovery reconciliation, the preserved existing Execution is projected as `ExecutionStatus.CREATED`.

**Classification:** EVIDENCE-SUPPORTED ARCHITECTURE DECISION.

**Consequences:** The same `executionId`, `correlationId`, `taskId`, `retryAttempt`, and `priorExecutionId` remain associated with the Execution. The Execution status does not become `RUNNING` during reconciliation. `version` remains unchanged by this status designation; the repository documents version advancement for checkpoint/resume transitions, and this recovery path is not checkpoint resume.

**Non-consequences:** `CREATED` does not mean a new Execution was created, a retry attempt occurred, retry budget was consumed, a checkpoint was resumed, or PATH A/PATH B retry was performed.

**Implementation status:** NOT IMPLEMENTED; documentation-only architecture closure.

### DEC-7.8 — Process-Death Recovery Ownership

**Question:** Which responsibility owns startup triggering, detection, reconciliation, ordinary retry scheduling, Execution lifecycle, and infrastructure?

**Repository evidence:**
- `specs/BACKGROUND_EXECUTION.md` §3 states that `BootReceiver` checks incomplete executions after app kill or device restart and starts the background execution path for checkpoint resume; the DEC-7 clarification in that document explicitly excludes reconstruction of `RetryPending`.
- `architecture/RUNTIME.md` §Service Inventory identifies `Executor` as managing execution state and `Background Runtime` as the background execution boundary.
- `architecture/RUNTIME.md` §ExecutionStatus Lifecycle assigns ExecutionStatus lifecycle semantics to the Executor.
- `state-machines/TaskLifecycle.md` §Implementation Notes assigns automatic Task transition driving and RetryPending backoff behavior to `TaskScheduler`.
- `specs/BACKGROUND_EXECUTION.md` §1 identifies WorkManager as the mechanism for scheduled and deferred work.

**Candidates and analysis:** BootReceiver is a trigger, not the owner of Task or Execution lifecycle semantics. TaskScheduler owns ordinary queue and retry scheduling, not process-death reconciliation. Executor owns ExecutionStatus lifecycle, not the Task lifecycle. WorkManager supplies execution infrastructure, not recovery policy. The repository does not establish a named existing component that owns the cross-entity R4 detection/reconciliation boundary.

**Selected decision:** BootReceiver is the startup trigger; an explicit documentation-level process-death recovery responsibility detects and reconciles eligible R4 evidence; TaskScheduler owns ordinary scheduling after `Queued`; Executor owns ExecutionStatus transitions; WorkManager remains infrastructure. The reconciliation responsibility is not a new implementation class or module.

**Classification:** EVIDENCE-SUPPORTED ARCHITECTURE DECISION with an explicit responsibility boundary.

**Caveat:** The repository does not establish a concrete implementation owner for the cross-entity reconciliation responsibility. That implementation choice remains separate from this documentation decision.

**Implementation status:** NOT IMPLEMENTED; documentation-only architecture closure.

### DEC-7.9 — Startup Eligibility and Duplicate / Idempotency Semantics

**Question:** When may startup recovery reconcile R4 evidence, and what happens when the same evidence is observed more than once?

**Repository evidence:**
- `specs/DATABASE_SCHEMA.md` is canonical for Room persistence and documents separate `execution`, `execution_checkpoint`, and `execution_replay` storage.
- `state-machines/TaskLifecycle.md` §Normative Transition Contract requires guards against current persisted version, durable persistence before event publication, rejection of invalid transitions without mutation, and duplicate-command convergence through an idempotency key; it also requires event deduplication by entity and transition version.
- `architecture/RUNTIME.md` §ExecutionStatus Lifecycle separates ExecutionStatus from TaskStatus and defines versioned checkpoint/resume and terminal-retry behavior.
- `models/Execution.md` §Retry Lineage defines `priorExecutionId` only for explicit retry/restart after a committed terminal state.

**Selected decision:** R4 evidence is eligible only when all of the following are true: it identifies the affected Task; identifies the preserved existing Execution; proves the relevant RetryPending provenance; represents process-death recovery rather than ordinary retry or checkpoint recovery; is unreconciled; is compatible with the current Task and Execution projections; has no newer authoritative lifecycle or version boundary; and has no stale or conflicting evidence.

The following are explicitly ineligible: ordinary `Queued`; `Running`; checkpoint recovery; terminal retry; ordinary RetryPending retry; already reconciled evidence; stale or conflicting evidence; and evidence for an unrelated Execution.

The first valid reconciliation commits one recovery result. A later observation converges to that committed result or is rejected as already reconciled or stale. It must not create another Execution, increment `retryAttempt`, consume retry budget, mutate `priorExecutionId`, perform a second semantic Task transition, or repeat a non-idempotent side effect. No concrete key format is introduced; existing lifecycle version and idempotency-key semantics are reused where applicable.

**Atomicity contract:** Successful reconciliation must durably establish one coherent projection: Task = `Queued`; the preserved Execution identity and selected status; unchanged `retryAttempt`; unchanged `priorExecutionId`; unchanged retry budget; and R4 evidence marked reconciled. A failed reconciliation must not be represented as successful recovery. `state-machines/TaskLifecycle.md` provides the required atomic transition and durable-persistence semantics; this decision does not claim that a concrete reconciliation transaction is implemented.

**Classification:** ARCHITECTURE CONTRACT grounded in existing lifecycle/version/idempotency semantics; not an implementation claim.

**Implementation status:** NOT IMPLEMENTED; documentation-only architecture closure.

### DEC-7.10 — Post-Recovery Scheduling

**Question:** What happens after successful process-death reconciliation?

**Repository evidence:** `state-machines/TaskLifecycle.md` defines `Queued → Running` through `start()` and identifies `TaskScheduler` as the driver of automatic Task transitions. `specs/BACKGROUND_EXECUTION.md` distinguishes retryable failure handling from checkpoint resume. DEC-7 locks RetryPending as ephemeral.

**Selected decision:** The path is `Recovery → Queued → normal TaskScheduler scheduling lifecycle`. Recovery is not ordinary retry. It does not increment `retryAttempt`, consume retry budget, restore the previous RetryPending deadline, perform PATH A, perform PATH B, or resume a checkpoint. The recovered Task re-enters normal scheduling only after reconciliation succeeds.

**Classification:** EVIDENCE-SUPPORTED ARCHITECTURE DECISION constrained by locked DEC-7 invariants.

**Implementation status:** NOT IMPLEMENTED; documentation-only architecture closure.

### DEC-7.11 — Recovery-Evidence Retention

**Question:** How long must R4 evidence remain available?

**Repository evidence:** `specs/DATABASE_SCHEMA.md` establishes Room as the authoritative structured persistence store and defines retention policies for documented tables, but does not define a post-reconciliation R4 retention period.

**Selected decision:** Unreconciled R4 evidence must survive until the recovery outcome is durably established. It must not be removed while correctness depends on it. Post-reconciliation retention and deletion remain unspecified and require a separate decision if needed; no duration and no indefinite audit-retention policy are introduced here.

**Classification:** MINIMUM CORRECTNESS REQUIREMENT supported by the documented persistence boundary.

**Implementation status:** NOT IMPLEMENTED; documentation-only architecture closure.

### DEC-7.12 — Concrete R4 Persistence Placement

**Question:** Where is durable process-death recovery evidence placed?

**Repository evidence:** `specs/DATABASE_SCHEMA.md` is canonical for the Room relational store and separates Task, Execution, checkpoint, and replay persistence. `state-machines/TaskLifecycle.md` separates current lifecycle projection from transition semantics. No existing table is identified as the semantic owner of R4 evidence.

**Candidates and analysis:** Placing R4 in `task` or `execution` would merge recovery evidence with a current-state projection. Placing it in `execution_checkpoint` or `execution_replay` would merge process-death recovery with checkpoint or tool-replay semantics. Placing it in lifecycle history would merge evidence with history storage. Persisting RetryPending itself would contradict DEC-2. A dedicated Room recovery-evidence artifact is the narrowest compatible placement.

**Selected decision:** R4 is a dedicated Room recovery-evidence persistence artifact, conceptually separate from `task`, `execution`, `execution_checkpoint`, `execution_replay`, lifecycle-history storage, and durable RetryPending state. The artifact is retained through durable reconciliation according to DEC-7.11.

**Classification:** ARCHITECTURE DECISION; schema placement is documented, not implemented.

**Caveat:** The storage shape of this artifact (entity name, columns, keys, indexes, and status semantics) is defined by the `recovery_evidence` table in `specs/DATABASE_SCHEMA.md`. Concrete DAO operations, migrations, SQL, and post-reconciliation retention duration remain future implementation/specification work.

**Implementation status:** NOT IMPLEMENTED; documentation-only architecture closure.

---

## Atomicity and Evidence Contract

The DEC-7 recovery boundary is a semantic consistency contract, not a claim about an existing implementation transaction. A successful reconciliation must durably establish the Task projection `Queued`, the Execution projection `CREATED`, and the reconciled R4 evidence together while preserving the existing Execution identity, `retryAttempt`, `priorExecutionId`, retry budget, and absence of checkpoint resume. A failed reconciliation must leave no false semantic success and must not publish a success result for an uncommitted recovery.

The existing Task lifecycle contract in `state-machines/TaskLifecycle.md` requires guards against current persisted version, durable persistence before event publication, one semantic transition event after commit, and rejection of invalid or conflicting commands without state mutation. DEC-7 adopts those semantics at the architecture level without asserting that R4 reconciliation has been implemented.

---

## Decision Record Metadata

- **Decision ID:** DEC-7
- **Date:** 2026-08-11
- **Status:** CANONICAL
- **Owners:** Architecture Owner (retry lifecycle)
- **Related Audit:** NEXORA #7 — Corrected Architecture Decision Package

## Non-goals and guardrails

This decision establishes retry-attempt identity semantics only. It does not by itself authorize unbounded retry behavior. Retry orchestration remains subject to bounded progress, failure classification, and retry-storm prevention requirements defined by the execution and agent runtime specifications.
