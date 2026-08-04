> **Status: DERIVED** for Execution message contract.
> This document defines protocol messages for Runtime execution orchestration. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Runtime.
> Referenced by: models, APIs, testing, and orchestration implementations.

# Execution Protocol — Nexora

## States

Execution messages represent durable execution transitions such as `Pending`, `Queued`, `Running`, `Paused`, `Completed`, `Failed`, and `Cancelled`. Transition messages MUST carry committed `version` values and MUST NOT describe uncommitted lifecycle movement as durable fact.

## Checkpointing

Checkpoint creation, persistence, and replay MUST preserve `correlationId`, execution identity, checkpoint identity, and commit order. A checkpoint is externally visible only after the referenced state has been durably committed.

## Background Execution

Background job start, status, and cancellation messages are part of the execution protocol boundary. Cancellation is terminal only after durable cancellation commit and terminal event publication.

## Cross-Layer Contract Rules

Protocol messages MUST map to [docs/api/Runtime-API.md](../docs/api/Runtime-API.md). A message MUST preserve correlation ID, operation identity, lifecycle effect, transition version when applicable, and canonical error-envelope fields.

Consumers MUST treat events as at-least-once, deduplicate by `(entityId, version, transition)`, and never infer success from transport completion alone. Stream and cancellation messages MUST include explicit terminal outcome.

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| enqueueExecution | NXR-7001, NXR-7002, NXR-7004 |
| publishEvent / subscribe | NXR-7003, NXR-7005 |
| startBackgroundJob / cancelBackgroundJob | NXR-7006, NXR-7007 |
