# Test Evidence Conventions — Nexora

## Purpose

This document defines how test evidence should be referenced from the test inventory and traceability artifacts.

## Evidence Path Convention

Evidence SHOULD be stored or referenced using a stable logical pattern:

`evidence/<suite>/<case-id>/<yyyy-mm-dd>/<artifact>`

Examples:

- `evidence/unit/UT-CONTRACT-002/2026-08-04/report.md`
- `evidence/integration/IT-CONTRACT-001/2026-08-04/log.txt`
- `evidence/security/SEC-SBX-001/2026-08-04/findings.md`

## Result Convention

Test case inventories SHOULD eventually track one of:

- `Planned`
- `In Progress`
- `Passed`
- `Failed`
- `Blocked`
- `Obsolete`

## Minimum Evidence Metadata

Each evidence record SHOULD capture:

- case identifier
- execution date
- executor or system owner
- environment or fixture description
- result status
- artifact location
- notable findings or deviations

## Common Verification Matrix and Evidence Envelope (ADR-0010)

All existing unit, integration, end-to-end, performance, regression, security, lifecycle, streaming, context, liveness, sandbox, Android device/emulator, and recovery inventories use the same evidence-state distinction:

| Evidence state | Meaning |
|---|---|
| `CANONICAL REQUIREMENT` | An authoritative documented contract with an owner and source reference. |
| `IMPLEMENTED` | Source implementation exists and is attributable to that contract. |
| `TEST DEFINED` | A suite, case, fixture contract, or acceptance procedure exists. |
| `TESTED` | The test was executed and produced a result. |
| `EXECUTED EVIDENCE` | The executed result is retained in reproducible form with the required metadata and artifact reference. |

A planned case or evidence path is `TEST DEFINED`; it is not `TESTED` and does not constitute `EXECUTED EVIDENCE`. A test result without retained reproducible artifacts is `TESTED` but not `EXECUTED EVIDENCE`. Documentation MUST NOT promote any state without the corresponding source or execution artifact.

The common evidence envelope SHOULD capture, at minimum:

- suite and case ID, canonical owner, source revision, and fixture/control revision;
- execution date/time, executor or system owner, environment, Android device/emulator and OS where applicable;
- deterministic controls in force, including clock/deadline, seed/jitter, provider/stream, resource, process/device, permission, storage/lock, and scheduler inputs where applicable;
- existing `workspaceId`, `taskId`, `executionId`, `workflowId`, `agentId`, `toolId`, `streamId`, `correlationId`, checkpoint/version, and artifact references where applicable;
- expected owner state, observed result/transition, terminal disposition, duplicate-side-effect outcome, and notable findings/deviations;
- for Android environment cases, observed ABI/asset, mount, storage/quota, integrity, permission, battery, network, scheduling, checkpointability, and resource classifications, each marked verified, failed, unavailable, or unknown;
- for recovery-projection cases, the source identities, checkpoint/version lineage, heartbeat/deadline/budget observations, blocker/recovery candidate, evidence references, final disposition, and explicit confirmation that no adoption, reparenting, replay, budget reset, permission escalation, lifecycle mutation, or autonomous side effect came from the projection;
- result status from the existing `Planned`, `In Progress`, `Passed`, `Failed`, `Blocked`, or `Obsolete` vocabulary; and
- stable artifact location using `evidence/<suite>/<case-id>/<yyyy-mm-dd>/<artifact>`.

The matrix is a projection across existing inventories, not a new test authority. Applicable suite owners determine execution and release-gate coverage: `testing/UnitTests.md`, `testing/IntegrationTests.md`, `testing/E2ETests.md`, `testing/PerformanceTests.md`, `testing/RegressionTests.md`, `testing/SecurityTests.md`, and their `testing/cases/` inventories. Fault-injection scenarios are coverage categories selected by the affected contract and release gate, not a single milestone.

## Deterministic Test Controls (ADR-0010)

Test fixtures MAY control clock/deadline time, seeded jitter/randomness, provider/stream outcomes, resource conditions, process/device events, permission outcomes, storage/locks, scheduler order, and test identifiers only within the test boundary. Controls MUST be explicit, scoped, recorded in the evidence envelope, and unavailable to normal production execution.

Production authority means any capability that can change a production Task, Execution, Workflow, Tool, Permission, Context, lifecycle, deadline, retry budget, side effect, audit record, recovery outcome, or user-visible completion disposition. Test controls MUST NOT possess production authority, bypass PermissionModel/SandboxPolicy/audit/lifecycle checks, fabricate success, reset budgets, or resolve `UNKNOWN_COMPLETION`.

Repeated runs with fixed controls MUST be reproducible within the declared environment. Known-good and known-failure fixtures MUST preserve the owning state-machine transition, deadline, idempotency, audit, evidence, and user-visible disposition. The presence of a case or fixture remains planned documentation until it is executed and its reproducible result is retained.
