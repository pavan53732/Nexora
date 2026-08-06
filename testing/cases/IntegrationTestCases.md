# Integration Test Case Inventory — Nexora

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| IT-CONTRACT-001 | IT-CONTRACT | Validate cross-layer correlation continuity | Core Runtime | Planned | `evidence/integration/IT-CONTRACT-001/` | 2026-08-04 |
| IT-CONTRACT-002 | IT-CONTRACT | Validate lifecycle event ordering after durable commit | Core Runtime | Planned | `evidence/integration/IT-CONTRACT-002/` | 2026-08-04 |
| IT-AGENT-001 | IT-AGENT | Validate agent task start with durable projection | Agent Runtime | Planned | `evidence/integration/IT-AGENT-001/` | 2026-08-04 |
| IT-TOOL-001 | IT-TOOL | Validate permission and sandbox checks before tool side effects | Tooling + Sandbox | Planned | `evidence/integration/IT-TOOL-001/` | 2026-08-04 |
| IT-PROVIDER-001 | IT-PROVIDER | Validate provider stream terminal marker semantics | Provider Layer | Planned | `evidence/integration/IT-PROVIDER-001/` | 2026-08-04 |
| IT-PLUGIN-001 | IT-PLUGIN | Validate transactional plugin activation and rollback | Plugin System | Planned | `evidence/integration/IT-PLUGIN-001/` | 2026-08-04 |
| IT-MEMORY-001 | IT-MEMORY | Validate memory write/retrieve provenance linkage | Memory System | Planned | `evidence/integration/IT-MEMORY-001/` | 2026-08-04 |
| IT-TOOL-002 | IT-TOOL | TOOL-408 validates both required scopes before side effects | Tool + Security | Planned | `evidence/integration/IT-TOOL-002/` | 2026-08-06 |
| IT-TOOL-003 | IT-TOOL | Aggregated approval spans PermissionManager and ToolExecutor | Tool + Security | Planned | `evidence/integration/IT-TOOL-003/` | 2026-08-06 |
| IT-TOOL-004 | IT-TOOL | Malformed approval cannot cross authorization boundary | Tool + Security | Planned | `evidence/integration/IT-TOOL-004/` | 2026-08-06 |
| IT-TOOL-005 | IT-TOOL | Approved ASK proceeds to selected classifier | Tool + Security | Planned | `evidence/integration/IT-TOOL-005/` | 2026-08-06 |
| IT-TOOL-006 | IT-TOOL | Classifier DENY prevents sandbox/tool side effects | Tool + Security | Planned | `evidence/integration/IT-TOOL-006/` | 2026-08-06 |
| IT-TOOL-007 | IT-TOOL | Policy DENY prevents classifier and execution | Tool + Security | Planned | `evidence/integration/IT-TOOL-007/` | 2026-08-06 |
| IT-TOOL-008 | IT-TOOL | Classifier skip reason preserved in audit | Tool + Security | Planned | `evidence/integration/IT-TOOL-008/` | 2026-08-06 |
| IT-TOOL-009 | IT-TOOL | Authorization correlation/toolCall IDs preserved | Tool + Security | Planned | `evidence/integration/IT-TOOL-009/` | 2026-08-06 |
| IT-LC-001 | IT-LC | Checkpoint resume retains executionId | Runtime | Planned | `evidence/integration/IT-LC-001/` | 2026-08-06 |
| IT-LC-002 | IT-LC | Checkpoint resume increments version | Runtime | Planned | `evidence/integration/IT-LC-002/` | 2026-08-06 |
| IT-LC-003 | IT-LC | Checkpoint resume retains correlationId | Runtime | Planned | `evidence/integration/IT-LC-003/` | 2026-08-06 |
| IT-LC-004 | IT-LC | WorkManager handoff retains executionId | Runtime | Planned | `evidence/integration/IT-LC-004/` | 2026-08-06 |
| IT-LC-005 | IT-LC | BootReceiver resume retains executionId | Runtime | Planned | `evidence/integration/IT-LC-005/` | 2026-08-06 |
| IT-LC-006 | IT-LC | Retry after FAILED creates new executionId | Runtime | Planned | `evidence/integration/IT-LC-006/` | 2026-08-06 |
| IT-LC-007 | IT-LC | Retry after CANCELLED creates new executionId | Runtime | Planned | `evidence/integration/IT-LC-007/` | 2026-08-06 |
| IT-LC-008 | IT-LC | Retry after COMPLETED creates new executionId | Runtime | Planned | `evidence/integration/IT-LC-008/` | 2026-08-06 |
| IT-LC-009 | IT-LC | Retry records priorExecutionId | Runtime | Planned | `evidence/integration/IT-LC-009/` | 2026-08-06 |
| IT-LC-010 | IT-LC | Terminal Execution cannot transition to RUNNING | Runtime | Planned | `evidence/integration/IT-LC-010/` | 2026-08-06 |
| IT-LC-011 | IT-LC | Non-idempotent in-flight call reconciled, not replayed | Runtime | Planned | `evidence/integration/IT-LC-011/` | 2026-08-06 |
| IT-LC-012 | IT-LC | Idempotent incomplete call may replay safely | Runtime | Planned | `evidence/integration/IT-LC-012/` | 2026-08-06 |
| IT-LC-013 | IT-LC | Duplicate resume event deduplicated | Runtime | Planned | `evidence/integration/IT-LC-013/` | 2026-08-06 |
| IT-LC-014 | IT-LC | Session close drains/detaches active execution | Runtime + Session | Planned | `evidence/integration/IT-LC-014/` | 2026-08-06 |
| IT-LC-015 | IT-LC | ToolStatus transition and tool-call execution remain separate | Tool | Planned | `evidence/integration/IT-LC-015/` | 2026-08-06 |
| IT-TOOL-010 | IT-TOOL | Invalid permission declaration rejected during registration | Tool + Security | Planned | `evidence/integration/IT-TOOL-010/` | 2026-08-06 |
| IT-TOOL-011 | IT-TOOL | Classifier policy selects workspace-opted tool | Tool + Security | Planned | `evidence/integration/IT-TOOL-011/` | 2026-08-06 |
| IT-TOOL-012 | IT-TOOL | Approved ASK creates complete ResolvedPermission projection | Tool + Security | Planned | `evidence/integration/IT-TOOL-012/` | 2026-08-06 |
| IT-TOOL-013 | IT-TOOL | Classifier denial maps through Tool API/Protocol to NXR-2003 | Tool + Security | Planned | `evidence/integration/IT-TOOL-013/` | 2026-08-06 |
| IT-TOOL-014 | IT-TOOL | Authorization audit preserves toolCallId/correlationId | Tool + Security | Planned | `evidence/integration/IT-TOOL-014/` | 2026-08-06 |
| IT-LC-016 | IT-LC | Retry ExecutionProjection includes priorExecutionId | Runtime | Planned | `evidence/integration/IT-LC-016/` | 2026-08-06 |
| IT-LC-017 | IT-LC | Retry predecessor linkage is acyclic | Runtime | Planned | `evidence/integration/IT-LC-017/` | 2026-08-06 |
| IT-LC-018 | IT-LC | RESUME protocol preserves ID and increments version | Runtime | Planned | `evidence/integration/IT-LC-018/` | 2026-08-06 |
| IT-LC-019 | IT-LC | RETRY_AFTER_TERMINAL protocol creates new ID | Runtime | Planned | `evidence/integration/IT-LC-019/` | 2026-08-06 |
| IT-LC-020 | IT-LC | WorkManager and BootReceiver both use RESUME semantics | Runtime | Planned | `evidence/integration/IT-LC-020/` | 2026-08-06 |
