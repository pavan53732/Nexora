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

## Source Map

| Concept | Canonical source | Supporting / derived sources |
|---|---|---|
| Runtime composition and service boundaries | `architecture/RUNTIME.md` | `docs/ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md`, `docs/MODULE_BOUNDARIES.md`, `docs/DEPENDENCY_GRAPH.md` |
| Single-agent autonomous loop | `architecture/AGENT_RUNTIME.md` | `docs/SYSTEM_DESIGN.md`, `docs/api/Agent-API.md`, `sdk/AgentSDK.md` |
| Multi-agent coordination | `architecture/MULTI_AGENT_SYSTEM.md` | `protocols/Agent-Protocol.md`, `registry/AGENTS.md`, `registry/AGENT_MATRIX.md` |
| Workflow graph progression | `architecture/WORKFLOW_ENGINE.md` | `models/Workflow.md`, `state-machines/WorkflowLifecycle.md`, `docs/api/Runtime-API.md` |
| Conversation checkpoint and rollback semantics | `architecture/CONVERSATION_CHECKPOINTS.md` | `specs/CONVERSATION_CHECKPOINTS.md`, `decisions/DEC-8-conversation-checkpoint-rollback.md`, `decisions/DEC-9-conversation-rollback-operation.md`, `decisions/DEC-10-conversation-checkpoint-ownership.md` |
| Conversation identity and persistence contract | `decisions/DEC-13-conversation-identity-persistence.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `specs/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Session–Conversation relationship semantic status | `decisions/DEC-14-session-conversation-relationship-semantic-status.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `docs/TRACEABILITY.md` |
| Conversation checkpoint lifecycle | `state-machines/ConversationCheckpointLifecycle.md` | `architecture/CONVERSATION_CHECKPOINTS.md`, `specs/CONVERSATION_CHECKPOINTS.md` |
| Checkpoint, recovery, and resume | `specs/BACKGROUND_EXECUTION.md` | `architecture/RUNTIME.md` (§Checkpoint System), `architecture/AGENT_RUNTIME.md` (saveCheckpoint), `state-machines/TaskLifecycle.md` |
| Agent lifecycle | `state-machines/AgentLifecycle.md` | `architecture/AGENT_RUNTIME.md`, `docs/LIFECYCLES.md` |
| Context assembly, ReasoningPolicy, ContextSnapshot, grounding, and reasoning-artifact privacy | `specs/CONTEXT_MANAGEMENT.md` | `architecture/RUNTIME.md` (Context Builder), `architecture/AGENT_RUNTIME.md`, `architecture/MEMORY_SYSTEM.md`, `models/Inference.md`, `docs/adr/ADR-0008-Typed-Inference-Streaming.md` |
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
| Terminal session lifecycle | `state-machines/TerminalSessionLifecycle.md` | `lifecycle/TerminalSessionLifecycle.md`, `models/TerminalSession.md`, `specs/TERMINAL.md` |
| Task lifecycle | `state-machines/TaskLifecycle.md` | `models/Task.md`, `specs/EXECUTION_LIFECYCLE.md`, `docs/LIFECYCLES.md`, `protocols/Execution-Protocol.md` |
| Session lifecycle | `state-machines/SessionLifecycle.md` | `lifecycle/SessionLifecycle.md`, `models/Session.md`, `docs/LIFECYCLES.md` |
| Execution lifecycle | `architecture/RUNTIME.md` (§ExecutionStatus Lifecycle) | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `specs/EXECUTION_LIFECYCLE.md` |
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
| Browser page/action state | `specs/BROWSER.md` | `specs/BACKGROUND_EXECUTION.md`, `architecture/TOOL_SYSTEM.md` (§Browser tools) |

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
