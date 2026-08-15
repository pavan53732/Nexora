# DEC-44 — Normative 250-Item Research Workload

- **Status:** Accepted
- **Date:** 2026-08-16
- **Deciders:** Architecture Owner
- **Related:** `requirements/NFR.md`, `architecture/MULTI_AGENT_SYSTEM.md`, `specs/EXECUTION_LIFECYCLE.md`, `docs/PERFORMANCE_BUDGET.md`, `models/Task.md`, `specs/DATABASE_SCHEMA.md`, `testing/cases/E2ETestCases.md`, `testing/PerformanceTests.md`, `docs/TRACEABILITY.md`

## Context

The external capability comparison reports a public Wide Research claim of testing up to 250 items. That external claim does not define a Nexora unit, scope, concurrency rule, or Android validation boundary. Nexora already has a durable Task identity, acyclic dependency validation, bounded delegated concurrency, per-workspace resource controls, evidence and acceptance criteria, checkpoint recovery, and planned long-horizon validation. The decision must use those existing contracts rather than introduce a vendor-derived concurrent-agent limit or an unbounded queue.

## Decision

Nexora adopts **250 as the maximum admitted research-workload breadth for one root Research Task**.

A **research work item** is one distinct, bounded, leaf research objective admitted into that root Task’s validated execution plan. Each admitted item has an existing Task identity, an objective or scope boundary, acceptance criteria, dependency position in the validated acyclic graph, and an evidence target or explicit no-result disposition. A work item is counted by its stable admitted Task identity exactly once.

The count is not a count of sources, citations, claims, artifacts, tokens, provider calls, Tool calls, agents, retries, execution attempts, or generated messages. One research work item may use multiple sources and produce multiple claims, evidence references, and artifacts. Replanning, retrying, recovering, or changing the assigned worker does not increment the count when the admitted objective and scope remain the same. A materially new objective or scope is a new work item and consumes one additional admission.

The limit is **per root Research Task**, including all descendant Tasks in that root’s delegation lineage, and is scoped to the root Task’s existing `workspaceId`. It is not a per-agent, per-provider, per-session, per-device, per-workspace cumulative, or system-wide limit. Separate root Research Tasks have separate 250-item admission budgets, while every root and descendant remains subject to the existing workspace, device, provider, deadline, storage, memory, battery, and safety controls.

The 250-item limit is an **admission limit**, not a concurrency grant. Before an item is admitted, the Planner/Coordinator must validate its dependency reference and duplicate-scope status using the existing execution-planning and Multi-Agent contracts. Once admitted, it may be queued or executed according to the existing dependency graph and SA-3 dynamic concurrency formula:

```text
max_parallel_agents = min(
    memory_budget / per_agent_memory_estimate,
    cpu_cores,
    configurable_max
)
```

The existing default of 3 sub-agents and high-end bound of 8–16 remain unchanged. A 250-item root Task may therefore have queued work substantially larger than active parallelism. The cap does not authorize 250 agents, 250 processes, 250 provider streams, or any resource consumption beyond existing limits.

Items 1 through 250 may be admitted individually when the existing dependency, duplicate-scope, capability, permission, deadline, resource, and acceptance checks pass. An attempt to admit item 251 or any later distinct item is rejected before creation or queueing of that new child Task. The root execution preserves all already-admitted work, evidence, checkpoints, and provenance. The Coordinator must report the admission boundary as an incomplete or scope-limited result through the existing plan-repair, completion-gate, Task, Execution, API, audit, and UI contracts; it must not silently discard the request, silently reduce the requested scope, or claim that the unadmitted item was completed.

The 250-item boundary does not create a Task state, Execution state, Agent state, error code, permission scope, API operation, protocol primitive, persistence table, or new ownership component. Existing lifecycle owners determine whether the root Task remains eligible for other admitted work, requires clarification, reaches an incomplete outcome, or fails after the boundary prevents satisfaction of its acceptance criteria. Existing canonical error identity and recovery metadata remain authoritative when an implementation exposes the admission rejection at a boundary.

## Preserved invariants

The root Task and every descendant retain stable identity, versioning, parent lineage, effective deadline, dependency validation, retry identity, checkpoint, cancellation, authorization, evidence, and provenance semantics. An item that fails, is cancelled, becomes unknown completion, or remains blocked after admission still counts as one admitted item; retry or recovery does not create a second count.

The SA-3 resource-budgeted concurrency ceiling remains authoritative. The 250-item value never overrides Android CPU, memory, battery, storage, provider, stream, sandbox, process, deadline, or cancellation limits. Existing anti-loop, duplicate-scope prevention, semantic-progress, deadlock, bounded-retry, and completion-gate controls remain mandatory.

The private-reasoning boundary, cloud-only provider scope, no-local-AI-model boundary, permission and sandbox rules, and evidence/claim validation rules remain unchanged. A 250-item workload does not authorize raw private reasoning persistence, unsupported claims, unapproved Tools, unsafe side effects, or local inference.

## Required projections

`requirements/NFR.md` MUST define one normative scalability requirement for the 250-item research workload. `architecture/MULTI_AGENT_SYSTEM.md`, `specs/EXECUTION_LIFECYCLE.md`, `docs/PERFORMANCE_BUDGET.md`, and `models/Task.md` MUST project the counted unit, root-task scope, admission boundary, and unchanged SA-3 concurrency semantics. `specs/DATABASE_SCHEMA.md` and persistence projections MUST preserve existing Task identity and lineage; no 250-item-specific table or counter is required by this decision. `docs/TRACEABILITY.md`, `docs/REQUIREMENT_COVERAGE_LEDGER.md`, and `docs/FR_NFR_MAPPING.md` MUST map the requirement to the decision, canonical owner, and planned validation. Existing E2E and performance suites MUST validate the boundary and its resource/recovery behavior.

## Planned validation

The planned validation must cover: admission of exactly 250 unique items; rejection before creation or queueing of item 251; duplicate/retry/replan attempts not increasing the count; multiple sources and claims within one item not increasing the count; dependency-ordered queueing; SA-3 concurrency remaining at the dynamic bound; partial results at the boundary; checkpoint/restart preservation; cancellation and deadline propagation; memory, CPU, battery, storage, provider, and stream budgets; conflict/deadlock controls; and truthful incomplete/completion-gate reporting. These are planned evidence obligations and are not executed evidence.

## Rationale and rejected alternatives

Counting sources, citations, claims, or artifacts was rejected because those are variable evidence outputs and would make the workload boundary depend on research verbosity rather than planned work. Counting active agents or concurrent workers was rejected because it conflicts with SA-3 and Android resource controls. Counting all workspace or session work was rejected because it would couple independent root Tasks and make the limit non-local. Counting retries or provider calls was rejected because those are execution attempts governed by existing retry and provider contracts. A vague “250 items supported” statement was rejected because it would not define admission, scope, boundary behavior, or validation.

## Acceptance evidence

The documentation baseline is consistent when:

1. `requirements/NFR.md` contains one normative 250-item research-workload requirement.
2. The requirement maps to this decision and the existing Task, execution-planning, Multi-Agent, performance, persistence, evidence, and validation authorities.
3. The architecture continues to show SA-3 dynamic concurrency rather than 250 concurrent agents.
4. Item 251 is rejected before child Task creation or queueing, while admitted work remains recoverable and truthfully reported.
5. No source implementation or executed validation evidence is claimed by the documentation change.
6. Requirement-ledger parity, canonical paths, internal links, and regression checks remain clean.

## References

- `architecture/MULTI_AGENT_SYSTEM.md` §SA-3 — dynamic resource-budgeted concurrency.
- `specs/EXECUTION_LIFECYCLE.md` §§1, 3, and 4 — bounded Task decomposition, acceptance criteria, dependencies, recovery, and completion.
- `models/Task.md` — stable Task identity, parent/dependency lineage, deadline, and retry projection.
- `docs/PERFORMANCE_BUDGET.md` — Android memory, concurrency, storage, battery, and performance budgets.
- `testing/cases/E2ETestCases.md` — planned orchestration, long-horizon, reliability, liveness, and evidence cases.
- `testing/PerformanceTests.md` — planned multi-agent benchmark dimensions and vendor-claim evidence boundary.
- `/home/ubuntu/manus_vs_nexora_complete_comparison.md` — supporting external comparison; not a Nexora authority.

No external vendor behavior is adopted as an internal implementation fact by this decision.
