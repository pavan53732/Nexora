# Execution Protocol — Nexora

> Communication contract for task execution lifecycle.

## States

```
PENDING → planning → executing → COMPLETED
                      ↘ FAILED
                      ↘ CANCELLED
                      ↘ BLOCKED → executing (after approval)
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
