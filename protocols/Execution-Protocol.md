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
