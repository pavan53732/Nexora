# Security Test Case Inventory — Nexora

> **DEC-42 boundary:** `SEC-PERM-037..052`, `SEC-PERM-054`, and `SEC-PERM-056..064` retain classifier-era case identities for historical traceability only. Their classifier-selection, classifier-input, classifier-skip, and classifier-denial purposes are superseded as active execution requirements because no local classifier is implemented or invoked. The existing `Planned` values do not claim current implementation or execution evidence. Active authorization coverage remains governed by `security/PermissionModel.md`, the non-classifier PermissionModel cases, and the current Tool authorization contract.

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
| SEC-NET-001 | SEC-NET | Validate egress proxy Allowed Domains, DLP outbound scan, and direct-socket denial (guest processes cannot bypass the workspace egress proxy; pinned/foreign-cert traffic is denied — fail-closed) | Security | Planned | `evidence/security/SEC-NET-001/` | 2026-08-05 |
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
| SEC-PERM-024 | SEC-PERM | Duplicate required scope ID rejected | Security | Planned | `evidence/security/SEC-PERM-024/` | 2026-08-06 |
| SEC-PERM-025 | SEC-PERM | Duplicate pending approval scope rejected | Security | Planned | `evidence/security/SEC-PERM-025/` | 2026-08-06 |
| SEC-PERM-026 | SEC-PERM | Duplicate approval outcome rejected | Security | Planned | `evidence/security/SEC-PERM-026/` | 2026-08-06 |
| SEC-PERM-027 | SEC-PERM | Missing approval outcome rejected | Security | Planned | `evidence/security/SEC-PERM-027/` | 2026-08-06 |
| SEC-PERM-028 | SEC-PERM | Unexpected extra outcome rejected | Security | Planned | `evidence/security/SEC-PERM-028/` | 2026-08-06 |
| SEC-PERM-029 | SEC-PERM | Empty approval result rejected | Security | Planned | `evidence/security/SEC-PERM-029/` | 2026-08-06 |
| SEC-PERM-030 | SEC-PERM | Transaction ID mismatch rejected | Security | Planned | `evidence/security/SEC-PERM-030/` | 2026-08-06 |
| SEC-PERM-031 | SEC-PERM | Valid exact one-to-one approval accepted | Security | Planned | `evidence/security/SEC-PERM-031/` | 2026-08-06 |
| SEC-PERM-032 | SEC-PERM | Malformed result returns MALFORMED_APPROVAL | Security | Planned | `evidence/security/SEC-PERM-032/` | 2026-08-06 |
| SEC-PERM-033 | SEC-PERM | Malformed result is rejected before authorization completion and never executes the Tool | Security | Planned | `evidence/security/SEC-PERM-033/` | 2026-08-06 |
| SEC-PERM-034 | SEC-PERM | Malformed result never executes tool | Security | Planned | `evidence/security/SEC-PERM-034/` | 2026-08-06 |
| SEC-PERM-035 | SEC-PERM | resolvedPermissions includes all policy-allowed scopes | Security | Planned | `evidence/security/SEC-PERM-035/` | 2026-08-06 |
| SEC-PERM-036 | SEC-PERM | resolvedPermissions includes approved ASK scopes | Security | Planned | `evidence/security/SEC-PERM-036/` | 2026-08-06 |
| SEC-PERM-037 | SEC-PERM | Denied scopes never execute the Tool or become authorization success | Security | Planned | `evidence/security/SEC-PERM-037/` | 2026-08-06 |
| SEC-PERM-038 | SEC-PERM | Empty permission list follows the PermissionModel decision directly | Security | Planned | `evidence/security/SEC-PERM-038/` | 2026-08-06 |
| SEC-PERM-039 | SEC-PERM | Workspace scope override precedence remains deterministic | Security | Planned | `evidence/security/SEC-PERM-039/` | 2026-08-06 |
| SEC-PERM-040 | SEC-PERM | Workspace tool override precedence remains deterministic | Security | Planned | `evidence/security/SEC-PERM-040/` | 2026-08-06 |
| SEC-PERM-041 | SEC-PERM | ASK/DENY-default satisfied scope triggers SCOPE_RISK_POLICY | Security | Planned | `evidence/security/SEC-PERM-041/` | 2026-08-06 |
| SEC-PERM-042 | SEC-PERM | All low-risk ALLOW scopes produce NOT_SELECTED | Security | Planned | `evidence/security/SEC-PERM-042/` | 2026-08-06 |
| SEC-PERM-043 | SEC-PERM | Retired classifier-era selection case; no local classifier skip is part of the active contract | Security | Planned | `evidence/security/SEC-PERM-043/` | 2026-08-06 |
| SEC-PERM-044 | SEC-PERM | Authorization resolution and final denial outcomes are audited | Security | Planned | `evidence/security/SEC-PERM-044/` | 2026-08-06 |
| SEC-PERM-045 | SEC-PERM | PermissionModel ALLOW produces an authorization audit record without a classifier dependency | Security | Planned | `evidence/security/SEC-PERM-045/` | 2026-08-06 |
| SEC-PERM-046 | SEC-PERM | Preserved classification-denial compatibility outcome maps through canonical NXR-2003 when applicable | Security | Planned | `evidence/security/SEC-PERM-046/` | 2026-08-06 |
| SEC-PERM-047 | SEC-PERM | Canonical authorization denial is final for the current call | Security | Planned | `evidence/security/SEC-PERM-047/` | 2026-08-06 |
| SEC-PERM-048 | SEC-PERM | Approved ASK followed by a canonical denial blocks execution without side effects | Security | Planned | `evidence/security/SEC-PERM-048/` | 2026-08-06 |
| SEC-PERM-049 | SEC-PERM | Rejected ASK never executes the Tool | Security | Planned | `evidence/security/SEC-PERM-049/` | 2026-08-06 |
| SEC-PERM-050 | SEC-PERM | Policy DENY never executes the Tool | Security | Planned | `evidence/security/SEC-PERM-050/` | 2026-08-06 |
| SEC-PERM-051 | SEC-PERM | Permission resolution is order-independent for declared scopes | Security | Planned | `evidence/security/SEC-PERM-051/` | 2026-08-06 |
| SEC-PERM-052 | SEC-PERM | Authorization audit redacts sensitive inputs | Security | Planned | `evidence/security/SEC-PERM-052/` | 2026-08-06 |
| SEC-PERM-053 | SEC-PERM | Approved ASK ResolvedPermission includes declaredDefault | Security | Planned | `evidence/security/SEC-PERM-053/` | 2026-08-06 |
| SEC-PERM-054 | SEC-PERM | Denied outcomes never enter authorization success or Tool execution | Security | Planned | `evidence/security/SEC-PERM-054/` | 2026-08-06 |
| SEC-PERM-055 | SEC-PERM | Duplicate Tool scope declaration maps to INVALID_SCOPE_DECLARATION | Security | Planned | `evidence/security/SEC-PERM-055/` | 2026-08-06 |
| SEC-PERM-056 | SEC-PERM | Workspace tool override precedence | Security | Planned | `evidence/security/SEC-PERM-056/` | 2026-08-06 |
| SEC-PERM-057 | SEC-PERM | Workspace scope override precedence | Security | Planned | `evidence/security/SEC-PERM-057/` | 2026-08-06 |
| SEC-PERM-058 | SEC-PERM | Scope resolution precedence remains deterministic | Security | Planned | `evidence/security/SEC-PERM-058/` | 2026-08-06 |
| SEC-PERM-059 | SEC-PERM | Tool risk metadata does not bypass PermissionModel resolution | Security | Planned | `evidence/security/SEC-PERM-059/` | 2026-08-06 |
| SEC-PERM-060 | SEC-PERM | No local classifier is selectable or active; PermissionModel remains authoritative | Security | Planned | `evidence/security/SEC-PERM-060/` | 2026-08-06 |
| SEC-PERM-061 | SEC-PERM | Empty-permission high-risk Tool follows current PermissionModel scope rules | Security | Planned | `evidence/security/SEC-PERM-061/` | 2026-08-06 |
| SEC-PERM-062 | SEC-PERM | Preserved classification-denial compatibility outcome uses canonical NXR-2003 audit semantics when applicable | Security | Planned | `evidence/security/SEC-PERM-062/` | 2026-08-06 |
| SEC-PERM-063 | SEC-PERM | Authorization outcome audit includes a deterministic reason | Security | Planned | `evidence/security/SEC-PERM-063/` | 2026-08-06 |
| SEC-PERM-064 | SEC-PERM | Audit redacts authorization-sensitive details | Security | Planned | `evidence/security/SEC-PERM-064/` | 2026-08-06 |
| SEC-PERM-065 | SEC-PERM | Malformed approval audit preserves transaction ID | Security | Planned | `evidence/security/SEC-PERM-065/` | 2026-08-06 |
| SEC-PERM-066 | SEC-PERM | Invalid descriptor rejected before Tool activation | Security | Planned | `evidence/security/SEC-PERM-066/` | 2026-08-06 |
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
| SEC-STREAM-001 | SEC-STREAM | Reject forged or duplicate terminal event | Security + Provider | Planned | `evidence/security/SEC-STREAM-001/` | 2026-08-06 |
| SEC-STREAM-002 | SEC-STREAM | Detect replay and sequence-gap injection | Security + Provider | Planned | `evidence/security/SEC-STREAM-002/` | 2026-08-06 |
| SEC-STREAM-003 | SEC-STREAM | Incomplete Tool fragments never execute | Security + Tooling | Planned | `evidence/security/SEC-STREAM-003/` | 2026-08-06 |
| SEC-STREAM-004 | SEC-STREAM | Reconnect and failover remain attributable in audit | Security + Observability | Planned | `evidence/security/SEC-STREAM-004/` | 2026-08-06 |
| SEC-STREAM-005 | SEC-STREAM | Raw private reasoning and secrets never persist/export | Security + Context | Planned | `evidence/security/SEC-STREAM-005/` | 2026-08-06 |
| SEC-STREAM-006 | SEC-STREAM | Resume token is scoped, redacted, and expiry-enforced | Security + Provider | Planned | `evidence/security/SEC-STREAM-006/` | 2026-08-06 |
| SEC-STREAM-007 | SEC-STREAM | Privacy-constrained routing blocks ineligible failover | Security + Provider | Planned | `evidence/security/SEC-STREAM-007/` | 2026-08-06 |
| SEC-STREAM-008 | SEC-STREAM | Oversized event fails without unbounded allocation | Security + Provider | Planned | `evidence/security/SEC-STREAM-008/` | 2026-08-06 |
| SEC-STREAM-009 | SEC-STREAM | Slow consumer preserves semantic events under backpressure | Security + Provider | Planned | `evidence/security/SEC-STREAM-009/` | 2026-08-06 |
| SEC-STREAM-010 | SEC-STREAM | Reasoning budget exhaustion escalates without runaway | Security + Reasoning | Planned | `evidence/security/SEC-STREAM-010/` | 2026-08-06 |
| SEC-ESC-001 | SEC-ESC | Unsupported Terminal/Background capability cannot be self-granted by an agent | Security + Agent Runtime | Planned | `evidence/security/SEC-ESC-001/` | 2026-08-15 |
| SEC-ESC-002 | SEC-ESC | Task-scoped escalation cannot transfer across agent, task, workspace, or execution lineage | Security + Agent Runtime | Planned | `evidence/security/SEC-ESC-002/` | 2026-08-15 |
| SEC-ESC-003 | SEC-ESC | Terminal escalation still enforces sandbox scopes, canonical denial, path, network, process, output, and timeout controls | Security + Terminal + Sandbox | Planned | `evidence/security/SEC-ESC-003/` | 2026-08-15 |
| SEC-ESC-004 | SEC-ESC | Background escalation cannot bypass checkpoint, notification, cancellation, resource, Android lifecycle, or degraded-mode controls | Security + Background Runtime | Planned | `evidence/security/SEC-ESC-004/` | 2026-08-15 |
| SEC-ESC-005 | SEC-ESC | Expiry/revocation cancels active descendants, preserves checkpoint/audit lineage, and cannot reset deadlines or retry budgets | Security + Recovery | Planned | `evidence/security/SEC-ESC-005/` | 2026-08-15 |
| SEC-ESC-006 | SEC-ESC | Escalation request, approval, use, denial, expiry, revocation, and final disposition are redacted and audit-correlated | Security + Observability | Planned | `evidence/security/SEC-ESC-006/` | 2026-08-15 |
