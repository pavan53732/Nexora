# DEC-25 — No Internal Credit or Cost Gating

> **Status: CANONICAL DECISION**
> Nexora does not impose an internal credit balance, spending wallet, cost quota, or automatic cost-based execution stop on agents. Financial or provider-cost information may remain observable and may inform non-blocking presentation or preference behavior, but it must not become an execution gate.

## Problem

Existing documentation used cost terminology alongside technical token, call, repair, verifier, and wall-clock limits. FR-AS-003 also described cost exhaustion as a pause condition, while ADR-0009 and the Autonomy & Stability specification already stated that cost is not an autonomous-stop gate. The product owner has explicitly selected the no-internal-credit/cost-gating policy.

## Repository evidence

- `docs/adr/ADR-0009-Adaptive-Autonomy-And-Persistence.md` states that token and cost ceilings are out of scope as execution termination gates and that execution is governed by semantic progress failure, safety violations, or explicit user cancellation.
- `specs/AUTONOMY_STABILITY.md` states that cost is not an autonomous-stop gate and that execution continues while genuine progress is being made.
- `specs/CONTEXT_MANAGEMENT.md` and `requirements/FR.md` define technical token, provider-call, Tool-call, repair, verifier, wall-clock, context-window, and safety-boundary controls that are independent of financial cost.
- `requirements/FR.md` defines per-session token usage tracking and provider capability/cost/latency/privacy metadata, establishing observability and routing metadata without requiring an internal credit wallet.
- The product owner explicitly selected that Nexora agents must not be restricted by an internal credit or spending budget.

## Decision

Nexora has no internal credit balance, credit allowance, spending wallet, or financial cost quota that blocks, pauses, downgrades, refuses, or terminates an otherwise valid agent operation.

Cost and usage information MAY be collected, reconciled, displayed, audited, and used as a non-blocking routing preference or tie-breaker when separately configured. Cost information MUST NOT override capability, privacy, security, provider-health, reliability, lifecycle, or user-approval requirements. A provider-side rate limit, provider outage, unavailable model, authorization denial, safety violation, device/resource restriction, technical context limit, deadline, cancellation, or semantic-progress failure remains an independent control and is not an internal credit gate.

Technical limits remain mandatory. These include context-window and output-token limits, provider-call limits, Tool-call limits, repair-cycle limits, verifier-pass limits, wall-clock deadlines, cancellation budgets, Android lifecycle limits, device/resource-class safety ceilings, memory/disk limits, stream limits, and retry/reconciliation rules. These limits exist for correctness, safety, liveness, and device protection; they are not financial credit restrictions.

If an agent reaches a technical limit, the owning technical contract determines whether it summarizes, pauses, retries, reconciles, escalates, becomes incomplete, or terminates. If an agent reaches a reported cost or usage threshold, the runtime may notify or record the event, but it MUST NOT stop or block the agent solely for that reason while the technical and safety contracts remain satisfied.

## Explicit non-decisions

This decision does not remove provider-imposed rate limits, API quotas imposed by external providers, Android service limits, device memory or storage limits, context-window limits, output-token limits, Tool or repair ceilings, safety policy denials, permission gates, deadlines, cancellation, or semantic-progress loop protection.

This decision does not require unlimited provider capacity, unlimited model context, unlimited device resources, or successful execution after a provider or platform failure. It does not select a concrete billing display, accounting schema, cost-estimation algorithm, provider pricing source, or routing-preference UI.

## Compatibility

- ADR-0009 remains compatible: cost is not an execution termination gate.
- FR-P009 remains a usage-observability requirement, not a credit restriction.
- FR-P018 may retain provider cost metadata only as non-blocking routing information or preference.
- NFR-CI-005 remains unchanged: non-overridable provider, device, and resource-class safety ceilings remain mandatory.
- FR-AS-003 is reinterpreted through this decision so that technical exhaustion and cost notification are separate concepts; cost alone cannot trigger execution suspension or termination.
- Security, permission, sandbox, lifecycle, retry, checkpoint, Android background-execution, and unknown-completion contracts remain unchanged unless they independently refer to cost as an execution gate.

## Validation obligations

Future requirements, architecture, models, APIs, provider specifications, tests, risk records, and user-facing settings documents MUST distinguish financial-cost observability from technical execution limits. No active document may describe an internal cost or credit threshold as a mandatory stop, pause, downgrade, or refusal condition. Validation must include a negative case demonstrating that cost telemetry cannot block an otherwise progressing and technically valid execution, while technical safety and liveness ceilings remain enforced.

## Canonical ownership

This decision owns the product-level no-internal-credit/cost-gating rule. `requirements/FR.md` owns the requirement projection, `architecture/AGENT_RUNTIME.md` owns agent-loop enforcement, `architecture/PROVIDER_SYSTEM.md` owns provider route behavior, `specs/CONTEXT_MANAGEMENT.md` owns context and reasoning policy semantics, and the relevant security, Android, lifecycle, and testing documents retain their independent controls.

## References

- `docs/adr/ADR-0009-Adaptive-Autonomy-And-Persistence.md`
- `specs/AUTONOMY_STABILITY.md`
- `specs/CONTEXT_MANAGEMENT.md`
- `requirements/FR.md`
- `requirements/NFR.md`
- `architecture/AGENT_RUNTIME.md`
- `architecture/PROVIDER_SYSTEM.md`
- `docs/ROADMAP.md`
