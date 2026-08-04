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
| FR-A001 Agent registration and runtime identity | `architecture/AGENT_RUNTIME.md` | `models/Agent.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md`, `sdk/AgentSDK.md`, `registry/AGENTS.md` | `testing/UnitTests.md` (`UT-CONTRACT-*`), `testing/IntegrationTests.md` (`IT-AGENT-*`) | OK |
| FR-A007 Task execution orchestration | `architecture/AGENT_RUNTIME.md` | `models/Task.md`, `models/Execution.md`, `protocols/Agent-Protocol.md`, `protocols/Execution-Protocol.md`, `docs/api/Agent-API.md`, `docs/api/Runtime-API.md` | `testing/E2ETests.md` (`E2E-CORE-*`, `E2E-ORCH-*`), `testing/IntegrationTests.md` (`IT-AGENT-*`, `IT-CONTRACT-*`) | PARTIAL |
| FR-T001 Tool invocation and lifecycle | `architecture/TOOL_SYSTEM.md` | `models/Tool.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md`, `sdk/ToolSDK.md`, `registry/TOOLS.md` | `testing/UnitTests.md` (`UT-CONTRACT-*`), `testing/SecurityTests.md` (`SEC-PERM-*`, `SEC-SBX-*`), `testing/IntegrationTests.md` (`IT-TOOL-*`) | OK |
| FR-P001 Provider registration and capability abstraction | `architecture/PROVIDER_SYSTEM.md` | `models/Provider.md`, `protocols/Provider-Protocol.md`, `docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `registry/PROVIDERS.md` | `testing/IntegrationTests.md` (`IT-PROVIDER-*`), `testing/RegressionTests.md` (`RT-PROVIDER-*`) | PARTIAL |
| FR-PL001 Plugin lifecycle and exported capability registration | `architecture/PLUGIN_SYSTEM.md` | `models/Plugin.md`, `protocols/Plugin-Protocol.md`, `docs/api/Plugin-API.md`, `sdk/PluginSDK.md`, `registry/PLUGINS.md` | `testing/IntegrationTests.md` (`IT-PLUGIN-*`), `testing/SecurityTests.md` (`SEC-PLUGIN-*`), `testing/RegressionTests.md` (`RT-PLUGIN-*`) | PARTIAL |
| FR-EL-006 Execution lifecycle and checkpoint durability | `architecture/RUNTIME.md`, `specs/EXECUTION_LIFECYCLE.md` | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `state-machines/TaskLifecycle.md` | `testing/IntegrationTests.md` (`IT-CONTRACT-*`), `testing/PerformanceTests.md` (`PERF-EXEC-*`) | OK |
| FR-S011 Sandbox mediation for execution | `architecture/SANDBOX.md` | `security/SandboxPolicy.md`, `specs/FULL_ENVIRONMENT.md`, `docs/SANDBOX_DEPTH.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md` | `testing/SecurityTests.md` (`SEC-SBX-*`, `SEC-PERM-*`) | PARTIAL |
| FR-M011 Tool history memory persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/UnitTests.md` (`UT-CONTRACT-*`), `testing/IntegrationTests.md` (`IT-MEMORY-*`) | PARTIAL |
| FR-M012 File history persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/FILE_SYSTEM.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/IntegrationTests.md` (`IT-MEMORY-*`) | PARTIAL |
| FR-M013 User preference persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `docs/PRODUCT_PRINCIPLES.md` | `testing/UnitTests.md` (`UT-CONTRACT-*`) | PARTIAL |
| FR-M014 Knowledge graph entity persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/IntegrationTests.md` (`IT-MEMORY-*`) | PARTIAL |
| FR-M015 Knowledge graph relationship persistence | `architecture/MEMORY_SYSTEM.md` | `models/Memory.md`, `protocols/Memory-Protocol.md`, `specs/CONTEXT_MANAGEMENT.md` | `testing/IntegrationTests.md` (`IT-MEMORY-*`) | PARTIAL |
| FR-W001 Workspace runtime ownership | `architecture/RUNTIME.md` | `models/Workspace.md`, `docs/api/Runtime-API.md`, `docs/ARCHITECTURE.md` | `testing/UnitTests.md` (`UT-CONTRACT-*`) | PARTIAL |
| FR-TE001 Terminal tool execution | `specs/TERMINAL.md`, `architecture/SANDBOX.md` | `models/TerminalSession.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md` | `testing/SecurityTests.md` (`SEC-SBX-*`), `testing/IntegrationTests.md` (`IT-TOOL-*`) | PARTIAL |
| FR-MA-003 Multi-agent delegation | `architecture/MULTI_AGENT_SYSTEM.md` | `models/Task.md`, `protocols/Agent-Protocol.md`, `docs/api/Agent-API.md` | `testing/E2ETests.md` (`E2E-MA-*`), `testing/UnitTests.md` (`UT-MA-*`) | PARTIAL |
| FR-WF-001 Workflow lifecycle orchestration | `architecture/WORKFLOW_ENGINE.md` | `models/Workflow.md`, `state-machines/WorkflowLifecycle.md` | `testing/IntegrationTests.md` (`IT-CONTRACT-*`) | PARTIAL |
| NFR-PERF-001 Startup and navigation performance | `docs/PERFORMANCE_BUDGET.md` | `architecture/RUNTIME.md`, `testing/PerformanceTests.md` | `testing/PerformanceTests.md` (`PERF-START-*`), `testing/E2ETests.md` (`E2E-CORE-*`) | PARTIAL |
| NFR-SEC-001 Permission and sandbox enforcement | `security/SandboxPolicy.md`, `security/PermissionModel.md` | `architecture/SANDBOX.md`, `protocols/Tool-Protocol.md`, `protocols/Plugin-Protocol.md`, `testing/SecurityTests.md` | `testing/SecurityTests.md` (`SEC-PERM-*`, `SEC-SBX-*`, `SEC-SECRET-*`) | PARTIAL |
| NFR-REL-001 Durable lifecycle and replay safety | `specs/EXECUTION_LIFECYCLE.md` | `models/Execution.md`, `protocols/Execution-Protocol.md`, `docs/api/Runtime-API.md`, `testing/IntegrationTests.md` | `testing/IntegrationTests.md` (`IT-CONTRACT-*`), `testing/RegressionTests.md` (`RT-CONTRACT-*`) | PARTIAL |
| NFR-COMP-001 Contract compatibility and versioning | `VERSIONING.md`, `standards/Registry-Standard.md` | `docs/api/*`, `sdk/*`, `registry/AGENTS.md`, `registry/PROVIDERS.md`, `registry/PLUGINS.md`, `registry/TOOLS.md`, `registry/SKILLS.md` | `testing/RegressionTests.md` (`RT-CONTRACT-*`, `RT-PLUGIN-*`, `RT-PROVIDER-*`) | PARTIAL |
| Canonical error envelope | `errors/ERROR_CODES.md` | all `docs/api/*`, `protocols/*`, `sdk/*`, runtime and task projections | `testing/RegressionTests.md` (`RT-CONTRACT-*`), `testing/IntegrationTests.md` (`IT-CONTRACT-*`) | OK |
| Correlation, idempotency, resume, and version semantics | owning architecture documents | API envelopes, execution/task/workflow models, protocol events, SDK helpers, testing docs | `testing/E2ETests.md` (`E2E-CORE-*`), `testing/UnitTests.md` (`UT-CONTRACT-*`), `testing/IntegrationTests.md` (`IT-CONTRACT-*`) | PARTIAL |

## Open Gaps

- Requirement-level mapping remains incomplete for large portions of `requirements/FR.md` and most `requirements/NFR.md` entries.
- Suite identifiers are now defined, but the repository still lacks concrete executable test case inventories behind most suite families.
- Some entities still rely on architecture/spec documents rather than dedicated lifecycle authorities.
- Registry compatibility expectations are closer to normalized, but existing registry content has not been fully rewritten into one shared schema.
