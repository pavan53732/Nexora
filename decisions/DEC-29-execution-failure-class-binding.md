# DEC-29 — Execution-Failure Class Binding

## Status

**Accepted documentation decision.**

## Context

`specs/EXECUTION_LIFECYCLE.md` classified execution failures as transient, permanent, or escalation failures but left the binding to canonical error signals and lifecycle effects open. The repository already establishes the error catalog as authoritative for error identity and shared recovery metadata, `TaskLifecycle` as authoritative for Task states and retry transitions, `architecture/RUNTIME.md` and `models/Execution.md` as authoritative for ExecutionStatus, and the operation owner as authoritative for idempotency and retry conditions.

## Decision

The failure class is a classification overlay. It does not create a new error code, lifecycle state, owner, or protocol.

### 1. Error identity

The canonical error catalog and its public-operation mapping matrix remain authoritative for the concrete `NXR-` identity, category, retryability, idempotency, lifecycle effect, recovery owner, and redacted details. A failure class MUST NOT replace or reinterpret the canonical error code.

The catalog examples remain valid: provider connection/timeout/rate-limit/stream transport failures use their existing provider identities; Tool timeout and authorization/validation failures use their existing Tool identities; sandbox disk/memory/wall-clock failures use their existing Sandbox identities; and stream sequence-gap or missing-terminal failures use `NXR-4015`/`NXR-4017` as already defined. This is a reference to existing catalog authority, not a new exhaustive error mapping.

### 2. Transient failure

A transient classification permits retry only when the canonical error envelope and operation policy mark the operation retryable and the retry condition remains satisfied.

For a running Task, the legal retry projection is `Running → RetryPending` under `TaskLifecycle.fail(error)` when the error is retryable and the retry limit has not been reached. `RetryPending → Queued` occurs through the canonical retry transition after backoff. No new Task or Execution state is created by the classification.

Before a terminal Execution decision, a retryable operation does not force `ExecutionStatus.FAILED`. If the retry policy is exhausted or the error becomes non-retryable, the permanent or escalation binding applies.

### 3. Permanent failure

A permanent classification prohibits retry without an explicit strategy change or user intervention. The owning lifecycle commits its canonical terminal failure effect: `TaskLifecycle` uses `Running → Failed`, and `ExecutionStatus` uses `RUNNING → FAILED` through the Executor-owned lifecycle contract. A committed terminal Execution is never resumed under the same identity; an explicit retry/restart creates a new Execution with the existing retry lineage rules.

### 4. Escalation failure

An escalation classification indicates a systemic constraint, bounded-progress violation, retry storm, deadline exhaustion, or resource constraint that requires notification, incomplete termination, or a user clarification path.

Escalation does not create a new Task state. `TaskLifecycle.Running → BlockedAwaitingInput` is used only when the owning runtime explicitly invokes `requestEscalation(question)` for user clarification or a capability gap. If the operation terminates, the existing terminal failure effects apply: `Task Running → Failed` and `ExecutionStatus RUNNING → FAILED`. The error envelope and operation owner determine whether notification, clarification, cleanup, or a new operation is required.

### 5. Authority separation

The error catalog owns error identity and shared recovery metadata. The owning lifecycle owns legal state effects. The operation owner owns idempotency, retry conditions, and side-effect recovery. Protocols, APIs, and SDKs preserve the canonical envelope and MUST NOT infer lifecycle transitions from category or message text alone.

## Consequences

`specs/EXECUTION_LIFECYCLE.md` may treat the class-to-authority binding as resolved while concrete operation mappings continue to be governed by the canonical error matrix and owning lifecycle documents. No arbitrary error-to-state mapping is permitted.

This decision preserves the existing Task, Execution, Tool, Provider, Sandbox, Plugin, and stream lifecycle authorities. It does not alter existing error identities or existing DEC-* decisions.

## Planned validation

`UT-EXEC-001` and the applicable lifecycle/protocol regression cases MUST assert that retryability, idempotency, lifecycle effect, and recovery owner come from the canonical error envelope and operation policy; that retryable failures use only legal retry transitions; that terminal failure does not resume the same Execution; and that escalation does not create an undocumented state.

## Authority and dependencies

`errors/ERROR_CODES.md` owns error identity and shared recovery metadata.

`state-machines/TaskLifecycle.md` owns Task states and transitions.

`architecture/RUNTIME.md` and `models/Execution.md` own ExecutionStatus semantics.

The relevant Tool, Provider, Sandbox, Plugin, protocol, API, and operation-owner documents remain authoritative for their specific operations.

This decision does not modify any existing `DEC-*` record.
