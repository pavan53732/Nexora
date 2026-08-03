# Nexora Repository-Wide Documentation Consistency and Architecture Audit

Audit basis: repository `main` at commit `071f7b5`.

Scope: every Markdown document in the repository treated as one integrated specification.

Methodology followed: repository discovery, complete reading of all Markdown documents, internal repository model construction, canonical-source identification, subsystem cross-reference mapping, repeated subsystem reading, deep cross-document analysis, evidence verification, and false-positive prevention.

## Executive Summary

Nexora has unusually broad documentation coverage for a product at this stage. The repository contains root specifications, architecture documents, ADRs, requirements, models, protocols, APIs, SDKs, registries, state machines, diagrams, testing plans, standards, and UI guidance. That breadth is a strength because almost every major subsystem is described somewhere in the repository.

The main weakness is not absence of documentation. The main weakness is distributed authority. The repository frequently documents the same subsystem across architecture, state, model, protocol, SDK, API, and registry layers without always declaring which document is authoritative and which ones are derived. This produces architectural ambiguity more often than direct contradiction.

The repository is structurally healthy enough to support consolidation work. It is not yet fully implementation-safe for multiple independent teams without further canonical-source clarification, lifecycle unification, and requirement traceability hardening.

## Scores

Repository Health Score: 82 out of 100.

Documentation Quality Score: 77 out of 100.

Architecture Consistency Score: 71 out of 100.

Requirements Traceability Score: 68 out of 100.

Implementation Readiness Score: 64 out of 100.

## Repository Structure

The repository contains 129 Markdown documents organized across the following documentation areas:

- Root documents.
- Architecture.
- Backlog.
- Diagrams.
- General docs.
- ADRs.
- APIs.
- Errors.
- Models.
- Protocols.
- Registries.
- Requirements.
- SDKs.
- Security.
- Specs.
- Standards.
- State machines.
- Testing.
- UI.

The root and documentation-entry files act as orientation and synthesis layers. The architecture directory defines subsystem intent. The specs directory tends to define implementation-oriented behavior for focused areas such as background execution, context, terminal, browser, workspace, filesystem, and bundled full environment behavior. The model, protocol, API, SDK, registry, and state-machine directories then describe the same system from different representational layers.

## Repository Understanding Model

The integrated architecture represented by the repository can be understood as follows.

At the top level Nexora is a workspace-first, agent-oriented Android application with a runtime capable of orchestrating agents, workflows, tools, providers, memory, plugins, permissions, sandboxed execution, and background continuation. The system is designed around a structured execution loop rather than ad hoc prompt dispatch.

The major architectural subsystems are:

- Workspace and session management.
- Core runtime and execution services.
- Agent runtime and multi-agent orchestration.
- Workflow engine and task execution.
- Tool system and tool registry.
- Sandbox and full bundled environment.
- Provider abstraction and provider selection.
- Memory and context construction.
- Plugin and skills system.
- Security, permissions, and threat containment.
- Persistence and database support.
- Testing and standards.

The design intent shown across the repository is that a workspace contains persistent user context and execution history; an agent-oriented runtime interprets user goals, plans work, invokes tools or providers, and persists results; tools run through permission-aware and sandbox-aware execution paths; providers are abstracted and replaceable; memory is tiered and feeds context construction; plugins extend tools, providers, and agent capabilities; and testing covers unit, integration, E2E, performance, regression, and security layers.

## Canonical Source Assessment

The repository does not contain a single explicit canonical-source index. However, relative authority can still be inferred conservatively from document role and cross-document usage.

Most likely canonical or near-canonical sources by concept are:

- Product direction: `docs/PRODUCT_VISION.md`, supported by `PROJECT_SPECIFICATION.md` and `README.md`.
- Architectural overview: `docs/ARCHITECTURE.md` and `docs/SYSTEM_DESIGN.md`, with subsystem authority often pushed down into `architecture/*.md` documents.
- Requirements: `requirements/FR.md` and `requirements/NFR.md`.
- ADR decisions: `docs/adr/ADR-*.md`.
- Error identity: `errors/ERROR_CODES.md`.
- Entity state logic: likely `state-machines/*.md`, although that authority is not always declared.
- Subsystem responsibility: likely `architecture/*.md`, although some responsibilities are also expressed in `docs/LIFECYCLES.md`, `docs/MODULE_BOUNDARIES.md`, and focused `specs/*.md` documents.
- Full bundled environment behavior: `specs/FULL_ENVIRONMENT.md`, supported by `architecture/SANDBOX.md`, `docs/ENVIRONMENT_SETUP.md`, and `docs/PERFORMANCE_BUDGET.md`.

The main audit conclusion in this area is that canonical-source ownership must be made explicit, because the repository frequently behaves as if canonicality exists while not stating it directly.

## Cross-Document Consistency Audit

### Finding 1

Severity: CRITICAL  
Category: Architecture Compatibility

Files involved:

- `architecture/RUNTIME.md`
- `architecture/AGENT_RUNTIME.md`
- `architecture/MULTI_AGENT_SYSTEM.md`
- `architecture/WORKFLOW_ENGINE.md`
- `docs/SYSTEM_DESIGN.md`
- `docs/MODULE_BOUNDARIES.md`

Issue:
Execution coordination authority is distributed across multiple architectural centers.

Evidence:

`architecture/RUNTIME.md` presents Core Runtime as the place where major execution services are orchestrated, including planner, executor, workflow engine, tool manager, context builder, memory manager, permission manager, plugin manager, scheduler, security manager, resource manager, and agent manager.  

`architecture/AGENT_RUNTIME.md` separately describes the agent loop and execution behavior as a first-class runtime concern.  

`architecture/MULTI_AGENT_SYSTEM.md` gives the Agent Orchestrator responsibilities that include planning decomposition, sub-agent spawning, coordination, result merging, and completion control.  

`architecture/WORKFLOW_ENGINE.md` introduces another execution-control layer for workflow progression, dependencies, and transitions.  

`docs/SYSTEM_DESIGN.md` also describes execution flow at the system level.  

`docs/MODULE_BOUNDARIES.md` defines module responsibilities in a way that affects ownership assumptions across runtime, agents, workflows, tools, and supporting services.

Reasoning:
The documents are compatible in broad intent, but they do not fully separate which component is the single orchestration owner and which ones are subordinate engines or domain services.

Impact:
Independent teams could produce materially different implementations of planning, dispatch, concurrency, task ownership, cancellation, or completion semantics.

Recommendation:
Declare a single canonical execution coordinator and define all other runtime-control components as subordinate or domain-specific collaborators.

Status:
AMBIGUOUS with implementation-level architectural conflict risk.

### Finding 2

Severity: CRITICAL  
Category: Lifecycle Consistency

Files involved:

- `architecture/RUNTIME.md`
- `state-machines/TaskLifecycle.md`
- `models/Task.md`
- `docs/LIFECYCLES.md`
- `specs/EXECUTION_LIFECYCLE.md`

Issue:
Task lifecycle states are not represented identically across all related documents.

Evidence:

`architecture/RUNTIME.md` describes a task progression using status names centered on planning and execution control such as pending, planning, executing, blocked, completed, failed, and cancelled.  

`state-machines/TaskLifecycle.md` describes a formal task state set that includes states such as draft, pending, queued, running, completed, failed, cancelled, and error.  

`models/Task.md` defines the task entity but does not by itself resolve the discrepancy between architecture prose and formal state-machine terminology.  

`docs/LIFECYCLES.md` and `specs/EXECUTION_LIFECYCLE.md` add lifecycle narrative but do not clearly re-establish one canonical task state enum.

Reasoning:
This is more than stylistic naming drift because the differences affect the existence of pre-execution and failure-adjacent states.

Impact:
Implementations could diverge in persistence schema, UI rendering, retry semantics, event streams, and test expectations.

Recommendation:
Choose one canonical task status model and require all architecture, model, protocol, API, SDK, lifecycle, and testing documents to reference that single definition.

Status:
CONTRADICTION.

### Finding 3

Severity: HIGH  
Category: Architecture Compatibility

Files involved:

- `architecture/RUNTIME.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/DEPENDENCY_GRAPH.md`
- `docs/ARCHITECTURE.md`

Issue:
Module and package boundary definitions are not fully aligned.

Evidence:

`architecture/RUNTIME.md` describes runtime-owned services in a manner that implies a deep runtime-centered package structure.  

`docs/MODULE_BOUNDARIES.md` presents a stronger separation among modules such as runtime, agents, workflows, tools, providers, memory, plugins, and security, including allowed and forbidden dependency directions.  

`docs/DEPENDENCY_GRAPH.md` reinforces dependency layering but does not completely reconcile all service ownership statements found in runtime architecture.  

`docs/ARCHITECTURE.md` provides another broad system-layer framing.

Reasoning:
The documents are pointing at the same overall layered system, but they are not precise enough about whether certain components belong inside runtime as implementation detail or outside runtime as peer modules.

Impact:
This can alter dependency injection wiring, module ownership, internal APIs, test seams, and forbidden-dependency enforcement.

Recommendation:
Make one module-boundary document authoritative and explicitly align package ownership examples with it.

Status:
AMBIGUOUS bordering on contradiction.

### Finding 4

Severity: HIGH  
Category: Documentation Dependency Audit

Files involved:

- `docs/ARCHITECTURE.md`
- `docs/SYSTEM_DESIGN.md`
- `architecture/*.md`
- `docs/LIFECYCLES.md`
- `specs/*.md`

Issue:
High-level system documents and subsystem-specific documents do not always declare derivation direction.

Evidence:
The repository has multiple documents that behave like top-level authority for overlapping subjects: architecture overview, system design, lifecycle narrative, and focused specifications.

Reasoning:
This does not create immediate contradiction in every area, but it increases drift risk because supporting documents are able to reframe subsystem behavior without stating whether they are summarizing or redefining it.

Impact:
Readers may treat summary prose as normative and miss more precise subsystem contracts elsewhere.

Recommendation:
Add a canonical-source header or ownership note to high-level and subsystem documents.

Status:
AMBIGUOUS.

## Architecture Compatibility Audit

### Finding 5

Severity: HIGH  
Category: Architecture Compatibility

Files involved:

- `architecture/MEMORY_SYSTEM.md`
- `architecture/RUNTIME.md`
- `specs/CONTEXT_MANAGEMENT.md`
- `models/Memory.md`
- `protocols/Memory-Protocol.md`

Issue:
Memory, context assembly, and runtime ownership are distributed without a fully explicit authority split.

Evidence:

`architecture/MEMORY_SYSTEM.md` defines memory tiers, flow, and storage semantics.  

`architecture/RUNTIME.md` gives Memory Manager a broad operational role.  

`specs/CONTEXT_MANAGEMENT.md` consumes memory as part of context-building behavior.  

`models/Memory.md` and `protocols/Memory-Protocol.md` define the memory object and message layer, but not the full operational ownership boundary.

Reasoning:
The repository consistently shows memory feeding context and runtime behavior, but it does not fully settle which layer owns retention rules, summarization, promotion across tiers, or mutation authorization.

Impact:
Different teams could implement retention, summarization, or access policy in different layers.

Recommendation:
Define one canonical operational authority for memory writes, retention, tier transitions, summarization, and context projection.

Status:
AMBIGUOUS.

### Finding 6

Severity: HIGH  
Category: Cross-Subsystem Compatibility

Files involved:

- `architecture/TOOL_SYSTEM.md`
- `architecture/RUNTIME.md`
- `architecture/SANDBOX.md`
- `security/PermissionModel.md`
- `security/SandboxPolicy.md`
- `docs/LIFECYCLES.md`
- `protocols/Tool-Protocol.md`
- `sdk/ToolSDK.md`
- `registry/TOOLS.md`

Issue:
Tool registration, invocation, authorization, and sandbox execution are conceptually aligned but operational ownership remains split.

Evidence:

`architecture/TOOL_SYSTEM.md` defines tool categories, contracts, and lifecycle concepts.  

`architecture/RUNTIME.md` assigns Tool Manager broad registration and invocation responsibility.  

`architecture/SANDBOX.md`, `security/SandboxPolicy.md`, and `security/PermissionModel.md` define execution isolation and permission constraints.  

`docs/LIFECYCLES.md` references Tool Registry and Tool Manager responsibilities.  

`protocols/Tool-Protocol.md`, `sdk/ToolSDK.md`, and `registry/TOOLS.md` further describe tool behavior, identity, and integration.

Reasoning:
The repository clearly intends a permission-aware, sandbox-aware, registry-backed tool system, but it does not isolate one single source for the full registration-to-execution contract.

Impact:
Tool discovery, plugin-contributed tools, permission prompts, preflight validation, and execution routing may be implemented differently.

Recommendation:
Define a canonical end-to-end tool contract that names the authoritative source for identity, registration, permission metadata, invocation, and execution environment.

Status:
AMBIGUOUS.

### Finding 7

Severity: HIGH  
Category: Implementation Boundary Audit

Files involved:

- `architecture/SECURITY_MODEL.md`
- `architecture/SANDBOX.md`
- `architecture/RUNTIME.md`
- `security/PermissionModel.md`
- `security/SandboxPolicy.md`
- `security/ThreatModel.md`
- `requirements/NFR.md`
- `requirements/RISKS.md`

Issue:
Security, permissions, sandboxing, and runtime enforcement are documented across several layers without a strict ownership partition.

Evidence:
The runtime architecture assigns security and permission managers broad responsibilities. The security model defines permission flow and isolation goals. The sandbox policy defines sandbox rules. The threat model defines adversarial concerns. Requirements and risks add further normative constraints.

Reasoning:
These documents are complementary, but the repository does not state exactly which component is the enforcement authority for user approvals, sandbox containment, resource quotas, network egress, provider secret protection, and audit logging.

Impact:
Security-sensitive behavior may be duplicated, partially implemented, or inconsistently tested.

Recommendation:
Explicitly partition security responsibilities into authorization, containment, secret handling, quota enforcement, egress policy, and audit domains.

Status:
AMBIGUOUS.

## Requirements Traceability Audit

### Finding 8

Severity: HIGH  
Category: Requirements Traceability

Files involved:

- `requirements/FR.md`
- `requirements/NFR.md`
- `architecture/*.md`
- `models/*.md`
- `protocols/*.md`
- `docs/api/*.md`
- `sdk/*.md`
- `state-machines/*.md`
- `testing/*.md`

Issue:
Requirements are widely represented but not fully traceable end to end.

Evidence:
The repository has dedicated FR and NFR documents and those requirements are referenced in architecture, specs, testing, and planning documents. However, the repository does not provide a complete explicit traceability layer that consistently links each major requirement through architecture, model, protocol or API, SDK, state machine, and test.

Reasoning:
A requirement can appear repeatedly and still lack one definitive implementation path and one definitive acceptance path.

Impact:
Coverage can look stronger than it actually is, and teams may interpret the same requirement differently.

Recommendation:
Create an explicit repository-wide traceability matrix for every Must and Should requirement.

Status:
INCOMPLETE.

### Finding 9

Severity: MEDIUM  
Category: Requirements Traceability

Files involved:

- `specs/FULL_ENVIRONMENT.md`
- `architecture/SANDBOX.md`
- `docs/ENVIRONMENT_SETUP.md`
- `docs/PERFORMANCE_BUDGET.md`
- `requirements/FR.md`
- `testing/PerformanceTests.md`
- `testing/IntegrationTests.md`

Issue:
The bundled Full Environment is comparatively well documented but still lacks one visible end-to-end acceptance mapping.

Evidence:
The full environment behavior is defined in focused specification and supported architecture documents, environment-setup guidance, performance budgeting, and requirements. Testing documents cover relevant areas, but the repository does not present one integrated traceability mapping from environment requirements to implementation and verification artifacts.

Reasoning:
This is a traceability gap rather than a subsystem-definition gap.

Impact:
Environment regressions may not be systematically proven against all requirement clauses.

Recommendation:
Add one focused Full Environment traceability section or matrix.

Status:
INCOMPLETE.

## Model, API, Protocol, SDK Compatibility Audit

### Finding 10

Severity: HIGH  
Category: Model/API/Protocol Compatibility

Files involved:

- `models/Agent.md`
- `protocols/Agent-Protocol.md`
- `docs/api/Agent-API.md`
- `sdk/AgentSDK.md`
- `state-machines/AgentLifecycle.md`
- `architecture/AGENT_RUNTIME.md`

Issue:
Agent lifecycle and operational semantics are broadly aligned but do not clearly point to one canonical source.

Evidence:
The agent model, protocol, API, SDK, lifecycle, and runtime documents all describe the same entity and execution behavior. The repository shows conceptual agreement on agent creation, execution, pause/failure/completion behavior, and lifecycle visibility. However, the documents do not explicitly declare which layer defines the normative state contract and which layers simply expose it.

Reasoning:
This creates drift risk even where no direct contradiction is visible.

Impact:
Agent persistence, client bindings, and runtime events may gradually diverge.

Recommendation:
Define one canonical AgentStatus contract and require all other layers to reference it.

Status:
AMBIGUOUS.

### Finding 11

Severity: HIGH  
Category: Model/API/Protocol Compatibility

Files involved:

- `architecture/PROVIDER_SYSTEM.md`
- `models/Provider.md`
- `protocols/Provider-Protocol.md`
- `docs/api/Provider-API.md`
- `sdk/ProviderSDK.md`
- `state-machines/ProviderLifecycle.md`
- `docs/LIFECYCLES.md`
- `specs/AI_PROVIDERS.md`

Issue:
Provider lifecycle, health semantics, and failover behavior are not fully normalized across all layers.

Evidence:
Architecture, model, protocol, API, SDK, lifecycle, and AI-provider specification documents all describe provider abstractions and runtime behavior. The documents are aligned on the existence of provider abstraction and failover concerns, but they are less explicit about whether health state, lifecycle state, disablement, and automatic switching belong to one unified status model or to multiple related models.

Reasoning:
This distinction matters operationally because provider state affects selection, retry, observability, and user messaging.

Impact:
Provider routing and failover policy can diverge across runtime, UI, and testing.

Recommendation:
Separate lifecycle state from health state if they are distinct, or unify them if they are not, and make that choice explicit in one canonical contract.

Status:
AMBIGUOUS.

### Finding 12

Severity: HIGH  
Category: Model/API/Protocol Compatibility

Files involved:

- `architecture/PLUGIN_SYSTEM.md`
- `models/Plugin.md`
- `protocols/Plugin-Protocol.md`
- `docs/api/Plugin-API.md`
- `sdk/PluginSDK.md`
- `state-machines/PluginLifecycle.md`
- `registry/PLUGINS.md`
- `docs/adr/ADR-0002-Plugin-System.md`

Issue:
Plugin lifecycle and integration are well covered but lack an explicit derivation hierarchy across representation layers.

Evidence:
The repository includes architecture, ADR, model, protocol, API, SDK, lifecycle, and registry documentation for plugins. These are clearly related and broadly compatible. The missing element is an explicit statement of which document is authoritative for lifecycle, identity, message format, client surface, and registry membership.

Reasoning:
The risk here is not missing plugin documentation. The risk is slow drift across overlapping plugin descriptions.

Impact:
Plugin activation, deactivation, loading, validation, and interoperability behavior can split across implementations over time.

Recommendation:
Declare plugin lifecycle, protocol, and registry authority explicitly.

Status:
AMBIGUOUS.

## Registry Consistency Audit

### Finding 13

Severity: MEDIUM  
Category: Registry Consistency

Files involved:

- `registry/AGENTS.md`
- `registry/AGENT_MATRIX.md`
- `models/Agent.md`
- `docs/api/Agent-API.md`

Issue:
Agent identity appears in more than one registry-style representation without an explicit derived-view rule.

Evidence:
The agent registry and agent matrix both catalog agent entities and are supported by model and API documentation.

Reasoning:
Multiple registry views are acceptable if one is explicitly canonical and the other is derived. That relationship is not clearly stated.

Impact:
Role, capability, or phase mapping can drift between registry representations.

Recommendation:
Declare one authoritative agent registry and mark the matrix as a derived view if that is the intent.

Status:
AMBIGUOUS.

### Finding 14

Severity: MEDIUM  
Category: Registry Consistency

Files involved:

- `registry/TOOLS.md`
- `registry/TOOL_MATRIX.md`
- `architecture/TOOL_SYSTEM.md`
- `protocols/Tool-Protocol.md`
- `sdk/ToolSDK.md`

Issue:
Tool identity, category mapping, and registry-view roles are not fully clarified.

Evidence:
The tool registry provides a large inventory of tool identifiers. Architecture describes tool categories. A separate tool matrix exists, but the repository does not clearly define whether that matrix is canonical, derived, partial, or analytical.

Reasoning:
The repository clearly has a tool identity system, but supporting registry views are not fully normalized in role.

Impact:
Teams may use different sources for tool metadata or category mapping.

Recommendation:
Make the role of each tool registry representation explicit.

Status:
AMBIGUOUS.

### Finding 15

Severity: MEDIUM  
Category: Registry Consistency

Files involved:

- `registry/PROVIDERS.md`
- `registry/PLUGINS.md`
- `architecture/PROVIDER_SYSTEM.md`
- `specs/AI_PROVIDERS.md`
- `docs/api/Provider-API.md`

Issue:
Provider identity, provider profile behavior, and plugin-based provider extension are documented across multiple sources without one consolidated identity authority statement.

Evidence:
The provider registry defines provider identity. Architecture and specification documents define provider roles and configuration. Plugin documents indicate extensibility. The relationship is conceptually clear but not formally centralized.

Impact:
Provider capability metadata and extension ownership may drift.

Recommendation:
State that provider identity lives in the registry and that behavior/configuration derive from architecture and specification layers.

Status:
AMBIGUOUS.

## Lifecycle Consistency Audit

### Finding 16

Severity: HIGH  
Category: Lifecycle Consistency

Files involved:

- `state-machines/AgentLifecycle.md`
- `state-machines/TaskLifecycle.md`
- `state-machines/WorkflowLifecycle.md`
- `state-machines/PluginLifecycle.md`
- `state-machines/ProviderLifecycle.md`
- `docs/LIFECYCLES.md`
- `architecture/*.md`
- `specs/EXECUTION_LIFECYCLE.md`
- `specs/BACKGROUND_EXECUTION.md`

Issue:
The repository has strong lifecycle coverage, but the relationship between formal state machines and lifecycle prose is not consistently declared.

Evidence:
There is a dedicated state-machine directory for major entities and a separate lifecycle narrative document covering overlapping behavior. Architecture and execution specs also discuss transitions.

Reasoning:
This is a governance problem: formal state machines appear intended to be normative, but the repository does not consistently say so.

Impact:
Lifecycle prose can silently diverge from formal transition contracts.

Recommendation:
State that formal state-machine documents are authoritative for state names and transitions unless explicitly overridden by an ADR.

Status:
AMBIGUOUS.

### Finding 17

Severity: HIGH  
Category: Architecture Compatibility

Files involved:

- `specs/BACKGROUND_EXECUTION.md`
- `architecture/RUNTIME.md`
- `docs/LIFECYCLES.md`
- `models/Execution.md`
- `testing/IntegrationTests.md`

Issue:
Background execution behavior is described in multiple documents without one fully dominant execution-owner declaration.

Evidence:
Focused background-execution specification, runtime architecture, lifecycle documentation, execution model, and testing documents all describe recovery, continuation, service behavior, or execution resumption.

Reasoning:
The repository clearly intends robust background continuation, but service naming and ownership are spread across several layers.

Impact:
Foreground service behavior, WorkManager scheduling, checkpointing, restart policy, and recovery handling can diverge.

Recommendation:
Make `specs/BACKGROUND_EXECUTION.md` authoritative and require runtime and lifecycle documents to reference it.

Status:
AMBIGUOUS.

## Dependency Audit

### Finding 18

Severity: MEDIUM  
Category: Dependency Audit

Files involved:

- `docs/DEPENDENCY_GRAPH.md`
- `docs/MODULE_BOUNDARIES.md`
- `architecture/RUNTIME.md`
- `architecture/MULTI_AGENT_SYSTEM.md`
- `architecture/WORKFLOW_ENGINE.md`
- `architecture/SECURITY_MODEL.md`
- `architecture/SANDBOX.md`

Issue:
The repository defines dependency direction well in principle, but some control-plane subsystems remain dependency hotspots.

Evidence:
The dependency and module-boundary documents provide layered direction. Architecture documents show runtime, orchestration, workflow, security, and sandbox subsystems all depending on or coordinating with many other areas.

Reasoning:
No definitive circular dependency is established by documentation alone, but the hotspot concentration indicates dependency-risk zones that need sharper ownership boundaries.

Impact:
Implementations can introduce cycles or privileged “god modules” unless boundaries are enforced.

Recommendation:
Use the boundary documents to define hard rules for control-plane dependencies and list forbidden relationships explicitly for runtime, orchestrator, workflow, security, and sandbox services.

Status:
NOT CONFIRMED as a cycle defect; confirmed as a dependency-risk area.

## Terminology Audit

### Finding 19

Severity: MEDIUM  
Category: Terminology Audit

Files involved:

- `architecture/RUNTIME.md`
- `architecture/AGENT_RUNTIME.md`
- `architecture/MULTI_AGENT_SYSTEM.md`
- `architecture/WORKFLOW_ENGINE.md`
- `docs/LIFECYCLES.md`
- `docs/SYSTEM_DESIGN.md`
- `specs/BACKGROUND_EXECUTION.md`

Issue:
The repository uses several runtime-control terms whose boundaries are not always explicit.

Evidence:
Terms including Core Runtime, Agent Runtime, Agent Orchestrator, Workflow Engine, Executor, Background Runtime, AgentExecutionService, Tool Manager, and Tool Registry appear across different documents.

Reasoning:
Many of these may represent valid distinct components, but the repository does not always define them relative to one another with one canonical glossary.

Impact:
Terminology drift increases the chance of architectural misreading even when substantive intent is similar.

Recommendation:
Create one canonical glossary for runtime-control vocabulary and cross-link it from architecture documents.

Status:
AMBIGUOUS.

### Finding 20

Severity: LOW  
Category: Documentation Drift Audit

Files involved:

- `docs/SANDBOX_DEPTH.md`
- `architecture/SANDBOX.md`
- `specs/FULL_ENVIRONMENT.md`

Issue:
Residual legacy environment wording remains after consolidation on the bundled Full Environment.

Evidence:
`docs/SANDBOX_DEPTH.md` still contains legacy phrasing while the sandbox architecture and full-environment specification describe the bundled full environment as the supported environment model.

Reasoning:
This appears to be residual wording rather than a surviving architectural split.

Impact:
It can confuse readers about whether multiple environment tiers are still supported.

Recommendation:
Remove the legacy wording or mark it explicitly as historical context.

Status:
DOCUMENTATION DRIFT.

## Top High Findings Summary

The highest-priority issues are:

- Execution coordination ownership spread across runtime, agent runtime, multi-agent orchestration, workflow, and system-design documents.
- Task lifecycle contradiction between architecture prose and formal state-machine representation.
- Module-boundary and package-ownership ambiguity.
- Security, sandbox, tool, and permission ownership ambiguity.
- Memory and context operational ownership ambiguity.
- Provider lifecycle versus provider health/failover ambiguity.
- Missing explicit derivation hierarchy across architecture, model, protocol, API, SDK, registry, and lifecycle layers.
- Background execution ownership ambiguity.
- Incomplete end-to-end requirements traceability.

## Medium Findings Summary

The medium-severity issues are mostly governance and documentation-shape risks rather than hard contradictions:

- Duplicate registry representations without explicit derived-view rules.
- Dependency hotspot concentration in control-plane subsystems.
- Terminology overlap across runtime-control concepts.
- Full Environment traceability incompleteness.
- Residual legacy wording in one sandbox-depth document.

## Contradiction Matrix

Confirmed contradiction:

- Task lifecycle definitions between `architecture/RUNTIME.md` and `state-machines/TaskLifecycle.md` with supporting ambiguity across related lifecycle documents.

Strong ambiguity with architectural conflict risk:

- Core Runtime versus Agent Runtime versus Agent Orchestrator versus Workflow Engine execution ownership.
- Runtime package ownership versus module-boundary layering.
- Provider lifecycle versus provider health/failover semantics.
- Security versus permission versus sandbox enforcement ownership.
- Tool Manager versus Tool Registry versus sandbox execution ownership.
- Background execution owner and service semantics.

Documentation drift:

- Legacy environment phrasing in `docs/SANDBOX_DEPTH.md` after Full Environment consolidation.

## Traceability Matrix Narrative

The repository has the components needed for strong traceability but not the linking mechanism needed for auditability.

For many major features the chain exists in distributed form:

Requirement  
→ architecture document  
→ model  
→ protocol or API  
→ SDK  
→ state machine  
→ testing document.

The problem is that the chain is rarely declared explicitly in one place. This makes traceability a human inference exercise instead of a maintained project artifact.

The best-documented area under the current repository structure is the bundled Full Environment and sandbox-adjacent behavior. The least normalized areas are execution ownership, lifecycle authority, and multi-layer derivation rules.

## Structural Integrity Audit

Positive structural findings:

- The repository is broad and systematically organized.
- Major subsystem categories are present.
- Models, APIs, SDKs, protocols, registries, state machines, and tests all exist.
- Architecture is decomposed by subsystem rather than kept as one monolith.
- ADRs exist and provide historical decision context.
- Focused specs exist for implementation-heavy domains.

Structural risks:

- There is no explicit canonical-source index.
- There is no explicit repository-wide traceability matrix.
- There is no single glossary for control-plane terminology.
- Some subjects have both formal state machines and prose lifecycle documents without an explicit authority rule.
- Some registries have matrix-style companion documents without an explicit derived-view rule.

## Canonical Source Matrix Narrative

Most plausible canonical-source assignments inferred from the repository are:

- Product direction: `docs/PRODUCT_VISION.md`.
- Requirements: `requirements/FR.md` and `requirements/NFR.md`.
- ADR decisions: `docs/adr/ADR-*.md`.
- Subsystem intent: `architecture/*.md` for each subsystem.
- Entity transitions: `state-machines/*.md`.
- Public error identity: `errors/ERROR_CODES.md`.
- Bundled environment behavior: `specs/FULL_ENVIRONMENT.md`.
- Security constraints: a combination of `architecture/SECURITY_MODEL.md`, `security/SandboxPolicy.md`, and `security/PermissionModel.md`, which currently needs clearer partitioning.

The audit does not claim these assignments are officially declared. It concludes that the repository behaves as if these are the intended authorities and should formalize that assumption.

## Documentation Drift Report

The dominant form of drift is not factual conflict. It is silent overlap.

Drift patterns observed:

- High-level architecture documents and subsystem architecture documents both describe ownership.
- Lifecycle prose and formal state machines both describe transitions.
- Model, protocol, API, and SDK documents all describe the same entities without always naming the source of truth.
- Registries and matrices both enumerate the same identity spaces.

The repository is therefore at higher risk of future drift than immediate collapse. The fix is governance clarity, not wholesale redesign.

## Implementation Readiness Audit

The repository is sufficient for starting implementation, but not sufficient for fully parallel implementation without coordination overhead.

Implementation-ready areas:

- Product direction and user-facing intent.
- Workspace-first model.
- Agent-oriented interaction model.
- Plugin extensibility as a concept.
- Provider abstraction as a concept.
- Tool-based execution as a concept.
- Bundled Full Environment direction.
- Presence of formal testing categories.

Not fully implementation-ready without clarification:

- Single execution-control owner.
- Canonical task state contract.
- Exact module and package authority.
- Security and sandbox ownership partition.
- Memory versus context operational ownership.
- Provider health, lifecycle, and failover contract.
- Registry authority and derived-view rules.
- Explicit requirement-to-test traceability.

## Implementation Risk Assessment

Primary implementation risks are:

1. Divergent execution engines built by different teams from different “runtime” documents.
2. Incompatible task-state handling across persistence, UI, and tests.
3. Permission and sandbox enforcement duplication or gaps.
4. Context and memory behavior implemented at inconsistent layers.
5. Provider routing/failover divergence across runtime and UI.
6. Plugin and tool registration drift as extension surfaces evolve.
7. Test coverage that appears complete but lacks explicit requirement mapping.

## Prioritized Remediation Plan

Priority 0:

- Declare canonical execution ownership across runtime, agent runtime, orchestration, and workflow layers.
- Unify task lifecycle definitions.
- Reconcile module-boundary authority with runtime architecture.

Priority 1:

- Define authority boundaries for security, permissioning, sandboxing, quotas, secret handling, and audit logging.
- Define authority boundaries for memory retention, summarization, tier promotion, and context projection.
- Normalize provider lifecycle, health, and failover semantics.
- Make background-execution authority explicit.

Priority 2:

- Add a canonical-source index for the repository.
- Add explicit derivation notes to models, protocols, APIs, SDKs, registries, and lifecycle documents.
- Mark matrix documents as derived views where applicable.
- Add a runtime-control glossary.

Priority 3:

- Build a repository-wide requirement traceability matrix.
- Add a focused Full Environment traceability section.
- Remove or mark residual historical environment wording.

## Final Conclusion

Nexora’s documentation repository is substantial, thoughtful, and closer to implementation-ready than many systems at a similar stage. The repository does not fail because it lacks design. It struggles because its design is described from many angles without always naming the source of truth.

The most important repository-wide problem is distributed authority. The most important hard contradiction is task lifecycle inconsistency. The most important delivery risk is incomplete traceability between requirements, architecture, contracts, and tests.

The correct remediation is not architectural redesign. The correct remediation is canonical-source declaration, lifecycle unification, boundary clarification, and traceability completion.
