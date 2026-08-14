# End-to-End Tests

## Scope

End-to-end tests validate user-visible workflows across the full stack.

## Suite IDs

- `E2E-CORE-*` — primary user-visible execution flows
- `E2E-GT-*` — Git grounding journeys
- `E2E-GND-*` — response grounding journeys
- `E2E-RN-*` — reasoning journeys
- `E2E-EV-*` — evidence journeys
- `E2E-MA-*` — multi-agent journeys
- `E2E-ORCH-*` — orchestration journeys

## Framework Stack

- device/emulator automation
- test orchestration harness
- provider/plugin doubles where isolation is required

## Test Device Matrix

Representative Android environments should be covered.

## Execution Policy

E2E suites should run for critical paths and before release gating.

## Flakiness Mitigation

Use deterministic fixtures and explicit readiness checks.

## Git Grounding E2E Journeys (anti-hallucination)

`E2E-GT-*` journeys should preserve evidence provenance across user-visible flows.

## Response Grounding E2E Journeys (anti-hallucination)

`E2E-GND-*` journeys should remain tied to retrievable evidence paths.

## Reasoning E2E Journeys (think before answering)

`E2E-RN-*` journeys should verify error and fallback behavior as well as success.

## Evidence & Validation E2E Journeys

`E2E-EV-*` journeys should keep evidence selection inspectable in user-facing workflows.

## Multi-Agent Sub-Task E2E Journeys

`E2E-MA-*` delegated flows should preserve task linkage and terminal roll-up behavior.

## Agent Orchestration E2E Journeys

`E2E-ORCH-*` orchestration flows should verify cross-agent correlation continuity.

## Canonical Contract Evidence

Critical E2E journeys SHOULD assert:

- correlation continuity across the full user-visible execution path
- explicit terminal outcomes for cancellations and streams
- stable retry behavior for idempotent operations
- absence of silent success inferred from transport closure

## Typed Inference User Journeys (ADR-0008)

- `E2E-STREAM-001..003` cover committed/provisional UI, reconnect/failure lineage, and cancellation.
- `E2E-REASON-001..002` cover bounded verification and reasoning-artifact privacy.
- `E2E-CONTEXT-001` covers reproducible context reconstruction after crash.

## Agent Reliability Fault-Injection Journeys

The following journeys are required for reliability evidence before release gating. Each journey MUST record execution identity, correlation identity, checkpoint version, task state, terminal disposition, user-visible notification state, and duplicate-side-effect outcome.

- `E2E-REL-001`: process death, device restart, and repeated restart resume from the latest valid checkpoint without duplicate side effects.
- `E2E-REL-002`: ANR suspension and service restart save and restore the execution checkpoint without blocking the Android main thread.
- `E2E-REL-003`: foreground-service time-limit handoff to WorkManager preserves execution lineage and resumes from checkpoint.
- `E2E-REL-004`: Doze, low battery, OEM auto-start denial, and WorkManager-only degradation produce explicit user-visible status and Manual autonomy where required.
- `E2E-REL-005`: provider first-byte/inter-token stall, backpressure, duplicate event, sequence gap, failover, and cancellation terminate with correct stream lineage and exactly one terminal outcome.
- `E2E-REL-006`: non-idempotent Tool timeout remains unknown completion until its declared reconciliation contract resolves it; no unsafe automatic replay occurs.
- `E2E-REL-007`: repeated identical and alternating ineffective actions trigger semantic progress escalation rather than an infinite treadmill.
- `E2E-REL-008`: multi-agent delegation timeout, lock cycle, child abort, parent re-plan, and conflicting-result abstention preserve provenance and do not deadlock.
- `E2E-REL-009`: claim-level evidence omission, stale evidence, contradictory evidence, and low confidence block or qualify the user-facing claim.

These journeys are planned evidence obligations. Their presence in this specification does not claim that the runtime implementation or device validation already exists.
