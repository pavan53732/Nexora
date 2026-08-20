# Unit Test Case Inventory — Nexora

> ADR-0010: case rows are `TEST DEFINED` until execution produces a result; `EXECUTED EVIDENCE` requires the common reproducible envelope in `testing/EVIDENCE_CONVENTIONS.md`. Deterministic controls are fixture-scoped and test-only.

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| UT-CONTRACT-001 | UT-CONTRACT | Validate tool input schema enforcement | Core Runtime | Planned | `evidence/unit/UT-CONTRACT-001/` | 2026-08-04 |
| UT-CONTRACT-002 | UT-CONTRACT | Validate canonical error-envelope field preservation | Core Runtime | Planned | `evidence/unit/UT-CONTRACT-002/` | 2026-08-04 |
| UT-CONTRACT-003 | UT-CONTRACT | Validate idempotent retry handling for keyed operations | Core Runtime | Planned | `evidence/unit/UT-CONTRACT-003/` | 2026-08-04 |
| UT-CONTRACT-004 | UT-CONTRACT | Validate pagination cursor encode/decode behavior | API Contracts | Planned | `evidence/unit/UT-CONTRACT-004/` | 2026-08-04 |
| UT-CONTRACT-005 | UT-CONTRACT | Validate event deduplication by entity/version/transition | Core Runtime | Planned | `evidence/unit/UT-CONTRACT-005/` | 2026-08-04 |
| UT-MA-001 | UT-MA | Validate delegated sub-task linkage | Agent Runtime | Planned | `evidence/unit/UT-MA-001/` | 2026-08-04 |
| UT-AG-001 | UT-AG | Validate agent cancellation lifecycle projection | Agent Runtime | Planned | `evidence/unit/UT-AG-001/` | 2026-08-04 |
| UT-GND-001 | UT-GND | Validate response grounding metadata shape | Grounding | Planned | `evidence/unit/UT-GND-001/` | 2026-08-04 |
| UT-STREAM-001 | UT-STREAM | Validate monotonic sequence and duplicate suppression | Provider Layer | Planned | `evidence/unit/UT-STREAM-001/` | 2026-08-06 |
| UT-STREAM-002 | UT-STREAM | Detect sequence gap and block terminal commit | Provider Layer | Planned | `evidence/unit/UT-STREAM-002/` | 2026-08-06 |
| UT-STREAM-003 | UT-STREAM | Assemble interleaved Tool-call fragments by toolCallId | Provider + Tooling | Planned | `evidence/unit/UT-STREAM-003/` | 2026-08-06 |
| UT-STREAM-004 | UT-STREAM | Reject second or missing terminal event | Provider Layer | Planned | `evidence/unit/UT-STREAM-004/` | 2026-08-06 |
| UT-REASON-001 | UT-REASON | Resolve deterministic ReasoningPolicy for all effort levels and verify Context FAST/BALANCED/THOROUGH to Agent FAST/NORMAL/DEEP/VERIFY mapping plus RECOVER isolation | Reasoning | Planned | `evidence/unit/UT-REASON-001/` | 2026-08-06 |
| UT-REASON-002 | UT-REASON | Enforce technical call/token/tool/repair/time/device-resource safety ceilings and verify cost/credit telemetry cannot block a technically valid progressing run | Reasoning | Planned | `evidence/unit/UT-REASON-002/` | 2026-08-06 |
| UT-AS-004 | UT-AS | Validate lesson provenance, planning retrieval, deterministic policy or user approval for existing `LEARNED` skill promotion, trust/safety/scope/lifecycle conditions, retirement, and permission-boundary preservation | Autonomy Learning | Planned | `evidence/unit/UT-AS-004/` | 2026-08-15 |
| UT-AS-005 | UT-AS | Validate per-agent/per-workspace trust updates, automatic `MANUAL`/`ASSISTED`/`AUTOPILOT` thresholds, immediate downgrade-only user override, explicit reset, degraded-mode `MANUAL` forcing, and security-boundary preservation | Autonomy Trust | Planned | `evidence/unit/UT-AS-005/` | 2026-08-15 |
| UT-AS-010 | UT-AS | Validate acceptance-criterion progress vector, checkpoint/initial baseline, same-logical-execution deltas, relevant-evidence gating, error-category-shift semantics, semantic-progress floor, notify-and-continue only for ordinary advancing progress within existing gates, and block/escalate behavior for gated conditions | Agent Runtime | Planned | `evidence/unit/UT-AS-010/` | 2026-08-15 |
| UT-CONTRACT-006 | UT-CONTRACT | Validate hierarchical deadline propagation, cancellation reservation, and automatic disposition for exhausted `UNKNOWN_COMPLETION`: child remains unresolved, checkpoint/evidence are retained, existing Task `Failed` plus Execution `FAILED` effects apply, and no Tool execution, automatic replay, or human escalation occurs | Core Runtime | Planned | `evidence/unit/UT-CONTRACT-006/` | 2026-08-15 |
| UT-EV-007 | UT-EV | Validate one-to-one ClaimRecord evidence binding, freshness, contradiction, verifier, confidence, and disposition fields | Evidence Engine | Planned | `evidence/unit/UT-EV-007/` | 2026-08-15 |
| UT-RN-013 | UT-RN | Validate rejection of ReasoningPolicy values above non-overridable provider, device, and resource-class ceilings | Reasoning + Context | Planned | `evidence/unit/UT-RN-013/` | 2026-08-15 |
| UT-TOOL-006 | UT-TOOL | Validate unknown-completion reconciliation blocks unsafe replay; after automatic exhaustion, child remains `UNKNOWN_COMPLETION`, checkpoint/evidence are retained, existing parent Task `Failed` plus Execution `FAILED` effects apply, and no human escalation, Tool execution, or automatic replay occurs | Tool + Runtime | Planned | `evidence/unit/UT-TOOL-006/` | 2026-08-15 |
| UT-EXEC-001 | UT-EXEC | Validate failure-class binding uses the canonical error envelope, legal Task/Execution retry or terminal effects, checkpoint-save/restore exhaustion preservation, operation-owner idempotency, automatic unknown-completion exhaustion with child remaining unresolved and existing parent non-success effects, no human escalation or unsafe replay, and no undocumented state | Execution Lifecycle | Planned | `evidence/unit/UT-EXEC-001/` | 2026-08-15 |
| UT-REASON-003 | UT-REASON | Redact ReasoningSummary and exclude private trace | Security + Reasoning | Planned | `evidence/unit/UT-REASON-003/` | 2026-08-06 |
| UT-CONTEXT-001 | UT-CONTEXT | Reproduce immutable ContextSnapshot from segment hashes | Context | Planned | `evidence/unit/UT-CONTEXT-001/` | 2026-08-06 |
| UT-CONTEXT-002 | UT-CONTEXT | Deduplicate retrieval while preserving source diversity | Context + Memory | Planned | `evidence/unit/UT-CONTEXT-002/` | 2026-08-06 |
| UT-ROUTE-001 | UT-ROUTE | Rank eligible providers by hard constraints then policy score | Provider Layer | Planned | `evidence/unit/UT-ROUTE-001/` | 2026-08-06 |

| UT-CONV-001 | UT-CONV | Validate immutable conversation checkpoint lifecycle state entry | Conversation/Session | Planned | `evidence/unit/UT-CONV-001/` | 2026-08-12 |
| UT-CONV-002 | UT-CONV | Validate newer checkpoint supersedes without mutating prior checkpoint | Conversation/Session | Planned | `evidence/unit/UT-CONV-002/` | 2026-08-12 |
| UT-CONV-003 | UT-CONV | Validate invalid transitions leave checkpoint state unchanged | Conversation/Session | Planned | `evidence/unit/UT-CONV-003/` | 2026-08-12 |
| UT-CONV-004 | UT-CONV | Validate non-destructive branch semantics preserve source lineage | Conversation/Session | Planned | `evidence/unit/UT-CONV-004/` | 2026-08-12 |
| UT-CONV-005 | UT-CONV | Validate repeated operation identity does not create duplicate branch result | Conversation/Session | Planned | `evidence/unit/UT-CONV-005/` | 2026-08-12 |
| UT-CONV-006 | UT-CONV | Validate rollback side-effect boundary excludes external reversal | Conversation/Session | Planned | `evidence/unit/UT-CONV-006/` | 2026-08-12 |
| UT-SKILL-001 | UT-SKILL | Validate skill state progression Registered→Validated→Available | Skill Registry | Planned | `evidence/unit/UT-SKILL-001/` | 2026-08-12 |
| UT-SKILL-002 | UT-SKILL | Validate binding does not transfer tool execution ownership to Skill Registry | Skill Registry + Agent Runtime | Planned | `evidence/unit/UT-SKILL-002/` | 2026-08-12 |
| UT-SKILL-003 | UT-SKILL | Validate revoked skill blocks new binding/selection transitions | Skill Registry | Planned | `evidence/unit/UT-SKILL-003/` | 2026-08-12 |
| UT-SKILL-004 | UT-SKILL | Validate replacement requires explicit compatibility validation | Skill Registry | Planned | `evidence/unit/UT-SKILL-004/` | 2026-08-12 |
| UT-SKILL-005 | UT-SKILL | Validate skill metadata cannot grant permissions | Skill Registry + Security | Planned | `evidence/unit/UT-SKILL-005/` | 2026-08-12 |
| UT-SKILL-006 | UT-SKILL | Validate skill-use authorization remains tool/security controlled | Agent Runtime + Security | Planned | `evidence/unit/UT-SKILL-006/` | 2026-08-12 |
| UT-ESC-001 | UT-ESC | Validate escalation request requires task, workspace, agent, execution-lineage, purpose, capability, scope, deadline, and revocation fields | Agent Runtime | Planned | `evidence/unit/UT-ESC-001/` | 2026-08-15 |
| UT-ESC-002 | UT-ESC | Validate unsupported static capability is rejected or routed to delegation without matrix mutation | Agent Runtime + Multi-Agent | Planned | `evidence/unit/UT-ESC-002/` | 2026-08-15 |
| UT-ESC-003 | UT-ESC | Validate Terminal and Background grants expire at completion, cancellation, deadline, revocation, or terminal failure | Runtime | Planned | `evidence/unit/UT-ESC-003/` | 2026-08-15 |
| UT-ESC-004 | UT-ESC | Validate grant transfer across task, agent, workspace, or execution lineage is rejected | Security + Agent Runtime | Planned | `evidence/unit/UT-ESC-004/` | 2026-08-15 |
| UT-ESC-005 | UT-ESC | Validate expiry/revocation preserves deadline, failure ledger, checkpoint, unknown-completion, and non-success semantics; explicit clarification/capability-gap escalation may use Task `BlockedAwaitingInput` with associated Execution retaining existing non-terminal/resumable `RUNNING` only, while exhausted unknown completion uses automatic non-success and no Tool execution or replay | Runtime + Recovery | Planned | `evidence/unit/UT-ESC-005/` | 2026-08-15 |
| UT-LIVE-001 | UT-LIVE | Validate STALLED failover guard consumes bounded budget and preserves new stream lineage | Provider Stream | Planned | `evidence/unit/UT-LIVE-001/` | 2026-08-15 |
| UT-LIVE-002 | UT-LIVE | Validate NXR-2002 timeout sets `UNKNOWN_COMPLETION`, blocks replay until reconciliation/idempotency authorization, and after automatic exhaustion retains the child unresolved/evidenced while existing Task `Failed` plus Execution `FAILED` effects apply; no human escalation, Tool execution, automatic replay, or false child success/failure occurs | Tool + Recovery | Planned | `evidence/unit/UT-LIVE-002/` | 2026-08-15 |
| UT-LIVE-003 | UT-LIVE | Validate RetryPending direct start rejects before backoff elapsed or scheduler authorization | Task Lifecycle | Planned | `evidence/unit/UT-LIVE-003/` | 2026-08-15 |
| UT-LIVE-004 | UT-LIVE | Validate Agent Completing finalization guard commits Completed only after required persistence and resource release | Agent Lifecycle | Planned | `evidence/unit/UT-LIVE-004/` | 2026-08-15 |
| UT-LIVE-005 | UT-LIVE | Validate failed/cancelled stream, denied Tool, missing draft, and failed completion gate cannot return success | Agent Runtime | Planned | `evidence/unit/UT-LIVE-005/` | 2026-08-15 |
