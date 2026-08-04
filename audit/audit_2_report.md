# Audit 2 Report — Semantic Meaning and Responsibility Audit

## Scope and Method

This audit covers the repository at commit `2fe8e43` on `main`. All 134 tracked Markdown documents were read completely again. The review compared concepts by responsibility and meaning across architecture, state machines, models, protocols, APIs, SDKs, registries, errors, security, requirements, tests, diagrams, standards, UI guidance, and the Full Environment specification.

Search and extraction were used only to organize documents already read in full. A term appearing in two documents was not treated as compatibility evidence. Findings below require an ownership, semantic, lifecycle, or evidence relationship that remains undefined, contradictory, or unverifiable after reading the related documents.

## Repository Integrity

The repository contains 134 Markdown documents and approximately 12,499 Markdown lines. The normalized internal Markdown graph has 649 edges and no broken relative links. Structural connectivity is strong, but semantic connectivity is incomplete: many related documents do not state the same authority, type, transition, error, or evidence relationship.

The audit question was whether two independent implementers could produce behaviorally equivalent runtime, persistence, protocol, security, and test implementations using only the repository. The answer remains no.

## Critical Finding 1 — Evidence Does Not Prove Coverage

The requirements corpus contains 274 distinct requirement-like identifiers. The traceability matrix contains 12 identifiers, leaving 262 requirements without traceability rows. Testing documents contain only 10 identifiers, leaving 264 requirements without explicit test linkage. The threat model contains 28 threat identifiers, while security tests contain no `TM-*` references.

This prevents proving the complete chain `requirement/threat → canonical behavior → implementation → executable test → result`. Scenario tables are useful planning material but are not evidence unless they identify the requirement or threat, contract source, implementation target, expected result, failure condition, and evidence artifact.

**Required action:** create a complete evidence matrix covering every FR, NFR, TM, and TOOL identifier with ownership, contract chain, implementation, tests, expected behavior, failure behavior, and status.

## Critical Finding 2 — Error Responsibility Is Not Distributed as a Contract

`errors/ERROR_CODES.md` defines 78 canonical `NXR-*` codes. Protocol, API, and SDK documents contain no canonical error-code references. Testing references only two codes, and security documents reference six. The error catalog describes recovery, but public contracts do not state which layer owns error classification, retryability, idempotency, lifecycle transition, audit sensitivity, or cleanup.

The semantic consequence is that “error handling” means different things at different boundaries. An API may return an error without a stable catalog identity; an SDK may throw without preserving retry policy; a protocol may describe failure without wire shape; and a background service may not know whether to retry, restore, cancel, or mark failed.

**Required action:** define a canonical error envelope and operation-level error mapping. Every public operation and protocol failure must identify code, category, retryability, idempotency, lifecycle effect, user action, audit policy, and recovery owner.

## Critical Finding 3 — Agent State Has No Single Meaning

The canonical Agent lifecycle defines `Created`, `Configured`, `Ready`, `Running`, `Paused`, `WaitingApproval`, `Reflecting`, `Completing`, `Completed`, `Failed`, and `Cancelled`. The Agent model defines `IDLE`, `THINKING`, `EXECUTING`, `WAITING`, `ERROR`, and `CANCELLED`. Runtime architecture describes planning, reflection, tool execution, and completion activities.

The documents never establish whether model status is a persisted lifecycle projection, whether runtime activities are phases, or whether `WAITING` means approval, dependency waiting, provider waiting, or another condition. Several canonical states have no model representation.

**Required action:** define separate lifecycle-state and execution-phase types, with mapping, persistence, event, API, UI, checkpoint, and recovery semantics. Alternatively, make the model exactly derive from the canonical Agent lifecycle.

## Critical Finding 4 — Lifecycle Authority Is Not Local to Contract Definitions

Models, protocols, APIs, SDKs, and registries for Agent, Plugin, Provider, Task, Workflow, ToolCall, Session, and Workspace generally do not directly link to their canonical lifecycle documents. The source index can point a reader toward lifecycle documents, but it does not itself define the status-to-state or event-to-transition relationship.

This is a responsibility problem: the lifecycle machine owns legal state transitions, the model owns representation, the protocol owns wire events, the API owns public operations, and the SDK owns convenience behavior. Without explicit local mappings, each layer can reinterpret the same word differently.

**Required action:** add direct lifecycle authority and compatibility sections to every lifecycle-bearing model, protocol, API, SDK, and registry document.

## High Finding 5 — Lifecycle Documents Do Not Fully Own Transition Semantics

The lifecycle documents contain state tables and transition tables with triggers, source, target, and guards. They do not consistently define side effects, emitted events, persistence points, rollback, idempotency, invalid transitions, duplicate-event behavior, or crash recovery.

A state machine without these responsibilities is not enough to implement reliable background execution or distributed event handling. Two implementations can follow the same listed transition while producing different durable state, event ordering, retry behavior, or recovery results.

**Required action:** expand every transition with guard, target, side effects, emitted events, persistence, rollback, idempotency, invalid-transition response, and recovery behavior.

## High Finding 6 — Provider Lifecycle Has No Stable State Owner

Provider lifecycle defines `Registered`, `Configuring`, `Configured`, `Testing`, `Healthy`, `Degraded`, `Unhealthy`, `Disabled`, and `Removed`. The Provider model defines identity and configuration but no explicit lifecycle status projection. Architecture refers to registry and in-memory health structures without resolving persistence authority, cache invalidation, API serialization, or routing eligibility.

**Required action:** define the provider state source of truth and its persisted, cached, registry, event, API, and router projections.

## High Finding 7 — Plugin Lifecycle Cannot Be Recovered Deterministically

Plugin lifecycle defines discovery, download, verification, installation, activation, deactivation, uninstall, and failure states. The model exposes only `INSTALLED`, `ACTIVE`, `DISABLED`, and `ERROR`. The repository does not define which states are durable, which are transient, how interrupted operations resume, or how `Inactive` differs from `Disabled`.

**Required action:** define durable/transient boundaries and lifecycle-to-model/event/API/registry projections, including process-death and partial-install recovery.

## High Finding 8 — Task Status and Execution Phase Have Different Responsibilities but No Mapping

Task lifecycle defines formal task states such as `Queued`, `Running`, `Blocked`, `WaitingApproval`, `RetryPending`, and `Completed`. Execution protocol and execution lifecycle documents introduce planning/execution phases and `PLANNING`/`EXECUTING` protocol vocabulary.

The repository does not state whether phases are persisted, events, protocol states, or an independent machine. It also does not define phase behavior during approval, cancellation, retry, checkpoint restore, or background interruption.

**Required action:** define `TaskStatus`, `ExecutionPhase`, `TaskEvent`, checkpoint state, and recovery in one normative compatibility matrix.

## High Finding 9 — ToolCall Responsibility Is Split Across Model, Policy, Protocol, and Error Catalog

The Tool model defines status values; tool architecture and API define approval predicates; tool protocol defines invocation, timeout, cancellation, and errors; security policy defines permission and containment; the error catalog defines tool codes. No single contract maps approval decision, permission result, execution, timeout, partial output, audit event, canonical error, retry, and final status.

**Required action:** make ToolCall a complete contract with request, decision, execution, result, error, audit, timeout, cancellation, and retry semantics.

## High Finding 10 — Operations Do Not Have End-to-End Contract Ownership

Provider architecture/API/SDK share operations such as completion, streaming, embedding, model listing, and health checks, but protocol documents do not explicitly map each operation to wire messages, models, events, errors, permissions, timeout, cancellation, and tests. Agent, Tool, Plugin, and Runtime layers show the same separation.

**Required action:** create an operation matrix for every public API and SDK operation. The matrix must identify request/response models, protocol messages, event order, errors, lifecycle effects, security controls, idempotency, and tests.

## High Finding 11 — Security Controls Are Not Semantically Assigned to Threats

Security ownership is split sensibly among security architecture, threat model, permission model, sandbox policy, and sandbox architecture. However, the 28 threat identifiers are not referenced by security tests, and controls do not consistently identify the threat they mitigate, enforcement point, audit event, expected containment, or residual risk.

**Required action:** map each threat to protected asset, attacker capability, precondition, control, enforcement point, expected denial/containment, telemetry, cleanup, test, and residual risk.

## High Finding 12 — Full Environment Invariants Lack Operational Proof

The Full Environment documents consistently specify one APK-bundled Debian-slim rootfs with glibc, apt, proot, on-demand extraction, Python, Node/npm, binary wheels, and overlays. The semantic gap is not the stated architecture; it is the absence of a complete proof chain for APK integrity, architecture selection, extraction rollback, proot startup, apt operations, Python wheel loading, npm native modules, overlay isolation, cache cleanup, and restart recovery.

**Required action:** link every environment invariant to a requirement, implementation owner, operational test, failure case, and rollback/recovery behavior.

## High Finding 13 — Canonical Ownership Is Often Deferred to an Unnamed Document

Multiple derived and supporting documents say that behavior belongs to an “owning architecture document” without naming it. This appears in protocols, registries, models, UI support, standards, and other focused documents.

This creates semantic ambiguity because architecture, behavior, lifecycle, model, protocol, API, SDK, registry, and test evidence do not have identical authority. A generic owner cannot resolve conflicts or determine which document governs a change.

**Required action:** replace generic language with explicit canonical source, supporting sources, derived boundaries, and conflict-resolution rules.

## Medium Finding 14 — Task Authority Metadata Is Duplicated

`models/Task.md` contains duplicate derived declarations. The Task status relationship to the Task lifecycle is substantively aligned, but document-level authority is ambiguous.

**Required action:** retain one authority block and move enum consistency into an explicit model-constraints section.

## Semantic Implementation Risk

The most dangerous gaps are responsibility gaps rather than missing words: who owns durable state after a crash, who owns event ordering, who owns error classification, who owns retry and idempotency, who owns approval decisions, who owns provider health truth, who owns plugin recovery, who owns sandbox cleanup, and who owns evidence that a requirement is satisfied.

The repository provides enough intent for a skilled team to make these decisions, but not enough normative detail to ensure two independent implementations behave equivalently.

## Required Remediation Sequence

1. Define semantic types: lifecycle state, execution phase, event, error, decision, result, projection, and recovery action.
2. Expand lifecycle machines into complete transition contracts.
3. Add direct lifecycle authority to all lifecycle-bearing contract layers.
4. Create operation-to-message-to-error-to-security-to-test matrices.
5. Build complete requirement and threat evidence traceability.
6. Assign implementation, persistence, event, and recovery ownership.
7. Add Full Environment provisioning and failure-recovery evidence.
8. Re-read every changed document and repeat semantic validation.

## Final Assessment

The repository is structurally connected and high-level intent is coherent, but it is not semantically deterministic or evidence-complete. The primary blockers are disconnected evidence, orphaned error semantics, divergent lifecycle/model/phase vocabularies, incomplete transition ownership, missing operation matrices, and unverified threat controls.

This report records the deepest semantic audit of the current repository state. No source documents were modified during the audit itself.
