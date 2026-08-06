# Security Test Case Inventory — Nexora

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| SEC-PERM-001 | SEC-PERM | Validate authorization before tool side effects | Security | Planned | `evidence/security/SEC-PERM-001/` | 2026-08-04 |
| SEC-PERM-002 | SEC-PERM | Validate cancellation/retry cannot bypass authorization | Security | Planned | `evidence/security/SEC-PERM-002/` | 2026-08-04 |
| SEC-SBX-001 | SEC-SBX | Validate sandbox escape resistance | Security + Sandbox | Planned | `evidence/security/SEC-SBX-001/` | 2026-08-04 |
| SEC-SECRET-001 | SEC-SECRET | Validate credential redaction across boundaries | Security | Planned | `evidence/security/SEC-SECRET-001/` | 2026-08-04 |
| SEC-PLUGIN-001 | SEC-PLUGIN | Validate plugin activation rollback preserves isolation | Security + Plugin System | Planned | `evidence/security/SEC-PLUGIN-001/` | 2026-08-04 |
| SEC-DOS-001 | SEC-DOS | Validate process spawn limiting and Doze handoffs | Security + Sandbox | Planned | `evidence/security/SEC-DOS-001/` | 2026-08-05 |
| SEC-DOS-002 | SEC-DOS | Validate workspace memory quotas and write-blocking | Security + Sandbox | Planned | `evidence/security/SEC-DOS-002/` | 2026-08-05 |
| SEC-FLOW-001 | SEC-FLOW | Validate provider profile isolation and credential containment | Security + Provider | Planned | `evidence/security/SEC-FLOW-001/` | 2026-08-05 |
| SEC-NET-001 | SEC-NET | Validate egress proxy Allowed Domains and DLP outbound scan | Security | Planned | `evidence/security/SEC-NET-001/` | 2026-08-05 |
| SEC-PERM-003 | SEC-PERM | Multi-scope permission: empty permission list → allowed | Security | Planned | `evidence/security/SEC-PERM-003/` | 2026-08-06 |
| SEC-PERM-004 | SEC-PERM | Multi-scope permission: one ALLOW scope → allowed | Security | Planned | `evidence/security/SEC-PERM-004/` | 2026-08-06 |
| SEC-PERM-005 | SEC-PERM | Multi-scope permission: one ASK scope approved → allowed | Security | Planned | `evidence/security/SEC-PERM-005/` | 2026-08-06 |
| SEC-PERM-006 | SEC-PERM | Multi-scope permission: one ASK scope denied → denied | Security | Planned | `evidence/security/SEC-PERM-006/` | 2026-08-06 |
| SEC-PERM-007 | SEC-PERM | Multi-scope permission: one DENY scope → denied | Security | Planned | `evidence/security/SEC-PERM-007/` | 2026-08-06 |
| SEC-PERM-008 | SEC-PERM | Multi-scope permission: multiple ALLOW → allowed | Security | Planned | `evidence/security/SEC-PERM-008/` | 2026-08-06 |
| SEC-PERM-009 | SEC-PERM | Multi-scope permission: ALLOW then DENY → denied | Security | Planned | `evidence/security/SEC-PERM-009/` | 2026-08-06 |
| SEC-PERM-010 | SEC-PERM | Multi-scope permission: DENY then ALLOW → denied (first DENY wins) | Security | Planned | `evidence/security/SEC-PERM-010/` | 2026-08-06 |
| SEC-PERM-011 | SEC-PERM | Multi-scope permission: ALLOW then ASK → ASK aggregated | Security | Planned | `evidence/security/SEC-PERM-011/` | 2026-08-06 |
| SEC-PERM-012 | SEC-PERM | Multi-scope permission: multiple ASK scopes aggregated | Security | Planned | `evidence/security/SEC-PERM-012/` | 2026-08-06 |
| SEC-PERM-013 | SEC-PERM | Multi-scope permission: unknown scope ID → immediate DENY | Security | Planned | `evidence/security/SEC-PERM-013/` | 2026-08-06 |
| SEC-PERM-014 | SEC-PERM | Multi-scope permission: Agent override precedence | Security | Planned | `evidence/security/SEC-PERM-014/` | 2026-08-06 |
| SEC-PERM-015 | SEC-PERM | Multi-scope permission: Workspace override precedence | Security | Planned | `evidence/security/SEC-PERM-015/` | 2026-08-06 |
| SEC-PERM-016 | SEC-PERM | Multi-scope permission: Global policy precedence | Security | Planned | `evidence/security/SEC-PERM-016/` | 2026-08-06 |
| SEC-PERM-017 | SEC-PERM | Multi-scope permission: known scope default fallback | Security | Planned | `evidence/security/SEC-PERM-017/` | 2026-08-06 |
| SEC-PERM-018 | SEC-PERM | TOOL-408 (pipe_delegate): both scopes approved | Security + Pipes | Planned | `evidence/security/SEC-PERM-018/` | 2026-08-06 |
| SEC-PERM-019 | SEC-PERM | TOOL-408: instance:delegate denied → tool denied | Security + Pipes | Planned | `evidence/security/SEC-PERM-019/` | 2026-08-06 |
| SEC-PERM-020 | SEC-PERM | TOOL-408: agent:create denied → tool denied | Security + Pipes | Planned | `evidence/security/SEC-PERM-020/` | 2026-08-06 |
| SEC-PERM-021 | SEC-PERM | TOOL-408: only one scope approved → tool denied | Security + Pipes | Planned | `evidence/security/SEC-PERM-021/` | 2026-08-06 |
| SEC-PERM-022 | SEC-PERM | TOOL-408: reversed scope order, same result | Security + Pipes | Planned | `evidence/security/SEC-PERM-022/` | 2026-08-06 |
| SEC-PERM-023 | SEC-PERM | Multi-scope audit: every preliminary and final scope result recorded | Security | Planned | `evidence/security/SEC-PERM-023/` | 2026-08-06 |
| SEC-LC-SESSION-001 | SEC-LC | Session: valid CREATED→ACTIVE transition | Security + Runtime | Planned | `evidence/security/SEC-LC-SESSION-001/` | 2026-08-06 |
| SEC-LC-SESSION-002 | SEC-LC | Session: valid ACTIVE→IDLE→ACTIVE cycle | Security + Runtime | Planned | `evidence/security/SEC-LC-SESSION-002/` | 2026-08-06 |
| SEC-LC-SESSION-003 | SEC-LC | Session: CLOSED is terminal, no further transitions | Security + Runtime | Planned | `evidence/security/SEC-LC-SESSION-003/` | 2026-08-06 |
| SEC-LC-SESSION-004 | SEC-LC | Session: EXPIRED is terminal, no further transitions | Security + Runtime | Planned | `evidence/security/SEC-LC-SESSION-004/` | 2026-08-06 |
| SEC-LC-SESSION-005 | SEC-LC | Session: ACTIVE→EXPIRED blocked by active nonterminal Task | Security + Runtime | Planned | `evidence/security/SEC-LC-SESSION-005/` | 2026-08-06 |
| SEC-LC-SESSION-006 | SEC-LC | Session: invalid CREATED→IDLE transition denied | Security + Runtime | Planned | `evidence/security/SEC-LC-SESSION-006/` | 2026-08-06 |
| SEC-LC-EXEC-001 | SEC-LC | Execution: valid CREATED→RUNNING→COMPLETED | Security + Runtime | Planned | `evidence/security/SEC-LC-EXEC-001/` | 2026-08-06 |
| SEC-LC-EXEC-002 | SEC-LC | Execution: checkpoint resume retains same executionId | Security + Runtime | Planned | `evidence/security/SEC-LC-EXEC-002/` | 2026-08-06 |
| SEC-LC-EXEC-003 | SEC-LC | Execution: terminal FAILED cannot transition to RUNNING | Security + Runtime | Planned | `evidence/security/SEC-LC-EXEC-003/` | 2026-08-06 |
| SEC-LC-EXEC-004 | SEC-LC | Execution: retry after terminal status creates new executionId | Security + Runtime | Planned | `evidence/security/SEC-LC-EXEC-004/` | 2026-08-06 |
| SEC-LC-TOOL-001 | SEC-LC | ToolStatus: valid DISCOVERED→REGISTERED→ACTIVE | Security + Tool | Planned | `evidence/security/SEC-LC-TOOL-001/` | 2026-08-06 |
| SEC-LC-TOOL-002 | SEC-LC | ToolStatus: failed invocation does not change descriptor to DISABLED | Security + Tool | Planned | `evidence/security/SEC-LC-TOOL-002/` | 2026-08-06 |
