> **Status: DERIVED** for Execution message contract.
> This document defines protocol messages for Execution. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Execution.
> Referenced by: models, APIs, SDKs, and tests.


# Execution Protocol — Nexora

> Communication contract for task execution lifecycle.

## States

```
PENDING → PLANNING → EXECUTING → COMPLETED
                      ↘ FAILED
                      ↘ CANCELLED
                      ↘ BLOCKED → EXECUTING (after approval)
```

## Checkpointing

Every N iterations (configurable, default 5), the runtime saves a checkpoint:
- Current plan and step index
- Memory snapshot
- Token usage so far
- Timestamp

On restart, the runtime loads the latest checkpoint and resumes.

## Background Execution

Tasks run in an Android `ForegroundService` with a persistent notification showing task ID and status.


## Cross-Layer Contract Rules

Protocol messages MUST map to the normative operation contract of the corresponding API. A message MUST preserve correlation ID, operation ID, lifecycle effect, transition version when applicable, and the canonical error envelope fields defined in [../errors/ERROR_CODES.md](../errors/ERROR_CODES.md).

A protocol consumer MUST treat events as at-least-once, deduplicate by entity and transition version, and never infer success from transport completion alone. Stream and cancellation messages MUST include an explicit terminal outcome.

## Canonical Error Mapping

The following mapping is normative. Adapters MUST preserve these codes and the canonical error-envelope fields; message text MUST NOT be used as a compatibility key.

| Operation | Canonical `NXR-*` codes |
|---|---|
| Task execution | NXR-1005, NXR-3004, NXR-3010, NXR-4002, NXR-1003 |
| Checkpoint save/restore | NXR-1003, NXR-1004, NXR-3009 |
| Cancellation | NXR-3010 |

See [ERROR_CODES.md](../errors/ERROR_CODES.md) for identity, retryability, idempotency, lifecycle effect, recovery owner, and redaction requirements.
