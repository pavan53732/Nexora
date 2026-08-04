# Unit Tests

## Scope

Unit tests validate individual domain and contract behaviors in isolation.

## Framework Stack

- Kotlin test framework
- JUnit
- MockK

## Naming Convention

Use deterministic names that tie the unit under test to the requirement or contract concern.

## Directory Structure

Tests SHOULD mirror the module and contract boundaries they validate.

## Example Tests

- schema validation for tool input
- error envelope mapping
- retry/idempotency handling
- pagination cursor encoding/decoding
- event deduplication behavior

## Coverage Targets

Unit coverage SHOULD include both functional correctness and contract-envelope semantics.

## Git Grounding Unit Tests (FR-GT-001..006)

Grounding checks must validate source provenance handling.

## CI Policy

Unit test changes that alter contract behavior MUST update the relevant traceability entry.

## Response Grounding Unit Tests (FR-GND-001..006)

Grounding metadata must remain structurally valid.

## Reasoning Unit Tests (FR-RN-001..006)

Reasoning outputs should preserve evidence references and failure signaling.

## Evidence & Validation Engine Unit Tests (FR-EV-001..006)

Evidence selection and validation logic should be deterministic and inspectable.

## Multi-Agent Sub-Task Unit Tests (FR-MA-001..005)

Sub-task linkage should preserve correlation and delegation semantics.

## Agent Orchestration Unit Tests (FR-AG-001..004)

Agent orchestration tests should verify lifecycle and cancellation behavior.

## Canonical Contract Evidence

At minimum, unit suites for contract-sensitive modules SHOULD explicitly assert:

- `correlationId` preservation
- `idempotencyKey` behavior
- `resumeToken` opacity and propagation where supported
- canonical error-envelope field preservation
- pagination cursor behavior where list APIs exist
- event deduplication by `(entityId, version, transition)`
