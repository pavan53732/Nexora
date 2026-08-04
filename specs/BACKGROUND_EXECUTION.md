> **Status: CANONICAL** for Android background execution behavior.
> This document owns foreground services, WorkManager integration, checkpointing,
> crash recovery, notifications, and background task persistence. Other documents
> may reference this behavior but must not redefine it.
>
> Depends on: [../architecture/RUNTIME.md](../architecture/RUNTIME.md) (service composition).
> Referenced by: [../architecture/RUNTIME.md](../architecture/RUNTIME.md), [../docs/LIFECYCLES.md](../docs/LIFECYCLES.md), [../models/Execution.md](../models/Execution.md).

# Background Execution Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See also [../docs/LIFECYCLES.md](../docs/LIFECYCLES.md) · [../architecture/RUNTIME.md](../architecture/RUNTIME.md) · [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md) · [../docs/api/Runtime-API.md](../docs/api/Runtime-API.md) · [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md)

---

## Overview

Nexora **continues working even when the user leaves the current screen**. Long-running
agent tasks survive navigation, app minimize, and device restart. Background execution
is an internal runtime capability (ADR-0006): the user sees it through notifications,
progress updates, and the activity feed — never through infrastructure UI.

It is built on four Android pillars:

- **Foreground Service** (`AgentExecutionService`) for active agent runs
- **WorkManager** for scheduled and deferred work (DL-010)
- **Checkpointing** for crash recovery and resume
- **Notifications + Event Bus** for progress and completion signals

## 1. Task Queue

Tasks are the unit of background work. A per-agent execution queue manages them
(see [TaskLifecycle](../state-machines/TaskLifecycle.md)):

| State | Meaning |
|-------|---------|
| `Pending` | Submitted; awaiting dependency resolution before enqueue |
| `Queued` | Dependencies satisfied; placed in the agent's execution queue |
| `Running` | Agent actively executing |
| `RetryPending` | Retryable failure; queued for re-execution after backoff |
| `Blocked` | Waiting on an unresolved dependency or resource lock |

Rules:

- **Priority ordering** — queued tasks are ordered by priority (FR-T003): `critical` >
  `high` > `medium` > `low`. Higher-priority tasks jump the queue when enqueued
  (FR-T012).
- **Dependencies** — a task is enqueued only when all `depends-on` tasks completed
  (FR-T004); the `TaskScheduler` watches dependency completions and triggers
  `enqueue()`.
- **Backoff & retry** — retryable failures enter `RetryPending` with exponential
  backoff (NFR-REL-003); retried tasks rejoin the queue (FR-T007).
- **Bulk operations** — cancel, retry, reassign in bulk (FR-T009).
- **Cancellation** — any queued or running task can be cancelled (FR-T008, FR-A012);
  cancellation preserves partial results.
- **Multi-agent queue** — agents share the workspace task queue for delegation and
  handoff ([MULTI_AGENT_SYSTEM](../architecture/MULTI_AGENT_SYSTEM.md)).

## 2. Scheduled Jobs

The **Scheduler** module (`com.nexora.app.runtime.scheduler`) schedules deferred,
recurring, and background tasks (RUNTIME.md), backed by **WorkManager** (DL-010).

| Job type | Mechanism | Example |
|----------|-----------|---------|
| One-off delayed | `OneTimeWorkRequest` (or expedited for user-initiated) | "Run this task in 1 hour" |
| Recurring | `PeriodicWorkRequest` (min 15-minute interval) | Daily workspace cleanup, nightly memory pruning |
| Chained | `WorkContinuation` / `beginWith().then()` | Pipeline: fetch → process → store |
| Unique | `ExistingWorkPolicy` (REPLACE / KEEP / APPEND) | Prevent duplicate scheduled jobs (dedupe) |
| Triggered | Event-bus hook + `WorkRequest` | Run after provider becomes healthy |

**Constraints** (applied per job, not globally):

| Constraint | Purpose |
|------------|---------|
| Network connected | Jobs that need the network |
| Network unmetered | Large downloads / heavy sync |
| Charging | Battery-intensive jobs |
| Doze-aware | Default — WorkManager defers during Doze; expedited work for time-sensitive user-initiated jobs |

Scheduling is also exposed to agents as the `workflow_schedule` tool (TOOL-132) and
surfaces in the workflow engine (Phase 8 plugin scheduling).

## 3. Resumable Execution

- Agent state is **checkpointed periodically** during execution (default every 30 s,
  reduced on low battery — [LIFECYCLES §7](../docs/LIFECYCLES.md)).
- On app kill or device restart, `BootReceiver` checks for incomplete executions,
  restarts `AgentExecutionService`, and agents **resume from their last checkpoint**
  with 100% state fidelity (NFR-REL-002, FR-A011).
- Cancellation and failure both preserve partial results and checkpoints for
  inspection or manual retry.
- Checkpoints are stored per workspace (`sandbox/workspaces/{id}/tasks/`) with WAL
  journaling for crash-safe writes (NFR-REL-001).

## 4. Notifications

| Notification | When | Channel |
|--------------|------|---------|
| Foreground running | Agent task active in background | `agent_running` (persistent) |
| Progress % | Periodic progress updates (see §5) | `agent_progress` |
| Completed | Task finished successfully | `agent_done` |
| Failed | Task failed (with retry action) | `agent_error` |
| Throttle warning | Battery/Doze throttling engaged | `agent_running` |
| Approval requested | Human approval gate opened | `agent_approval` |

Rules:

- `device:notifications` permission scope (default `ASK`, [PermissionModel](../security/PermissionModel.md)).
- Foreground service notification is **non-dismissible** while the agent runs.
- Notifications link to the task in-app (deep link into the activity feed).
- All notification behavior is centralized in `NotificationHelper`
  ([MODULE_BOUNDARIES](../docs/MODULE_BOUNDARIES.md)).

## 5. Progress Updates

- The agent loop publishes **`TaskProgress`** events on the event bus at each
  iteration (AGENT_RUNTIME): status, step index, plan state, and token usage
  (FR-A010, FR-P009).
- The UI renders progress via `TaskCard` (progress indicator) and `ActivityCard`
  (inline progress events) in the chat activity feed ([ui/Components.md](../ui/Components.md)).
- Token usage is tracked per request, session, provider, and model
  ([SYSTEM_DESIGN → Observability](../docs/SYSTEM_DESIGN.md)).

## 6. Checkpoint Recovery

| Aspect | Rule |
|--------|------|
| Interval | 30 s default; reduced when battery low (LIFECYCLES §7) |
| Storage | Per-workspace `tasks/` directory; WAL journaling (NFR-REL-001) |
| Events | `CHECKPOINT_SAVED` execution events ([models/Execution.md](../models/Execution.md)) |
| Fidelity | 100% state fidelity on resume (NFR-REL-002) |
| Integrity | CRC/checksum verification on every persistent write (NFR-REL-008) |
| Errors | Sandbox/resource failures → `NXR-7xxx`; retryable → `RetryPending` |

## 7. Android Platform Rules (API 34+)

These are **hard platform constraints** for the target stack (minSdk 34):

1. **Foreground service types** — `AgentExecutionService` must declare a
   `foregroundServiceType` (e.g. `dataSync`) in the manifest (required from API 34).
2. **Android 15 (API 35) time limit** — `dataSync` foreground services are capped at
   **6 hours per 24 h**; agent runs longer than that must hand off to WorkManager
   (chunked execution with checkpoints) or a **user-initiated data transfer job**
   (API 30+, `USER_INITIATED` / expedited work) that the user explicitly starts.
3. **Doze / App Standby** — WorkManager defers non-expedited work; expedited jobs are
   used only for genuinely user-visible time-sensitive work; the foreground service
   holds a CPU wake lock only while actively executing (within Android's limits).
4. **Battery** — target NFR-PERF-006 (< 10 % drain/hour active); low-battery throttle
   reduces checkpoint frequency and pauses non-essential work (LIFECYCLES §7).
5. **Boot** — `BootReceiver` restarts incomplete executions after reboot (LIFECYCLES §7).
6. **Threat mitigation** — TM-021 (battery drain): foreground service + Doze awareness
   + JobScheduler for non-urgent tasks.

## Phase Mapping

- **Phase 1**: Task interface + queue contracts; `TaskScheduler` interface;
  `AgentExecutionService` skeleton; notification channels.
- **Phase 2**: Agent loop with checkpointing; foreground service execution;
  `BootReceiver`; scheduler (delayed/recurring via WorkManager); progress events.
- **Phase 6**: Scheduled workflows (`workflow_schedule`); chained work.
- **Phase 8**: Plugin-provided scheduled jobs and background extensions.
