# Requirement-to-Implementation Traceability Matrix

> **Status: DERIVED** traceability index linking requirements to architecture, contracts, registries, security, and validation artifacts.

## Legend

- **Primary** — canonical owning document.
- **Derived** — supporting document derived from the primary owner.
- **Validation** — expected verification artifact.
- **Status** — `OK`, `PARTIAL`, or `GAP` based on current repository coverage.

## Maintenance Rule

When a canonical requirement, architecture, lifecycle, protocol, API, SDK, model, registry, security, or test artifact changes, this matrix MUST be updated in the same change or the gap MUST be recorded explicitly.

## Requirement-Level Matrix

| Requirement / Concern | Primary | Derived contracts | Validation | Status |
|---|---|---|---|---|
| FR-A001 Agent registration and runtime identity | `architecture/AGENT_RUNTIME.md` | `models/Agent.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md`, `sdk/AgentSDK.md`, `registry/AGENTS.md` | `UT-CONTRACT-001` (Owner: Core Runtime, Status: Planned), `IT-AGENT-001` (Owner: Agent Runtime, Status: Planned) | OK |
| FR-A007 Task execution orchestration | `architecture/AGENT_RUNTIME.md` | `models/Task.md`, `models/Execution.md`, `protocols/Agent-Protocol.md`, `protocols/Execution-Protocol.md`, `docs/api/Agent-API.md`, `docs/api/Runtime-API.md` | `E2E-CORE-001` (Orchestration, Planned), `E2E-ORCH-001` (Orchestration, Planned), `IT-AGENT-001` (Agent Runtime, Planned), `IT-CONTRACT-001` (Core Runtime, Planned), `IT-CONTRACT-002` (Core Runtime, Planned) | PARTIAL |
| FR-T001 Tool invocation and lifecycle | `architecture/TOOL_SYSTEM.md` | `models/Tool.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md`, `sdk/ToolSDK.md`, `registry/TOOLS.md` | `UT-CONTRACT-001` (Core Runtime, Planned), `UT-CONTRACT-002` (Core Runtime, Planned), `SEC-PERM-001` (Security, Planned), `SEC-SBX-001` (Security + Sandbox, Planned), `IT-TOOL-001` (Tooling + Sandbox, Planned) | OK |
| FR-P001 Provider registration and capability abstraction | `architecture/PROVIDER_SYSTEM.md` | `models/Provider.md`, `protocols/Provider-Protocol.md`, `docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `registry/PROVIDERS.md` | `IT-PROVIDER-001` (Provider Layer, Planned), `RT-PROVIDER-001` (Provider Layer, Planned) | PARTIAL |
| FR-PL001 Plugin lifecycle and exported capability registration | `architecture/PLUGIN_SYSTEM.md` | `models/Plugin.md`, `protocols/Plugin-Protocol.md`, `docs/api/Plugin-API.md`, `sdk/PluginSDK.md`, `registry/PLUGINS.md` | `IT-PLUGIN-001` (Plugin System, Planned), `SEC-PLUGIN-001` (Security + Plugin System, Planned), `RT-PLUGIN-001` (Plugin System, Planned) | PARTIAL |
| FR-EL-006 Execution lifecycle and checkpoint durability | `architecture/RUNTIME.md`, `specs/EXECUTION_LIFECYCLE.md` | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `state-machines/TaskLifecycle.md` | `IT-CONTRACT-002` (Core Runtime, Planned), `PERF-EXEC-001` (Performance, Planned), `RT-CONTRACT-001` (API Contracts, Planned) | OK |
| FR-S011 Sandbox mediation for execution | `architecture/SANDBOX.md` | `security/SandboxPolicy.md`, `specs/FULL_ENVIRONMENT.md`, `docs/SANDBOX_DEPTH.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md` | `SEC-SBX-001` (Security + Sandbox, Planned), `SEC-PERM-001` (Security, Planned) | PARTIAL |
| FR-M011 Tool history memory persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `lifecycle/MemoryLifecycle.md`, `specs/CONTEXT_MANAGEMENT.md` | `UT-CONTRACT-002` (Core Runtime, Planned), `IT-MEMORY-001` (Memory System, Planned) | PARTIAL |
| FR-M012 File history persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `lifecycle/MemoryLifecycle.md`, `specs/FILE_SYSTEM.md`, `specs/CONTEXT_MANAGEMENT.md` | `IT-MEMORY-001` (Memory System, Planned) | PARTIAL |
| FR-M013 User preference persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `lifecycle/MemoryLifecycle.md`, `docs/PRODUCT_PRINCIPLES.md` | `UT-CONTRACT-002` (Core Runtime, Planned) | PARTIAL |
| FR-M014 Knowledge graph entity persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `lifecycle/MemoryLifecycle.md`, `specs/CONTEXT_MANAGEMENT.md` | `IT-MEMORY-001` (Memory System, Planned) | PARTIAL |
| FR-M015 Knowledge graph relationship persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `lifecycle/MemoryLifecycle.md`, `specs/CONTEXT_MANAGEMENT.md` | `IT-MEMORY-001` (Memory System, Planned) | PARTIAL |
| FR-W001 Workspace runtime ownership | `architecture/RUNTIME.md` | `models/Workspace.md`, `lifecycle/WorkspaceLifecycle.md`, `docs/api/Runtime-API.md`, `docs/ARCHITECTURE.md` | `UT-CONTRACT-005` (Core Runtime, Planned) | PARTIAL |
| FR-TE001 Terminal tool execution | `specs/TERMINAL.md`, `architecture/SANDBOX.md` | `models/TerminalSession.md`, `lifecycle/TerminalSessionLifecycle.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md` | `SEC-SBX-001` (Security + Sandbox, Planned), `IT-TOOL-001` (Tooling + Sandbox, Planned) | PARTIAL |
| FR-MA-003 Multi-agent delegation | `architecture/MULTI_AGENT_SYSTEM.md` | `models/Task.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md` | `E2E-MA-001` (Orchestration, Planned), `UT-MA-001` (Agent Runtime, Planned) | PARTIAL |
| FR-WF-001 Workflow lifecycle orchestration | `architecture/WORKFLOW_ENGINE.md` | `models/Workflow.md`, `state-machines/WorkflowLifecycle.md` | `IT-CONTRACT-002` (Core Runtime, Planned) | PARTIAL |
| FR-SESS-001 Session context lifecycle | `architecture/RUNTIME.md`, `specs/CONTEXT_MANAGEMENT.md` | `models/Session.md`, `lifecycle/SessionLifecycle.md` | `UT-CONTRACT-005` (Core Runtime, Planned) | PARTIAL |
| NFR-PERF-001 Startup and navigation performance | `docs/PERFORMANCE_BUDGET.md` | `architecture/RUNTIME.md`, `testing/PerformanceTests.md`, `testing/cases/PerformanceTestCases.md` | `PERF-START-001` (Performance, Planned), `E2E-CORE-001` (Orchestration, Planned) | PARTIAL |
| NFR-SEC-001 Permission and sandbox enforcement | `security/SandboxPolicy.md`, `security/PermissionModel.md` | `architecture/SANDBOX.md`, `protocols/Tool-Protocol.md`, `protocols/Plugin-Protocol.md`, `testing/SecurityTests.md`, `testing/cases/SecurityTestCases.md` | `SEC-PERM-001` (Security, Planned), `SEC-SBX-001` (Security + Sandbox, Planned), `SEC-SECRET-001` (Security, Planned) | PARTIAL |
| NFR-REL-001 Durable lifecycle and replay safety | `specs/EXECUTION_LIFECYCLE.md` | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `lifecycle/WorkspaceLifecycle.md`, `lifecycle/SessionLifecycle.md` | `IT-CONTRACT-002` (Core Runtime, Planned), `RT-CONTRACT-001` (API Contracts, Planned) | PARTIAL |
| NFR-COMP-001 Contract compatibility and versioning | `VERSIONING.md`, `standards/Registry-Standard.md` | `docs/api/*`, `sdk/*`, `registry/AGENTS.md`, `registry/PROVIDERS.md`, `registry/PLUGINS.md`, `registry/TOOLS.md`, `registry/SKILLS.md` | `RT-CONTRACT-001` (API Contracts, Planned), `RT-PLUGIN-001` (Plugin System, Planned), `RT-PROVIDER-001` (Provider Layer, Planned) | PARTIAL |
| Canonical error envelope | `errors/ERROR_CODES.md` | all `docs/api/*`, `protocols/*`, `sdk/*`, runtime and task projections | `UT-CONTRACT-002` (Core Runtime, Planned), `RT-CONTRACT-001` (API Contracts, Planned), `IT-CONTRACT-001` (Core Runtime, Planned) | OK |
| Correlation, idempotency, resume, and version semantics | owning architecture documents | API envelopes, execution/task/workflow models, protocol events, SDK helpers, lifecycle docs, testing docs | `UT-CONTRACT-003` (Core Runtime, Planned), `UT-CONTRACT-005` (Core Runtime, Planned), `IT-CONTRACT-001` (Core Runtime, Planned), `E2E-CORE-001` (Orchestration, Planned) | PARTIAL |

## Open Gaps

- The matrix is stronger and now points to explicit case IDs with owner and status metadata, but it still does not enumerate the full requirement set from `requirements/FR.md` and `requirements/NFR.md`.
- Some validations still reference shared cross-cutting cases instead of requirement-unique case inventories.
- Newly added lifecycle authorities are now back-linked in core model/protocol areas, but not yet exhaustively across all architecture and SDK documents.
