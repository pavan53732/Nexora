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

## Source Map

| Concept | Canonical source | Supporting / derived sources |
|---|---|---|
| Runtime composition and service boundaries | `architecture/RUNTIME.md` | `docs/ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md`, `docs/MODULE_BOUNDARIES.md`, `docs/DEPENDENCY_GRAPH.md` |
| Single-agent autonomous loop | `architecture/AGENT_RUNTIME.md` | `docs/SYSTEM_DESIGN.md`, `docs/api/Agent-API.md`, `sdk/AgentSDK.md` |
| Multi-agent coordination | `architecture/MULTI_AGENT_SYSTEM.md` | `protocols/Agent-Protocol.md`, `registry/AGENTS.md`, `registry/AGENT_MATRIX.md` |
| Workflow graph progression | `architecture/WORKFLOW_ENGINE.md` | `models/Workflow.md`, `state-machines/WorkflowLifecycle.md`, `docs/api/Runtime-API.md` |
| Tool discovery and execution | `architecture/TOOL_SYSTEM.md` | `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md`, `sdk/ToolSDK.md`, `registry/TOOLS.md` |
| Tool identity catalog | `registry/TOOLS.md` | `registry/TOOL_MATRIX.md` |
| Memory storage, retention, promotion, summarization | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md` |
| Read-time context assembly | `specs/CONTEXT_MANAGEMENT.md` | `docs/api/Agent-API.md`, `diagrams/Memory-Store-Flow.md` |
| Provider architecture and routing | `architecture/PROVIDER_SYSTEM.md` | `models/Provider.md`, `protocols/Provider-Protocol.md`, `docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `specs/AI_PROVIDERS.md`, `registry/PROVIDERS.md` |
| Provider lifecycle, health, and failover | `state-machines/ProviderLifecycle.md` | `docs/LIFECYCLES.md`, `diagrams/Provider-Streaming-Flow.md` |
| MCP adapter contract (tool source interop) | `architecture/TOOL_SYSTEM.md` (§MCP Client) + `protocols/Tool-Protocol.md` (§MCP Invocation) | `registry/TOOLS.md` (`TOOL-397..402`), `registry/TOOL_MATRIX.md` (MCP capability rows), `specs/AI_PROVIDERS.md` (§Phase 5), `security/PermissionModel.md` (§MCP rules) |
| Plugin architecture and integration | `architecture/PLUGIN_SYSTEM.md` | `models/Plugin.md`, `protocols/Plugin-Protocol.md`, `docs/api/Plugin-API.md`, `sdk/PluginSDK.md`, `docs/adr/ADR-0002-Plugin-System.md`, `registry/PLUGINS.md` |
| Plugin lifecycle | `state-machines/PluginLifecycle.md` | `diagrams/Plugin-Lifecycle-Flow.md`, `docs/LIFECYCLES.md` |
| Sandbox architecture and proot integration | `architecture/SANDBOX.md` | `docs/ENVIRONMENT_SETUP.md`, `docs/SANDBOX_DEPTH.md`, `specs/TERMINAL.md`, `specs/FULL_ENVIRONMENT.md` |
| Security architecture and threat ownership | `architecture/SECURITY_MODEL.md` | `security/ThreatModel.md`, `SECURITY.md`, `standards/Security-Standard.md` |
| Permission semantics | `security/PermissionModel.md` | `models/Permission.md`, `architecture/SECURITY_MODEL.md` |
| Sandbox containment policy | `security/SandboxPolicy.md` | `architecture/SANDBOX.md`, `testing/SecurityTests.md` |
| Full Environment behavior | `specs/FULL_ENVIRONMENT.md` | `docs/ENVIRONMENT_SETUP.md`, `docs/PERFORMANCE_BUDGET.md`, `specs/TERMINAL.md` |
| Task lifecycle | `state-machines/TaskLifecycle.md` | `models/Task.md`, `specs/EXECUTION_LIFECYCLE.md`, `docs/LIFECYCLES.md`, `protocols/Execution-Protocol.md` |
| Background execution | `specs/BACKGROUND_EXECUTION.md` | `architecture/RUNTIME.md`, `docs/LIFECYCLES.md`, `testing/IntegrationTests.md` |

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
