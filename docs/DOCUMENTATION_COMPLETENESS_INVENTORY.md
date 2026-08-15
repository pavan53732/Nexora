# Nexora Documentation Completeness Inventory

> **Status: SUPPORTING** repository-wide documentation inventory. This document does not create or modify an architecture decision, canonical authority, implementation artifact, or lifecycle owner.
>
> **Purpose:** record the current documentation coverage and preserve unresolved downstream work without converting absence of implementation into absence of architecture.

## Audited domains

The repository corpus was inventoried across:

- Session, Conversation, checkpoint, Runtime, Task, Execution, Context, Memory, Agent, Workflow, Tool, Skill, Workspace, Provider, Plugin, persistence, API, security, recovery, state machines, protocols, testing, configuration, deployment, and Android/application boundaries.
- Requirements, assumptions, constraints, risks, architecture, decisions, models, lifecycle documents, specifications, APIs, registries, security documents, testing documents, roadmap, repository structure, and traceability sources.

## Coverage status

- Models: present for the documented domain entities under `models/`; no missing model is promoted to an architectural defect solely because an implementation type is absent.
- Architecture: present under `architecture/`; ownership remains governed by the cited decision or architecture document, not by naming alone.
- Lifecycles/state machines: present for documented lifecycle domains under `lifecycle/` and `state-machines/`; a lifecycle/state machine is not inferred for a domain where no repository source establishes one.
- Protocols/APIs: present for the documented Agent, Execution, Memory, Plugin, Provider, and Tool boundaries, with API documents under `docs/api/`; concrete transport and implementation details remain downstream where the source says so.
- Engineering specifications: present where the repository has selected a semantic contract, including persistence/schema, background execution, environment, workspace, terminal, checkpoints, and Session–Conversation handoff contracts.
- Runtime/recovery: documented for Session–Conversation recovery and existing runtime lifecycle material; process/platform-specific recovery mechanisms remain implementation choices unless selected by a canonical source.
- Errors/validation/security: documented through `errors/`, `security/`, relevant specifications, and domain contracts; numeric error encoding and concrete enforcement mechanisms remain downstream where not canonically selected.
- Testing: present through test strategy documents, case documents, and the Session–Conversation deterministic matrix; planned evidence directories are not treated as executed test evidence.
- Traceability/canonical sources: maintained through `docs/TRACEABILITY.md` and `docs/CANONICAL_SOURCES.md`.

## Architecture-resolution status

### Active OPEN/DEFERRED register

At the current published HEAD, the active engineering contract set has no unresolved approval-expiry error-identity boundary. DEC-36 classifies an approval transaction that expires before a valid authorization outcome as the existing `NXR-2003 / POLICY_DENIAL` authorization-gate denial, while preserving expiry as a distinct audit, trace, notification, and activity-feed outcome. All other product, architecture, ownership, lifecycle, protocol, security, and terminology decisions in this inventory are resolved or explicitly bounded downstream. The repository also contains historical unresolved wording, bounded downstream choices, and planned evidence obligations; these categories are not interchangeable with an active owner decision.

DEC-36 does not create a new NXR code, subreason, lifecycle state, transition, retry path, or authorization bypass. `USER_DENIED` remains explicit user rejection of an ASK approval, and `MALFORMED_APPROVAL` remains invalid transaction structure or correspondence.

The historical `OWNER DECISION REQUIRED / UNRESOLVED` passages in DEC-13 and DEC-14 are preserved decision records. Their formerly open boundaries are superseded or narrowed by DEC-15 through DEC-24 and DEC-25 through DEC-36: Session–Conversation ownership, relationship identity/representation/cardinality/lifecycle/continuation, BranchLineage ownership and operational policy, checkpoint metadata semantics and retention, no internal credit/cost gating, Android-first positioning, requirement-owner taxonomy, ROADMAP terminology, execution-failure binding, agent-loop liveness, Task liveness error identities, background terminal parent binding, approval-denial composition, approval-expiry classification, and workflow scope are now represented by later canonical decisions. DEC files remain immutable historical authority and are not rewritten.

The remaining bounded downstream choices are not OPEN/DEFERRED architecture decisions: concrete identifier encoding, message/turn ordering representation, storage/schema/serialization, API/transport names and DTO shapes, transaction/concurrency mechanisms, Android component realization, exact DAO/migration mechanics, terminal-session persistence encoding, and implementation-level cleanup scheduling details where the governing decision already fixes the required semantic outcome. DEC-34 fixes autonomous background terminal parent binding, deadline inheritance, and reconciliation; concrete process cleanup and persistence mechanics remain downstream. Planned unit, integration, performance, security, regression, and Android/device evidence is also not a missing architecture decision; it is an implementation/evidence obligation and must not be reported as executed evidence.

Other unresolved values allowed by this inventory are local `UNKNOWN` or `UNAVAILABLE` data states explicitly defined by a contract, such as Tool `UNKNOWN_COMPLETION` pending reconciliation or provider health before its first check. They are runtime states or evidence classifications, not owner decisions.

The current inventory does not treat the following as active OPEN/DEFERRED architecture gaps:

- Tool timeout (`NXR-2002`) is an execution outcome with no ToolStatus lifecycle effect; unknown completion and conditional retry remain governed by `architecture/TOOL_SYSTEM.md` and the canonical error mapping.
- `listAgents` has no collection-specific canonical error mapping; an empty collection result is not `NXR-3001`.
- Blocked-app interaction is authorization-classifier denial (`NXR-2003` / `CLASSIFIER_DENIAL`), preserving denial, audit, notification, isolation, no bypass, no automatic resume, and new-operation/task continuation.
- Provider `Retry-After` and Task `RetryPending` retain independent scopes and do not create a merged retry state.
- Session–Conversation semantic questions selected by DEC-13 through DEC-21 are closed; historical unresolved wording does not reopen relationship status, ownership, identity, representation, cardinality, lifecycle, or continuation semantics. DEC-22 and DEC-23 separately resolve BranchLineage ownership and checkpoint retention/deletion safety.
- Concrete Conversation/checkpoint mechanisms—metadata representation/encoding, message/turn ordering representation, storage technology, schema implementation, API/transport, and recovery mechanism—remain bounded implementation choices within the selected semantic invariants; no concrete mechanism is selected by this inventory.
- BranchLineage artifact ownership is resolved by DEC-22, and its operational identity/lifecycle/retention/deletion/quota/cleanup policy is resolved by DEC-31: a distinct BranchLineage artifact owns rollback parent/source lineage, uses `RECORDED`/`ACTIVE`/`DETACHED`/`DELETED`, protects dependent checkpoints, and applies the selected 30-day superseded retention and 100-checkpoint workspace quota. Concrete storage encoding and API transport remain implementation projections within those invariants.
- Requirement identifiers `FR-SESS-001`, `FR-WF-001`, and `NFR-COMP-001` are now defined and mapped. Their implementation and executed validation remain planned or partial because the repository has no source implementation or executed evidence.
- Execution-failure responsibility and class binding are resolved by DEC-29: `errors/ERROR_CODES.md` owns error identity and shared recovery metadata, the owning lifecycle owns legal lifecycle effect, and the operation owner owns idempotency and retry conditions. Transient, permanent, and escalation classifications do not create new lifecycle states; legal Task/Execution effects remain those of the existing canonical state machines. DEC-33 adds the exact Task liveness error identities `NXR-1014`, `NXR-1015`, and `NXR-1016`.
- Conversation-local metadata semantic boundary is resolved by DEC-24: creation provenance and integrity information required to interpret and validate the Conversation record are included; concrete field names, types, encoding, schema, storage, API, and implementation remain downstream.
- TM-008 and TM-037 are planned security-completion work with established owners, Phase 7 targets, acceptance criteria, and residual risks.
- Embedded runtimes and `TOOL-403`/`TOOL-404` streaming remain planned/later work; reserved tool IDs are not architecture gaps or reusable identifiers.
- JavaScript-scripted workflows and a dedicated `/workflows` monitoring panel are explicitly out of the current release scope under DEC-32; the declarative Workflow Engine and existing activity-feed projections remain authoritative, and no JavaScript runtime or dedicated panel implementation is claimed.
- The Product Vision exclusivity wording is resolved by DEC-26: Android-first positioning is preserved without presenting market exclusivity as a verified fact.

The Product Vision positioning, requirement owner labels, ROADMAP terminology boundaries, execution-failure class binding, agent-loop liveness boundaries, Task liveness error identities, background terminal liveness, approval-denial composition, approval-expiry classification, BranchLineage operational policy, and workflow scope are resolved by DEC-26 through DEC-36. DEC-31 selects 30-day superseded checkpoint retention, a 100-checkpoint per-workspace quota, and daily idempotent cleanup; DEC-34 selects parent binding, deadline inheritance, and orphan reconciliation for autonomous background terminals; concrete storage encoding, transaction mechanism, process cleanup, and transport remain downstream implementation choices. Concrete Conversation metadata fields and schema remain downstream under DEC-24.

Agent reliability hardening is now documented without claiming implementation completion. `NFR-REL-016` covers hierarchical deadline propagation, `NFR-REL-017` covers unknown-completion reconciliation, `NFR-REL-018` covers repeatable Android reliability evidence, `NFR-CI-003` covers claim-to-evidence binding, `NFR-CI-004` covers acceptance-criteria progress, and `NFR-CI-005` covers non-overridable reasoning ceilings. The ClaimRecord projection, final post-repair claim validation, learning-lesson boundary, and trust-state boundary are now represented in the derived models and contract projections. `testing/cases/E2ETestCases.md` defines the planned `E2E-REL-001` through `E2E-REL-009` evidence cases, while `testing/cases/UnitTestCases.md` defines `UT-AS-004`, `UT-AS-005`, `UT-AS-010`, `UT-CONTRACT-006`, `UT-EV-007`, `UT-RN-013`, and `UT-TOOL-006`. These remain planned validation obligations, not proof that implementation or device tests already exist. `UT-EXEC-001` covers DEC-29 failure-class binding and remains planned.

## Unresolved classification

The following are not silently promoted to architecture decisions:

- implementation module existence and package layout: **PLANNED/DOWNSTREAM** where identified by roadmap or project structure;
- concrete database tables, Room entities, DAOs, serialization, migrations, and storage engines: **IMPLEMENTATION CHOICE/DOWNSTREAM** unless a canonical specification selects them;
- concrete API endpoint names, DTOs, transport, event schemas, and idempotency mechanisms: **IMPLEMENTATION CHOICE/DOWNSTREAM** unless selected by a canonical API source;
- Android process restoration, scheduling, background execution mechanism, and deployment packaging: **DOWNSTREAM/IMPLEMENTATION CHOICE** subject to the existing Android/application boundary documentation;
- retention durations, cleanup timing, quotas, operational metrics, and migration execution procedures: **UNRESOLVED/DOWNSTREAM** where no canonical source selects values or mechanisms; DEC-31 is authoritative for checkpoint retention, quota, and cleanup values, while concrete execution mechanisms remain downstream;
- ownership questions not explicitly established by a decision or canonical architecture document: **OWNER DECISION REQUIRED**, with no owner inferred from terminology.
- Task dependency liveness is resolved by DEC-30: Task dependency graphs are validated acyclic before queueing; failed or cancelled dependencies make dependents fail; Pending/Blocked work inherits the effective deadline and fails on expiry; Workflow validation is not reused as Task authority.
- Task approval denial and external-wait state effects are resolved by DEC-30/DEC-35/DEC-36: explicit denial fails the Task through existing `NXR-2003`/`USER_DENIED`; an expired approval fails the Task through existing `NXR-2003`/`POLICY_DENIAL` under DEC-36 without automatic approval or retry; expiry remains distinct in audit and activity projections; unanswered `BlockedAwaitingInput` fails on the effective deadline; no new state is created.
- Agent failure retry identity is resolved by DEC-30: committed `AgentStatus.FAILED` is terminal for the runtime incarnation; retry creates a new incarnation/version and execution identity while preserving the stable registered `agentId` and predecessor linkage.
- Provider rate-limit wait bounds are resolved by DEC-30: valid Retry-After is bounded by the parent effective deadline; missing/invalid/repeated delays use bounded backoff; deadline exhaustion removes the queue item, checkpoints state, and applies the existing task-deadline failure effect.
- Delegation depth is resolved by DEC-30 at maximum active depth 4; requests beyond the bound fail with existing `NXR-3011` coordination semantics and return to parent replanning. Parent deadlines, concurrency, duplicate-scope, and deadlock controls remain independent.
- DEC-34 resolves autonomous background terminal liveness: every agent-created background session is bound to its parent Task/Execution and immutable effective deadline; parent cancellation, terminal state, or deadline expiry invokes existing termination/checkpoint recovery; missing or terminal parents are reconciled without new TerminalSession states.
- DEC-35 resolves approval-denial composition: `NXR-2003` remains the Tool/Permission result with no side effect; the owning Task commits `Failed`; the participating Agent may project `Paused`; later work requires a new authorization transaction and is not an automatic retry.

## Contradiction and stale-claim handling

Historical decision text is preserved as historical record. Active engineering documents must not treat historical unresolved wording as current authority after a later decision closes the matter. Negative statements about prohibited relationship identity, representation, lifecycle, and cardinality are not stale claims; they are explicit non-decisions or forbidden inferences under DEC-17 through DEC-20.

## Validation record

- Relative Markdown links: validated against the repository filesystem.
- Canonical-source and traceability references: validated for referenced Markdown paths.
- Implementation scope: documentation inventory only; no source implementation is created by this document.
- This inventory is supporting evidence and does not replace any decision, canonical source, model, protocol, specification, or test artifact.

## Implementation-handoff closure

For every documented domain, the existing model/architecture/lifecycle/state-machine/protocol/specification/API/security/testing artifacts are the authoritative evidence set when present. The following cross-domain rules are explicit for implementation handoff:

- Runtime may coordinate documented protocols but does not acquire ownership that a canonical source assigns to another domain.
- Session, Task, Execution, Context, Memory, Workspace, Provider, Plugin, Tool, and Workflow identities remain distinct unless a canonical source explicitly defines a relationship.
- Process death, restart, crash, retry, cancellation, timeout, shutdown, persistence failure, provider failure, plugin failure, authorization failure, quota exhaustion, and migration/version mismatch must preserve the owning domain's documented lifecycle and persistence invariants; no automatic semantic transition is inferred from the platform event alone.
- Duplicate requests and retries must follow the idempotency or repeat-submission rule of the owning protocol/specification; where no such rule exists, the operation is not granted implicit idempotency.
- Concrete schema, transport, Android component, package, and deployment mechanisms may be selected downstream only if they preserve the documented identity, ordering, lifecycle, authorization, concurrency, recovery, cleanup, and compatibility invariants.

## Adversarial scenario coverage

The repository's domain specifications and test strategy documents are the governing sources for adversarial implementation validation. The Session–Conversation matrix explicitly covers process death, restart, concurrency conflicts, rollback, continuation, recreation, checkpoint recovery, and identity/lineage violations. Other domains retain their scenario coverage in the corresponding lifecycle, protocol, security, API, and testing documents; absence of an executable test artifact is not treated as executed evidence.

## Requirement closure

Checkpoint requirements FR-CB001 through FR-CB006 no longer contain a stale decision-dependent TBD marker. Their semantic coverage is derived from the existing checkpoint decisions and supporting engineering contracts; concrete persistence and transport mechanisms remain bounded downstream choices.

## Domain evidence index

The following index records the repository evidence used for each current domain classification. “Contract complete” means semantic obligations and boundaries are documented even when concrete implementation mechanism remains selectable.

- Session — canonical: `models/Session.md`, `state-machines/SessionLifecycle.md`; supporting: `lifecycle/SessionLifecycle.md`, `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`, `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md`, `specs/SESSION_CONVERSATION_ERRORS.md`; tests: `testing/SESSION_CONVERSATION_TEST_MATRIX.md`; boundary: Session identity/lifecycle is distinct from Conversation identity and terminal reuse is forbidden.
- Conversation — canonical: `models/Conversation.md`, `decisions/DEC-13-conversation-identity-persistence.md`; supporting: `architecture/CONVERSATION_CHECKPOINTS.md`, `specs/CONVERSATION_CHECKPOINTS.md`, `specs/DATABASE_SCHEMA.md`, Session–Conversation contracts; tests: Session–Conversation matrix; boundary: immutable identity, ordered records, checkpoint/lineage preservation, and non-destructive branching.
- Checkpoint — canonical: `architecture/CONVERSATION_CHECKPOINTS.md`, `decisions/DEC-8-conversation-checkpoint-rollback.md` through `DEC-10-conversation-checkpoint-ownership.md`; supporting: `specs/CONVERSATION_CHECKPOINTS.md`, `specs/SESSION_CONVERSATION_ERRORS.md`; tests: T10–T13, T25; boundary: checkpoint identity and lifecycle remain distinct from Conversation and relationship identity, while BranchLineage owns rollback parent/source lineage under DEC-22.
- Runtime/Task/Execution/Context/Memory/Agent/Workflow/Tool/Skill/Workspace/Provider/Plugin — canonical sources are the matching `architecture/`, `models/`, `protocols/`, `docs/api/`, `lifecycle/`, `state-machines/`, `registry/`, and `specs/` documents; boundary: each domain retains its documented ownership and identity, and downstream implementation must preserve protocol, lifecycle, authorization, persistence, failure, retry, cancellation, and test obligations stated by those sources.
- Persistence — canonical: `specs/DATABASE.md`, `specs/DATABASE_SCHEMA.md`, `specs/FILE_SYSTEM.md`, and domain-specific persistence sections; boundary: semantic identity, ordering, consistency, recovery, retention/deletion obligations, and migration compatibility are fixed; engine/schema encoding is selectable only within those invariants.
- API — canonical: `docs/api/*.md`, matching `protocols/`, `specs/`, and domain engineering contracts; boundary: semantic operations, preconditions, postconditions, authorization, errors, concurrency, retry/idempotency requirements, and compatibility obligations are fixed; endpoint/DTO/transport names are selectable.
- Security — canonical: `architecture/SECURITY_MODEL.md`, `security/PermissionModel.md`, `security/SandboxPolicy.md`, `security/ThreatModel.md`; supporting: `architecture/SANDBOX.md`, `errors/ERROR_CODES.md`; tests: security test specifications; boundary: deny/authorization/sandbox invariants cannot be weakened by implementation choice.
- Recovery — canonical: lifecycle/state-machine documents and `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md`; boundary: process death, restart, crash, retry, restoration, cancellation, timeout, and shutdown cannot silently create semantic transitions not authorized by the owning domain.
- State machines/Lifecycle — canonical: matching files under `state-machines/` and `lifecycle/`; boundary: states, guards, legal/illegal transitions, terminal behavior, persistence and cleanup expectations are owned by the corresponding domain.
- Protocols — canonical: matching files under `protocols/`; boundary: participants, sequencing, validation, failure, retry, cancellation, timeout, ordering, concurrency, and ownership are preserved; wire representation is selectable where not fixed.
- Testing — canonical: `testing/*.md`, `testing/cases/*`, `testing/EVIDENCE_CONVENTIONS.md`, and the Session–Conversation matrix; boundary: every normative contract requires positive, negative, boundary, lifecycle, failure, recovery, security, persistence, API, and cross-domain validation as applicable.
- Configuration/Deployment/Android/application boundaries — canonical: `PROJECT_SPECIFICATION.md`, `README.md`, `docs/ENVIRONMENT_SETUP.md`, `specs/FULL_ENVIRONMENT.md`, `specs/BACKGROUND_EXECUTION.md`, `specs/GIT.md`, `docs/ROADMAP.md`, and Android/security architecture sources; boundary: planned modules, platform mechanisms, packaging, scheduling, and deployment choices are selectable only if documented lifecycle, persistence, security, resource, recovery, and compatibility invariants remain intact.
- Requirements/Architecture/Decisions/Registries/Roadmap/Repository structure — canonical: matching corpus plus `docs/TRACEABILITY.md` and `docs/CANONICAL_SOURCES.md`; boundary: requirements map to authority, projections, and tests, while planned directories are not represented as implemented.

## Resource and compatibility boundary

Retention, deletion, archive, cleanup, quota, resource exhaustion, operational metrics, migration, and version compatibility are classified per domain source. Where a numeric value or mechanism is absent, the implementation must preserve semantic safety: no unauthorized deletion, no identity/order/lineage loss, no silent incompatible migration, no bypass of quota/error semantics, and no loss of required audit/security evidence. Concrete durations, algorithms, metric names, migration tooling, and packaging remain selectable only when they preserve those constraints and are recorded in the relevant downstream design artifact.

## Legacy decision wording

Occurrences of “unresolved”, “future decision”, and “owner decision required” inside `decisions/` and historical decision projections are retained as historical decision evidence. They are not active gaps when a later decision and supporting contract supersede the earlier open question. The active inventory and engineering documents classify current implementation boundaries explicitly; no historical decision text is treated as a current conflicting authority.
