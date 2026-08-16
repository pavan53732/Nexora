> **Status: SUPPORTING** for execution lifecycle behavior.
> This document describes planning, pipeline resolution, and execution behavior but does not own formal task states.
> The canonical task state machine is [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md).
>
> Depends on: [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md), [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md), [../architecture/WORKFLOW_ENGINE.md](../architecture/WORKFLOW_ENGINE.md).
>
# Execution Lifecycle Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See also [../architecture/RUNTIME.md](../architecture/RUNTIME.md) · [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md) · [../docs/adr/ADR-0007-Skills-First-Class.md](../docs/adr/ADR-0007-Skills-First-Class.md) · [../registry/SKILLS.md](../registry/SKILLS.md)

---


> **DEC-7 (2026-08-11):** `RetryPending` is EPHEMERAL and is not reconstructed after process death. RetryPending retry (PATH A) preserves the same `executionId`; explicit retry after a committed terminal state via `retryExecution` (PATH B) creates a new `executionId` with `priorExecutionId` referencing the terminal predecessor. Idempotency is scoped per-Execution: PATH A preserves the same `idempotencyKey` and idempotency boundary; PATH B creates a new idempotency boundary. See [../decisions/DEC-7-retry-attempt-state.md](../decisions/DEC-7-retry-attempt-state.md).

## Overview

The AI determines **far more than tools and execution order**. For every goal, the
runtime resolves the full execution context: objective, tasks, agents, skills, tools,
plugins, providers, dependencies, permissions, ordering, parallelism, files, external
resources, validation criteria, error recovery, verification, and follow-up.

This spec defines that complete lifecycle and the software-engineering pipeline, formalizing a **Recursive Task Graph with Dynamic Plan Refinement** for long-running projects.
Before the Planner creates an ExecutionPlan, a pre-flight Project Introspection
pass (see [CONTEXT_MANAGEMENT.md](CONTEXT_MANAGEMENT.md) §8, FR-CM-009) reads
the workspace structure and populates a ProjectContext in working memory. The
Knowledge Graph is queried after introspection to retrieve relevant past entities.

> **Status: SUPPORTING.** Task state names referenced in this document (e.g. `RetryPending`, `WaitingApproval`) are defined canonically in [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md). This document describes lifecycle *behavior and pipeline resolution*, not state ownership. The canonical execution flow at the runtime level is defined in [../architecture/RUNTIME.md](../architecture/RUNTIME.md) §Execution Flow — this document expands on the planning, dependency resolution, and validation stages within that flow.

## 1. The Complete Execution Lifecycle

Given a user goal, Nexora automatically determines:

| # | What the AI determines | Resolved by | Where it lands |
|---|------------------------|-------------|----------------|
| 1 | The **objective** and expected outcome | Planner + Context Builder | Goal definition (acceptance criteria) |
| 2 | The required **tasks and subtasks** | Planner | ExecutionPlan |
| 3 | The complete **execution plan** | Planner | ExecutionPlan (steps + dependencies) |
| 4 | Which **specialized agent(s)** handle each task | Planner (via AgentRegistry) | Per-step agent assignment |
| 5 | Which **skills** are required | Planner (via SkillRegistry) | Per-step skill selection (FR-EL-004) |
| 6 | Which **tools** are required | Planner + Agent (via ToolRegistry) | Tool calls per step (FR-TL) |
| 7 | Which **plugins** are required | Planner + PluginManager | Dependency resolution (FR-EL-006) |
| 8 | Which **AI model/provider** suits each task | Planner (via ProviderRegistry) | Per-task provider profile (FR-EL-005) |
| 9 | Required **dependencies and runtime requirements** | Planner + Sandbox | Env template, package installs, runtimes |
| 10 | Required **permissions and approvals** | PermissionManager | Permission scopes per tool call (FR-S016 modes) |
| 11 | **Execution order and task dependencies** | Planner | ExecutionPlan dependencies |
| 12 | **Sequential vs parallel** execution | Executor (DAG analysis) | Parallel lanes for independent steps |
| 13 | Which **files** to create/read/modify | Agent (via VFS) | File plan in context (FR-M012 history) |
| 14 | Which **APIs, databases, external resources** to access | Agent (via tools) | Network/DB tools with egress policy (FR-S014) |
| 15 | How **progress** is tracked | Agent loop + EventBus | TaskProgress events (FR-A010) |
| 16 | **Validation criteria** for every step | Planner | Per-step pass/fail criteria (FR-EL-008) |
| 17 | **Error detection and recovery** strategies | Agent loop | Retry/fallback/checkpoint (FR-EL-009) |
| 18 | **Automatic retries** where appropriate | TaskScheduler | RetryPending + exponential backoff (NFR-REL-003) |
| 19 | **Reflection and self-review** after execution | Agent loop | Reflect phase (FR-EL-010) |
| 20 | **End-to-end testing** of completed work | Agent (via test tools) | Where applicable (FR-EL-011) |
| 21 | **Verification** the objective was achieved | Agent loop | Acceptance criteria re-check (FR-EL-011) |
| 22 | **Logs, reports, execution history** | Observability | ExecutionEvent stream, completion report (FR-EL-012) |
| 23 | **Knowledge and results** into project memory | MemoryManager | Memory stores (FR-M) |
| 24 | **Improvements / follow-up tasks** | Agent loop | Follow-up identification before completion (FR-EL-012) |

### Selection order (steps 4–9)

```
For each task:
  1. Determine required SKILLS (expertise)          -> SkillRegistry
  2. Determine applicable AGENTS (who has them)      -> AgentRegistry (skillsOf)
  3. Determine TOOLS (from skills + task needs)      -> ToolRegistry (requiredTools)
  4. Determine PROVIDER/MODEL (per task)             -> ProviderRegistry (profiles)
  5. Determine PLUGINS/DEPENDENCIES (missing pieces) -> PluginManager + Sandbox
  6. Validate: agent possesses skill; tool refs valid; permissions resolvable — if any fails, escalate to the user via `BlockedAwaitingInput` (TaskLifecycle `requestEscalation`); the planner does not silently degrade authority.
```

Skills are the **primary selection axis** (ADR-0007): the planner reasons in expertise
terms and resolves them to agents and tools.

Before queueing a task or workflow step, dependency references MUST be validated as an acyclic graph. A dependency cycle is rejected without queueing or execution. If a dependency later fails terminally, dependent work fails through the canonical Task lifecycle rather than remaining indefinitely blocked. Each task carries an effective deadline inherited by dependency waits, approval waits, capability clarification, provider rate-limit waits, and delegated children.


### Plan and acceptance artifact boundary

`ExecutionPlan` and `PlanStep` are the existing semantic plan projections (defined in `architecture/RUNTIME.md` §ExecutionPlan). Long-running tasks operate as a **Recursive Task Graph** where agents can dynamically spawn sub-plans, split blocked tasks, re-estimate token/time budgets, and prune obsolete branches when requirements shift. Before queueing, each plan step MUST have a stable step identity, objective, dependency position, required capabilities/tools, expected artifact or result, and pass/fail acceptance criteria.

**AcceptanceCriterion model.** Each declared acceptance criterion carries the following semantic shape; the Agent Runtime owns the vector (`architecture/AGENT_RUNTIME.md` §Agent State):

```kotlin
data class AcceptanceCriterion(
    val criterionId: String,          // stable identity within the task
    val description: String,          // pass/fail condition derived from goal/constraints
    val source: String                // goal-derived, constraint-derived, or user-declared
)
```

`AcceptanceCriterionProgress` (`criterionId`, `status: CriterionStatus`, `evidenceRefs`) tracks each criterion through `UNASSESSED`, `IN_PROGRESS`, `PASSED`, `FAILED` as defined in `architecture/AGENT_RUNTIME.md`. The Planner may derive criteria from the declared Task goal and constraints, but completion MUST re-check the declared criteria rather than infer success from activity, text output, file count, or provider completion alone. Criteria are not supplied by a separate task-start field.

**Persistence home.** The durable projection is carried by the existing checkpoint schema (`specs/DATABASE_SCHEMA.md`): `execution_checkpoint.acceptanceProgressJson` stores the `AcceptanceProgressVector` with evidence references, and `execution_checkpoint.variablesJson` carries the serialized `AgentCheckpoint` state including `plan: ExecutionPlan` (`architecture/RUNTIME.md` §Checkpoint System). Plan repair MUST preserve the current execution identity and checkpoint lineage while recording the verified failure or changed constraint that justified the revision; a repair is not substantive progress unless it improves an acceptance criterion, relevant evidence, verification result, or declared scope. Concrete storage, DTO, serialization, and plan-version representation remain downstream choices within these semantic invariants.

## 2. Software Engineering Pipeline

For software-engineering tasks, the lifecycle concretizes into:

```
User Goal
   │
   ▼
Requirement Analysis      -> objective, acceptance criteria, constraints
   ▼
Planning                  -> plan, tasks, dependencies, validation criteria
   ▼
Task Decomposition        -> subtasks, ordering, parallel lanes
   ▼
Agent Selection           -> Coder / Tester / Reviewer / Debugger / Git Agent ...
   ▼
Skill Selection           -> Kotlin Development, Android Debugging, Git Workflow ...
   ▼
Tool Selection            -> file_*, build_*, git_*, test_* ...
   ▼
Dependency Resolution     -> plugins, packages, runtimes, env templates
   ▼
Code Generation / Modification
   ▼
Build                     -> build_* tools (Gradle/Make)
   ▼
Static Analysis           -> lint, code_review, security_scan
   ▼
Unit Testing              -> test_run (targeted)
   ▼
Integration Testing       -> test_integration
   ▼
End-to-End Testing        -> test_e2e (where applicable)
   ▼
Performance & Security Checks -> obs_metrics, security_*, perf budget
   ▼
Self Review & Reflection  -> code_review, review results vs criteria
   ▼
Automatic Fixes (if needed) -> fix loop with retries (bounded)
   ▼
Final Validation          -> acceptance criteria re-check
   ▼
Completion Report         -> logs, results, artifacts
   ▼
Update Memory & Project History -> memory_store, execution history
```

Stages marked with `->` are mandatory; testing stages apply **where applicable**
(small tasks may skip E2E). Each stage has a **pass gate**: if validation fails, the
pipeline returns to the relevant earlier stage (bounded fix loop, FR-EL-013).


## Failure Classification

Execution failures are classified as follows. Classification determines whether retry, recovery, escalation, or termination is permitted.

### Transient failures (retry permitted)

Transient failures MAY be retried subject to bounded retry policy. Examples include:

- Network timeouts (soft);
- Provider rate-limit (429);
- Temporary resource exhaustion;
- Transient tool errors (retryable per tool policy).

Classification criterion: the failure is recoverable without strategy change and is not on the permanent-failure list.

### Permanent failures (retry not permitted)

Permanent failures MUST NOT be retried without explicit strategy change or user intervention. Examples include:

- Authorization failures;
- Schema validation failures;
- Missing required resources;
- Permanent tool errors (non-retryable per tool policy);
- Repeated identical failures after strategy mutation.

Classification criterion: the failure is not recoverable without strategy change, or the tool explicitly declares it non-retryable.

### Escalation failures (user notification or termination)

Escalation failures trigger user notification or termination with incomplete/blocked status. Examples include:

- Bounded-progress violations;
- Retry-storm detection;
- Deadline exceeded;
- Resource quota exceeded.

Classification criterion: the failure indicates a systemic constraint violation rather than a recoverable operation failure.

### Canonical Failure-Class Binding

DEC-29 resolves the authority binding for the failure classes without creating new errors, states, or transitions.

The canonical error catalog owns the concrete `NXR-` identity, category, retryability, idempotency, lifecycle effect, recovery owner, and redacted details. The owning lifecycle owns the legal state effect. The operation owner owns idempotency, retry conditions, and side-effect recovery. Classification MUST NOT replace or reinterpret the canonical error envelope.

A **transient** failure permits `TaskLifecycle.Running → RetryPending` only when the canonical error envelope and operation policy mark the operation retryable and the retry limit remains available. `RetryPending → Queued` uses the existing Task transition after backoff. A transient classification does not create a new Task or Execution state.

A **permanent** failure prohibits retry without an explicit strategy change or user intervention. The owning lifecycle commits its existing terminal failure effect: `TaskLifecycle.Running → Failed` and `ExecutionStatus.RUNNING → FAILED`. A committed terminal Execution is never resumed under the same identity; explicit retry/restart creates a new Execution under the existing retry-lineage rules.

An **escalation** failure represents a systemic constraint, bounded-progress violation, retry storm, deadline exhaustion, or resource constraint. `TaskLifecycle.Running → BlockedAwaitingInput` is used only when the owning runtime explicitly invokes `requestEscalation(question)` for clarification or a capability gap. Otherwise, termination uses the existing `Failed` effects and the canonical error/recovery contract. Approval denial is not an implicit pause: it uses `NXR-2003` / `USER_DENIED` and the canonical `WaitingApproval → Failed` transition; approval expiry uses `NXR-2003` / `POLICY_DENIAL`. Invalid dependency references or cycles are rejected before queueing with `NXR-1014`, terminally failed dependencies propagate `NXR-1015`, and effective-deadline expiry uses `NXR-1016`. `Pending`, `Blocked`, and `BlockedAwaitingInput` are deadline-bounded and expire to `Failed`; provider `Retry-After` waits are bounded by the effective parent deadline. Escalation does not create a new Task state.

Protocols, APIs, and SDKs MUST preserve the canonical error envelope and MUST NOT infer lifecycle transitions from category or message text alone. Concrete operation mappings remain governed by `errors/ERROR_CODES.md`, the applicable state machine, and the operation owner. See [DEC-29](../decisions/DEC-29-execution-failure-class-binding.md).

Implementations MUST NOT invent arbitrary classification authority.


## 3. Validation & Verification (FR-EL-008, FR-EL-011)

| Stage | Validation criteria |
|-------|---------------------|
| Requirement analysis | Objective statement + acceptance criteria written; agreed before execution |
| Each plan step | Step declares pass/fail criteria and expected artifacts |
| Build | Exit code 0; artifacts produced |
| Static analysis | No new critical lint/security findings |
| Tests | Defined pass threshold (e.g. 0 failures) |
| Final validation | Acceptance criteria re-checked end-to-end; result artifact attached |
| Completion | Report generated; memory updated; follow-ups listed |

## 4. Error Recovery (FR-EL-009)

| Failure | Strategy |
|---------|----------|
| Retryable (transient) | Automatic retry, exponential backoff (NFR-REL-003), max 3 |
| Build/test failure | Auto-fix loop (bounded): analyze error → fix → rebuild; fall back to human approval after N iterations |
| Non-retryable | Fail task, save checkpoint, notify, offer retry |
| Approval required | Suspend at approval gate (`WaitingApproval`); approval denial uses `NXR-2003` / `USER_DENIED`, approval expiry uses `NXR-2003` / `POLICY_DENIAL`, and both transition the Task to `Failed` under DEC-35; participating Agent availability may project `Paused` without resuming the Task |
| Escalation / missing capability / clarification needed | Suspend at `BlockedAwaitingInput` gate (TaskLifecycle `requestEscalation`); emit user-facing clarification prompt; preserve checkpoint; resume on user input (`resolveEscalation`) from the checkpoint captured at suspension (same `executionId`; `version` increment per RUNTIME.md §ExecutionStatus Lifecycle). Effective deadline expiry returns `NXR-1016` and transitions the Task to `Failed`. |
| Provider failure | Provider failover via ProviderRouter (health-based); provider `Retry-After` waiting is bounded by the parent task effective deadline |
| Sandbox resource limit | Graceful termination + partial results (NXR-7xxx) |

## 5. Phase Mapping

- **Phase 2**: Lifecycle core — objective definition, planning, decomposition, ordering,
  validation criteria, error recovery, reflection, verification (FR-EL-001…012 core).
- **Phase 4**: Skill registry and selection (FR-SK-001…005, FR-EL-004); SE pipeline
  build/static-analysis/test stages (FR-EL-013); tool/plugin selection.
- **Phase 5**: Per-task provider/model selection (FR-EL-005).
- **Phase 6**: Memory storage of results, follow-up identification (FR-EL-012).
- **Phase 7**: Automatic agent selection across the 16 agent types (FR-EL-003).


## Execution Modes and Bounded Progress

This upgrade formalizes five execution modes across the lifecycle:

- **FAST** — minimal planning and direct execution when evidence and risk allow;
- **NORMAL** — structured planning, bounded decomposition, evidence gathering, and validation;
- **DEEP** — bounded deep reasoning with competing hypotheses, contradiction checks, and explicit uncertainty;
- **VERIFY** — independent validation of important outputs and compliance against requirements/constraints;
- **RECOVER** — bounded recovery using retry/fallback/checkpoint restoration and context reconstruction.

### Minimum execution contract

Every iterative execution cycle MUST declare:

- iteration identity;
- active mode;
- progress signals under evaluation;
- retry and time budget;
- termination condition;
- escalation condition.

### Progress definition

Meaningful progress includes one or more of:

- new evidence collected;
- execution state transition;
- a completed acceptance criterion;
- reduced unresolved requirements;
- a resolved contradiction;
- successful tool result after prior failure;
- materially improved verification result.

Repeated iterations without meaningful progress MUST terminate, recover, or escalate.