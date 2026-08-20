# DEC-46 — Autonomous Operation Elevation

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** Architecture Owner / Product Owner
- **Scope:** Documentation contract only; implementation and executed evidence remain separately authorized work.

## Context

Nexora is intended to operate autonomously across ordinary low-risk execution, recovery, learning, tool use, and escalation while preserving existing Android, permission, sandbox, lifecycle, evidence, and security boundaries. The existing corpus contains autonomy modes, trust thresholds, permission defaults, lesson promotion, Tool idempotency/recovery, and escalation contracts, but several projections still imply manual mode selection, per-action confirmation, mandatory approval for every learned-skill proposal, incomplete Tool recovery declaration, or blocking escalation for ordinary forward progress.

The creator has selected the following bounded autonomy elevations. They strengthen existing owners and do not create a new authority or lifecycle.

## Decision

### 1. Automatic autonomy-mode selection with trust thresholds

The existing autonomy mode is selected automatically from the existing scoped trust score and existing thresholds:

- `MANUAL`: trust `0–39`.
- `ASSISTED`: trust `40–74`.
- `AUTOPILOT`: trust `75–100`.

A user does not confirm the mode on every session or every action. The effective mode MUST be recorded in existing execution, audit, activity, and evidence projections. The user MAY override the effective mode at any time only by downgrading it. A downgrade takes effect immediately, is recorded through existing settings/permission/audit projections, and cannot be silently upgraded by the agent. Trust changes cannot grant permissions or bypass existing high-risk gates.

The existing Android degraded-mode contract remains an explicit exception: when Android background or OEM conditions require degraded behavior, the existing degraded path forces `MANUAL` regardless of trust. This is not a new mode or state.

### 2. Category-level ALLOW defaults for low-risk operations

Permission defaults are interpreted by existing scope category. Low-risk categories may default to `ALLOW` when the existing PermissionModel table and higher-precedence policy permit it. High-risk categories retain their existing `ASK` or `DENY` defaults and gates. Category defaults do not bypass explicit workspace, agent, global, tool-risk, sandbox, sensitive-domain, device, plugin, network, or audit controls. No local classifier or AI authority selects permission outcomes.

### 3. Policy-based learned-skill promotion

An existing learned lesson may become an existing `LEARNED` Skill when the existing provenance, evidence, trust, safety, scope, and lifecycle conditions are satisfied. Promotion may be approved by the existing user path or by the existing deterministic policy path. A policy-approved promotion is recorded through existing Skill Registry, memory, audit, and evidence projections. The policy path MUST NOT create a new authority, permission, skill lifecycle, or capability bypass. An agent may retire an acquired or learned skill through the existing retirement path at any time.

### 4. Maximal truthful Tool recovery declaration

Every new Tool MUST declare the strongest truthful existing operation-level recovery contract: idempotent replay, query/status reconciliation, or deterministic local transaction/compensating operation. If none is available, the Tool MUST be treated as non-retryable and its registration or invocation MUST be rejected through the existing Tool validation/error path. The declaration remains metadata of the existing Tool descriptor and does not create a recovery owner, Tool identity, lifecycle state, or error code.

### 5. Notify-and-continue for ordinary advancing progress

When bounded execution reaches ordinary low-risk advancing progress and no permission, safety, capability, deadline, or evidence gate requires blocking, the runtime MUST surface an existing user-visible notification/status update and continue through the existing execution path. Notifications are observability, not approval.

The runtime MUST still block, escalate, degrade, fail, cancel, or stop when an existing contract requires it, including high-risk or denied operations, explicit clarification or capability gaps, unsafe or unverified conditions, deadline/resource exhaustion, failed verification, unresolved non-idempotent completion, or Android degraded-mode restrictions. No approval gate is removed by this decision.

## Ownership and invariants

- `specs/AUTONOMY_STABILITY.md` owns autonomy thresholds, learning, promotion conditions, and bounded escalation semantics.
- `models/AutonomyLearning.md` and `models/Skill.md` project existing trust, lesson, skill, provenance, and approval data.
- `security/PermissionModel.md` owns category defaults, precedence, ASK/DENY/ALLOW outcomes, and audit semantics.
- `architecture/AGENT_RUNTIME.md` owns mode selection, notify-and-continue behavior, progress, and escalation projection.
- `architecture/TOOL_SYSTEM.md` owns Tool recovery-contract semantics; SDK, registry, protocol, API, and model documents are derived projections.
- Existing Task, Execution, Agent, Tool, Permission, Skill, Workspace, Android, and evidence owners remain authoritative.

This decision introduces no new lifecycle state, ExecutionStatus, TaskStatus, ToolCompletionState, error code, persistent identity, permission scope, recovery manager, policy engine, classifier, AI authority, or cross-platform architecture. It does not authorize Kotlin/Java/Gradle implementation or claim `TESTED` or `EXECUTED EVIDENCE`.

## Required propagation

The owning and derived documents MUST align the existing contracts, including `specs/AUTONOMY_STABILITY.md`, `models/AutonomyLearning.md`, `requirements/FR.md`, `security/PermissionModel.md`, `architecture/AGENT_RUNTIME.md`, `architecture/TOOL_SYSTEM.md`, `sdk/ToolSDK.md`, `registry/TOOLS.md`, `registry/SKILLS.md`, relevant UI projections, existing test inventories, `docs/TRACEABILITY.md`, `docs/REQUIREMENT_COVERAGE_LEDGER.md`, `docs/FR_NFR_MAPPING.md`, and `docs/DOCUMENTATION_COMPLETENESS_INVENTORY.md`. Historical records remain historical and are not rewritten.

## References

- `specs/AUTONOMY_STABILITY.md`
- `models/AutonomyLearning.md`
- `models/Skill.md`
- `security/PermissionModel.md`
- `architecture/AGENT_RUNTIME.md`
- `architecture/TOOL_SYSTEM.md`
- `state-machines/TaskLifecycle.md`
- `specs/BACKGROUND_EXECUTION.md`
- `testing/EVIDENCE_CONVENTIONS.md`
