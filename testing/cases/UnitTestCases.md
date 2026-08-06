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
| UT-REASON-002 | UT-REASON | Enforce call/token/tool/repair/time/cost budgets | Reasoning | Planned | `evidence/unit/UT-REASON-002/` | 2026-08-06 |
| UT-REASON-003 | UT-REASON | Redact ReasoningSummary and exclude private trace | Security + Reasoning | Planned | `evidence/unit/UT-REASON-003/` | 2026-08-06 |
| UT-CONTEXT-001 | UT-CONTEXT | Reproduce immutable ContextSnapshot from segment hashes | Context | Planned | `evidence/unit/UT-CONTEXT-001/` | 2026-08-06 |
| UT-CONTEXT-002 | UT-CONTEXT | Deduplicate retrieval while preserving source diversity | Context + Memory | Planned | `evidence/unit/UT-CONTEXT-002/` | 2026-08-06 |
| UT-ROUTE-001 | UT-ROUTE | Rank eligible providers by hard constraints then policy score | Provider Layer | Planned | `evidence/unit/UT-ROUTE-001/` | 2026-08-06 |
