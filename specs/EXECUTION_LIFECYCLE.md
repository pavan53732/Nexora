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


> **DEC-7 (2026-08-11):** `RetryPending` is EPHEMERAL and is not reconstructed after process death. Execution identity remains stable for RetryPending retry and changes only for explicit retry after a committed terminal state. See [../decisions/DEC-7-retry-attempt-state.md](../decisions/DEC-7-retry-attempt-state.md).

## Overview

The AI determines **far more than tools and execution order**. For every goal, the
runtime resolves the full execution context: objective, tasks, agents, skills, tools,
plugins, providers, dependencies, permissions, ordering, parallelism, files, external
resources, validation criteria, error recovery, verification, and follow-up.

This spec defines that complete lifecycle and the software-engineering pipeline.
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
| Approval required | Suspend at approval gate (WaitingApproval), resume on approve |
| Escalation / missing capability / clarification needed | Suspend at `BlockedAwaitingInput` gate (TaskLifecycle `requestEscalation`); emit user-facing clarification prompt; preserve checkpoint; resume on user input (`resolveEscalation`) from the checkpoint captured at suspension (same `executionId`; `version` increment per RUNTIME.md §ExecutionStatus Lifecycle). |
| Provider failure | Provider failover via ProviderRouter (health-based) |
| Sandbox resource limit | Graceful termination + partial results (NXR-7xxx) |

## 5. Phase Mapping

- **Phase 2**: Lifecycle core — objective definition, planning, decomposition, ordering,
  validation criteria, error recovery, reflection, verification (FR-EL-001…012 core).
- **Phase 4**: Skill registry and selection (FR-SK-001…005, FR-EL-004); SE pipeline
  build/static-analysis/test stages (FR-EL-013); tool/plugin selection.
- **Phase 5**: Per-task provider/model selection (FR-EL-005).
- **Phase 6**: Memory storage of results, follow-up identification (FR-EL-012).
- **Phase 7**: Automatic agent selection across the 16 agent types (FR-EL-003).
