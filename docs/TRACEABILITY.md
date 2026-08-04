# Requirement-to-Implementation Traceability Matrix

> **Status: CANONICAL** for mapping requirements to architecture, contracts, and tests.

| Requirement ID | Architecture Doc | State Machine | Model | Protocol | API | SDK | Tests | Error Contract | Security | Evidence | Status |
|---------------|------------------|---------------|-------|----------|-----|-----|-------|----------------|----------|----------|--------|
| FR-W001 | architecture/RUNTIME.md | — | models/Workspace.md | — | docs/api/Runtime-API.md | — | testing/UnitTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-W006 | architecture/SANDBOX.md | — | models/Workspace.md | — | — | — | testing/SecurityTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-A001 | architecture/AGENT_RUNTIME.md | — | models/Agent.md | protocols/Agent-Protocol.md | docs/api/Agent-API.md | sdk/AgentSDK.md | testing/UnitTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-A007 | architecture/AGENT_RUNTIME.md | — | models/Session.md | protocols/Execution-Protocol.md | docs/api/Agent-API.md | — | testing/E2ETests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-T001 | architecture/AGENT_RUNTIME.md | state-machines/TaskLifecycle.md | models/Task.md | protocols/Execution-Protocol.md | docs/api/Runtime-API.md | — | testing/UnitTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-S011 | architecture/SANDBOX.md | — | — | — | — | — | testing/SecurityTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-S012 | architecture/SANDBOX.md | — | — | — | — | — | testing/UnitTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-S014 | security/SandboxPolicy.md | — | — | — | — | — | testing/SecurityTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-S016 | docs/SANDBOX_DEPTH.md | — | — | — | — | — | testing/SecurityTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-TE001 | specs/TERMINAL.md | — | models/TerminalSession.md | protocols/Tool-Protocol.md | docs/api/Tool-API.md | — | testing/UnitTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-EL-006 | specs/EXECUTION_LIFECYCLE.md | — | models/Execution.md | protocols/Execution-Protocol.md | — | — | testing/IntegrationTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |
| FR-MA-003 | architecture/MULTI_AGENT_SYSTEM.md | — | — | protocols/Agent-Protocol.md | — | — | testing/IntegrationTests.md | errors/ERROR_CODES.md | security/PermissionModel.md | ✅ | ✅ |

## Legend

- **✅** = Traced
- **🚧** = Partial
- **❌** = Missing
- **⏳** = Deferred

## Maintenance Rule

Every requirement row MUST identify the canonical behavior owner and the executable evidence owner. A row is `✅` only when the linked documents agree on the same semantic type, lifecycle state, protocol operation, error contract, and expected test result. A row is `🚧` when any contract or evidence link is partial; `❌` when the requirement has no implementation or test mapping; and `⏳` only when the deferral is explicitly approved.

The matrix MUST be updated in the same change as any requirement, lifecycle, model, protocol, API, SDK, security, or test contract change.

When adding a new requirement or changing an existing one, update this matrix
in the SAME commit. A PR that adds/modifies a requirement without updating
traceability will fail CI.

## Contract Coverage

The following cross-layer operation contracts are mandatory traceability anchors. Each row MUST be linked to a requirement identifier before implementation status can be marked `✅`.

| Operation | Lifecycle | Model | Protocol | API | SDK | Error contract | Test evidence |
|---|---|---|---|---|---|---|---|
| Task execution | TaskLifecycle, AgentLifecycle | Task, Agent | Execution-Protocol | Runtime-API | AgentSDK | ERROR_CODES | Integration/E2E |
| Task cancellation | TaskLifecycle, AgentLifecycle | Task, Agent | Execution-Protocol | Runtime-API | AgentSDK | ERROR_CODES | Lifecycle/cancellation |
| Tool invocation | ToolCall semantics | Tool | Tool-Protocol | Tool-API | ToolSDK | ERROR_CODES | Security/integration |
| Provider completion | ProviderLifecycle | Provider, Execution | Provider-Protocol | Provider-API | ProviderSDK | ERROR_CODES | Provider integration |
| Plugin installation | PluginLifecycle | Plugin | Plugin-Protocol | Plugin-API | PluginSDK | ERROR_CODES | Plugin/security |
