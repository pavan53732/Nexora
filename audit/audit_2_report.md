# Audit 2 Report — Maximum-Depth Architectural Contract Audit

## Scope and Method

This maximum-depth pass audits the repository at commit `88d4fcc` on `main`. All 134 tracked Markdown documents were read completely again, including prior audit output. Priority subsystem chains were re-read and compared at four boundaries: lifecycle-to-model, architecture-to-API, protocol-to-error, and requirement-to-test.

The review treats extraction as navigation only. Findings are based on document meaning, cross-layer compatibility, explicit ownership, and whether an implementer can derive deterministic behavior without inventing undocumented rules.

## Repository Integrity

The repository contains 134 Markdown documents and 12,509 Markdown lines. The normalized internal Markdown graph has 649 edges and zero broken relative links. No source documents were modified during this audit pass before the report update.

Structural integrity is good. Semantic integrity is not yet sufficient: links connect documents, but many connected documents do not expose the same state, error, lifecycle, or evidence contract.

## Critical Finding 1 — Complete Evidence Chain Does Not Exist

The requirements corpus defines 274 requirement-like identifiers. The traceability matrix contains 12 identifiers, leaving 262 requirements without traceability rows. The testing corpus contains only 10 identifiers, leaving 264 requirements without explicit test identifiers. The threat model defines 28 `TM-*` identifiers, while testing documents contain no threat identifiers.

This prevents proving `requirement/threat → canonical behavior → implementation → executable test → result`. Test tables can describe useful scenarios while still failing to identify which requirement, threat, lifecycle, error, and implementation behavior they prove.

**Required action:** create a complete evidence matrix covering FR, NFR, TM, and TOOL identifiers with canonical source, contract chain, implementation owner, test case, expected result, failure behavior, evidence artifact, and status.

## Critical Finding 2 — Error Catalog Is Orphaned From Public Contracts

`errors/ERROR_CODES.md` defines 78 canonical `NXR-*` error codes. The protocol documents contain no `NXR-*` references, the API documents contain no `NXR-*` references, and the SDK documents contain no `NXR-*` references. Testing references only `NXR-2003` and `NXR-7005`, while security documents reference six codes.

The result is not merely missing citations: public consumers cannot determine which canonical error code corresponds to an API failure, protocol failure, SDK exception, retry decision, or lifecycle transition. The error catalog’s recovery instructions are therefore not enforceable at the contract boundaries.

**Required action:** define one error envelope and map every protocol/API/SDK operation to canonical error codes, category, retryability, idempotency, lifecycle transition, audit sensitivity, user action, and cleanup rule. Add assertions for every mapped code.

## Critical Finding 3 — Agent State Contract Is Structurally Divergent

The canonical Agent lifecycle defines `Created`, `Configured`, `Ready`, `Running`, `Paused`, `WaitingApproval`, `Reflecting`, `Completing`, `Completed`, `Failed`, and `Cancelled`. `models/Agent.md` defines `IDLE`, `THINKING`, `EXECUTING`, `WAITING`, `ERROR`, and `CANCELLED`.

No normative mapping explains which model value represents `Ready`, `Paused`, `Reflecting`, or `Completing`, whether `THINKING` is a phase, or whether `WAITING` means approval, dependency blocking, or provider waiting. APIs and SDKs do not explicitly reference the canonical lifecycle.

**Impact:** persistence, UI, event consumers, checkpoint restore, approval gates, and cancellation can disagree.

**Required action:** split `AgentLifecycleState` from `AgentExecutionPhase`, define the mapping and serialization rules, or make the model exactly derive from the lifecycle.

## Critical Finding 4 — Lifecycle Documents Are Not Referenced by Contract Layers

The API, model, protocol, and SDK documents in the audited subsystem set do not explicitly link to their canonical lifecycle documents. This includes Agent, Plugin, Provider, Tool, Task, Workflow, and related model/protocol layers.

A lifecycle can be indirectly known through architecture or source maps, but indirect knowledge is not enough for a contract consumer. A model enum, protocol event, or API status field needs an explicit lifecycle authority and mapping rule at the point where it is defined.

**Required action:** add direct lifecycle ownership links and compatibility sections to each affected model, protocol, API, SDK, and registry document.

## High Finding 5 — Provider Lifecycle Has No Model/API State Surface

`state-machines/ProviderLifecycle.md` defines nine provider states, but `models/Provider.md` does not define a lifecycle status field or explicit state projection. The architecture mentions a registry and in-memory provider status map, but the persistence and public API authority is not resolved.

**Impact:** health, degraded operation, failover, disabled providers, and removal can behave differently in persistence, memory, registry, and API responses.

**Required action:** define the authoritative provider-state store, cache invalidation, registry behavior, event payload, and API serialization.

## High Finding 6 — Plugin Lifecycle Has No Complete Durable/Transient Boundary

The Plugin lifecycle defines 13 states, including download, verification, installation, activation, deactivation, uninstall, and failure. The Plugin model exposes only four coarse statuses. The documents do not say which lifecycle states are durable, which are events only, how progress is recovered, or how `Inactive` differs from `Disabled`.

**Required action:** add a durable/transient state table and lifecycle-to-model/event/API/registry projection.

## High Finding 7 — Task Status and Execution Phase Are Unresolved

Task lifecycle states are defined formally, while execution protocol and execution-lifecycle documents introduce `PLANNING`, `EXECUTING`, stages, and phases. The repository does not define whether these are Task statuses, transient phases, events, or a second machine.

**Impact:** status display, event ordering, checkpointing, cancellation, approval, retry, and background recovery can become incompatible.

**Required action:** define `TaskStatus`, `ExecutionPhase`, `TaskEvent`, and their legal transitions in one compatibility matrix.

## High Finding 8 — ToolCall Status, Approval, Error, and Timeout Are Unmapped

The Tool model defines six status values; the architecture/API defines `NeedsApproval`; the protocol defines invocation, timeout, and errors; and the error catalog defines tool-specific codes. No single document maps approval decisions, timeout, cancellation, partial output, audit records, retries, and canonical errors to ToolCall status transitions.

**Required action:** make ToolCall a complete contract with request, approval decision, execution, timeout, cancellation, result, error, audit, and retry semantics.

## High Finding 9 — Contract Operations Are Not Consistently Exposed Across Layers

Provider architecture, API, and SDK documents share operations such as `complete`, `stream`, `embed`, `listModels`, and `healthCheck`, but protocol documents express the wire behavior without an explicit operation-to-message mapping. Agent, Task, Tool, and Plugin chains show similar separation: architecture/API/SDK method names exist, while protocol documents are prose or event tables without a complete method/message/error correspondence.

**Impact:** a developer cannot mechanically derive the wire request, response, event stream, error envelope, timeout, cancellation, and idempotency behavior for each public operation.

**Required action:** add operation matrices for every public API and SDK operation, including protocol messages, models, errors, lifecycle effects, permissions, and tests.

## High Finding 10 — Security Controls Lack Threat-Linked Verification

The security architecture is divided sensibly among security model, threat model, permission model, sandbox policy, and sandbox architecture. However, 28 threat identifiers are not referenced by security tests, and most security controls are not mapped to an enforcement point, audit event, expected denial/containment behavior, or cleanup assertion.

**Required action:** make each threat a testable row with attacker capability, asset, precondition, control, enforcement point, expected result, telemetry, and residual risk.

## High Finding 11 — Full Environment Runtime Contract Is Not Evidence-Complete

The Full Environment specification is internally consistent: one APK-bundled Debian-slim rootfs, glibc, apt, proot, on-demand extraction, Python, Node/npm, wheels, and overlays. The cross-document gap is test and implementation evidence for architecture selection, APK integrity, extraction rollback, proot startup, apt operations, Python wheels, npm native modules, overlay isolation, cache cleanup, and restart recovery.

**Required action:** link each environment behavior to a requirement, implementation owner, and executable test with failure and rollback cases.

## Medium Finding 12 — Derived Ownership Metadata Is Still Too Generic

Twenty-six documents use generic “owning architecture document” language. Additional derived documents lack precise source links in their authority headers. Architecture, behavior, lifecycle, model, protocol, API, SDK, registry, and test evidence have different ownership semantics and should not all point generically to architecture.

**Required action:** replace generic declarations with precise canonical source, supporting sources, derived boundaries, and conflict-resolution rules.

## Medium Finding 13 — Task Model Contains Duplicate Authority Blocks

`models/Task.md` contains duplicate derived declarations. The status enum’s relationship to the Task lifecycle is substantively correct, but metadata ownership is ambiguous.

**Required action:** retain one document authority block and move consistency requirements into a model constraints section.

## Implementation Feasibility

The documents name concrete runtime components, including registries, status maps, managers, event bus, permission manager, process manager, execution services, Room persistence, APK assets, proot binaries, rootfs overlays, checkpoints, and background services. The cross-layer contracts do not consistently identify one owner for each component’s state, persistence, errors, lifecycle transitions, and tests.

This does not prove infeasibility. It proves that implementation still requires undocumented decisions at critical boundaries: process termination, background recovery, error propagation, cache invalidation, provider health persistence, plugin transient states, tool approval, and agent checkpoint restore.

## Remediation Sequence

1. Canonicalize error identity and recovery envelopes.
2. Define lifecycle/model/phase/event matrices for every lifecycle-bearing subsystem.
3. Add direct lifecycle links to models, protocols, APIs, SDKs, and registries.
4. Add operation-to-message-to-error-to-test matrices.
5. Build complete requirement and threat evidence traceability.
6. Assign implementation and persistence ownership for every named runtime component.
7. Add Full Environment provisioning and runtime tests.
8. Re-read every changed document and repeat graph, contract, and evidence validation.

## Final Assessment

The repository has strong document organization and coherent high-level intent, but it is not yet implementation-proof or evidence-complete. The strongest blockers are orphaned error contracts, lifecycle/model divergence, absent direct lifecycle authority in contract layers, unresolved execution phases, absent provider/plugin projections, and disconnected requirement/threat/test evidence.

This is the maximum-depth audit report for the current repository state. No source documents were modified during the audit itself.
