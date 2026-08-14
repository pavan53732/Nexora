# Unit Test Case Inventory — Nexora

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
| UT-REASON-001 | UT-REASON | Resolve deterministic ReasoningPolicy for all effort levels | Reasoning | Planned | `evidence/unit/UT-REASON-001/` | 2026-08-06 |
| UT-REASON-002 | UT-REASON | Enforce technical call/token/tool/repair/time/device-resource safety ceilings and verify cost/credit telemetry cannot block a technically valid progressing run | Reasoning | Planned | `evidence/unit/UT-REASON-002/` | 2026-08-06 |
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
