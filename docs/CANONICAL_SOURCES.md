# Canonical Sources — Nexora

> **Status: CANONICAL** for document ownership and source-of-truth declarations.
> This index defines which document owns each major concept. Supporting and derived
> documents may explain or project canonical behavior but must not redefine it.

## Ownership Rules

- A canonical document owns normative behavior for its subject.
- A supporting document explains a focused view and must link to its canonical source.
- A derived document projects identity, shape, capability, or integration data from canonical sources.
- An ADR records a decision and its rationale; it does not replace the implementation specification unless explicitly stated.
- High-level overviews and diagrams are non-normative unless explicitly marked canonical.
- Diagram artifacts use two tiers: (1) Mermaid code-block diagrams in ADRs and design docs follow the DL-011 practice; (2) the SVG/HTML overview visuals under `docs/diagrams/` are DERIVED, non-normative design-doc visuals added by DL-045..DL-047. DL-011 remains the historical record for the Mermaid code-block standard; it is not amended here.

## Creator-Owned Product Design Authority

`NEXORA_PRODUCT_DESIGN_BY_CREATER.md` is the **CREATOR-OWNED PRODUCT DESIGN AUTHORITY** for what Nexora is. It is not an AI-owned canonical subsystem document, ADR, implementation manifest, or replacement for any canonical architecture, specification, lifecycle, model, protocol, API, SDK, registry, requirement, UI, security, or testing owner. AI agents MUST read it before product or architectural changes, MUST follow its selected product decisions, and MUST NOT modify or silently reinterpret it.

If a canonical document conflicts with the creator-owned product design, the required protocol is:

> **CONFLICT → STOP → REPORT → CREATOR DECISION**

The conflict report MUST identify both documents, exact line ranges, competing statements, affected ownership/lifecycle/security/persistence/evidence semantics, and the creator decision required. This document does not silently resolve conflicts by changing either authority.

## Source Map

| Concept | Canonical source | Supporting / derived sources |
|---|---|---|
| Creator-owned product design boundary (what Nexora is; not a canonical subsystem source) | `NEXORA_PRODUCT_DESIGN_BY_CREATER.md` | `PROJECT_SPECIFICATION.md`, `docs/PRODUCT_VISION.md`, `docs/PRODUCT_PRINCIPLES.md`; all canonical subsystem owners below define realization |
| Runtime composition and service boundaries | `architecture/RUNTIME.md` | `docs/ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md`, `docs/MODULE_BOUNDARIES.md`, `docs/DEPENDENCY_GRAPH.md` |
| Single-agent autonomous loop | `architecture/AGENT_RUNTIME.md` | `docs/SYSTEM_DESIGN.md`, `docs/api/Agent-API.md`, `sdk/AgentSDK.md`, `specs/EXECUTION_LIFECYCLE.md` |
| Bounded reasoning modes and per-iteration progress guards | `architecture/AGENT_RUNTIME.md` | `specs/EXECUTION_LIFECYCLE.md`, `decisions/DEC-7-retry-attempt-state.md`, `state-machines/AgentLifecycle.md`, `state-machines/TaskLifecycle.md` |
| Deterministic context assembly and authority-aware token budgeting | `specs/CONTEXT_MANAGEMENT.md` | `architecture/MEMORY_SYSTEM.md`, `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/PERFORMANCE_BUDGET.md` |
| Multi-agent coordination | `architecture/MULTI_AGENT_SYSTEM.md` | `protocols/Agent-Protocol.md`, `registry/AGENTS.md`, `registry/AGENT_MATRIX.md` |
| Workflow graph progression | `architecture/WORKFLOW_ENGINE.md` | `models/Workflow.md`, `state-machines/WorkflowLifecycle.md`, `docs/api/Runtime-API.md` |
| Conversation checkpoint and rollback semantics | `architecture/CONVERSATION_CHECKPOINTS.md` | `specs/CONVERSATION_CHECKPOINTS.md`, `decisions/DEC-8-conversation-checkpoint-rollback.md`, `decisions/DEC-9-conversation-rollback-operation.md`, `decisions/DEC-10-conversation-checkpoint-ownership.md` |
| Conversation identity and persistence contract | `decisions/DEC-13-conversation-identity-persistence.md` | `models/Conversation.md`, `architecture/CONVERSATION_CHECKPOINTS.md`, `specs/CONVERSATION_CHECKPOINTS.md`, `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`, `docs/TRACEABILITY.md` |
| Session–Conversation relationship semantic status | `decisions/DEC-14-session-conversation-relationship-semantic-status.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation relationship ownership | `decisions/DEC-15-session-conversation-relationship-ownership.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation relationship identity semantic status | `decisions/DEC-16-session-conversation-relationship-identity.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation relationship semantic identity status | `decisions/DEC-17-session-conversation-relationship-semantic-identity-status.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation relationship semantic representation | `decisions/DEC-18-session-conversation-relationship-semantic-representation.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation active cardinality semantics | `decisions/DEC-19-session-conversation-active-cardinality.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation association lifecycle semantics | `decisions/DEC-20-session-conversation-association-lifecycle.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation continuation and recovery semantics | `decisions/DEC-21-session-conversation-continuation-recovery.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| BranchLineage artifact ownership | `decisions/DEC-22-branch-lineage-artifact-ownership.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `models/Conversation.md`, `docs/TRACEABILITY.md` |
| Conversation checkpoint retention, deletion, quota, cleanup, and dependency safety | `decisions/DEC-23-conversation-checkpoint-retention-deletion-policy.md` + `decisions/DEC-31-branch-lineage-and-checkpoint-operational-policy.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `state-machines/ConversationCheckpointLifecycle.md`, `specs/CONVERSATION_CHECKPOINTS.md`, `models/Conversation.md`, `docs/TRACEABILITY.md` |
| Conversation-local metadata semantic boundary | `decisions/DEC-24-conversation-local-metadata-boundary.md` | `decisions/DEC-13-conversation-identity-persistence.md`, `architecture/CONVERSATION_CHECKPOINTS.md`, `models/Conversation.md`, `specs/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Conversation checkpoint lifecycle | `state-machines/ConversationCheckpointLifecycle.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `specs/CONVERSATION_CHECKPOINTS.md` |
| Conversation lifecycle | `state-machines/ConversationLifecycle.md` | `models/Conversation.md`, `specs/DATABASE_SCHEMA.md` (`conversation`), `architecture/CONVERSATION_CHECKPOINTS.md` |
| Checkpoint, recovery, and resume | `specs/BACKGROUND_EXECUTION.md` | `architecture/RUNTIME.md` (§Checkpoint System), `architecture/AGENT_RUNTIME.md` (saveCheckpoint), `state-machines/TaskLifecycle.md` |
| Agent lifecycle | `state-machines/AgentLifecycle.md` | `architecture/AGENT_RUNTIME.md`, `docs/LIFECYCLES.md` |
| Context assembly, ReasoningPolicy, ContextSnapshot, grounding, and reasoning-artifact privacy | `specs/CONTEXT_MANAGEMENT.md` | `architecture/RUNTIME.md` (Context Builder), `architecture/AGENT_RUNTIME.md`, `architecture/MEMORY_SYSTEM.md`, `models/Inference.md`, `specs/DATABASE_SCHEMA.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md`, `docs/adr/ADR-0008-Typed-Inference-Streaming.md` |
| Autonomy learning lessons and trust-state projection | `specs/AUTONOMY_STABILITY.md` | `models/AutonomyLearning.md`, `models/Skill.md`, `architecture/MEMORY_SYSTEM.md`, `security/PermissionModel.md`, `testing/cases/UnitTestCases.md` |
| No internal credit or cost gating | `decisions/DEC-25-no-internal-credit-cost-gating.md` | `requirements/FR.md`, `architecture/AGENT_RUNTIME.md`, `architecture/PROVIDER_SYSTEM.md`, `specs/CONTEXT_MANAGEMENT.md`, `models/Inference.md`, `docs/api/Provider-API.md`, `specs/AI_PROVIDERS.md`, `docs/PRODUCT_PRINCIPLES.md`, `docs/ROADMAP.md`, `specs/TERMINAL.md`, `security/ThreatModel.md`, `requirements/RISKS.md` |
| Non-functional requirement identity separation | `decisions/DEC-43-requirement-identity-separation.md` + `requirements/NFR.md` | `docs/REQUIREMENT_COVERAGE_LEDGER.md`, `docs/TRACEABILITY.md`, `docs/FR_NFR_MAPPING.md`, `architecture/AGENT_RUNTIME.md`, `docs/api/Runtime-API.md`, `docs/DOCUMENTATION_COMPLETENESS_INVENTORY.md` |
| Android-first Product Vision positioning | `decisions/DEC-26-android-first-product-positioning.md` | `docs/PRODUCT_VISION.md`, `docs/PRODUCT_PRINCIPLES.md` |
| Concrete requirement owner labels | `decisions/DEC-27-concrete-requirement-owner-labels.md` | `docs/REQUIREMENT_COVERAGE_LEDGER.md`, `testing/cases/RegressionTestCases.md`, `standards/Coding-Standard.md`, `VERSIONING.md`, `docs/ENVIRONMENT_SETUP.md` |
| ROADMAP terminology normalization | `decisions/DEC-28-roadmap-terminology-normalization.md` | `docs/ROADMAP.md`, `ui/Navigation.md`, `architecture/PLUGIN_SYSTEM.md`, `sdk/PluginSDK.md`, `models/Plugin.md`, `registry/PLUGINS.md` |
| Execution-failure class binding | `decisions/DEC-29-execution-failure-class-binding.md` + `specs/EXECUTION_LIFECYCLE.md` | `errors/ERROR_CODES.md`, `state-machines/TaskLifecycle.md`, `architecture/RUNTIME.md`, `models/Execution.md`, `architecture/TOOL_SYSTEM.md`, applicable Provider/Sandbox/Plugin protocols and APIs, `testing/cases/UnitTestCases.md` |
| Agent-loop liveness, retry, external-wait, provider-wait, and delegation-depth policy | `decisions/DEC-30-agent-loop-liveness-and-retry-bounds.md` + owning lifecycle/protocol authorities | `state-machines/TaskLifecycle.md`, `state-machines/AgentLifecycle.md`, `state-machines/ProviderStreamLifecycle.md`, `architecture/AGENT_RUNTIME.md`, `architecture/RUNTIME.md`, `architecture/MULTI_AGENT_SYSTEM.md`, `docs/api/Tool-API.md`, `testing/*` |
| Task dependency, unsatisfied-dependency, and deadline error identities | `decisions/DEC-33-task-liveness-error-identities.md` + `errors/ERROR_CODES.md` | `state-machines/TaskLifecycle.md`, `models/Task.md`, `architecture/RUNTIME.md`, `docs/api/Runtime-API.md`, `specs/BACKGROUND_EXECUTION.md`, `docs/TRACEABILITY.md`, `testing/*` |
| Background terminal session liveness and parent binding | `decisions/DEC-34-background-terminal-session-liveness.md` + `state-machines/TerminalSessionLifecycle.md` | `specs/TERMINAL.md`, `models/TerminalSession.md`, `architecture/RUNTIME.md`, `docs/api/Runtime-API.md`, `specs/BACKGROUND_EXECUTION.md`, `specs/DATABASE_SCHEMA.md`, `testing/*` |
| Approval denial cross-layer projection and approval-expiry classification | `decisions/DEC-35-approval-denial-cross-layer-projection.md` + `decisions/DEC-36-approval-expiry-classification.md` + owning lifecycle/protocol authorities | `errors/ERROR_CODES.md`, `security/PermissionModel.md`, `state-machines/TaskLifecycle.md`, `state-machines/AgentLifecycle.md`, `protocols/Tool-Protocol.md`, `protocols/Agent-Protocol.md`, `docs/api/Tool-API.md`, `architecture/RUNTIME.md`, `testing/*` |
| Android build target and compatibility policy | `decisions/DEC-37-android-build-target-policy.md` | `requirements/CONSTRAINTS.md`, `requirements/DEPENDENCIES.md`, `docs/ENVIRONMENT_SETUP.md`, `specs/FULL_ENVIRONMENT.md`, `docs/PERFORMANCE_BUDGET.md` |
| Full Environment packaging and release-size policy | `decisions/DEC-38-full-environment-packaging-and-size-policy.md` | `requirements/CONSTRAINTS.md`, `specs/FULL_ENVIRONMENT.md`, `docs/PERFORMANCE_BUDGET.md`, `docs/ENVIRONMENT_SETUP.md` |
| Historical GGUF provider execution boundary (superseded active scope) | `decisions/DEC-39-gguf-execution-boundary.md` | Historical record only; current provider scope is governed by DEC-41 |
| Module interface dependency and EventBus transport boundary | `decisions/DEC-40-module-interface-and-event-transport-boundary.md` | `requirements/CONSTRAINTS.md`, `docs/MODULE_BOUNDARIES.md`, `docs/MODULE_LAYER_MAPPING.md`, `docs/DEPENDENCY_GRAPH.md`, `standards/Coding-Standard.md` |
| Cloud-only AI provider scope and cloud degradation policy | `decisions/DEC-41-cloud-only-ai-provider-scope.md` (superseded in active scope by `decisions/DEC-44-standing-cloud-only-ai-models.md`; DEC-41 remains immutable historical authority) | `architecture/PROVIDER_SYSTEM.md`, `requirements/FR.md`, `requirements/NFR.md`, `requirements/CONSTRAINTS.md`, `requirements/ASSUMPTIONS.md`, `specs/AI_PROVIDERS.md`, provider API/protocol/SDK/model projections, `specs/AUTONOMY_STABILITY.md`, product, roadmap, environment, security, sandbox, and testing documents |
| No local AI models and security classifier boundary | `decisions/DEC-42-no-local-ai-models-and-classifier-boundary.md` (superseded in active scope by `decisions/DEC-44-standing-cloud-only-ai-models.md`; DEC-42 remains immutable historical authority) | `security/PermissionModel.md`, `specs/PIPES.md`, `requirements/CONSTRAINTS.md`, `requirements/ASSUMPTIONS.md`, `docs/PRODUCT_PRINCIPLES.md`, `docs/PRODUCT_VISION.md`, `docs/SANDBOX_DEPTH.md`, `docs/TRACEABILITY.md`, and testing documents |
| Standing cloud-only AI models rule | `decisions/DEC-44-standing-cloud-only-ai-models.md` + `AGENTS.md` (Rule 9) | `decisions/DEC-41-cloud-only-ai-provider-scope.md`, `decisions/DEC-42-no-local-ai-models-and-classifier-boundary.md`, `requirements/FR.md`, `requirements/NFR.md`, `requirements/CONSTRAINTS.md`, `requirements/ASSUMPTIONS.md`, `architecture/PROVIDER_SYSTEM.md`, `specs/AI_PROVIDERS.md`, `security/PermissionModel.md`, `docs/PRODUCT_PRINCIPLES.md`, `docs/PRODUCT_VISION.md`, `docs/SANDBOX_DEPTH.md`, `docs/TRACEABILITY.md`, and testing documents |
| No API credit or token-budget limits for the user | `decisions/DEC-45-no-api-credit-or-token-limits-for-user.md` + `AGENTS.md` (Rule 9) | `decisions/DEC-25-no-internal-credit-cost-gating.md`, `requirements/FR.md`, `requirements/NFR.md`, `architecture/AGENT_RUNTIME.md`, `architecture/PROVIDER_SYSTEM.md`, `specs/CONTEXT_MANAGEMENT.md`, `specs/AUTONOMY_STABILITY.md`, `docs/PRODUCT_PRINCIPLES.md`, `docs/ROADMAP.md`, and testing documents |
| BranchLineage operational policy | `decisions/DEC-31-branch-lineage-and-checkpoint-operational-policy.md` + `state-machines/BranchLineageLifecycle.md` | `models/BranchLineage.md`, `models/Conversation.md`, `architecture/CONVERSATION_CHECKPOINTS.md`, `specs/CONVERSATION_CHECKPOINTS.md`, `decisions/DEC-22-branch-lineage-artifact-ownership.md`, `decisions/DEC-23-conversation-checkpoint-retention-deletion-policy.md`, `specs/DATABASE_SCHEMA.md` |
| Workflow scope and monitoring surface | `decisions/DEC-32-workflow-scope-and-monitoring-surface.md` | `architecture/WORKFLOW_ENGINE.md`, `state-machines/WorkflowLifecycle.md`, `ui/Navigation.md`, `ui/Components.md`, `docs/ROADMAP.md` |
| Event bus | `architecture/RUNTIME.md` (§Core Interfaces — EventBus) | `docs/MODULE_BOUNDARIES.md` (shared module) |
| Observability | `architecture/RUNTIME.md` (§Module Inventory — Observability) | `docs/SYSTEM_DESIGN.md`, `docs/MODULE_BOUNDARIES.md` |
| Resource management | `architecture/RUNTIME.md` (§Module Inventory — Resource Manager) | `architecture/MULTI_AGENT_SYSTEM.md` (§SA-3), `security/SandboxPolicy.md` |
| Skill registry and skill runtime boundary | `architecture/RUNTIME.md` (§Module Inventory — Skill Registry) + `decisions/DEC-11-skill-lifecycle.md` | `registry/SKILLS.md`, `docs/adr/ADR-0007-Skills-First-Class.md` |
| Evidence and validation | `specs/CONTEXT_MANAGEMENT.md` (§7) | `architecture/RUNTIME.md` (§Module Inventory), `architecture/MULTI_AGENT_SYSTEM.md` (§Mandatory Review Rule) |
| Tool identity catalog | `registry/TOOLS.md` | `registry/TOOL_MATRIX.md` |
| Memory storage, retention, promotion, summarization | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md` |
| Read-time context assembly | `specs/CONTEXT_MANAGEMENT.md` | `docs/api/Agent-API.md`, `diagrams/Memory-Store-Flow.md` |
| Provider architecture and routing | `architecture/PROVIDER_SYSTEM.md` | `models/Provider.md`, `protocols/Provider-Protocol.md`, `docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `specs/AI_PROVIDERS.md`, `registry/PROVIDERS.md` |
| Provider inference streaming, routing, ordering, resume, and failover lineage | `architecture/PROVIDER_SYSTEM.md` + `state-machines/ProviderStreamLifecycle.md` | `models/Inference.md`, `models/Provider.md`, `protocols/Provider-Protocol.md`, `docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `diagrams/Provider-Streaming-Flow.md`, `docs/adr/ADR-0008-Typed-Inference-Streaming.md` |
| Provider lifecycle, health, and failover | `state-machines/ProviderLifecycle.md` | `docs/LIFECYCLES.md`, `diagrams/Provider-Streaming-Flow.md` |
| MCP adapter contract (tool source interop) | `architecture/TOOL_SYSTEM.md` (§MCP Client) + `protocols/Tool-Protocol.md` (§MCP Invocation) | `registry/TOOLS.md` (`TOOL-397..402`), `registry/TOOL_MATRIX.md` (MCP capability rows), `specs/AI_PROVIDERS.md` (§Phase 5), `security/PermissionModel.md` (§MCP rules) |
| Plugin architecture and integration | `architecture/PLUGIN_SYSTEM.md` | `models/Plugin.md`, `protocols/Plugin-Protocol.md`, `docs/api/Plugin-API.md`, `sdk/PluginSDK.md`, `docs/adr/ADR-0002-Plugin-System.md`, `registry/PLUGINS.md` |
| Plugin lifecycle | `state-machines/PluginLifecycle.md` | `diagrams/Plugin-Lifecycle-Flow.md`, `docs/LIFECYCLES.md` |
| Sandbox architecture and proot integration | `architecture/SANDBOX.md` | `docs/ENVIRONMENT_SETUP.md`, `docs/SANDBOX_DEPTH.md`, `specs/TERMINAL.md`, `specs/FULL_ENVIRONMENT.md` |
| Security architecture and threat ownership | `architecture/SECURITY_MODEL.md` | `security/ThreatModel.md`, `SECURITY.md`, `standards/Security-Standard.md` |
| Permission semantics | `security/PermissionModel.md` | `models/Permission.md`, `architecture/SECURITY_MODEL.md` |
| Sandbox containment policy | `security/SandboxPolicy.md` | `architecture/SANDBOX.md`, `testing/SecurityTests.md` |
| Full Environment behavior | `specs/FULL_ENVIRONMENT.md` | `docs/ENVIRONMENT_SETUP.md`, `docs/PERFORMANCE_BUDGET.md`, `specs/TERMINAL.md` |
| Workspace lifecycle | `state-machines/WorkspaceLifecycle.md` | `lifecycle/WorkspaceLifecycle.md`, `models/Workspace.md`, `docs/LIFECYCLES.md` |
| Memory lifecycle | `state-machines/MemoryLifecycle.md` | `lifecycle/MemoryLifecycle.md`, `models/Memory.md` |
| Terminal session lifecycle | `state-machines/TerminalSessionLifecycle.md` | `lifecycle/TerminalSessionLifecycle.md`, `models/TerminalSession.md`, `specs/TERMINAL.md`, `decisions/DEC-34-background-terminal-session-liveness.md` |
| Task lifecycle | `state-machines/TaskLifecycle.md` | `models/Task.md`, `specs/EXECUTION_LIFECYCLE.md`, `docs/LIFECYCLES.md`, `protocols/Execution-Protocol.md` |
| Session lifecycle | `state-machines/SessionLifecycle.md` | `lifecycle/SessionLifecycle.md`, `models/Session.md`, `docs/LIFECYCLES.md`, `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md` |
| Conversation domain model projection | `decisions/DEC-13-conversation-identity-persistence.md` | `models/Conversation.md`, `docs/SESSION_CONVERSATION_IMPLEMENTATION_HANDOFF.md` |
| Session–Conversation engineering handoff contract | `architecture/CONVERSATION_CHECKPOINTS.md` | `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`, `specs/SESSION_CONVERSATION_RUNTIME_RECOVERY.md`, `specs/SESSION_CONVERSATION_ERRORS.md`, `testing/SESSION_CONVERSATION_TEST_MATRIX.md`, `docs/SESSION_CONVERSATION_IMPLEMENTATION_HANDOFF.md` |
| Execution lifecycle | `architecture/RUNTIME.md` (§ExecutionStatus Lifecycle) | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `specs/EXECUTION_LIFECYCLE.md` |
| Execution recovery and checkpoint event contract | `protocols/Execution-Protocol.md` | `specs/BACKGROUND_EXECUTION.md`, `models/Execution.md`, `protocols/Agent-Protocol.md`, `docs/api/Runtime-API.md`, `testing/*` |
| Tool descriptor lifecycle | `architecture/TOOL_SYSTEM.md` (§ToolStatus Lifecycle) | `models/Tool.md`, `docs/api/Tool-API.md`, `protocols/Tool-Protocol.md`, `sdk/ToolSDK.md` |
| Background execution | `specs/BACKGROUND_EXECUTION.md` | `architecture/RUNTIME.md`, `docs/LIFECYCLES.md`, `testing/IntegrationTests.md` |
| Multi-instance pipes (discovery, pairing, transport, cross-instance delegation) | `specs/PIPES.md` | `architecture/MULTI_AGENT_SYSTEM.md` (§Cross-Instance Extension), `models/Instance.md`, `registry/TOOLS.md` (`TOOL-405..408`), `security/PermissionModel.md` (`instance:*` scopes) |
| Instance/pipe lifecycle | `state-machines/InstanceLifecycle.md` | `models/Instance.md`, `specs/PIPES.md` |
| Application database and persistence | `specs/DATABASE_SCHEMA.md` | `architecture/RUNTIME.md` (§Persistence), `architecture/MEMORY_SYSTEM.md` (§Memory Backing Stores), `architecture/SECURITY_MODEL.md` (§Encryption), `specs/DATABASE.md` (sandbox user-facing SQLite) |
| Per-stream inference lifecycle | `state-machines/ProviderStreamLifecycle.md` | `architecture/PROVIDER_SYSTEM.md`, `models/Inference.md`, `protocols/Provider-Protocol.md`, `diagrams/Provider-Streaming-Flow.md` |
| ContextSnapshot retention | `specs/CONTEXT_MANAGEMENT.md` | `architecture/MEMORY_SYSTEM.md` (§Inference Artifact Retention), `models/Inference.md` |
| ReasoningSummary retention | `specs/CONTEXT_MANAGEMENT.md` | `architecture/MEMORY_SYSTEM.md` (§Inference Artifact Retention), `models/Inference.md` |
| Stream lineage persistence | `state-machines/ProviderStreamLifecycle.md` | `architecture/PROVIDER_SYSTEM.md`, `models/Inference.md`, `architecture/MEMORY_SYSTEM.md` (§Inference Artifact Retention) |
| Tool invocation lifecycle | `protocols/Tool-Protocol.md` | `architecture/TOOL_SYSTEM.md` (§Tool Execution Flow), `docs/api/Tool-API.md`, `sdk/ToolSDK.md` |
| Workflow-step lifecycle | `state-machines/WorkflowLifecycle.md` | `architecture/WORKFLOW_ENGINE.md`, `models/Workflow.md`, `docs/api/Runtime-API.md` |
| Multi-agent delegation ownership | `architecture/MULTI_AGENT_SYSTEM.md` | `protocols/Agent-Protocol.md`, `registry/AGENTS.md`, `registry/AGENT_MATRIX.md` |
| Concurrent file-lock ownership | `architecture/WORKFLOW_ENGINE.md` (§Execution Model) | `architecture/RUNTIME.md` (§Resource Manager), `architecture/MULTI_AGENT_SYSTEM.md` (§SA-3) |
| Plugin trust and revocation | `architecture/PLUGIN_SYSTEM.md` | `state-machines/PluginLifecycle.md`, `registry/PLUGINS.md`, `sdk/PluginSDK.md` |
| Browser page/action state | `specs/BROWSER.md` | `specs/BACKGROUND_EXECUTION.md`, `architecture/TOOL_SYSTEM.md` (§Browser tools), `architecture/TOOL_SYSTEM.md` (§Operation-Level Side-Effect Recovery) |
| Documentation governance and implementation-ready contract discipline | `standards/Documentation-Standard.md` + `docs/TRACEABILITY_RULES.md` | `docs/DOCUMENTATION_COMPLETENESS_INVENTORY.md`, `docs/TRACEABILITY.md`, `docs/REQUIREMENT_COVERAGE_LEDGER.md` |

| ADR-0010 accepted decision record | `docs/adr/ADR-0010-Evidence-Bounded-Nexora-Execution-Strengthening-And-Verification.md` | The canonical owners listed below; `docs/TRACEABILITY.md`; `docs/REQUIREMENT_COVERAGE_LEDGER.md` | Records the accepted Nexora decision; it does not replace the owning architecture, security, specification, standards, or testing documents. |
| Metric-driven execution/progress/verification projection | `architecture/AGENT_RUNTIME.md` | `architecture/RUNTIME.md`, `architecture/WORKFLOW_ENGINE.md`, `specs/CONTEXT_MANAGEMENT.md`, `architecture/MULTI_AGENT_SYSTEM.md`, `testing/EVIDENCE_CONVENTIONS.md` | Derived evaluations use existing Agent/Task/Execution/Workflow/ProgressSignal/acceptance/evidence identities; no GoalMetric identity or lifecycle. |
| Bounded read-only investigation/reviewer projection | `architecture/MULTI_AGENT_SYSTEM.md` | `architecture/AGENT_RUNTIME.md`, `architecture/RUNTIME.md`, `security/PermissionModel.md`, `testing/EVIDENCE_CONVENTIONS.md` | Uses existing agent/task/execution/delegation/artifact identities and authority; no reviewer or Batch lifecycle is created. |
| Derived work-group projection | `architecture/RUNTIME.md` | `architecture/WORKFLOW_ENGINE.md`, `architecture/AGENT_RUNTIME.md`, `models/Task.md`, `models/Execution.md`, `models/Workflow.md`, `testing/EVIDENCE_CONVENTIONS.md` | Recomputable view over existing source identities; no persisted work-group identity, lifecycle, scheduler, authorization, recovery, or evidence root. |
| Android boundary enforcement | `docs/MODULE_BOUNDARIES.md` + `docs/DEPENDENCY_GRAPH.md` | `architecture/RUNTIME.md`, `security/PermissionModel.md`, `security/SandboxPolicy.md`, `specs/BACKGROUND_EXECUTION.md`, `testing/EVIDENCE_CONVENTIONS.md` | Existing Android-aware owners and allowed dependency edges remain authoritative; checks and tests enforce rather than replace them. |
| Derived cross-policy eligibility report and stateless evaluator boundary | `security/PermissionModel.md` | `architecture/RUNTIME.md`, `architecture/TOOL_SYSTEM.md`, `specs/CONTEXT_MANAGEMENT.md`, `docs/DEPENDENCY_GRAPH.md`, `testing/EVIDENCE_CONVENTIONS.md` | Existing owner decisions remain authoritative; no persisted Policy Engine identity, lifecycle, precedence, veto, or recovery authority. |
| Mechanical architecture/dependency/documentation compliance checks | `docs/DEPENDENCY_GRAPH.md` + `standards/Documentation-Standard.md` | `docs/MODULE_BOUNDARIES.md`, `docs/CANONICAL_SOURCES.md`, `docs/TRACEABILITY.md`, `docs/REQUIREMENT_COVERAGE_LEDGER.md`, `testing/EVIDENCE_CONVENTIONS.md` | Checks may enforce existing canonical contracts and report findings; they cannot invent or own architecture. |
| Common verification matrix, evidence envelope, and deterministic test controls | `testing/EVIDENCE_CONVENTIONS.md` | Existing unit, integration, E2E, performance, regression, security, lifecycle, context, liveness, sandbox, and Android test inventories; `requirements/NFR.md`; `docs/TRACEABILITY.md` | Distinguishes requirement, implementation, test definition, tested execution, and retained executed evidence; controls are test-only. |

## Contract Derivation

For each subsystem, the expected derivation order is:

```text
Canonical architecture or specification
    → lifecycle/state machine
    → model
    → protocol
    → API
    → SDK
    → registry or capability view
    → requirements and tests
```

When a document disagrees with its canonical source, the canonical source wins and the disagreement must be corrected or recorded as an ADR.

| Memory Protocol as internal subsystem contract boundary | `protocols/Memory-Protocol.md` | `architecture/MEMORY_SYSTEM.md`, `models/Memory.md`, `lifecycle/MemoryLifecycle.md`, `specs/CONTEXT_MANAGEMENT.md` | Memory is an internal subsystem boundary; no separate `docs/api/Memory-API.md` artifact is required by current repository evidence. |
