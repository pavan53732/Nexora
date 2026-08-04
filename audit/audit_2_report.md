# Audit 2 Report — Deep Architecture and Contract Audit

## Audit Scope

This deep audit covers the repository at commit `8491b8d` on `main`, including the previously generated audit report as part of the repository corpus. All 134 tracked Markdown documents were read completely. High-risk subsystem chains were re-read in full, then compared across canonical architecture, ADRs, lifecycle state machines, models, protocols, APIs, SDKs, registries, requirements, security documents, tests, and diagrams.

The audit intentionally treats search and extraction as navigation and bookkeeping only. Findings below are based on cross-document interpretation and contract comparison, not isolated keyword absence.

## Deep Repository Model

The repository describes an Android agent-first runtime with a layered execution path: user/workspace interaction feeds tasks and workflows; the runtime resolves context and plans execution; agent loops invoke providers and tools; tools cross permission and sandbox boundaries; plugins and registries extend capabilities; memory and context services persist and project state; background execution preserves eligible work; lifecycle state machines define formal state; APIs, protocols, and SDKs expose contracts; tests and requirements define expected behavior.

The document graph contains 649 normalized internal Markdown edges with no unresolved relative file links. Structural link correctness is therefore strong, but semantic traceability and contract completeness are not equivalent to link correctness.

## Critical Finding 1 — Requirements Are Not Traceable End to End

The requirements corpus contains 274 distinct requirement-like identifiers, while `docs/TRACEABILITY.md` contains 12 rows and 12 identifiers. Testing documents contain only 10 requirement identifiers, and the 28 threat IDs in `security/ThreatModel.md` appear in none of the testing documents.

This is a direct cross-document failure between requirements, threat analysis, traceability, and testing. The current matrix has only a small sample and marks each sample as `✅`, but it does not prove implementation, test behavior, security coverage, performance coverage, or end-to-end satisfaction.

**Impact:** the project cannot demonstrate that its specified behavior is implemented or testable. Missing rows conceal unimplemented, contradictory, deferred, and untested requirements.

**Remediation:** create one row per requirement and threat identifier with canonical owner, lifecycle, model, protocol, API, SDK, registry, implementation owner, unit test, integration test, E2E test, security/performance test, evidence, and status. Do not use `✅` unless the linked evidence defines and verifies the requirement.

## Critical Finding 2 — Security Threats Are Not Connected to Security Tests

`security/ThreatModel.md` defines 28 threat identifiers, but `testing/SecurityTests.md`, `testing/IntegrationTests.md`, and the other testing documents contain no threat identifiers. The security test document describes penetration scenarios, but the scenarios are not traceably tied to the threat model’s specific threats.

**Impact:** a security scenario can appear covered while the actual threat, attack precondition, expected control, and failure signal remain unknown. This prevents proving that sandbox escape, credential leakage, permission bypass, network policy failure, plugin abuse, and prompt-injection containment are tested against the stated threat model.

**Remediation:** map every `TM-*` identifier to one or more test cases with attacker capability, precondition, action, expected control, expected denial or containment result, logging/audit expectation, and cleanup condition.

## High Finding 3 — Formal Agent Lifecycle and Agent Model Use Different State Vocabularies

The canonical Agent lifecycle defines `Created`, `Configured`, `Ready`, `Running`, `Paused`, `WaitingApproval`, `Reflecting`, `Completing`, `Completed`, `Failed`, and `Cancelled`. `models/Agent.md` instead defines `IDLE`, `THINKING`, `EXECUTING`, `WAITING`, `ERROR`, and `CANCELLED` as `AgentStatus` values.

These may be intended as persisted lifecycle states versus runtime loop phases, but the model does not establish that distinction strongly enough. `WAITING` is not the canonical `WaitingApproval`; `ERROR` is not the canonical `Failed`; `THINKING` and `EXECUTING` are not canonical states; and `Created`, `Configured`, `Ready`, `Paused`, `Reflecting`, and `Completing` are absent from the model enum.

**Impact:** persistence, event consumers, API responses, and UI state can disagree about the current agent state. Recovery and approval logic may be implemented against the wrong enum.

**Remediation:** either make `AgentStatus` exactly derive from the canonical state machine or explicitly split the model into `AgentLifecycleState` and `AgentExecutionPhase`, with a normative mapping table and API serialization rules.

## High Finding 4 — Plugin Model Is a Projection, but Its Mapping Is Undefined

The canonical Plugin lifecycle contains 13 states, including discovery, download, verification, installation, activation, deactivation, uninstall, and failure states. `models/Plugin.md` exposes only `INSTALLED`, `ACTIVE`, `DISABLED`, and `ERROR`.

A compact persisted status can be valid, but the repository does not define whether the model is a coarse projection, whether transient states are event-only, or how `Failed`, `Inactive`, `Verifying`, and `Activating` are represented during recovery. The protocol and API documents describe lifecycle messages and hooks, but do not provide a complete state-to-model mapping.

**Impact:** plugin installation progress, retries, failure recovery, UI display, and audit logs cannot be implemented consistently.

**Remediation:** define a canonical mapping from every lifecycle state to persisted model state, event state, API state, and registry state. Specify which transitions are durable and which are transient.

## High Finding 5 — Tool Protocol and Tool Model Are Not Fully Aligned

`models/Tool.md` defines `PENDING`, `APPROVED`, `EXECUTING`, `COMPLETED`, `DENIED`, and `ERROR` for `ToolCallStatus`. `protocols/Tool-Protocol.md` defines invocation, error handling, and timeout behavior but does not expose the complete status contract or a formal mapping to the model. The tool architecture and API additionally use approval predicates such as `NeedsApproval`.

**Impact:** callers cannot determine whether approval is a state, a permission decision, or an operation result; timeout and denial outcomes may be serialized inconsistently; and tool execution events may not match persisted status.

**Remediation:** define ToolCall lifecycle ownership, request/response fields, approval decision semantics, timeout transitions, cancellation transitions, error codes, and event-to-model mapping in one normative contract chain.

## High Finding 6 — Execution Protocol Uses Phase Terms Without a Formal Relationship to Task Lifecycle

The canonical Task lifecycle defines `Draft`, `Pending`, `Queued`, `Running`, `Blocked`, `WaitingApproval`, `Completed`, `Failed`, `Cancelled`, and `RetryPending`. `protocols/Execution-Protocol.md` introduces `PLANNING` and `EXECUTING`, while `specs/EXECUTION_LIFECYCLE.md` describes planning and execution stages and background execution uses task lifecycle terms.

Those terms may correctly represent execution phases, but the protocol does not make the phase/state distinction normative. There is no complete mapping specifying whether `PLANNING` is inside `Pending`, `Queued`, or `Running`, or how phase transitions are emitted while the Task remains in a formal lifecycle state.

**Impact:** event consumers, checkpoint recovery, retry logic, and user-facing status can diverge.

**Remediation:** add a formal TaskState/ExecutionPhase compatibility matrix, define serialization, persistence, events, cancellation, approval, retry, and recovery behavior for every combination.

## High Finding 7 — Provider Model Does Not Expose the Canonical Provider Lifecycle

The canonical Provider lifecycle defines `Registered`, `Configuring`, `Configured`, `Testing`, `Healthy`, `Degraded`, `Unhealthy`, `Disabled`, and `Removed`. `models/Provider.md` defines provider identity and configuration but does not provide a corresponding lifecycle status field or explicit state projection.

The provider architecture, API, protocol, SDK, registry, and lifecycle documents describe routing and health behavior, but the persisted model does not clearly identify where lifecycle state is stored or how API consumers observe it.

**Impact:** provider health, failover eligibility, disablement, removal, and routing decisions may be maintained only in implementation assumptions instead of a stable domain contract.

**Remediation:** add a canonical provider status projection and define the relationship between persisted status, in-memory `ProviderStatusMap`, registry membership, API responses, and routing eligibility.

## High Finding 8 — API, Protocol, SDK, Registry, and Test Ownership Remains Generic

Twenty-six documents use derived headers that refer to an “owning architecture document” without identifying the precise source relationship. This includes APIs, protocols, SDKs, registries, and testing documents. Several additional derived headers lack a Markdown source link in their opening metadata, including `models/Session.md`, all protocol documents, and `registry/FEATURES.md`.

These layers cannot all derive the same way: protocols define message contracts, APIs define public operations, SDKs define convenience wrappers, registries define identity/catalog membership, and tests define evidence. Generic ownership statements make conflict resolution and change impact analysis unreliable.

**Remediation:** replace generic headers with precise ownership and dependency declarations for every contract-layer document.

## Medium Finding 9 — Task Model Contains Duplicate Authority Metadata

`models/Task.md` has two document-level derived declarations. Its enum constraint correctly points to `state-machines/TaskLifecycle.md`, but the duplicate authority blocks create ambiguity about document metadata and should be reduced to one declaration plus a separate model constraint section.

This is a documentation governance defect, not a verified Task state mismatch: the Task status values correspond to the canonical lifecycle names.

## Medium Finding 10 — Full Environment Behavior Is Strongly Specified but Not Fully Verified by Tests

`specs/FULL_ENVIRONMENT.md` and `architecture/SANDBOX.md` consistently describe the single bundled Debian-slim environment: glibc, apt, proot, APK assets, on-demand extraction, Python, Node/npm, binary-wheel compatibility, and workspace overlays. The obsolete “legacy optional environment” phrase is absent.

However, the requirement and testing layers do not establish complete evidence for architecture selection, APK asset integrity, rootfs extraction, proot startup, apt installation, Python binary wheels, npm native modules, overlay isolation, cache cleanup, and recovery. The environment specification is detailed, but the implementation and test chain is incomplete.

**Remediation:** add explicit requirement and test mappings for each provisioning and runtime behavior, including failure and rollback conditions.

## High Finding 11 — Testing Documents Describe Areas but Not Complete Behavioral Contracts

The testing corpus has six documents and covers unit, integration, E2E, performance, regression, and security categories. However, most testing documents do not carry requirement IDs, threat IDs, lifecycle IDs, or complete scenario structures. `testing/E2ETests.md` contains journey tables, but the broader test corpus is not connected to the full requirement universe.

**Impact:** test existence cannot be distinguished from test intent, and gaps in cancellation, approval, checkpoint recovery, provider failover, plugin disablement, sandbox isolation, package installation, background recovery, and secret handling remain unmeasured.

**Remediation:** define each test with setup, input, action, expected output, failure condition, state transition, requirement ID, and test level.

## Deep Security Boundary Assessment

The ownership split among `SECURITY_MODEL.md`, `ThreatModel.md`, `PermissionModel.md`, `SandboxPolicy.md`, and `SANDBOX.md` is architecturally sensible. The missing piece is a verifiable chain from each security responsibility to a requirement, enforcement point, audit event, and test.

The most important unproven controls are permission-before-execution, plugin containment, provider credential isolation from guest processes, network egress enforcement, background approval preservation, secret-safe logging, package installation confinement, and prompt-injection containment. These should be treated as explicit control objectives rather than prose assertions.

## Deep Feasibility Assessment

The Full Environment documents contain concrete assumptions about Debian rootfs assets, proot binaries, APK extraction, overlays, PT_INTERP handling, package managers, and runtime probes. Runtime and background documents contain Android service and lifecycle assumptions. The repository still lacks a complete stable mapping from these assumptions to implementation modules, service classes, persistence tables, process-control components, and test fixtures.

The system is not proven infeasible from the documents reviewed. It is under-specified at the implementation traceability boundary. The next remediation must identify the implementation owner for every named service, manager, registry, process boundary, asset, database record, and recovery operation.

## Required Remediation Order

1. Define exact ownership and mapping rules for lifecycle states, execution phases, events, models, and APIs.
2. Resolve Agent, Plugin, Provider, Tool, and Task contract mismatches.
3. Replace generic derived headers with precise source relationships.
4. Build complete requirement and threat traceability.
5. Add implementation-owner mappings for runtime, Android services, sandbox, Full Environment, persistence, and process control.
6. Expand test documents into requirement- and threat-linked behavioral scenarios.
7. Reconcile diagrams and supporting overviews with the corrected canonical contracts.
8. Re-read all changed and related documents, rebuild the graph, and repeat the deep audit.

## Final Assessment

The repository has a coherent high-level architecture and a strong structural documentation graph, but it is not yet contract-complete or evidence-complete. The most serious risks are incomplete traceability, absent threat-to-test mapping, and lifecycle/model/protocol ambiguity across Agent, Plugin, Provider, Tool, and Task execution.

This report is a deep audit of the current repository state; it is not a completion claim. The repository remains clean except for this report file, and no remediation changes were made during the audit.
