# DEC-45 — No API Credit or Token-Budget Limits for the User

- **Status:** Accepted
- **Date:** 2026-08-17
- **Deciders:** Architecture Owner / Product Owner
- **Supersedes:** The active user-facing effect of any credit, spending, or
  token-budget control; DEC-25 remains immutable historical authority for the
  no-internal-credit/cost-gating policy at the agent level.

## Context

DEC-25 established that Nexora does not impose an internal credit balance,
spending wallet, cost quota, or automatic cost-based execution stop on agents.
Financial or provider-cost information may remain observable and may inform
non-blocking presentation or preference behavior, but it must not become an
execution gate.

The product owner has now confirmed that, because the user of the Nexora app
is the product owner, the app imposes **no API credit limits and no
token-budgeting limits** on that user. There is no internal credit balance,
spending wallet, cost quota, token ceiling, or automatic cost/token-based
execution stop, pause, downgrade, or refusal for the user. This decision
elevates and sharpens DEC-25's user-facing guarantee into a permanent
repository rule (Rule 9 of `AGENTS.md`) so that no future agent, builder, or
decision can reintroduce user-facing credit, spending, or token-budget
controls without an explicit, recorded override.

## Decision

Nexora imposes no API credit limits and no token-budgeting limits on the user.
Specifically:

- There is no internal credit balance, credit allowance, spending wallet,
  financial cost quota, token ceiling, or token budget that blocks, pauses,
  downgrades, refuses, or terminates an otherwise valid agent operation for the
  user.
- Cost and usage information MAY be collected, reconciled, displayed, audited,
  and used as a non-blocking routing preference or tie-breaker when separately
  configured. Cost information MUST NOT override capability, privacy, security,
  provider-health, reliability, lifecycle, or user-approval requirements.
- A provider-side rate limit, provider outage, unavailable model,
  authorization denial, safety violation, device/resource restriction,
  technical context limit, deadline, cancellation, or semantic-progress
  failure remains an independent control and is not an internal credit or
  token-budget gate.
- If an agent reaches a reported cost or usage threshold, the runtime may
  notify or record the event, but it MUST NOT stop or block the agent solely
  for that reason while the technical and safety contracts remain satisfied.

## Technical limits that remain mandatory

Technical limits are unaffected and remain mandatory. These include
context-window and output-token limits, provider-call limits, Tool-call
limits, repair-cycle limits, verifier-pass limits, wall-clock deadlines,
cancellation budgets, Android lifecycle limits, device/resource-class safety
ceilings, memory/disk limits, stream limits, and retry/reconciliation rules.
These limits exist for correctness, safety, liveness, and device protection;
they are not financial credit restrictions and must not be removed.

## Explicit non-decisions

This decision does not remove provider-imposed rate limits, API quotas imposed
by external providers, Android service limits, device memory or storage limits,
context-window limits, output-token limits, Tool or repair ceilings, safety
policy denials, permission gates, deadlines, cancellation, or semantic-progress
loop protection.

This decision does not require unlimited provider capacity, unlimited model
context, unlimited device resources, or successful execution after a provider
or platform failure. It does not select a concrete billing display, accounting
schema, cost-estimation algorithm, provider pricing source, or routing-
preference UI.

## Required Projections

Future requirements, architecture, models, APIs, provider specifications, tests,
risk records, and user-facing settings documents MUST distinguish financial-cost
observability from technical execution limits. No active document may describe an
internal cost or credit threshold, token ceiling, or token budget as a mandatory
stop, pause, downgrade, or refusal condition for the user. Validation must
include a negative case demonstrating that cost or token telemetry cannot block
an otherwise progressing and technically valid execution for the user, while
technical safety and liveness ceilings remain enforced.

## Canonical ownership

This decision owns the user-facing no-credit/no-token-budget rule at the
repository level. `AGENTS.md` (Rule 9) owns the agent-facing restatement.
`decisions/DEC-25-no-internal-credit-cost-gating.md` owns the agent-level
no-cost-gating policy and remains unchanged. `requirements/FR.md` owns the
requirement projection. `architecture/AGENT_RUNTIME.md` owns agent-loop
enforcement. `architecture/PROVIDER_SYSTEM.md` owns provider route behavior.
`specs/CONTEXT_MANAGEMENT.md` owns context and reasoning policy semantics.
`docs/PRODUCT_PRINCIPLES.md` owns the product-principle projection.
`docs/CANONICAL_SOURCES.md` owns the canonical-source map entry.
`docs/CHANGELOG.md` and `docs/DECISION_LOG.md` own the historical record.

## References

- `decisions/DEC-25-no-internal-credit-cost-gating.md`
- `AGENTS.md` Rule 9
- `docs/adr/ADR-0009-Adaptive-Autonomy-And-Persistence.md`
- `specs/AUTONOMY_STABILITY.md`
- `specs/CONTEXT_MANAGEMENT.md`
- `requirements/FR.md`
- `requirements/NFR.md`
- `architecture/AGENT_RUNTIME.md`
- `architecture/PROVIDER_SYSTEM.md`
- `docs/PRODUCT_PRINCIPLES.md`
- `docs/ROADMAP.md`
