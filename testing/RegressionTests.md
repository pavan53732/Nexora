# Regression Tests

## Scope

Regression tests guard against contract drift and previously fixed failures.

## Suite IDs

- `RT-CONTRACT-*` — contract sample regression
- `RT-PLUGIN-*` — plugin compatibility regression
- `RT-PROVIDER-*` — provider compatibility regression
- `RT-MIG-*` — schema and migration regression

## Framework Stack

- reproducible fixture harness
- golden contract samples
- compatibility comparison tooling

## Regression Test Database

The regression corpus SHOULD include canonical request/response/event samples for Agent, Tool, Provider, Plugin, Runtime, and Memory paths.

## Data Migration Testing

Schema or manifest changes must retain backward-compatible interpretation where required.

## Plugin API Backward Compatibility

Plugin compatibility testing SHOULD include activation rollback and exported capability compatibility checks.

## Run Schedule

Run on release candidates and on any contract-affecting change.

## Controlled Execution Escalation Compatibility

`RT-ESC-001` MUST protect the static agent capability matrix: unsupported Terminal or Background requests are denied or delegated and cannot silently acquire capability.

`RT-ESC-002` MUST protect task-scoped grant binding to workspace, task, agent, and execution lineage; grants cannot transfer, persist as agent overrides, or mutate the matrix.

`RT-ESC-003` MUST protect the requirement that Terminal and Background escalation still passes existing permission, approval, classifier, sandbox, resource, deadline, notification, checkpoint, and cancellation gates.

`RT-ESC-004` MUST protect expiry and revocation behavior: active descendants are cancelled, recoverable state is checkpointed, deadline and failure ledgers are not reset, and final outcomes are not silently marked successful.

`RT-ESC-005` MUST protect audit and correlated trace records for request, decision, approval, delegation, use, expiry/revocation, cancellation, and final disposition.

All escalation regression cases are planned until implementation and executed evidence exist.

## Typed Inference Compatibility

`RT-STREAM-001..002` and `RT-REASON-001` protect adapter event normalization,
non-stream fallback adaptation, and reasoning-policy/summary contract compatibility.

`RT-MODEL-001..002` MUST protect model-catalog snapshot identity, capability negotiation,
model deprecation handling, and provider-contract compatibility without mutating in-flight
route plans. `RT-REASON-002` MUST protect provider-native reasoning continuation privacy
and incompatible-failover rejection. `RT-TOOLDISC-001` MUST protect bounded discovery,
canonical Tool identity, stale-descriptor fail-closed behavior, and MCP tool/resource/prompt
primitive separation.

`RT-LIVE-001` MUST protect the explicit ProviderStream `STALLED → RECONNECTING` failover guard and stalled-failover budget.

`RT-LIVE-002` MUST protect NXR-2002 unknown-completion reconciliation and prohibit generic timeout replay without operation-level authorization.

`RT-LIVE-003` MUST protect RetryPending backoff enforcement so direct start cannot bypass the scheduler guard.

`RT-LIVE-004` MUST protect the Agent `Completing → Completed` finalize transition and reject completion before required persistence/resource-release guards.

`RT-LIVE-005` MUST protect non-success routing for stream failure/cancellation, denied Tool calls, missing committed drafts, and unsatisfied completion gates.

Task dependency-cycle handling, Task approval denial/expiry, Agent failure retry identity, provider rate-limit wait bounds, and delegation depth remain OPEN/DEFERRED owner boundaries until explicitly selected.
