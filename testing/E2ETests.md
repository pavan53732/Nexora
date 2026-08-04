# End-to-End Tests

## Scope

End-to-end tests validate user-visible workflows across the full stack.

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

Grounding journeys should preserve evidence provenance across user-visible flows.

## Response Grounding E2E Journeys (anti-hallucination)

Visible responses should remain tied to retrievable evidence paths.

## Reasoning E2E Journeys (think before answering)

Reasoning journeys should verify error and fallback behavior as well as success.

## Evidence & Validation E2E Journeys

Evidence selection should remain inspectable in user-facing workflows.

## Multi-Agent Sub-Task E2E Journeys

Delegated flows should preserve task linkage and terminal roll-up behavior.

## Agent Orchestration E2E Journeys

Orchestration flows should verify cross-agent correlation continuity.

## Canonical Contract Evidence

Critical E2E journeys SHOULD assert:

- correlation continuity across the full user-visible execution path
- explicit terminal outcomes for cancellations and streams
- stable retry behavior for idempotent operations
- absence of silent success inferred from transport closure
