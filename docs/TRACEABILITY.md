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
| FR-A001 Agent registration and runtime identity | `architecture/AGENT_RUNTIME.md` | `models/Agent.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md`, `sdk/AgentSDK.md`, `registry/AGENTS.md` | `testing/UnitTests.md`, `testing/IntegrationTests.md` | OK |
| FR-A007 Task execution orchestration | `architecture/AGENT_RUNTIME.md` | `models/Task.md`, `models/Execution.md`, `protocols/Agent-Protocol.md`, `protocols/Execution-Protocol.md`, `docs/api/Agent-API.md`, `docs/api/Runtime-API.md` | `testing/E2ETests.md`, `testing/IntegrationTests.md` | PARTIAL |
| FR-T001 Tool invocation and lifecycle | `architecture/TOOL_SYSTEM.md` | `models/Tool.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md`, `sdk/ToolSDK.md`, `registry/TOOLS.md` | `testing/UnitTests.md`, `testing/SecurityTests.md`, `testing/IntegrationTests.md` | OK |
| FR-P001 Provider registration and capability abstraction | `architecture/PROVIDER_SYSTEM.md` | `models/Provider.md`, `protocols/Provider-Protocol.md`, `docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `registry/PROVIDERS.md` | `testing/IntegrationTests.md`, `testing/RegressionTests.md` | PARTIAL |
| FR-PL001 Plugin lifecycle and exported capability registration | `architecture/PLUGIN_SYSTEM.md` | `models/Plugin.md`, `protocols/Plugin-Protocol.md`, `docs/api/Plugin-API.md`, `sdk/PluginSDK.md`, `registry/PLUGINS.md` | `testing/IntegrationTests.md`, `testing/SecurityTests.md`, `testing/RegressionTests.md` | PARTIAL |
| FR-EL-006 Execution lifecycle and checkpoint durability | `architecture/RUNTIME.md`, `specs/EXECUTION_LIFECYCLE.md` | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `state-machines/TaskLifecycle.md` | `testing/IntegrationTests.md`, `testing/PerformanceTests.md` | OK |
| FR-S011 Sandbox mediation for execution | `architecture/SANDBOX.md` | `security/SandboxPolicy.md`, `specs/FULL_ENVIRONMENT.md`, `docs/SANDBOX_DEPTH.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md` | `testing/SecurityTests.md` | PARTIAL |
| FR-M011 Tool history memory persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/UnitTests.md`, `testing/IntegrationTests.md` | PARTIAL |
| FR-M012 File history persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/FILE_SYSTEM.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/IntegrationTests.md` | PARTIAL |
| FR-M013 User preference persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `docs/PRODUCT_PRINCIPLES.md` | `testing/UnitTests.md` | PARTIAL |
| FR-M014 Knowledge graph entity persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/IntegrationTests.md` | PARTIAL |
| FR-M015 Knowledge graph relationship persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/IntegrationTests.md` | PARTIAL |
| FR-W001 Workspace runtime ownership | `architecture/RUNTIME.md` | `models/Workspace.md`, `docs/api/Runtime-API.md`, `docs/ARCHITECTURE.md` | `testing/UnitTests.md` | PARTIAL |
| FR-TE001 Terminal tool execution | `specs/TERMINAL.md`, `architecture/SANDBOX.md` | `models/TerminalSession.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md` | `testing/SecurityTests.md`, `testing/IntegrationTests.md` | PARTIAL |
| FR-MA-003 Multi-agent delegation | `architecture/MULTI_AGENT_SYSTEM.md` | `models/Task.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md` | `testing/E2ETests.md`, `testing/UnitTests.md` | PARTIAL |
| FR-WF-001 Workflow lifecycle orchestration | `architecture/WORKFLOW_ENGINE.md` | `models/Workflow.md`, `state-machines/WorkflowLifecycle.md` | `testing/IntegrationTests.md` | PARTIAL |
| NFR-PERF-001 Startup and navigation performance | `docs/PERFORMANCE_BUDGET.md` | `architecture/RUNTIME.md`, `testing/PerformanceTests.md`, `testing/E2ETests.md` | performance baselines and release checks | PARTIAL |
| NFR-SEC-001 Permission and sandbox enforcement | `security/SandboxPolicy.md`, `security/PermissionModel.md` | `architecture/SANDBOX.md`, `protocols/Tool-Protocol.md`, `protocols/Plugin-Protocol.md`, `testing/SecurityTests.md` | security and regression validation | PARTIAL |
| NFR-REL-001 Durable lifecycle and replay safety | `specs/EXECUTION_LIFECYCLE.md` | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `testing/IntegrationTests.md` | replay, cancellation, and resilience validation | PARTIAL |
| NFR-COMP-001 Contract compatibility and versioning | `VERSIONING.md` | `docs/api/*`, `sdk/*`, `registry/AGENTS.md`, `registry/PROVIDERS.md`, `registry/PLUGINS.md`, `registry/TOOLS.md`, `registry/SKILLS.md` | regression and compatibility review | PARTIAL |
| Canonical error envelope | `errors/ERROR_CODES.md` | all `docs/api/*`, `protocols/*`, `sdk/*`, runtime and task projections | `testing/RegressionTests.md`, `testing/IntegrationTests.md` | OK |
| Correlation, idempotency, resume, and version semantics | owning architecture documents | API envelopes, execution/task/workflow models, protocol events, SDK helpers, testing docs | `testing/E2ETests.md`, `testing/UnitTests.md`, `testing/IntegrationTests.md` | PARTIAL |

## Open Gaps

- Requirement-level mapping remains incomplete for large portions of `requirements/FR.md` and most `requirements/NFR.md` entries.
- Several validation artifacts still describe coverage at a high level rather than linking to explicit requirement IDs or executable suite IDs.
- Some registries remain inventory-first and only partially capture compatibility metadata.
- Workspace and session lifecycle semantics are still less explicit than task, execution, and workflow semantics.
