# End-to-End Test Case Inventory — Nexora

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| E2E-CORE-001 | E2E-CORE | Validate primary user-visible task execution flow | Orchestration | Planned | `evidence/e2e/E2E-CORE-001/` | 2026-08-04 |
| E2E-ORCH-001 | E2E-ORCH | Validate cross-agent orchestration correlation continuity | Orchestration | Planned | `evidence/e2e/E2E-ORCH-001/` | 2026-08-04 |
| E2E-MA-001 | E2E-MA | Validate delegated multi-agent flow terminal roll-up | Orchestration | Planned | `evidence/e2e/E2E-MA-001/` | 2026-08-04 |
| E2E-GT-001 | E2E-GT | Validate Git grounding evidence retention | Grounding | Planned | `evidence/e2e/E2E-GT-001/` | 2026-08-04 |
| E2E-GND-001 | E2E-GND | Validate response grounding evidence trace | Grounding | Planned | `evidence/e2e/E2E-GND-001/` | 2026-08-04 |
| E2E-RN-001 | E2E-RN | Validate reasoning fallback and failure signaling | Reasoning | Planned | `evidence/e2e/E2E-RN-001/` | 2026-08-04 |
| E2E-STREAM-001 | E2E-STREAM | User sees provisional streaming then committed terminal response | Orchestration + UI | Planned | `evidence/e2e/E2E-STREAM-001/` | 2026-08-06 |
| E2E-STREAM-002 | E2E-STREAM | Network loss resumes or fails partial without silent splice | Orchestration + Provider | Planned | `evidence/e2e/E2E-STREAM-002/` | 2026-08-06 |
| E2E-STREAM-003 | E2E-STREAM | User cancellation stops provider and child Tool work | Orchestration | Planned | `evidence/e2e/E2E-STREAM-003/` | 2026-08-06 |
| E2E-REASON-001 | E2E-REASON | High-stakes task uses bounded critic/verifier and evidence summary | Reasoning + Evidence | Planned | `evidence/e2e/E2E-REASON-001/` | 2026-08-06 |
| E2E-REASON-002 | E2E-REASON | Private reasoning is absent from history/export | Security + Reasoning | Planned | `evidence/e2e/E2E-REASON-002/` | 2026-08-06 |
| E2E-CONTEXT-001 | E2E-CONTEXT | Crash/resume reconstructs reproducible ContextSnapshot | Context + Runtime | Planned | `evidence/e2e/E2E-CONTEXT-001/` | 2026-08-06 |
| E2E-REL-001 | E2E-REL | Process death and device restart resume the latest valid checkpoint without duplicate side effects | Android Runtime + Core Runtime | Planned | `evidence/e2e/E2E-REL-001/` | 2026-08-15 |
| E2E-REL-002 | E2E-REL | ANR suspension and service restart persist and restore the checkpoint without blocking the Android main thread | Android Runtime | Planned | `evidence/e2e/E2E-REL-002/` | 2026-08-15 |
| E2E-REL-003 | E2E-REL | Foreground-service time-limit handoff to WorkManager preserves execution and checkpoint lineage | Android Runtime | Planned | `evidence/e2e/E2E-REL-003/` | 2026-08-15 |
| E2E-REL-004 | E2E-REL | Doze, low battery, OEM auto-start denial, and WorkManager-only degradation expose status and force required Manual autonomy | Android Runtime | Planned | `evidence/e2e/E2E-REL-004/` | 2026-08-15 |
| E2E-REL-005 | E2E-REL | Provider stall, backpressure, duplicate/sequence-gap event, failover, and cancellation produce one terminal stream outcome with lineage | Provider + Runtime | Planned | `evidence/e2e/E2E-REL-005/` | 2026-08-15 |
| E2E-REL-006 | E2E-REL | Non-idempotent Tool timeout remains unknown completion until reconciliation and is never unsafely replayed | Tool + Runtime | Planned | `evidence/e2e/E2E-REL-006/` | 2026-08-15 |
| E2E-REL-007 | E2E-REL | Repeated identical and ineffective actions trigger semantic-progress escalation rather than an infinite treadmill | Agent Runtime | Planned | `evidence/e2e/E2E-REL-007/` | 2026-08-15 |
| E2E-REL-008 | E2E-REL | Delegation timeout, lock cycle, child abort, parent re-plan, and conflict abstention preserve provenance without deadlock | Multi-Agent Runtime | Planned | `evidence/e2e/E2E-REL-008/` | 2026-08-15 |
| E2E-REL-009 | E2E-REL | Missing, stale, contradictory, or low-confidence claim evidence blocks or qualifies the user-facing claim | Evidence Engine + Agent Runtime | Planned | `evidence/e2e/E2E-REL-009/` | 2026-08-15 |
| E2E-MODEL-001 | E2E-MODEL | Route selection records exact model descriptor, catalog snapshot, and adapter contract without in-flight mutation after catalog refresh | Provider + Runtime | Planned | `evidence/e2e/E2E-MODEL-001/` | 2026-08-15 |
| E2E-MODEL-002 | E2E-MODEL | Unsupported hard capability produces explicit incompatibility or policy-approved fallback without silent downgrade | Provider + Runtime | Planned | `evidence/e2e/E2E-MODEL-002/` | 2026-08-15 |
| E2E-MODEL-003 | E2E-MODEL | Provider-native reasoning continuation remains bound to compatible provider/model/adapter and is not replayed across incompatible failover | Provider + Reasoning | Planned | `evidence/e2e/E2E-MODEL-003/` | 2026-08-15 |
| E2E-TOOLDISC-001 | E2E-TOOLDISC | Large Tool registry produces bounded candidate projection with canonical IDs, examples, edge cases, boundaries, and permissions | Tool + Agent Runtime | Planned | `evidence/e2e/E2E-TOOLDISC-001/` | 2026-08-15 |
| E2E-TOOLDISC-002 | E2E-TOOLDISC | Stale, incompatible, unknown-scope, or unavailable Tool descriptor fails closed without invented Tool or silent substitution | Tool + Security | Planned | `evidence/e2e/E2E-TOOLDISC-002/` | 2026-08-15 |
| E2E-TOOLDISC-003 | E2E-TOOLDISC | Tool candidate set, selection, rejected alternatives, repair, authorization, and progress outcome are correlated in the trace | Tool + Observability | Planned | `evidence/e2e/E2E-TOOLDISC-003/` | 2026-08-15 |
| E2E-LONG-001 | E2E-LONG | Context compaction and crash resume reconstruct goal, phase, acceptance criteria, evidence gaps, delegated work, artifacts, and next safe action | Context + Runtime | Planned | `evidence/e2e/E2E-LONG-001/` | 2026-08-15 |
| E2E-LONG-002 | E2E-LONG | Delegated large output is preserved through permissioned artifact references with provenance rather than repeated free-form copying | Multi-Agent + Context | Planned | `evidence/e2e/E2E-LONG-002/` | 2026-08-15 |
| E2E-LONG-003 | E2E-LONG | Missing, stale, or incompatible authoritative task/artifact state pauses reconstruction instead of inferring continuity | Context + Recovery | Planned | `evidence/e2e/E2E-LONG-003/` | 2026-08-15 |
| E2E-MM-001 | E2E-MM | Negotiated multimodal, audio, screen, and computer-action events obey capability, permission, approval, cancellation, ordering, and terminal rules | Provider + Security + UI | Planned | `evidence/e2e/E2E-MM-001/` | 2026-08-15 |
| E2E-MM-002 | E2E-MM | Unsupported or unauthorized advanced event family fails closed and is not silently reduced to text or treated as successful side effect | Provider + Security | Planned | `evidence/e2e/E2E-MM-002/` | 2026-08-15 |
