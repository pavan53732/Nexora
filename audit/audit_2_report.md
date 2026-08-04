# Audit 2 Report — End-to-End Repository Architecture Validation

## Scope and Method

This audit covers the Nexora repository at baseline commit `e768f19` on `main`. The repository was treated as an integrated specification rather than a collection of isolated files: all 133 tracked Markdown documents were read completely, subsystem document chains were re-read, canonical ownership was compared with supporting and derived documents, and relative links were resolved before findings were recorded.

The audit distinguishes document navigation from evidence. Search-like extraction was used only to organize already-read material; findings below are based on cross-document reasoning across architecture, state machines, models, protocols, APIs, SDKs, registries, requirements, security, testing, and diagrams.

## Repository Model

The repository contains 136 tracked files, including 133 Markdown documents and 12,365 Markdown lines. The documentation hierarchy consists of 10 architecture documents, 8 ADR documents, 13 models, 6 protocols, 5 APIs, 4 SDKs, 8 registries, 6 requirement documents, 5 lifecycle state machines, 6 testing documents, 5 diagrams, 3 security documents, 12 focused specifications, 7 standards, 7 UI documents, 4 backlog documents, and master/meta documents.

The integrated system model is: product and master specification → runtime and subsystem architecture → lifecycle state machines → domain models → wire protocols → public APIs → SDK convenience layers → registries and capability views → requirements → tests and diagrams. The repository now contains a canonical-source index and glossary, but those documents are governance aids; the subsystem documents remain the behavioral authorities identified by that index.

## Ownership and Graph Validation

`docs/CANONICAL_SOURCES.md` identifies 19 major concept owners, including runtime, agent loop, multi-agent coordination, workflow progression, tools, memory, context assembly, providers, plugins, sandbox, security, permissions, Full Environment behavior, task lifecycle, and background execution. The cross-reference graph contains 649 normalized internal Markdown edges and no unresolved relative file links.

The graph is structurally connected, but structural connectivity is not equivalent to semantic traceability. Several API, protocol, SDK, registry, and testing documents still use generic “owning architecture document” language instead of precise ownership relationships. That weakens the ability to determine whether a contract is authoritative, derived, or merely explanatory.

## Finding 1 — Traceability Is Incomplete

**Severity: Critical.** The requirements documents contain 274 distinct requirement-like identifiers, while `docs/TRACEABILITY.md` contains only 12 rows and 12 identifiers. The matrix therefore omits 262 identified requirements, including large portions of agent, autonomy, context management, execution lifecycle, sandbox, and environment requirements.

This is a cross-document gap between `requirements/FR.md` and `requirements/NFR.md` on one side and `docs/TRACEABILITY.md` on the other. The matrix currently maps only a small sample and marks every mapped row with `✅`, but it does not provide implementation modules, security/performance test columns, or evidence that each linked document actually satisfies the requirement.

**Required remediation:** expand the matrix to one row per requirement, add canonical architecture, lifecycle, model, protocol, API, SDK, registry, implementation, unit, integration, E2E, security/performance, and status columns, and use evidence-based statuses rather than treating a link as proof.

## Finding 2 — Derived Contract Ownership Is Too Generic

**Severity: High.** Twenty-six documents have derived status declarations that still refer generically to “the owning architecture document.” This affects API, protocol, SDK, registry, and test documents. Those layers have different responsibilities and cannot all be derived from architecture in the same way.

For example, an API should derive public operations and request/response semantics from architecture plus its protocol and model; a protocol should own wire/message shape; an SDK should provide convenience behavior over the API; a registry should own catalog membership or a capability projection; and testing documents should map behavior to requirements and lifecycle contracts. Generic ownership language makes it difficult to resolve conflicts and violates the repository’s intended distinction between identity, behavior, lifecycle, wire contract, API, SDK, registry, and derived capability view.

**Required remediation:** assign precise source relationships to every API, protocol, SDK, registry, and test document. State what the document owns and what it may not redefine.

## Finding 3 — Task Model Has Duplicate Authority Declarations

**Severity: Medium.** `models/Task.md` contains two top-level derived status declarations: one document-level block and a second block immediately above the persisted shape. The second block is useful because it states that the `TaskStatus` enum must match `state-machines/TaskLifecycle.md`, but the duplicate document authority declaration creates ambiguity about which block is the controlling metadata.

The canonical task lifecycle defines Draft, Pending, Queued, Running, Blocked, WaitingApproval, Completed, Failed, Cancelled, and RetryPending. The model includes corresponding status values, so the lifecycle relationship is substantively clear; the problem is ownership metadata duplication rather than a verified state mismatch.

**Required remediation:** retain one document-level authority block and convert the enum consistency statement into a normal model constraint or explicit “Derived constraints” section.

## Finding 4 — Lifecycle Contract Requires Explicit Compatibility Matrices

**Severity: High.** The canonical state machines define formal states for Agent, Plugin, Provider, Task, and Workflow, but supporting execution and background documents use overlapping state vocabulary from multiple lifecycles. For example, `specs/EXECUTION_LIFECYCLE.md` and `specs/BACKGROUND_EXECUTION.md` use task and execution terms such as `RetryPending`, `WaitingApproval`, `Queued`, `Running`, and `Blocked`, while the protocol layer introduces execution terms such as `PLANNING` and `EXECUTING`.

This is not automatically a contradiction: some terms may represent execution phases rather than TaskStatus values. However, the repository does not consistently state that distinction at every contract boundary. Without compatibility tables, implementers can incorrectly treat a phase as a persisted state or introduce a state that is absent from the canonical machine.

**Required remediation:** add compatibility tables for Task/Execution, Agent/AgentStep, Workflow/WorkflowStep, Provider/ProviderRequest, Plugin/PluginOperation, TerminalSession, Workspace, and ToolCall. Each table must classify every term as formal state, phase, operation, event, or prose and identify the canonical owner.

## Finding 5 — Full Environment Architecture Is Consistent but Cross-Document Coverage Is Uneven

**Severity: Medium.** `specs/FULL_ENVIRONMENT.md` and `architecture/SANDBOX.md` consistently describe one bundled Debian-slim environment with glibc, apt, proot, APK-bundled rootfs assets, on-demand extraction, Python, Node/npm, and workspace overlays. The old “legacy optional environment” phrase is absent from the repository, and the sandbox roadmap no longer presents that phrase as an alternative installation tier.

The supporting security policy and several requirement documents describe the containment or requirement consequences without repeating all Full Environment properties. That is acceptable when ownership is explicit, but the current source map and traceability matrix do not connect every environment requirement to the Full Environment canonical source and the corresponding extraction, apt, Python, Node, APK-integrity, and performance tests.

**Required remediation:** keep `specs/FULL_ENVIRONMENT.md` as the environment behavior owner, link every environment requirement to it, and add explicit tests for bundled asset integrity, architecture selection, extraction, proot launch, apt installation, Python wheel behavior, npm/native-module behavior, cleanup, and recovery.

## Finding 6 — Test Documents Are Not Yet Requirement-Complete

**Severity: Critical.** The six testing documents describe unit, integration, E2E, performance, regression, and security areas, but only 10 requirement identifiers appear across the testing corpus. The testing layer therefore does not provide complete requirement traceability for the 274 requirement identifiers.

The test documents include important scenario themes, but a feature mention is not enough to demonstrate coverage. The audit requires each behavior to identify inputs, setup, action, expected result, failure conditions, and relevant state transitions. This information must be connected to requirement IDs and contract documents.

**Required remediation:** add requirement IDs and executable scenario definitions to each testing document, then link every requirement to the appropriate test level and identify uncovered or deferred behavior explicitly.

## Finding 7 — Implementation Feasibility Evidence Is Not Yet Traceable

**Severity: High.** The Full Environment documentation contains detailed implementation assumptions, including Debian rootfs assets, proot binaries, APK extraction, overlays, package installation, PT_INTERP handling, and runtime probes. Background and runtime documents also describe Android service and lifecycle behavior. However, there is no complete implementation traceability layer connecting each referenced service, class, module, package, asset, process-control behavior, and recovery rule to a stable implementation owner and tests.

This does not establish that the implementation is impossible. It establishes that feasibility is not yet demonstrated end to end from specification to implementation module and test evidence.

**Required remediation:** create implementation-owner mappings inside the traceability matrix or an authoritative implementation mapping document, then verify module names, service names, Android lifecycle assumptions, process termination, storage cleanup, asset integrity, and checkpoint recovery against tests.

## Security and Boundary Assessment

The repository assigns security architecture to `architecture/SECURITY_MODEL.md`, threat analysis to `security/ThreatModel.md`, permission semantics to `security/PermissionModel.md`, containment to `security/SandboxPolicy.md`, and implementation architecture to `architecture/SANDBOX.md`. This ownership division is coherent and should be preserved.

The remaining validation need is evidence linkage: permission-before-execution, plugin containment, credential isolation, network policy, background approval enforcement, secret-safe logs, package-install containment, and prompt-injection containment must each map to requirements and security/integration tests. The current testing and traceability documents do not yet demonstrate that complete chain.

## Required Execution Order

1. Normalize the remaining document ownership declarations, especially API, protocol, SDK, registry, and testing documents.
2. Add lifecycle compatibility matrices for all formal state machines and execution phases.
3. Expand requirement traceability from 12 rows to the complete requirement universe.
4. Map implementation ownership and feasibility assumptions.
5. Add detailed test scenarios and requirement IDs across unit, integration, E2E, security, performance, and regression documents.
6. Reconcile diagrams and high-level overviews with canonical sources.
7. Re-read every changed and related document.
8. Rebuild the graph, rerun link validation, and perform a final finding verification.

## Final Status

The repository has completed the full-read discovery and integrated-model phases, and the current audit has verified the main cross-document gaps above. It is **not yet end-to-end normalized** because requirement traceability, test mapping, precise contract ownership, lifecycle compatibility tables, and implementation feasibility mapping remain incomplete.

The current baseline remains clean at commit `e768f19`. No repository files were modified during this audit pass.
