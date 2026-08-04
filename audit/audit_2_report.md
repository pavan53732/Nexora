# Audit 2 Report — Forensic Architecture, Contract, and Evidence Audit

## Method and Scope

This pass audits the repository at commit `477173b` on `main`. Every one of the 134 tracked Markdown documents was read completely again. Priority chains were re-read and compared at the symbol, lifecycle, event, error, requirement, security-control, test-scenario, and implementation-assumption levels.

The audit does not treat filenames, headings, or keyword presence as proof. Extracted identifiers and tables were used only to navigate and organize content that had already been read. Findings require cross-document evidence and are phrased conservatively where the documents may represent different abstraction levels.

## Repository Integrity

The repository contains 134 Markdown documents and 12,503 Markdown lines. The normalized Markdown graph contains 649 internal file edges with no broken relative links. The current branch was clean before the audit and no source documents were modified during this pass.

The documentation system is structurally extensive, but the number of links and documents is not evidence that the contracts are compatible. The forensic audit therefore focuses on whether a developer could implement one consistent runtime from the documents without inventing state mappings, error mappings, security controls, or test semantics.

## Critical Finding 1 — Requirement, Threat, and Test Evidence Is Disconnected

The requirement corpus contains 274 distinct requirement-like identifiers. `docs/TRACEABILITY.md` contains 12 rows and 12 identifiers, leaving 262 requirements without traceability rows. The testing corpus contains only 10 requirement identifiers, leaving 264 requirements without explicit test identifiers. `security/ThreatModel.md` contains 28 threat identifiers, while the testing documents contain no `TM-*` identifiers.

This is stronger than an incomplete matrix: it means the repository cannot currently prove the chain `requirement/threat → canonical behavior → implementation → test evidence`. A test table may describe a scenario, but without an identifier, expected control, and linked requirement or threat, it cannot be used as auditable evidence.

**Impact:** critical requirements may be specified but unimplemented, implemented but untested, or tested under a scenario that does not address the stated threat.

**Required action:** build a complete evidence matrix with separate rows for all FR, NFR, TM, and TOOL identifiers; include requirement text, canonical owner, contract chain, implementation owner, test case, expected result, failure condition, evidence location, and status.

## Critical Finding 2 — Error Catalog Is Not Contract-Connected

`errors/ERROR_CODES.md` defines the `NXR-` error namespace and a large catalog spanning runtime, tools, agents, providers, memory, plugins, and sandbox behavior. The protocol, API, SDK, and testing documents do not consistently reference these error codes. The protocol and API layers therefore describe error concepts without a verifiable mapping to the canonical catalog.

**Impact:** callers may receive free-form errors, inconsistent categories, or different retry behavior for the same failure. Recovery rules such as retry, fallback, cancellation, checkpoint restore, and user approval cannot be verified against one error taxonomy.

**Required action:** make `errors/ERROR_CODES.md` canonical for error identity and map every protocol/API/SDK error outcome to an `NXR-*` code, category, retryability, user action, audit requirement, and lifecycle transition. Add error-code assertions to unit, integration, security, and E2E tests.

## Critical Finding 3 — Agent Lifecycle and Agent Model Are Not the Same Contract

`state-machines/AgentLifecycle.md` defines 11 formal lifecycle states: `Created`, `Configured`, `Ready`, `Running`, `Paused`, `WaitingApproval`, `Reflecting`, `Completing`, `Completed`, `Failed`, and `Cancelled`. `models/Agent.md` defines a separate `AgentStatus` enum: `IDLE`, `THINKING`, `EXECUTING`, `WAITING`, `ERROR`, and `CANCELLED`.

The repository does not define a normative projection between these sets. `WAITING` is not equivalent by definition to `WaitingApproval`; `ERROR` is not explicitly `Failed`; `THINKING` and `EXECUTING` are loop phases or statuses not present in the canonical lifecycle; and several canonical states have no persisted model representation.

**Impact:** event payloads, database state, API responses, UI state, resumption, approval gating, and failure recovery can disagree about the agent’s state.

**Required action:** split lifecycle state from execution phase or make the model derive exactly from the canonical lifecycle. Define serialization, persistence, event, API, and UI mappings for every state and phase.

## High Finding 4 — Plugin Lifecycle Is Not Projected Into the Plugin Model

`state-machines/PluginLifecycle.md` defines discovery, download, verification, installation, activation, active, deactivation, inactive, uninstall, uninstalled, and failure states. `models/Plugin.md` exposes only `INSTALLED`, `ACTIVE`, `DISABLED`, and `ERROR`.

A coarse projection may be intentional, but no mapping specifies where transient states live, how failure and retry are persisted, how `Inactive` differs from `Disabled`, or how progress is exposed through the API and events.

**Impact:** installation recovery, audit history, UI progress, disablement, reactivation, and plugin registry consistency are under-specified.

**Required action:** define lifecycle-to-model, lifecycle-to-event, lifecycle-to-API, and lifecycle-to-registry mappings, including durable versus transient state.

## High Finding 5 — Provider Lifecycle Has No Clear Domain-State Projection

`state-machines/ProviderLifecycle.md` defines `Registered`, `Configuring`, `Configured`, `Testing`, `Healthy`, `Degraded`, `Unhealthy`, `Disabled`, and `Removed`. `models/Provider.md` defines provider identity and configuration but does not expose a corresponding provider lifecycle status field or explicit status projection.

The lifecycle text refers to `ProviderRegistry`, a persisted Room provider table, and an in-memory `ProviderStatusMap`, but the model/API/SDK chain does not define which representation is authoritative for routing eligibility or how health transitions are serialized.

**Impact:** routing, failover, health display, manual disablement, and removal can diverge between persistence, memory, and public API consumers.

**Required action:** define the provider status projection, persistence authority, in-memory cache authority, invalidation rules, and API/event serialization.

## High Finding 6 — Task Lifecycle, Execution Phases, and Protocol States Are Not Mapped

`state-machines/TaskLifecycle.md` defines the formal task states. `protocols/Execution-Protocol.md` introduces `PLANNING` and `EXECUTING`, while `specs/EXECUTION_LIFECYCLE.md` describes planning and execution stages and background execution mixes task states with execution behavior.

The documents do not define whether the protocol states are persisted TaskStatus values, transient execution phases, event names, or a second lifecycle. They also do not define how phase transitions interact with `WaitingApproval`, `Blocked`, `RetryPending`, cancellation, checkpointing, and background recovery.

**Impact:** a task can be displayed as Running while an execution protocol consumer sees PLANNING, or resumed into an invalid state after background interruption.

**Required action:** create a normative TaskStatus/ExecutionPhase/Event compatibility table and specify phase persistence, event ordering, cancellation, retry, approval, and checkpoint semantics.

## High Finding 7 — Tool Errors, Approval, Timeout, and Status Are Separate Unmapped Concepts

`models/Tool.md` defines `ToolCallStatus` values `PENDING`, `APPROVED`, `EXECUTING`, `COMPLETED`, `DENIED`, and `ERROR`. `protocols/Tool-Protocol.md` defines invocation, error handling, and timeout behavior. `architecture/TOOL_SYSTEM.md` and `docs/api/Tool-API.md` use `NeedsApproval` as an approval predicate, while `errors/ERROR_CODES.md` defines tool-specific `NXR-2001` through `NXR-2011` errors.

The repository does not establish one normative ToolCall contract connecting status, approval decision, timeout transition, cancellation, structured error code, partial output, audit record, and retry behavior.

**Impact:** permission denial may be confused with execution failure; timeout may be treated as a generic error; partial output and retry decisions may be lost; audit logs may not capture the policy decision.

**Required action:** define a ToolCall lifecycle and error mapping with explicit request/response/event schemas and test each transition.

## High Finding 8 — Error Recovery Semantics Are Not Consistent Across Layers

The error catalog assigns recovery actions such as retry, fallback provider, checkpoint restore, process termination, user approval, and context pruning. Protocols and APIs do not consistently carry the recovery metadata, and the testing corpus does not assert error code, retryability, lifecycle transition, or cleanup behavior.

**Impact:** the same error can produce different behavior depending on whether it is observed by the runtime, an API caller, an SDK consumer, or a background-service recovery path.

**Required action:** define an error envelope containing code, category, retryability, idempotency, user action, lifecycle transition, checkpoint impact, audit sensitivity, and recovery owner. Map every catalog row to tests.

## High Finding 9 — Threat Model Controls Are Not Tested by Threat Identifier

`security/ThreatModel.md` contains 28 threats. `testing/SecurityTests.md` contains OWASP categories and penetration scenarios but no threat identifiers. The test document therefore cannot demonstrate that every threat has a control objective and a pass/fail test.

**Required action:** add `TM-*` references to security scenarios, identify the enforcement point, attacker capability, protected asset, expected denial/containment result, telemetry, and residual risk.

## Medium Finding 10 — Derived Document Ownership Remains Imprecise

Twenty-six documents still use generic derived declarations referring to an owning architecture document. Additional derived documents lack a precise source link in their initial authority metadata, including `models/Session.md`, protocol documents, and `registry/FEATURES.md`.

**Required action:** define ownership separately for identity, behavior, lifecycle, wire contract, public API, SDK convenience, registry membership, capability projection, and test evidence. Every derived document should name its canonical source and its non-authoritative boundaries.

## Medium Finding 11 — Task Model Contains Duplicate Authority Blocks

`models/Task.md` has two derived status declarations. The model correctly states that `TaskStatus` must match the canonical task lifecycle, but the duplicate authority blocks make document-level ownership ambiguous.

**Required action:** retain one authority declaration and move enum consistency into a model constraint section.

## Medium Finding 12 — Full Environment Is Specified More Strongly Than It Is Proven

`specs/FULL_ENVIRONMENT.md` and `architecture/SANDBOX.md` consistently define one bundled Debian-slim rootfs with glibc, apt, proot, APK assets, on-demand extraction, Python, Node/npm, binary-wheel compatibility, and workspace overlays. The obsolete “legacy optional environment” wording is absent.

The remaining gap is evidence: requirements and tests do not fully map asset integrity, architecture selection, extraction rollback, proot launch, apt installation, Python wheel loading, npm native modules, overlay isolation, cache cleanup, and recovery. The specification is detailed, but the implementation/test proof chain is incomplete.

## Deep Implementation Feasibility Assessment

The documentation names concrete implementation concepts such as `ProviderRegistry`, `ProviderStatusMap`, `HealthMonitor`, `PluginManager`, `ToolRegistry`, `EventBus`, `PermissionManager`, `ProcessManager`, `AgentExecutionService`, Room tables, APK assets, proot binaries, rootfs overlays, and checkpoint storage. The cross-layer documents do not consistently identify one implementation owner, lifecycle owner, persistence owner, and test fixture for each concept.

The risk is not that the architecture is obviously impossible. The risk is that implementation will require undocumented decisions at boundaries where the system needs deterministic behavior: process termination, background recovery, error propagation, registry cache invalidation, provider health persistence, plugin transient states, tool approval, and agent checkpoint restore.

**Required action:** create an implementation contract map for every named service, manager, registry, database entity, process boundary, APK asset, and recovery operation.

## Deep Test Quality Assessment

The testing documents contain structured tables, but most are category or scenario inventories rather than complete executable specifications. `testing/E2ETests.md` has journey tables with pass criteria; unit and integration documents list areas and scenarios; security tests list OWASP areas and penetration scenarios; performance tests define metrics. These are useful test plans, but they are not fully connected to requirements, threats, lifecycle states, error codes, or implementation owners.

A complete test evidence record must specify setup, input, action, expected output, failure condition, state transition, requirement/threat ID, contract source, test level, and cleanup. Without those fields, a test can be present in prose while the actual behavior remains unverified.

## Required Remediation Order

1. Establish canonical error identity and recovery mapping.
2. Define lifecycle/model/phase/event compatibility for Agent, Task, Plugin, Provider, Workflow, ToolCall, TerminalSession, Workspace, and background execution.
3. Resolve precise ownership for API, protocol, SDK, registry, model, and test documents.
4. Build complete requirement and threat traceability.
5. Build implementation-owner and persistence-owner mappings.
6. Convert test inventories into requirement- and threat-linked behavioral evidence.
7. Add Full Environment extraction and package-runtime tests.
8. Re-read all affected documents and repeat the deep comparison.

## Final Assessment

The repository has a coherent high-level design and a strong structural document graph, but it is not yet implementation-proof. The deepest unresolved risks are disconnected evidence, missing error-contract integration, lifecycle/model divergence, unmapped execution phases, absent provider/plugin state projections, and incomplete threat/test linkage.

This report records the forensic audit status and does not claim end-to-end completion. No source documents were changed during this audit pass.
