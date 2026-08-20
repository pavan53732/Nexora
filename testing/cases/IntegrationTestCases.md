# Integration Test Case Inventory — Nexora

> ADR-0010: case rows are `TEST DEFINED` until execution produces a result; `EXECUTED EVIDENCE` requires the common reproducible envelope in `testing/EVIDENCE_CONVENTIONS.md`. Deterministic controls are fixture-scoped and test-only.

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| IT-CONTRACT-001 | IT-CONTRACT | Validate cross-layer correlation continuity | Core Runtime | Planned | `evidence/integration/IT-CONTRACT-001/` | 2026-08-04 |
| IT-CONTRACT-002 | IT-CONTRACT | Validate lifecycle event ordering after durable commit, including workflow/step transitions and existing approval, retry, deadline, cancellation, checkpoint, and reconciliation projections | Core Runtime | Planned | `evidence/integration/IT-CONTRACT-002/` | 2026-08-04 |
| IT-AGENT-001 | IT-AGENT | Validate agent task start with durable projection of objective, phase/action, acceptance progress, ProgressSignal reason, next safe action, and final result classifications (`Passed`, `Failed`, `Skipped`, `Blocked`, `Unverified`) over existing Agent/Task/Execution identities; separately verify the evidence state and retained `EXECUTED EVIDENCE` envelope | Agent Runtime | Planned | `evidence/integration/IT-AGENT-001/` | 2026-08-04 |
| IT-TOOL-001 | IT-TOOL | Validate permission and sandbox checks before tool side effects | Tooling + Sandbox | Planned | `evidence/integration/IT-TOOL-001/` | 2026-08-04 |
| IT-PROVIDER-001 | IT-PROVIDER | Validate provider stream terminal marker semantics | Provider Layer | Planned | `evidence/integration/IT-PROVIDER-001/` | 2026-08-04 |
| IT-PROVIDER-002 | IT-PROVIDER | Validate AI Settings Test Connection and capability refresh use provider-owned health/catalog checks without creating Task/Execution state, granting permissions, invoking Tools, or exposing API keys | Provider + UI + Security | Planned | `evidence/integration/IT-PROVIDER-002/` | 2026-08-19 |
| IT-PLUGIN-001 | IT-PLUGIN | Validate transactional plugin activation compensation: `Installed` restores to `Installed` and `Inactive` restores to `Inactive` after verified cleanup; failed or unproven cleanup remains `Failed`, with no affected capability executable and retry only after verified cleanup | Plugin System | Planned | `evidence/integration/IT-PLUGIN-001/` | 2026-08-04 |
| IT-MEMORY-001 | IT-MEMORY | Validate memory write/retrieve provenance linkage | Memory System | Planned | `evidence/integration/IT-MEMORY-001/` | 2026-08-04 |
| IT-TOOL-002 | IT-TOOL | TOOL-408 validates both required scopes before side effects | Tool + Security | Planned | `evidence/integration/IT-TOOL-002/` | 2026-08-06 |
| IT-TOOL-003 | IT-TOOL | Aggregated approval spans PermissionManager and ToolExecutor | Tool + Security | Planned | `evidence/integration/IT-TOOL-003/` | 2026-08-06 |
| IT-TOOL-004 | IT-TOOL | Malformed approval cannot cross authorization boundary | Tool + Security | Planned | `evidence/integration/IT-TOOL-004/` | 2026-08-06 |
| IT-TOOL-005 | IT-TOOL | Approved ASK proceeds through complete authorization to Tool execution | Tool + Security | Planned | `evidence/integration/IT-TOOL-005/` | 2026-08-06 |
| IT-TOOL-006 | IT-TOOL | Canonical authorization denial prevents sandbox/Tool side effects | Tool + Security | Planned | `evidence/integration/IT-TOOL-006/` | 2026-08-06 |
| IT-TOOL-007 | IT-TOOL | Policy DENY prevents authorization success and Tool execution | Tool + Security | Planned | `evidence/integration/IT-TOOL-007/` | 2026-08-06 |
| IT-TOOL-008 | IT-TOOL | Authorization outcome and deterministic reason are preserved in audit | Tool + Security | Planned | `evidence/integration/IT-TOOL-008/` | 2026-08-06 |
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
| IT-LC-011 | IT-LC | Non-idempotent in-flight call remains `UNKNOWN_COMPLETION` through reconciliation exhaustion, is never replayed, and uses `requestEscalation` to place the parent Task in `BlockedAwaitingInput` while the associated Execution retains existing non-terminal/resumable `RUNNING` only; no Tool execution or automatic replay occurs while blocked, and checkpoint/resume and expiry remain canonical | Runtime | Planned | `evidence/integration/IT-LC-011/` | 2026-08-06 |
| IT-LC-012 | IT-LC | Idempotent incomplete call may replay safely | Runtime | Planned | `evidence/integration/IT-LC-012/` | 2026-08-06 |
| IT-LC-013 | IT-LC | Duplicate resume event deduplicated | Runtime | Planned | `evidence/integration/IT-LC-013/` | 2026-08-06 |
| IT-LC-014 | IT-LC | Session close drains/detaches active execution | Runtime + Session | Planned | `evidence/integration/IT-LC-014/` | 2026-08-06 |
| IT-LC-015 | IT-LC | ToolStatus transition and tool-call execution remain separate | Tool | Planned | `evidence/integration/IT-LC-015/` | 2026-08-06 |
| IT-TOOL-010 | IT-TOOL | Invalid permission declaration rejected during registration | Tool + Security | Planned | `evidence/integration/IT-TOOL-010/` | 2026-08-06 |
| IT-TOOL-011 | IT-TOOL | Workspace policy precedence governs authorization for an opted tool | Tool + Security | Planned | `evidence/integration/IT-TOOL-011/` | 2026-08-06 |
| IT-TOOL-012 | IT-TOOL | Approved ASK creates complete ResolvedPermission projection | Tool + Security | Planned | `evidence/integration/IT-TOOL-012/` | 2026-08-06 |
| IT-TOOL-013 | IT-TOOL | Canonical authorization denial maps through Tool API/Protocol to NXR-2003 | Tool + Security | Planned | `evidence/integration/IT-TOOL-013/` | 2026-08-06 |
| IT-TOOL-014 | IT-TOOL | Authorization audit preserves toolCallId/correlationId | Tool + Security | Planned | `evidence/integration/IT-TOOL-014/` | 2026-08-06 |
| IT-LC-016 | IT-LC | Retry ExecutionProjection includes priorExecutionId | Runtime | Planned | `evidence/integration/IT-LC-016/` | 2026-08-06 |
| IT-LC-017 | IT-LC | Retry predecessor linkage is acyclic | Runtime | Planned | `evidence/integration/IT-LC-017/` | 2026-08-06 |
| IT-LC-018 | IT-LC | RESUME protocol preserves ID and increments version | Runtime | Planned | `evidence/integration/IT-LC-018/` | 2026-08-06 |
| IT-LC-019 | IT-LC | RETRY_AFTER_TERMINAL protocol creates new ID | Runtime | Planned | `evidence/integration/IT-LC-019/` | 2026-08-06 |
| IT-LC-020 | IT-LC | WorkManager and BootReceiver both use RESUME semantics | Runtime | Planned | `evidence/integration/IT-LC-020/` | 2026-08-06 |
| IT-STREAM-001 | IT-STREAM | Provider adapter normalizes native SSE into typed StreamEnvelope | Provider Layer | Planned | `evidence/integration/IT-STREAM-001/` | 2026-08-06 |
| IT-STREAM-002 | IT-STREAM | Slow UI applies bounded backpressure without semantic-event loss | Provider + UI | Planned | `evidence/integration/IT-STREAM-002/` | 2026-08-06 |
| IT-STREAM-003 | IT-STREAM | Cancellation propagates Agent to adapter and commits once | Agent + Provider | Planned | `evidence/integration/IT-STREAM-003/` | 2026-08-06 |
| IT-STREAM-004 | IT-STREAM | Native resume preserves streamId and next sequence | Provider Layer | Planned | `evidence/integration/IT-STREAM-004/` | 2026-08-06 |
| IT-STREAM-005 | IT-STREAM | Unsupported resume restarts with priorStreamId lineage | Provider + Runtime | Planned | `evidence/integration/IT-STREAM-005/` | 2026-08-06 |
| IT-STREAM-006 | IT-STREAM | Cross-provider failover never splices output | Provider + Runtime | Planned | `evidence/integration/IT-STREAM-006/` | 2026-08-06 |
| IT-STREAM-007 | IT-STREAM | Terminal usage reconciles accounting exactly once | Provider + Accounting | Planned | `evidence/integration/IT-STREAM-007/` | 2026-08-06 |
| IT-STREAM-008 | IT-STREAM | Partial Tool call never crosses authorization gate | Provider + Tooling | Planned | `evidence/integration/IT-STREAM-008/` | 2026-08-06 |
| IT-REASON-001 | IT-REASON | HIGH effort invokes verifier and bounded repair | Agent + Reasoning | Planned | `evidence/integration/IT-REASON-001/` | 2026-08-06 |
| IT-REASON-002 | IT-REASON | X_HIGH fails fast without eligible reasoning model | Reasoning + Provider | Planned | `evidence/integration/IT-REASON-002/` | 2026-08-06 |
| IT-REASON-003 | IT-REASON | OFF skips deliberation but retains grounding/evidence gates | Reasoning + Evidence | Planned | `evidence/integration/IT-REASON-003/` | 2026-08-06 |
| IT-REASON-004 | IT-REASON | Critic disagreement triggers bounded repair then escalation | Reasoning + Agent | Planned | `evidence/integration/IT-REASON-004/` | 2026-08-06 |
| IT-CONTEXT-001 | IT-CONTEXT | ContextSnapshot budget accounts for tools/output/reasoning | Context + Provider | Planned | `evidence/integration/IT-CONTEXT-001/` | 2026-08-06 |
| IT-CONTEXT-002 | IT-CONTEXT | Resume reconstructs identical ContextSnapshot lineage | Context + Memory | Planned | `evidence/integration/IT-CONTEXT-002/` | 2026-08-06 |

| IT-CONV-001 | IT-CONV | Validate immutable conversation checkpoint creation at selected post-turn boundary | Conversation/Session | Planned | `evidence/integration/IT-CONV-001/` | 2026-08-12 |
| IT-CONV-002 | IT-CONV | Validate non-destructive branch creation preserves source conversation | Conversation/Session | Planned | `evidence/integration/IT-CONV-002/` | 2026-08-12 |
| IT-CONV-003 | IT-CONV | Reject stale, expired, invalid, or unauthorized checkpoint operations without source mutation | Conversation/Session + Security | Planned | `evidence/integration/IT-CONV-003/` | 2026-08-12 |
| IT-CONV-004 | IT-CONV | Reject conflicting concurrent conversation mutation during branch request | Conversation/Session | Planned | `evidence/integration/IT-CONV-004/` | 2026-08-12 |
| IT-CONV-005 | IT-CONV | Recover interrupted or rollback-cleanup-failed branch operation as no branch or one complete branch, never success with partial branch state | Conversation/Session | Planned | `evidence/integration/IT-CONV-005/` | 2026-08-12 |
| IT-CONV-006 | IT-CONV | Confirm conversation rollback does not restore task, execution, memory, file, workspace, provider, or Git state | Conversation/Session + Runtime | Planned | `evidence/integration/IT-CONV-006/` | 2026-08-12 |
| IT-CONV-007 | IT-CONV | Confirm conversation rollback does not reverse external side effects | Conversation/Session + Runtime | Planned | `evidence/integration/IT-CONV-007/` | 2026-08-12 |
| IT-SKILL-001 | IT-SKILL | Validate skill registration and compatibility validation before availability | Skill Registry | Planned | `evidence/integration/IT-SKILL-001/` | 2026-08-12 |
| IT-SKILL-002 | IT-SKILL | Validate skill acquisition and agent binding preserve registry authority | Skill Registry + Agent Runtime | Planned | `evidence/integration/IT-SKILL-002/` | 2026-08-12 |
| IT-SKILL-003 | IT-SKILL | Validate automatic skill selection does not require manual user selection | Agent Runtime | Planned | `evidence/integration/IT-SKILL-003/` | 2026-08-12 |
| IT-SKILL-004 | IT-SKILL | Validate revoked skill blocks new selection without inventing separate permission rules | Skill Registry + Security | Planned | `evidence/integration/IT-SKILL-004/` | 2026-08-12 |
| IT-SKILL-005 | IT-SKILL | Validate skill use inherits tool authorization and sandbox constraints | Agent Runtime + Tooling + Security | Planned | `evidence/integration/IT-SKILL-005/` | 2026-08-12 |
| IT-SKILL-006 | IT-SKILL | Validate replacement path is new versioned registration plus explicit compatibility validation | Skill Registry | Planned | `evidence/integration/IT-SKILL-006/` | 2026-08-12 |
| IT-ESC-001 | IT-ESC | Unsupported Terminal/Background request is denied or delegated without silent capability acquisition | Agent Runtime + Multi-Agent | Planned | `evidence/integration/IT-ESC-001/` | 2026-08-15 |
| IT-ESC-002 | IT-ESC | Restricted agent delegation preserves complete handoff, worker isolation, artifact promotion, and parent correlation | Multi-Agent + Sandbox | Planned | `evidence/integration/IT-ESC-002/` | 2026-08-15 |
| IT-ESC-003 | IT-ESC | Task-scoped Terminal escalation passes matrix, permission, approval, sandbox, schema, timeout, and resource gates | Terminal + Security | Planned | `evidence/integration/IT-ESC-003/` | 2026-08-15 |
| IT-ESC-004 | IT-ESC | Task-scoped Background escalation validates checkpoint, progress, heartbeat/freshness, immutable deadline/remaining budget, notification, cancellation, Android lifecycle, resource, and degradation prerequisites | Background Runtime + Security | Planned | `evidence/integration/IT-ESC-004/` | 2026-08-15 |
| IT-ESC-005 | IT-ESC | Grant expiry and revocation cancel descendants, preserve checkpoint/audit lineage, and do not reset deadline or failure ledger | Runtime + Recovery | Planned | `evidence/integration/IT-ESC-005/` | 2026-08-15 |
| IT-ESC-006 | IT-ESC | Temporary grant cannot transfer across task, agent, workspace, or execution lineage and cannot mutate the static matrix | Agent Runtime + Security | Planned | `evidence/integration/IT-ESC-006/` | 2026-08-15 |
| IT-ESC-007 | IT-ESC | Correlated trace and permission audit preserve request, decision, approval, use, expiry/revocation, cancellation, final disposition, and the distinction between test-defined, tested, and retained executed evidence | Observability + Security | Planned | `evidence/integration/IT-ESC-007/` | 2026-08-15 |
| IT-LIVE-001 | IT-LIVE | STALLED provider stream uses bounded failover transition and preserves priorStreamId lineage | Provider + Runtime | Planned | `evidence/integration/IT-LIVE-001/` | 2026-08-15 |
| IT-LIVE-002 | IT-LIVE | NXR-2002 timeout preserves `UNKNOWN_COMPLETION`, retries only after reconciliation/idempotency authorization, and after exhaustion uses existing escalation to Task `BlockedAwaitingInput` with associated Execution retaining existing non-terminal/resumable `RUNNING` only, no Tool execution or automatic replay while blocked | Tool + Runtime | Planned | `evidence/integration/IT-LIVE-002/` | 2026-08-15 |
| IT-LIVE-003 | IT-LIVE | RetryPending cannot start before backoff and scheduler authorization | Task Scheduler + Runtime | Planned | `evidence/integration/IT-LIVE-003/` | 2026-08-15 |
| IT-LIVE-004 | IT-LIVE | Agent Completing finalizes artifacts and resources before Completed commit | Agent Runtime | Planned | `evidence/integration/IT-LIVE-004/` | 2026-08-15 |
| IT-LIVE-005 | IT-LIVE | Stream failure, cancellation, missing draft, and denied Tool call route to non-success effects without completion synthesis | Agent + Provider + Tool | Planned | `evidence/integration/IT-LIVE-005/` | 2026-08-15 |
| IT-LIVE-006 | IT-LIVE | Invalid dependency, unsatisfied dependency, and effective-deadline expiry persist NXR-1014/NXR-1015/NXR-1016 and the selected Task effects | Task + Runtime | Planned | `evidence/integration/IT-LIVE-006/` | 2026-08-15 |
| IT-TERM-001 | IT-TERM | Background TerminalSession inherits parent identity/deadline and reconciles cancellation, terminal parent, expiry, restart, and bounded cleanup failure without reattachment | Terminal + Runtime | Planned | `evidence/integration/IT-TERM-001/` | 2026-08-15 |
| IT-BROWSER-001 | IT-BROWSER | WebView bridge interruption preserves UNKNOWN_COMPLETION and prevents silent replay of potentially mutating browser operations | Browser + Tool System | Planned | `evidence/integration/IT-BROWSER-001/` | 2026-08-15 |
| IT-AUTH-001 | IT-AUTH | Approval denial/expiry emits NXR-2003, prevents side effects, commits Task Failed, and independently projects Agent Paused | Security + Agent + Task | Planned | `evidence/integration/IT-AUTH-001/` | 2026-08-15 |
