# Integration Tests

## Scope

Integration tests validate subsystem interactions and cross-layer contract preservation.

## Framework Stack

- Kotlin integration test framework
- emulator/device harness where needed
- service doubles for providers and plugins

## Test Environment

Integration environments MUST exercise storage, eventing, and orchestration layers together.

## Key Scenarios

- agent starts task and emits durable lifecycle events
- tool invocation flows through permission and sandbox checks
- provider streaming returns ordered terminal semantics
- plugin activation registers capabilities transactionally
- runtime replay or retry preserves correlation and durable versions

## Naming Convention

Names SHOULD reflect subsystem boundaries and requirement or contract concerns.

## Coverage Target

Cross-layer contract-sensitive paths are mandatory.

## CI Policy

Contract-affecting documentation changes SHOULD be mirrored by integration evidence updates.

## Canonical Contract Evidence

Integration suites SHOULD explicitly validate:

- `correlationId` continuity across subsystem boundaries
- idempotent retry behavior for keyed operations
- terminal outcome semantics for streaming and cancellation
- canonical error-envelope preservation across adapters
- lifecycle event ordering after durable commit
- event deduplication and replay behavior
