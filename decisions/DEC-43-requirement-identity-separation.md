# DEC-43 — Non-Functional Requirement Identity Separation

- **Status:** Accepted
- **Date:** 2026-08-16
- **Deciders:** Architecture Owner
- **Related:** `requirements/NFR.md`, `docs/REQUIREMENT_COVERAGE_LEDGER.md`, `docs/TRACEABILITY.md`, `NFR-PERF-006`, `NFR-REL-004`, `NFR-CI-006`, `NFR-CI-007`

## Context

The requirements authority contained two duplicate identifiers with distinct meanings. `NFR-PERF-006` was used once for active-agent battery impact and again for minimum-sufficient execution-mode selection. `NFR-REL-004` was used once for ACID data persistence and again for bounded-progress controls in iterative reasoning and execution loops. A single requirement identifier cannot provide one authoritative requirement text, owner, validation mapping, and evidence path for two materially distinct contracts.

The first definitions are established within the existing Performance and Reliability sections. The later definitions are part of the existing Context Integrity and Bounded Execution section and already have compatible canonical owners and planned validation projections. The correction must preserve every requirement meaning while removing identity collision.

## Decision

The original section meanings remain unchanged:

- `NFR-PERF-006` remains the active-agent battery-impact requirement with its existing target and measurement.
- `NFR-REL-004` remains the ACID data-persistence requirement with its existing strategy.

The distinct Context Integrity meanings receive the following new identities:

- `NFR-CI-006` owns minimum-sufficient execution-mode selection across `FAST`, `NORMAL`, `DEEP`, `VERIFY`, and `RECOVER`. Its canonical owner is the Agent Runtime, with Provider and Context projections. Planned validation uses the existing `UT-REASON-001` and `E2E-RN-001` cases.
- `NFR-CI-007` owns bounded-progress controls for iterative reasoning and execution loops, including explicit retry, step, and time limits. Its canonical owner is the Agent Runtime, with Autonomy Stability, Execution Lifecycle, and Runtime API projections. Planned validation uses the existing `UT-AS-010` case.

No requirement text is deleted, merged, weakened, or silently reinterpreted. No NXR error code, lifecycle state, protocol primitive, API operation, schema object, permission scope, or implementation mechanism is created by this decision.

## Preserved Invariants

The Agent Runtime remains the canonical owner of single-agent mode selection, progress evaluation, anti-loop controls, bounded repair, escalation, and completion gating. Provider and Context documents project those semantics without acquiring loop ownership.

The Runtime and Task/Execution lifecycle authorities retain their existing state sets and transitions. Bounded-progress exhaustion continues through the existing recovery, escalation, incomplete, blocked, failed, or terminal paths; no new lifecycle state is introduced.

The no-internal-credit/cost-gating decision remains unchanged. Technical token, call, time, device, provider, resource, and liveness ceilings remain enforceable, while financial cost telemetry remains observational and non-blocking when genuine progress continues.

## Required Projections

The canonical requirement document, coverage ledger, curated traceability matrix, FR/NFR mapping, Runtime API projection, Agent Runtime projection, and completeness inventory must use the separated identities consistently. Historical decision and changelog records remain unchanged and are interpreted as historical where they describe the former collision.

All validation references remain planned until implementation and evidence exist. Documentation validation must confirm 177 unique FR/NFR identifiers, no duplicate requirement identity, complete ledger parity, and consistent dependent references.

## Acceptance Evidence

The documentation baseline is consistent when:

1. `requirements/NFR.md` contains one definition for each of `NFR-PERF-006`, `NFR-REL-004`, `NFR-CI-006`, and `NFR-CI-007`.
2. `docs/REQUIREMENT_COVERAGE_LEDGER.md` contains one mapped row for each identifier.
3. `docs/TRACEABILITY.md` and `docs/FR_NFR_MAPPING.md` map each meaning to its canonical owner and existing planned validation cases.
4. Repository-wide searches find no remaining statement that `NFR-PERF-006` or `NFR-REL-004` has two meanings or remains an identity collision.
5. No source implementation, executed test evidence, or unsupported architecture is claimed.
