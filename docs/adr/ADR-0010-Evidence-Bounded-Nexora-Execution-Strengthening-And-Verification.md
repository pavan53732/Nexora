# ADR-0010: Evidence-Bounded Nexora Execution Strengthening and Verification

- **Status:** Accepted
- **Date:** 2026-08-19
- **Deciders:** Lead Architect, Runtime, Security, Verification
- **Decision type:** Nexora architecture and verification-boundary decision
- **Scope:** Existing Nexora contracts only; no repository implementation authorization
- **Related:** [ADR-0003](ADR-0003-Agent-Runtime.md) · [ADR-0009](ADR-0009-Adaptive-Autonomy-And-Persistence.md) · [Agent Runtime](../../architecture/AGENT_RUNTIME.md) · [Runtime](../../architecture/RUNTIME.md) · [Workflow Engine](../../architecture/WORKFLOW_ENGINE.md) · [Context Management](../../specs/CONTEXT_MANAGEMENT.md)

## Context

The Lovable → Nexora opportunity analysis and six follow-up investigations identified useful operational patterns, but the resulting decision must be Nexora’s decision. The supplied ChatGPT/Lovable-derived text is secondary evidence. Official Lovable documentation independently confirms Lovable’s agentic implementation/verification workflow, browser/frontend/backend testing modes, security scans, focused read-only subagents, persistent project knowledge, and portable web application model. It does **not** establish a Lovable-specific Execution Kernel, persisted Batch identity, `@platform/*` namespace, authoritative Policy Engine, deterministic clock/randomness harness, or 90–95% framework-independent target. Those concepts are not treated as Lovable architecture adopted by Nexora.

Where Nexora already had the principle, Lovable independently **validates or reinforces** it. Where Lovable supplied a useful operational pattern, Nexora adapts only the bounded portion that fits existing ownership. The Nexora evidence baseline is the investigation report, which cites the canonical owners and records that the current repository is a Phase 0 documentation baseline with no tracked Kotlin, Java, Gradle, or planned-module implementation files. `NEXORA_LOVABLE_INVESTIGATION_REPORT.md:7-19,326-354`; `PROJECT_SPECIFICATION.md:9-17,347-357,376-388`

Nexora already owns the relevant semantics. Runtime composes services but does not replace subsystem ownership. `architecture/RUNTIME.md:19-37` Agent Runtime owns execution modes, deadlines, acceptance progress, progress signals, bounded repair, and escalation. `architecture/AGENT_RUNTIME.md:27-35,58-66,140-188,263-280` Workflow owns graph progression and bounded iteration without replacing Task, Execution, Tool, Provider, Permission, or Android background authorities. `architecture/WORKFLOW_ENGINE.md:1-8,91-115` Dependency, permission, resource, context, tool, Android, security, and evidence ownership is already documented. `docs/MODULE_BOUNDARIES.md:11-43`; `docs/DEPENDENCY_GRAPH.md:11-83`; `security/PermissionModel.md:20-75,351-390,505-513`; `specs/CONTEXT_MANAGEMENT.md:22-82,351-353`

The problem addressed by this ADR is **evidence-bounded implementation closure**: strengthen and verify the existing contracts without confusing documented requirements, source implementation, test definitions, test execution, and reproducible executed evidence.

## Decision summary

Nexora adopts six bounded decisions:

1. Strengthen metric-driven execution over existing Agent/Task/Execution/Workflow/ProgressSignal/acceptance/evidence contracts.
2. Use a derived work-group projection without creating a persisted Batch identity or lifecycle.
3. Enforce Android-facing boundaries through existing modules, interfaces, dependency rules, and Android integration evidence.
4. Adopt derived cross-policy eligibility reporting and investigate a stateless evaluator; do not create an authoritative Policy Engine in this ADR.
5. Adopt mechanical architecture/dependency/compliance checks derived from existing canonical contracts.
6. Strengthen deterministic test controls and fault-injection evidence against existing lifecycle/state-machine authorities.

These decisions do not create a new module, package namespace, persisted identity, lifecycle, scheduler authority, production override authority, policy god-object, cross-platform product, or AI authority.

## Lovable contribution versus Nexora decision

| Topic | Lovable contribution | Nexora decision |
|---|---|---|
| Agentic implementation and verification | Official Build-mode documentation describes codebase exploration, multi-file changes, visible tasks, diffs, and verification. | Nexora strengthens its existing plan/execute/reflect, evidence, validation, trace, and checkpoint contracts; it does not adopt a Lovable runtime architecture. `architecture/RUNTIME.md:19-31,124-167,183-234` |
| Focused investigations and subagents | Official Subagents documentation describes temporary read-only focused investigations, parallel execution, traceable findings, and main-agent synthesis. | Nexora adapts the operational pattern for bounded investigation and evidence collection where useful; no persisted Lovable Batch or subagent lifecycle is adopted. `docs/CANONICAL_SOURCES.md:24,104-105` |
| Multi-mode verification | Official Testing documentation describes browser testing, frontend tests, direct edge calls, edge tests, and captured verification signals. | Nexora strengthens its existing test inventories and executed-evidence discipline. `PROJECT_SPECIFICATION.md:250-259`; `testing/IntegrationTests.md:7-22,63-99` |
| Automated security findings | Official Security documentation describes Basic/Deep scans and explicitly says scans do not replace full security review. | Nexora adopts mechanical compliance checks derived from its own canonical dependency/security/evidence contracts; no Lovable Policy Engine is ratified. `docs/DEPENDENCY_GRAPH.md:81-83`; `security/PermissionModel.md:20-75` |
| Persistent project knowledge | Official Knowledge documentation describes persistent workspace/project instructions and always-included context. | Nexora strengthens its existing Context Management, Memory, provenance, and ClaimRecord contracts. `specs/CONTEXT_MANAGEMENT.md:22-82,351-353` |
| Portable web hosting/data | Official Deployment documentation describes Vite + React, portable code/data, and managed/self-hosted web deployment. | Nexora remains a native Android product. No web hosting, Cloudflare/V8-isolate runtime, or cross-platform product architecture is adopted. `PROJECT_SPECIFICATION.md:9-14,35-41`; `requirements/CONSTRAINTS.md:9-14,41-48` |
| Execution Kernel, Batch lifecycle, `@platform/*`, 90–95% target, Policy Engine | No primary Lovable source established these as Lovable implementation facts; they appear in the supplied secondary text. | These are not ratified as Lovable architecture. Nexora decisions below evaluate the underlying problems using Nexora ownership and evidence. |

## Evidence-state rule

Every statement about a requirement, implementation, test, or completion MUST distinguish:

> **CANONICAL REQUIREMENT** ≠ **IMPLEMENTED** ≠ **TEST DEFINED** ≠ **TESTED** ≠ **EXECUTED EVIDENCE**

- **Canonical requirement:** an authoritative documented contract with owner and exact source evidence.
- **Implemented:** source implementation exists and is attributable to the owning contract.
- **Test defined:** a test specification, case, suite, fixture contract, or acceptance procedure exists.
- **Tested:** the test was actually executed and produced a result.
- **Executed evidence:** the executed result is retained in reproducible form with environment, fixture, identity, version/timestamp, result, and artifact location.

Nexora’s Phase 0 baseline proves documented contracts and planned test inventories, not source implementation or executed runtime/device evidence. `PROJECT_SPECIFICATION.md:14,347-357`; `testing/IntegrationTests.md:63-69`; `testing/PerformanceTests.md:70,78-82`

# Decision 1 — Metric-driven execution strengthening

## Problem

Long-running agent work needs measurable acceptance progress, bounded next actions, recovery/replanning signals, and evidence-linked completion instead of relying on unstructured narrative progress. Nexora already documents execution modes, acceptance progress, ProgressSignal, deadlines, failure ledgers, bounded repair, and evidence. `architecture/AGENT_RUNTIME.md:27-35,58-66,140-188,263-280`; `specs/EXECUTION_LIFECYCLE.md:81-97,206-218,245-274`

## Decision

Strengthen metric-driven execution over existing Agent, Task, Execution, Workflow, delegation, acceptance, ProgressSignal, deadline, failure-ledger, and evidence contracts. Metrics are derived evaluations over existing acceptance criteria, ProgressSignal, Task/Execution/Workflow state, and evidence references.

This ADR does **not** create a persisted `GoalMetric` identity, lifecycle, owner, scheduler, telemetry root, or completion authority. A metric cannot independently transition a lifecycle, grant permission, reset a deadline/retry budget, or declare success.

## Lovable contribution

Lovable’s official Build-mode documentation independently validates visible progress, codebase exploration, multi-file execution, and verification as useful operational patterns. Nexora already had the underlying plan/execute/reflect and evidence principle. Lovable reinforces the operational presentation and feedback loop; Nexora makes the decision to strengthen its own existing contracts.

## Ownership, identity, persistence, lifecycle, and authority

| Field | Decision |
|---|---|
| Ownership | Agent Runtime owns progress/mode semantics; Task, Execution, Workflow, and delegation retain their existing owners. |
| Identity | Existing `agentId`, `taskId`, `executionId`, `workflowId`, `correlationId`, acceptance/evidence references. No GoalMetric identity. |
| Persistence | Persist only through existing Task/Execution/Workflow/checkpoint/evidence records. No new metric table required by this ADR. |
| Lifecycle | Existing lifecycle state machines remain authoritative. Metric observations are diagnostic/evaluative projections. |
| Authority | Metrics may recommend continue, recover, replan, or report incomplete; only existing owners may transition state or authorize side effects. |

## Security and Android implications

Metrics must not bypass PermissionModel, audit, sandbox, resource, provider, context, deadline, or unknown-completion rules. `security/PermissionModel.md:20-75`; `architecture/TOOL_SYSTEM.md:36-76`; `architecture/RUNTIME.md:169-173,230-234` Android background work continues to use existing foreground-service, WorkManager, notification, checkpoint, deadline, and process-recovery contracts. `architecture/RUNTIME.md:55,61-63,169-181`

## Invariants

1. No GoalMetric identity or lifecycle exists.
2. Every metric resolves to an existing owning identity and evidence reference.
3. Metric values never infer lifecycle transitions from confidence, latency, or logs alone.
4. Metric evaluation never resets deadlines, retry budgets, failure ledgers, or lineage.
5. Unknown completion remains unresolved until the owning Tool reconciliation contract resolves it. `architecture/WORKFLOW_ENGINE.md:111-115`

## Acceptance criteria

1. A trace fixture demonstrates the documented Planner → ExecutionPlan → Context → Provider → Tool → Permission → Executor → Memory/EventBus path. `architecture/RUNTIME.md:124-155`
2. Each metric observation links to acceptance criteria, ProgressSignal, Task/Execution/Workflow identity, and evidence.
3. Known-good, stalled, failed, recovered, and incomplete scenarios preserve existing lifecycle outcomes.
4. No metric path mutates lifecycle, authorization, deadline, retry, checkpoint, or evidence ownership.
5. Reports identify whether the result is canonical, implemented, test-defined, tested, or executed evidence.

## Migration and rollback

Migration is additive to existing projections: implement metric evaluation behind existing interfaces and emit existing trace/evidence references. Rollback disables the derived evaluation or report without changing Task/Execution/Workflow records or lifecycle semantics.

## Testing requirements

Define deterministic progress fixtures, deadline/retry fixtures, acceptance vectors, failure-ledger fixtures, and plan-versus-actual trace assertions. Test execution and retained evidence are required before any implementation claim.

## Explicit non-goals

No GoalMetric identity, Batch lifecycle, Execution Kernel, metric-owned scheduler, metric-owned authorization, AI authority, or cross-platform metric architecture.

# Decision 2 — Derived work-group projection

## Problem

A bounded view of actionable work may improve progress communication, recovery selection, and replanning. Nexora already has Task/Execution/Workflow/PlanStep identities, bounded Workflow iteration, checkpoints, delegated-child relationships, acceptance progress, and evidence. `architecture/RUNTIME.md:67-107,183-198`; `architecture/WORKFLOW_ENGINE.md:24-35,91-115`

## Decision

Adopt a **derived work-group projection** computed from existing Task, Execution, Workflow, PlanStep, delegated-child, checkpoint, acceptance, and evidence records. It is a view, not a persisted domain entity.

A work-group MUST NOT substitute for Task, Execution, Workflow, or delegated-child identity in persistence, telemetry, correlation, authorization, recovery, checkpointing, audit, evidence, deadlines, retries, or completion. It must be recomputable from existing records.

## Lovable contribution

Lovable primary documentation contributes focused investigation, bounded read-only subagents, visible tasks, and main-agent synthesis. The persisted Batch/work-group interpretation came only from the secondary supplied text. Nexora adapts the useful bounded-view pattern without adopting a Lovable lifecycle.

## Ownership, identity, persistence, lifecycle, and authority

| Field | Decision |
|---|---|
| Ownership | Runtime/Agent Runtime may compute the projection; Workflow owns graph progression; Task/Execution/delegation owners remain authoritative. |
| Identity | No work-group identity is required. Every row references existing source identities. |
| Persistence | Recompute from existing records; no new table or lifecycle is authorized. Cached presentation data must remain non-authoritative and invalidatable. |
| Lifecycle | No work-group lifecycle, retry state, deadline, checkpoint, or terminal state. |
| Authority | Projection may inform display/replanning; it cannot authorize tools, transition states, or declare completion. |

## Security and Android implications

The projection must retain existing workspace/permission visibility and redact sensitive content under existing audit/security rules. `architecture/RUNTIME.md:201-234` Android background progress remains bound to existing Task/Execution/workspace/correlation/deadline contracts. `architecture/RUNTIME.md:169-173`

## Invariants

1. 100% of projection rows resolve to existing source identities.
2. No projection-only lifecycle transition exists.
3. Refresh after checkpoint, retry, failure, cancellation, or unknown completion reproduces the source owner’s state and lineage.
4. A projection cannot reset deadlines/retry budgets or mark unknown completion successful.
5. A batch/work-group never becomes the telemetry, evidence, authorization, recovery, or persistence root.

## Acceptance criteria

1. Linear, iterative, parallel-lock, delegated-child, and checkpoint/unknown-completion fixtures pass identity conservation.
2. Projection recomputation produces the same result from the same source snapshot.
3. Replanning usefulness is measured by decision time/step reduction without lowering acceptance/evidence correctness.
4. Zero authority mutations and zero duplicate lifecycle records are observed.
5. Any request for durable identity or lifecycle is rejected from this decision and escalated to a separate ADR.

## Migration and rollback

Introduce the projection as a derived read model or in-memory view. Rollback removes the projection and its presentation consumers; source records, lifecycles, and evidence remain unchanged.

## Testing requirements

Use source snapshots with Task/Execution/Workflow/PlanStep/delegated-child/checkpoint states; assert identity conservation, recomputation, recovery, deadline/lineage preservation, unknown-completion handling, and permission visibility.

## Explicit non-goals

No persisted Batch identity, Batch lifecycle/state machine, Batch scheduler, Batch retry/deadline owner, Batch permission scope, Batch checkpoint/evidence root, or Batch replacement for existing entities.

# Decision 3 — Android boundary enforcement

## Problem

Nexora must preserve Android lifecycle, foreground/background execution, notifications, storage, sandbox, process, permissions, and security semantics while keeping runtime/application logic interface-driven. The repository is Phase 0, so actual implementation leakage cannot yet be measured. `PROJECT_SPECIFICATION.md:9-17,347-357`; `docs/MODULE_BOUNDARIES.md:11-28`

## Decision

Strengthen enforcement of existing Android-facing module/interface boundaries. Use existing `services`, `sandbox`, `storage`, `security`, `runtime`, `application`, `ui`, and `shared` ownership and the canonical dependency graph. `docs/MODULE_BOUNDARIES.md:15-28`; `docs/DEPENDENCY_GRAPH.md:31-63`

## Lovable contribution

Lovable’s primary deployment documentation independently demonstrates explicit separation between application code, frontend, backend/data, and hosting implementations. Nexora adapts only the general boundary principle; it does not adopt Lovable’s Vite/React web architecture, hosting model, or cross-platform target.

## Ownership, identity, persistence, lifecycle, and authority

| Field | Decision |
|---|---|
| Ownership | Existing module owners; Android services own foreground/WorkManager concerns, Sandbox owns process/files/resource limits, Storage owns persistence, Security/PermissionManager own security and authorization. |
| Identity | Existing Workspace, Task, Execution, Tool, Permission, process/session, correlation, and audit identities. |
| Persistence | Existing Room/DataStore, audit, checkpoint, policy, and workspace records; no adapter-owned duplicate authority. |
| Lifecycle | Existing Android, Task, Execution, TerminalSession, Workspace, and background lifecycles remain authoritative. |
| Authority | Existing public interfaces and canonical owners; Hilt binding composes implementations. `docs/MODULE_BOUNDARIES.md:32-37` |

## Security and Android implications

Static checks must prevent `ui → sandbox/providers/tools`, `tools → ui`, `providers → Android UI`, `sandbox → providers`, and `shared → domain` violations. `docs/DEPENDENCY_GRAPH.md:50-63` Device/emulator tests must cover process death, foreground/background transitions, notifications/checkpoints, permission approval/denial, app-private storage, quotas, and provider/network degradation.

## Invariants

1. UI never talks directly to implementations.
2. Consumers use existing public interfaces, not concrete implementations.
3. No module cycle or forbidden dependency is permitted.
4. Android-owned behavior is not hidden behind a generic abstraction that removes lifecycle/security semantics.
5. No new `@platform/*` namespace or cross-platform target is created.

## Acceptance criteria

1. Every Android-facing implementation is reachable via an existing public interface and allowed dependency edge.
2. Static analysis reports zero forbidden edges and cycles on the implemented tree.
3. Interface tests pass against fakes for services, storage, sandbox, security, permission, background, and provider boundaries.
4. Emulator/device tests cover the required Android lifecycle and security cases.
5. No adapter test bypasses PermissionModel, SandboxPolicy, audit, egress, deadline, or lifecycle owners.

## Migration and rollback

Apply checks and test seams to existing modules as they are implemented. Rollback removes the enforcement invocation or test adapter without relocating ownership or changing persisted state. A new module/owner would require a separate ADR before introduction.

## Testing requirements

Dependency graph fixtures, interface contract tests, Hilt binding tests, emulator/device lifecycle tests, sandbox/permission/security integration tests, and provider/network degradation tests are required. Planned tests are not executed evidence.

## Explicit non-goals

No `@platform/*` package namespace, generic cross-platform core, Desktop/Web/CLI product, Cloudflare/V8-isolate hosting, replacement of Android-owned services, or framework-independence percentage target.

# Decision 4 — Derived cross-policy eligibility reporting and stateless evaluator investigation

## Problem

Nexora has separate authorities for Permission, Task/Execution deadlines and recovery, ResourceManager budgets, ContextSnapshot/evidence eligibility, Tool unknown-completion reconciliation, Workflow progression, Security, and Observability. The investigation found no canonical preflight contract that assembles their combined eligibility result before a side-effecting operation. `docs/CANONICAL_SOURCES.md:18-23,41-44,67-82`; `architecture/RUNTIME.md:49-59,157-173,201-234`; `security/PermissionModel.md:20-75`; `architecture/TOOL_SYSTEM.md:36-76`

## Decision

Adopt a **derived cross-policy eligibility report** and investigate a **stateless evaluator** within existing ownership.

The report joins existing owner decisions, versions/timestamps, effective deadline, resource snapshot, context/evidence result, Tool/operation identity, permission/approval transaction, and unknown-completion status. It is diagnostic/evaluative and cannot mutate state.

The stateless evaluator may compute a deterministic composite eligibility projection from existing owner results. It MUST delegate actual authority to existing owners and must not grant permission, transition lifecycle, reset budgets, mark unknown completion successful, or create persisted policy identity.

An authoritative Policy Engine is **not selected**. It may be considered only by a future ADR if the report and stateless evaluator fail measurable acceptance criteria and the failure demonstrates that existing authorities are insufficient.

## Lovable contribution

Lovable’s primary security documentation independently contributes layered automated scans, actionable findings, and the explicit distinction between automated findings and complete security review. It does not prove a Lovable Policy Engine. Nexora adapts the reporting/evaluation pattern while making its own authority decision.

## Ownership, identity, persistence, lifecycle, and authority

| Field | Decision |
|---|---|
| Ownership | Existing PermissionManager, Security, ResourceManager, Context/Evidence, Tool, Workflow, Task/Execution, and Observability owners. |
| Identity | Existing operation, Tool invocation, Task/Execution/Workflow, approval, context snapshot, evidence, checkpoint, and correlation identities. |
| Persistence | Recompute from existing decisions/traces; no policy identity/table is authorized by this ADR. Retained reports follow existing audit/observability retention. |
| Lifecycle | No policy lifecycle, approval lifecycle, Task/Execution transition, or Tool completion transition is created. |
| Authority | Existing owners decide. The report/evaluator explains or projects; it does not grant, veto, override, or recover. |

## Security and Android implications

The composite view must be fail-closed when owner inputs conflict or are unavailable, must preserve redaction/permission/tenant/workspace scope, and must not expose secrets or private reasoning artifacts. `security/PermissionModel.md:20-75,351-390,505-513`; `architecture/RUNTIME.md:201-234` Android background operations remain governed by existing deadline, permission, foreground service, WorkManager, checkpoint, and audit contracts.

## Invariants

1. Existing policy/lifecycle authorities remain the source of truth.
2. A report or evaluator cannot grant permission or alter state.
3. Conflicts fail closed and identify the conflicting owners.
4. Unknown completion is never converted to success by an aggregate result.
5. No persisted Policy Engine identity, lifecycle, override, or recovery owner exists under this ADR.

## Acceptance criteria

1. The report identifies all contributing owners for each representative operation.
2. The stateless evaluator matches owner decisions on 100% of permission, deadline, budget, context/evidence, Tool risk, cancellation, and unknown-completion fixtures.
3. Four seeded conflict classes—denial/allow, expired/valid deadline, budget allowed/exceeded, and grounded/untrusted or unknown completion—are measured with explainable fail-closed outcomes.
4. Report/evaluator outputs are deterministic and fully attributable to source decisions.
5. A future authoritative engine is considered only if these criteria fail for a demonstrated reason that existing owners cannot address.

## Migration and rollback

Add report/evaluator outputs as derived traces or read models. Rollback disables their consumers and removes derived artifacts without changing source decisions or persisted authorities. Any request for persisted policy precedence, veto, override, or recovery must stop and open a new ADR.

## Testing requirements

Owner-decision fixtures, conflict matrices, expiry/deadline tests, resource/context/tool eligibility tests, redaction tests, unknown-completion tests, deterministic repeat tests, and fail-closed tests are required. No implementation or execution claim follows from this ADR alone.

## Explicit non-goals

No authoritative Policy Engine, `ArchitecturePolicyEngine`, policy god-object, AI policy authority, new permission scope, new lifecycle, persisted policy identity, independent merge/release veto, or production override authority.

# Decision 5 — Mechanical architecture and compliance checks

## Problem

Nexora’s dependency graph, public interfaces, module ownership, status/ID/link conventions, canonical ownership, and evidence-state distinctions need mechanical verification. The canonical dependency document already calls for CI fitness checks. `docs/DEPENDENCY_GRAPH.md:11-83`; `docs/MODULE_BOUNDARIES.md:11-32`; `standards/Documentation-Standard.md:28-41`

## Decision

Adopt mechanical checks derived directly from existing canonical contracts. Initial checks cover forbidden dependency edges, cycles, concrete-implementation imports, interface/Hilt boundaries, status headers, IDs, links, canonical-owner references, lifecycle names, and evidence-state classification.

Checks produce findings with rule ID, path, line, owner, severity, and remediation. CI MAY block a change when an existing canonical contract is violated. This is enforcement of the existing contract, not a new architecture authority.

## Lovable contribution

Lovable’s primary Security documentation independently validates automated scanning, actionable findings, layered coverage, and the limit that automation does not replace review. Nexora adapts the mechanical-check pattern to its own dependency and documentation contracts; it does not adopt a Lovable architecture scanner or Policy Engine.

## Ownership, identity, persistence, lifecycle, and authority

| Field | Decision |
|---|---|
| Ownership | Existing canonical documents and their named owners define rules; CI reports violations. |
| Identity | Existing rule IDs, FR/NFR/TOOL and document IDs, path/line references, commit/source revision, and change identity. No architecture-engine identity. |
| Persistence | Findings may be retained as CI artifacts or review evidence under existing conventions; no new lifecycle/policy database. |
| Lifecycle | Checks do not transition Task/Execution/Workflow or production state. CI status belongs to the existing development/review workflow. |
| Authority | Existing canonical contracts are authoritative; checks enforce them mechanically. No independent veto semantics beyond the violated contract. |

## Security and Android implications

Checks must protect against platform/security boundary drift, including forbidden UI/sandbox/provider/tools edges, provider Android UI dependencies, sandbox/provider coupling, shared upward dependencies, permission/security contract drift, and missing audit/evidence references. `docs/DEPENDENCY_GRAPH.md:50-83`; `security/PermissionModel.md:20-75`

## Invariants

1. A check cannot invent a new contract and then enforce it as canonical.
2. Every finding names the existing source rule and owner.
3. Checks cannot grant permission, mutate runtime state, or create lifecycle/policy authority.
4. False positives and escaped violations are measured, not assumed to be zero.
5. Blocking occurs only for a violated existing contract or an explicitly accepted project rule.

## Acceptance criteria

Use seeded known-good and known-bad fixtures for every forbidden edge in `docs/DEPENDENCY_GRAPH.md:50-63`, cycles, direct implementation imports, missing interfaces, missing owners, broken links, missing status headers, invalid IDs, and missing evidence classification.

1. 100% of seeded violations are detected.
2. 0 false positives occur on the canonical allowed graph and approved known-good fixtures.
3. 0 seeded violations escape after direct, transitive, alias, generated-source, and configuration variants applicable to the checker are tested.
4. Every finding includes rule, path, line, owner, severity, and remediation.
5. CI blocking can be traced to the violated canonical contract.

## Migration and rollback

Add checks in report-only mode, establish a baseline, then enable blocking for existing-contract violations after false-positive and escape measurements meet acceptance criteria. Rollback disables the check or returns to report-only mode; it does not alter canonical contracts or persisted runtime state.

## Testing requirements

Checker unit tests, parser tests, known-good/known-bad fixture tests, graph cycle tests, documentation/link/ID tests, generated-source tests, CI integration tests, and false-positive/escape measurement are required.

## Explicit non-goals

No `ArchitecturePolicyEngine`, independent architecture owner, new production veto authority, new policy persistence, new lifecycle, AI decision authority, or replacement of canonical documentation ownership.

# Decision 6 — Deterministic test controls and fault-injection evidence

## Problem

Nexora documents deadlines, retries, checkpoints, unknown completion, permissions, workflow bounds, resource limits, and security conditions, but the Phase 0 baseline has no implementation or executed evidence. `requirements/NFR.md:30-67`; `architecture/WORKFLOW_ENGINE.md:91-115`; `testing/IntegrationTests.md:63-69`

## Decision

Strengthen deterministic testing through test-only fixture controls and fault-injection coverage against existing state machines and operation contracts.

Fixtures MAY control clock/deadline time, seeded jitter/randomness, provider/stream outcomes, resource conditions, process/device events, permission outcomes, storage/locks, scheduler order, and test identifiers where explicitly allowed. They MUST be unavailable to normal production authority.

Fault-injection scenarios are **coverage categories**, not one implementation milestone. Applicable test inventories, suite ownership, environment requirements, and release gates determine which categories execute for a given change/release.

## Lovable contribution

Lovable’s primary Testing documentation independently contributes multiple verification modes and captured console/network/test/build/request-response signals. Its Build-mode and Subagents documentation contributes bounded investigation and visible verification patterns. Nexora adapts the evidence discipline and bounded fixture pattern; the state machines, permission boundaries, and security authority remain Nexora’s own.

## Ownership, identity, persistence, lifecycle, and authority

| Field | Decision |
|---|---|
| Ownership | Existing state-machine owners, test-suite owners, PermissionModel, Tool/Provider, Sandbox, Context, Runtime, and evidence conventions. |
| Identity | Existing test case/suite ID, source/fixture revision, Task/Execution/Workflow/agent/tool/stream/correlation/checkpoint identities. |
| Persistence | Retain executed results and artifacts under existing evidence conventions; test-control configuration is fixture-scoped, not production-persisted. |
| Lifecycle | Existing state machines remain authoritative. A fixture can request a condition; it cannot perform a production transition. |
| Authority | Test controls have no production authority. Production authority means any capability that can change a production Task, Execution, Workflow, Tool, Permission, Context, lifecycle, deadline, retry budget, side effect, audit record, recovery outcome, or user-visible completion disposition. |

## Security and Android implications

Fixtures cannot bypass PermissionModel, SandboxPolicy, audit, egress, deadlines, idempotency, provider privacy, or lifecycle checks. Android tests must cover process death, ANR, Doze, foreground/background, notifications, restart/checkpoint, app-private storage, quotas, and network/provider degradation using emulator/device controls where applicable. `architecture/RUNTIME.md:169-181,236-288`; `security/PermissionModel.md:20-75`; `requirements/CONSTRAINTS.md:41-63`

## Invariants

1. Test-only controls are scoped, explicit, recorded, and unavailable in normal production execution.
2. Fixed inputs produce reproducible results.
3. No fixture grants permission, changes lifecycle ownership, suppresses audit, resets deadlines/retry budgets, or fabricates success.
4. Unknown completion is never silently replayed or marked successful.
5. Executed evidence retains source/fixture/environment/identity/result/artifact metadata.

## Acceptance criteria

1. Every applicable failure category has a defined test case owned by an existing authority.
2. Repeated runs with fixed clock, seed, provider, resource, and process conditions produce stable results.
3. Known-good and known-failure fixtures preserve expected transitions, deadlines, idempotency, audit, and user-visible dispositions.
4. Every executed result is reproducible from retained inputs/artifacts and follows `testing/EVIDENCE_CONVENTIONS.md:1-40`.
5. No test-only control is callable by normal production execution.

## Migration and rollback

Define fixture interfaces and scenario categories in test infrastructure first, then add suites according to existing inventories and release gates. Rollback removes or disables a fixture/suite without changing production lifecycle or persisted runtime state. Any production override request requires a separate ADR.

## Testing requirements

Unit, integration, E2E, performance, security, lifecycle, streaming, context, liveness, sandbox, Android device/emulator, and recovery tests execute according to applicable inventories. A test definition is not a tested result; a tested result without retained reproducible artifacts is not executed evidence.

## Explicit non-goals

No production override API, no production nondeterminism authority, no new lifecycle, no new fault-injection production module, no AI authority, and no claim that the Phase 0 repository already implements or has executed these tests.

# Explicitly rejected or non-adopted concepts

This ADR does not adopt the following concepts:

1. **Execution Kernel as a new authoritative owner.** A stateless composition façade may be investigated under Decision 1; a new owner requires a future ADR proving existing composition insufficient.
2. **Persisted Batch/work-group identity or lifecycle.** Only the derived projection in Decision 2 is authorized.
3. **Authoritative Policy Engine or ArchitecturePolicyEngine.** Only the derived report and stateless evaluator investigation in Decision 4 are authorized.
4. **`@platform/*` namespace or invented equivalent.** Existing module/package ownership remains authoritative.
5. **Next.js/TanStack migration architecture, Cloudflare/V8-isolate hosting, or cross-platform Desktop/Web/CLI product expansion.** Nexora remains a pure Android application. `PROJECT_SPECIFICATION.md:9-14,35-41`; `requirements/CONSTRAINTS.md:9-14,41-48`
6. **90–95% framework-independent target.** Boundary health is measured through concrete forbidden edges, cycles, interface violations, and test/evidence coverage.
7. **AI as an architecture, permission, security, lifecycle, or completion authority.** Existing deterministic owners remain authoritative. `security/PermissionModel.md:505-513`; `architecture/RUNTIME.md:230-234`
8. **Policy/architecture god-object.** Cross-policy reporting/evaluation must remain bounded and attributable unless a future ADR proves a new authority necessary.

These are Nexora scope decisions based on product/security contradictions or authority-preservation requirements, not blanket claims that the concepts have no value elsewhere.

# Consequences

## Positive consequences

- Nexora’s existing contracts become measurable without duplicate identity or lifecycle authorities.
- Progress and work-group views improve operational clarity without creating a Batch lifecycle.
- Android boundaries become mechanically enforceable and device-testable.
- Cross-policy decisions become explainable and attributable without an authority god-object.
- Architecture/compliance checks can block violations of existing contracts while remaining derived.
- Fault injection and deterministic controls make recovery and nondeterministic conditions reproducible.
- Reports preserve the difference between canonical requirement, implementation, test definition, tested execution, and executed evidence.

## Negative consequences and risks

- Engineering work is required before implementation/evidence claims can be made; the current repository is a Phase 0 documentation baseline.
- Derived reports/evaluators can be misleading if they are mistaken for authority; provenance and non-mutation tests are mandatory.
- Mechanical checks may produce false positives or miss violations; seeded fixtures and escape-rate measurement are required.
- Deterministic fixtures increase test infrastructure complexity and must be kept unavailable to normal production execution.
- Android device/emulator evidence, provider behavior, resource conditions, and security artifacts require controlled environments and retention.
- Future requests for new owners, identities, lifecycles, persistence, production overrides, or cross-platform targets require separate ADRs.

# Acceptance conditions for this ADR

Acceptance records the Nexora decision boundary only. It does **not** authorize implementation, source changes, test execution, or production rollout.

This ADR may be accepted only when the deciders confirm that:

1. The six decisions are understood as Nexora decisions, not adoption of Lovable architecture.
2. Lovable primary evidence is separated from secondary supplied interpretation.
3. Existing owners, identities, persistence, lifecycles, authorities, Android/security boundaries, invariants, acceptance criteria, migration/rollback, and testing requirements above are preserved.
4. No Execution Kernel, persisted Batch identity, authoritative Policy Engine, `@platform/*` namespace, cross-platform product architecture, or AI authority is introduced by acceptance.
5. Canonical documentation is updated first and the normal implementation-authorization process is completed before implementation.
6. The evidence-state distinction remains explicit: **CANONICAL REQUIREMENT ≠ IMPLEMENTED ≠ TEST DEFINED ≠ TESTED ≠ EXECUTED EVIDENCE**.

# Required sequence after acceptance

> **ADR → canonical documentation update → implementation authorization → implementation → tests → executed evidence**

Acceptance of this ADR does not itself authorize implementation. After acceptance, every affected canonical document, source map, lifecycle/protocol/model/API/SDK projection, requirement ledger, registry, and test inventory must be updated according to `docs/CANONICAL_SOURCES.md:110-125` and `standards/Documentation-Standard.md:28-41`. The normal project implementation-authorization process then applies. Only after those steps may implementation begin.

# References

[1]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/docs/CANONICAL_SOURCES.md#L3-L14 "Nexora canonical ownership rules"
[2]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/architecture/RUNTIME.md#L19-L37 "Nexora runtime composition"
[3]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/architecture/WORKFLOW_ENGINE.md#L91-L115 "Nexora workflow authority and bounded iteration"
[4]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/docs/MODULE_BOUNDARIES.md#L11-L43 "Nexora module/interface ownership"
[5]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/docs/DEPENDENCY_GRAPH.md#L11-L83 "Nexora dependency and CI fitness rules"
[6]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/security/PermissionModel.md#L20-L75 "Nexora permission authority"
[7]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/specs/CONTEXT_MANAGEMENT.md#L22-L82 "Nexora context management"
[8]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/requirements/NFR.md#L30-L67 "Nexora reliability and resource requirements"
[9]: https://github.com/pavan53732/Nexora/blob/c789cd3e8a9f6fab301eba2693a8b08ce1c086b6/testing/IntegrationTests.md#L63-L99 "Nexora planned integration/evidence boundary"
[10]: https://docs.lovable.dev/features/agent-mode "Lovable official Build mode documentation"
[11]: https://docs.lovable.dev/features/testing "Lovable official testing documentation"
[12]: https://docs.lovable.dev/features/security "Lovable official security documentation"
[13]: https://docs.lovable.dev/features/subagents "Lovable official subagents documentation"
[14]: https://docs.lovable.dev/features/knowledge "Lovable official knowledge documentation"
[15]: https://docs.lovable.dev/tips-tricks/deployment-hosting-ownership "Lovable official deployment and ownership documentation"
