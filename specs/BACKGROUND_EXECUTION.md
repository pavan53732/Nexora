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

## Proactive Android Resource Negotiation Protocol

Nexora implements a **Proactive Android Resource Negotiation Protocol** to maintain background execution resilience against aggressive OS power management (Doze mode, OEM battery savers, thermal throttling):

1. **Expedited Job Promotion:** High-priority background tasks (`critical` / `high`) automatically request Android's expedited WorkManager job status and foreground service promotion to minimize OS scheduling latency.
2. **Thermal & Battery Telemetry Feedback Loop:** Device telemetry (thermal throttling states, battery percentage, low-power mode) is fed directly into the Agent Runtime reasoning loop. When thermal stress or critical battery levels are detected, the runtime automatically invokes an **Emergency Checkpoint**, reduces active polling, or shifts execution mode from `DEEP`/`NORMAL` to `FAST` until system vitals recover.
3. **Pre-Termination Hook:** The runtime registers an application lifecycle process-death receiver that intercepts OS termination signals and executes a final, atomic SQLite commit of all in-flight reasoning, task checkpoints, and failure ledgers before process destruction.

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
  `enqueue()`. The dependency graph is validated as acyclic before queueing. A failed
  dependency propagates terminal failure to dependent tasks instead of leaving them
  indefinitely blocked.
- **Backoff & retry** — retryable failures enter `RetryPending` with exponential
  backoff (NFR-REL-003); retried tasks rejoin the queue (FR-T007).
- **Bulk operations** — cancel, retry, reassign in bulk (FR-T009).
- **Cancellation** — any queued or running task can be cancelled (FR-T008, FR-A012);
  cancellation preserves partial results.
- **Multi-agent queue** — agents share the workspace task queue for delegation and
  handoff ([MULTI_AGENT_SYSTEM](../architecture/MULTI_AGENT_SYSTEM.md)).
- **Bounded waiting** — each task has an effective deadline inherited by dependency
  waits, approval waits, clarification waits, delegated children, and provider
  `Retry-After` waits.   `Pending`, `Blocked`, and `BlockedAwaitingInput` expire to
  `Failed` when that deadline is reached, using `NXR-1016` under DEC-33. Invalid
  dependency references or cycles are rejected with `NXR-1014`; terminally failed
  dependencies propagate `NXR-1015` to dependent Tasks. Approval denial uses
  `NXR-2003` / `USER_DENIED` and transitions `WaitingApproval` to `Failed`; approval
  expiry uses `NXR-2003` / `POLICY_DENIAL`. These outcomes do not silently resume,
  renew the deadline, or remain pending.


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
- **ANR safeguard:** if the Android main thread is blocked beyond the platform ANR
  threshold (6 s foreground / 10 s background per Android API 34+), `AgentExecutionService`
  MUST emit a `TASK_SUSPENDED` event, transactionally commit a checkpoint via `saveCheckpoint`,
  and release the main dispatcher — the foreground coroutine holds a CPU wake lock but must
  never block the main thread. Agents resume from the checkpoint on service restart
  (NFR-REL-002, ADR-0009 Decision #7).
- On app kill or device restart, `BootReceiver` checks for incomplete executions,
  restarts `AgentExecutionService`, and agents **resume from their last checkpoint**
  with 100% state fidelity (NFR-REL-002, FR-A011).
- Checkpoint resume retains the same `executionId` and `correlationId`; `version`
  increments for every committed checkpoint/resume transition (see
  [../architecture/RUNTIME.md](../architecture/RUNTIME.md) §ExecutionStatus Lifecycle).
- A terminal Execution (`FAILED`, `CANCELLED`, `COMPLETED`) is never mutated back to
  `RUNNING`. Explicit retry after a terminal state creates a new `executionId`
  with `priorExecutionId` referencing the terminal predecessor.
- WorkManager handoff and BootReceiver resume are checkpoint resumes, not retries.
- Cancellation and failure both preserve partial results and checkpoints for
  inspection or manual retry.
- Checkpoints are stored per workspace (`sandbox/workspaces/{id}/tasks/`) with WAL
  journaling for crash-safe writes (NFR-REL-001).

> **DEC-7:** BootReceiver does **not** reconstruct RetryPending state or restore its previous deadline. RetryPending is ephemeral and is lost on process death. BootReceiver is the startup trigger; eligible durable R4 evidence is reconciled through the separate process-death recovery responsibility. That recovery returns the Task to `Queued` and does not resume a checkpoint; checkpoint recovery remains the separate path described above. See [DEC-7](../decisions/DEC-7-retry-attempt-state.md) §DEC-7.7–DEC-7.12.

### Android trigger and reconciliation boundary

Process death, app termination, reboot, OEM termination, Doze or App Standby deferral, battery degradation, and force-stop are platform/runtime triggers or conditions; they are not additional Task or Execution lifecycle states. A trigger or condition MUST NOT by itself be interpreted as successful completion, cancellation, failure, or permission to replay an uncertain side effect. The durable Task/Execution state, checkpoint identity, effective deadline, and idempotency rules remain governed by their existing canonical authorities. When a later eligible runtime start or reconciliation path is available, it MUST inspect that durable state and apply the existing resume, queue, cancellation, failure, or retry rules; it MUST NOT renew a deadline, create a new lifecycle state, or silently replay an unresolved operation. This clarification is a recovery and validation boundary, not a new Android implementation contract.

## 4. Notifications

| Notification | When | Channel |
|--------------|------|---------|
| Foreground running | Agent task active in background | `agent_running` (persistent) |
| Progress % | Periodic progress updates (see §5) | `agent_progress` |
| Completed | Task finished successfully | `agent_done` |
| Failed | Task failed (with retry action) | `agent_error` |
| Throttle warning | Battery/Doze throttling engaged | `agent_running` |
| Approval requested | Human approval gate opened | `agent_approval` |
| Approval denied / deadline failure | Approval denied or bounded wait expired | `agent_error` |

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

   #### Preemptive Handoff Protocol
   To prevent Android 15 from forcefully killing the `AgentExecutionService` after its 6-hour runtime cap (which would abort the agent mid-task and risk database corruption), Nexora implements a preemptive **Handoff Protocol** managed by the `BackgroundExecutionWatchdog`:
   * **Watchdog Timer**: The `BackgroundExecutionWatchdog` tracks the exact elapsed active time of the `AgentExecutionService`.
   * **Preemptive Suspension (5.5h mark)**: At exactly 5 hours and 30 minutes of continuous runtime, the watchdog triggers a suspension signal.
   * **Graceful Checkpoint**: The active `AgentLoop` intercepts this signal, completes its current step iteration (planning, tool call, or reasoning pass), and transactionally saves a complete, integrity-verified execution checkpoint.
   * **Service Teardown**: The watchdog stops `AgentExecutionService` cleanly, releasing its CPU wake locks and removing its persistent notification.
   * **WorkManager Handoff**: The watchdog immediately schedules a `OneTimeWorkRequest` via `WorkManager` with the constraints: `NetworkType.CONNECTED` and `BatteryNotLow`. It passes the `executionId` and `correlationId` in the input data.
   * **Task Resumption**: The WorkManager worker loads the checkpoint and resumes execution in a chunked background task, ensuring the agent loop continues without system-enforced interruption or crash events.

3. **Doze / App Standby** — WorkManager defers non-expedited work; expedited jobs are
   used only for genuinely user-visible time-sensitive work; the foreground service
   holds a CPU wake lock only while actively executing (within Android's limits).
4. **Battery** — target NFR-PERF-006 (< 10 % drain/hour active); low-battery throttle
   reduces checkpoint frequency and pauses non-essential work (LIFECYCLES §7).
5. **Boot** — `BootReceiver` restarts incomplete executions after reboot (LIFECYCLES §7).
6. **Threat mitigation** — TM-021 (battery drain): foreground service + Doze awareness
   + JobScheduler for non-urgent tasks.

## 8. OEM Battery-Optimization & Auto-Start Onboarding (G1 — Added 2026-08-06)

> **Status:** CANONICAL specification for OEM battery-optimization handling (G1 — 2026-08-06).  
> **Verified research reference:** `aihackers.net` 2026-07-03 (`Kimi Claw` / `MiniMax Hailuo` pattern); `digitalapplied.com` 2026-07-03 (`OEM battery managers kill background processes regardless of Android API rules`).  
> **Principle:** OEM battery managers (`Xiaomi` HyperOS, `Huawei` EMUI, `OnePlus` OxygenOS, `Samsung` OneUI, `Oppo` ColorOS) enforce stricter kill rules than Android API contracts (`API 34+` `Doze`, `App Standby`, `dataSync` 6-hour cap). Nexora must detect denial and gracefully degrade — not assume Android rules alone guarantee background survival.

### 8.1 Detection of Battery-Optimization Denial

At startup (`AgentExecutionService` initialization) and before scheduling any `WorkRequest` (`FR-T011`), the runtime performs:

- **Battery optimization status check**: Query `PowerManager.isIgnoringBatteryOptimizations()` (or OEM-specific equivalent via reflection, where permitted) and read `device_battery` (`TOOL-297`) status.
- **Auto-start denial check**: Verify `BootReceiver` (`BootReceiver` — registered in manifest) has launch permission (`RECEIVE_BOOT_COMPLETED`); if denied (OEM-specific — `Xiaomi` auto-start, `Huawei` protected apps, `OnePlus` app autolaunch), log event (`FR-TL015` — audit trail) and trigger onboarding flow.
- **OEM-specific detection**: Check `Build.MANUFACTURER` (`Xiaomi`, `Huawei`, `OnePlus`, `Samsung`, `Oppo`, etc.) and read system settings (`Settings.Global` / `Secure` keys where accessible) to detect stricter kill policies.

**Evidence classification (per G1 / audit rules):**
- `VERIFIED`: `Kimi Claw` (`aihackers.net` 2026-07-03) and `MiniMax Hailuo` (`digitalapplied.com` 2026-07-03) document OEM battery manager kills; `specs/BACKGROUND_EXECUTION.md` (§7 Android Platform Rules) already notes `Doze` / `App Standby` / `Battery` throttle (`FR-T011` constraints: `Charging`, `BatteryNotLow`).
- `ENGINEERING INFERENCE`: OEM-specific reflection checks (`Build.MANUFACTURER`, system settings keys) — standard Android technique, no new architecture; detection results feed into existing event bus (`EventBus`) and scheduling module (`TaskScheduler`).
- `UNKNOWN` (explicitly noted): Exact reflection keys for every OEM version (`HyperOS` 2.0 vs `EMUI` 14) — documented as variable; the onboarding flow handles absence gracefully (defaults to `DENIED` if check fails).

### 8.2 Settings Surface — "Keep Nexora Running"

When detection indicates denial (`BatteryOptimizationStatus.DENIED` or `AutoStartDenied`), the app surfaces a user-facing settings flow (not an infrastructure screen — `ADR-0006`: infrastructure hidden; user sees it through notifications/activity feed):

- **Notification (`agent_approval`)**: Deep-link into `Workspace Settings` (`FR-W005` — workspace settings surface; `PermissionModel.md` — `ASK` default for `device:notifications`).
- **Settings entry (`Keep Nexora running`)**: Per-workspace toggle (`workspace.json` — `FR-W005`) that triggers the `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` intent (standard Android API 23+) and OEM-specific onboarding (`Xiaomi` auto-start settings, `Huawei` protected apps, `OnePlus` battery optimization exceptions).
- **User action**: User must explicitly navigate to OEM settings (guided by instructions) and grant the exception; Nexora does not auto-grant or bypass OEM restrictions.

**Permission model (`security/PermissionModel.md`):**
- `device:notifications` remains `ASK` (default); the settings surface does not change the permission model — it provides user education and navigation links (`FR-U011`: chat is single interaction surface; settings links surface through chat settings or workspace settings).
- No new scope added — `device:*` scopes (`device:notifications`, `device:camera`, `device:microphone`, etc.) remain unchanged; the settings flow is a user-guidance mechanism, not a new permission.

### 8.3 Graceful Degradation to WorkManager-Only (Reduced Autonomy)

If the user refuses battery optimization (or OEM denies auto-start and the user does not complete onboarding), the agent degrades gracefully — it does not crash or silently fail:

- **Foreground service disabled** (`AgentExecutionService` not started for new tasks; existing tasks complete gracefully with checkpoint at cancellation).
- **WorkManager-only mode** (`FR-T011`): All scheduling uses `PeriodicWorkRequest` (min 15 min interval) and `OneTimeWorkRequest` (deferred) — no expedited jobs; no real-time progress notifications (`agent_progress` disabled); no persistent `agent_running` notification (`agent_done`/`agent_error` only).
- **Checkpoint interval reduced** (`LIFECYCLES §7` — already reduced on low battery; now reduced unconditionally in degraded mode): from 30 s default to 10 s (faster recovery from `WorkManager` interruption).
- **Autonomy mode forced to `Manual`** (`FR-S016` — autonomy modes: `Manual` requires user approval for every action; `Assisted`/`Autopilot` disabled in degraded mode to prevent unexpected actions without real-time user awareness).
- **Task priority capped** (`FR-T003`/`FR-T012`): `CRITICAL` tasks still queued; `HIGH`/`MEDIUM`/`LOW` tasks deferred until user initiates (`Manual` mode — user must explicitly trigger task execution).
- **No browser preview updates** (`specs/BROWSER.md`): Live preview requires continuous agent loop; in `WorkManager`-only mode, preview updates occur only at task completion (`TaskProgress` event batch delivered at `agent_done`).
- **Audit log preserved** (`FR-TL015` — execution logging + audit trail): Degradation state is logged (`WorkManagerOnly` mode with timestamp, reason — `BatteryOptimizationDenied` or `AutoStartDenied`); no audit entry deleted.

**Reference mapping (existing IDs, no redesign):**
- `FR-T011` (scheduled execution — `WorkManager`-backed)
- `FR-AS-009` (fault-injection + degradation ladder — extended with `BatteryOptimizationDenied` and `AutoStartDenied` triggers)
- `FR-S016` (autonomy modes — `Manual` forced in degraded mode)
- `NFR-REL-002` (resume after restart — preserved; `WorkManager` resumes from last checkpoint)
- `NFR-REL-003` (exponential backoff — preserved for retry in degraded mode)
- `NFR-PERF-006` (battery drain < 10%/hour — `WorkManager`-only mode reduces drain further by removing foreground service wake lock)
- `FR-W005` (workspace settings — `Keep Nexora running` toggle added)
- `DL-021` (decision log entry above — documents the decision)

**Phase mapping:** Phase 2 (`specs/BACKGROUND_EXECUTION.md` — documentation update; no new architecture; no new module; `TaskScheduler` and `NotificationHelper` unchanged except for degradation-state checks).

---

## 8.4 Task-Scoped Background Capability Escalation

Background execution is not universal across agent types. The static agent capability matrix remains the dispatch boundary. When a non-background-capable agent needs a long-running operation, the coordinator MUST delegate to an eligible worker or request a task-scoped escalation through the existing permission and approval flow.

A background escalation is bound to one `workspaceId`, `taskId`, execution lineage, requesting `agentId`, purpose, affected operation class or canonical Tool IDs, effective deadline, resource/concurrency limits, notification policy, checkpoint requirement, cancellation rule, and revocation condition. It is not a new Task or Execution lifecycle state, does not mutate the static matrix, and does not grant unrestricted Terminal, network, device, plugin, MCP, browser, or sensitive-action access.

Before starting background work, the runtime MUST verify the existing background prerequisites: checkpointability, cancellation propagation, progress publication, notification behavior, resource limits, Android foreground-service/WorkManager eligibility, and applicable PermissionModel authorization decisions. If a prerequisite is unavailable, the request fails closed, is delegated, or remains in the existing user-clarification/approval path; it MUST NOT silently run in the background. No local classifier is invoked.

The grant expires at task completion, cancellation, effective deadline, explicit revocation, terminal failure, or Android/runtime degradation that prevents the declared contract. Expiry or revocation MUST checkpoint recoverable state, propagate cancellation to descendant provider and Tool operations, publish the existing activity/notification outcome, and preserve the existing incomplete, cancelled, failed, or degraded classification. It MUST NOT reset the deadline or create a fresh retry budget.

Every request, decision, approval, delegation, start, progress update, notification, expiry, revocation, cancellation, checkpoint, and final disposition MUST be included in the existing execution history, permission audit trail, and correlated runtime trace. The activity feed and notification surface MUST distinguish requested, delegated, approved, denied, active, degraded, expired, revoked, cancelled, and completed outcomes.

## Phase Mapping

- **Phase 1**: Task interface + queue contracts; `TaskScheduler` interface;
  `AgentExecutionService` skeleton; notification channels.
- **Phase 2**: Agent loop with checkpointing; foreground service execution;
  `BootReceiver`; scheduler (delayed/recurring via WorkManager); progress events.
- **Phase 6**: Scheduled workflows (`workflow_schedule`); chained work.
- **Phase 8**: Plugin-provided scheduled jobs and background extensions.


> **S4 — Terminal session restore in background execution:** Background tasks (`run_background`, `terminal_run_background`) reference terminal session state (`TerminalSession.status`, `restoreCheckpoint`, `sessionBufferReplay`) per `specs/TERMINAL.md` (§Restore Behavior). Under DEC-34, every autonomous background TerminalSession also carries the parent `taskId`, `executionId`, `workspaceId`, `correlationId`, and immutable effective deadline; parent cancellation, terminal state, or deadline expiry invokes the existing termination/checkpoint path, and missing or terminal parents are reconciled without a new state. Session restore aligns with `FR-AS-007` (idempotent recovery) + `NFR-REL-012` (exactly-once) + `FR-M013` (user preferences for persistence). A checkpoint is saved while the canonical session is `Detached` with `suspended=true`; restoration follows the existing `Detached → Attached → Running` path (`state-machines/TerminalSessionLifecycle.md`). See `docs/DECISION_LOG.md` DL-028 and DEC-34.
