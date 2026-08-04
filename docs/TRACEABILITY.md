# Requirement-to-Implementation Traceability Matrix

> **Status: CANONICAL** for mapping requirements to architecture, contracts, and tests.

| Requirement ID | Architecture Doc | State Machine | Model | Protocol | API | SDK | Tests | Status |
|---------------|------------------|---------------|-------|----------|-----|-----|-------|--------|
| FR-W001 | architecture/RUNTIME.md | — | models/Workspace.md | — | docs/api/Runtime-API.md | — | testing/UnitTests.md | ✅ |
| FR-W006 | architecture/SANDBOX.md | — | models/Workspace.md | — | — | — | testing/SecurityTests.md | ✅ |
| FR-A001 | architecture/AGENT_RUNTIME.md | — | models/Agent.md | protocols/Agent-Protocol.md | docs/api/Agent-API.md | sdk/AgentSDK.md | testing/UnitTests.md | ✅ |
| FR-A007 | architecture/AGENT_RUNTIME.md | — | models/Session.md | protocols/Execution-Protocol.md | docs/api/Agent-API.md | — | testing/E2ETests.md | ✅ |
| FR-T001 | architecture/AGENT_RUNTIME.md | state-machines/TaskLifecycle.md | models/Task.md | protocols/Execution-Protocol.md | docs/api/Runtime-API.md | — | testing/UnitTests.md | ✅ |
| FR-S011 | architecture/SANDBOX.md | — | — | — | — | — | testing/SecurityTests.md | ✅ |
| FR-S012 | architecture/SANDBOX.md | — | — | — | — | — | testing/UnitTests.md | ✅ |
| FR-S014 | security/SandboxPolicy.md | — | — | — | — | — | testing/SecurityTests.md | ✅ |
| FR-S016 | docs/SANDBOX_DEPTH.md | — | — | — | — | — | testing/SecurityTests.md | ✅ |
| FR-TE001 | specs/TERMINAL.md | — | models/TerminalSession.md | protocols/Tool-Protocol.md | docs/api/Tool-API.md | — | testing/UnitTests.md | ✅ |
| FR-EL-006 | specs/EXECUTION_LIFECYCLE.md | — | models/Execution.md | protocols/Execution-Protocol.md | — | — | testing/IntegrationTests.md | ✅ |
| FR-MA-003 | architecture/MULTI_AGENT_SYSTEM.md | — | — | protocols/Agent-Protocol.md | — | — | testing/IntegrationTests.md | ✅ |

## Legend

- **✅** = Traced
- **🚧** = Partial
- **❌** = Missing
- **⏳** = Deferred

## Maintenance Rule

When adding a new requirement or changing an existing one, update this matrix
in the SAME commit. A PR that adds/modifies a requirement without updating
traceability will fail CI.
