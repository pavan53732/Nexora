# Requirement-to-Implementation Traceability Matrix

> **Status: DERIVED** traceability index linking requirements to architecture, contracts, and validation artifacts.

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
| Canonical error envelope | `errors/ERROR_CODES.md` | all `docs/api/*`, `protocols/*`, `sdk/*`, runtime and task projections | `testing/RegressionTests.md`, `testing/IntegrationTests.md` | OK |
| Correlation, idempotency, resume, and version semantics | owning architecture documents | API envelopes, execution/task models, protocol events, SDK helpers | `testing/E2ETests.md`, replay/retry scenarios | PARTIAL |

## Open Gaps

- Requirement-level mapping remains incomplete for many `FR-*` identifiers outside the core contract path.
- Some registries and testing docs describe capability coverage but do not yet reference the hardened envelope semantics explicitly.
- State-machine alignment is stronger for Task/Execution than for every remaining domain model.
