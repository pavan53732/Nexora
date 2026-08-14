> **Status: SUPPORTING** for AUTONOMY STABILITY focused behavior.
> This document explains focused behavior for AUTONOMY STABILITY. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# Autonomy & Stability Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See also [../specs/CONTEXT_MANAGEMENT.md](./CONTEXT_MANAGEMENT.md) · [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md) · [../docs/LIFECYCLES.md](../docs/LIFECYCLES.md) · [../security/SandboxPolicy.md](../security/SandboxPolicy.md)

---


> **DEC-7 (2026-08-11):** Retry lifecycle clarification: RetryPending retry preserves `executionId`; explicit retry after terminal state creates a new `executionId` with `priorExecutionId` linkage. RetryPending is EPHEMERAL. See [../decisions/DEC-7-retry-attempt-state.md](../decisions/DEC-7-retry-attempt-state.md).

## Overview

Two goals: **deeper autonomy** (agents recover, re-plan, learn, and earn trust on
their own) and **full stability** (no data loss, no double side-effects, no silent
stops, no blank crashes). Part A covers autonomy; Part B covers stability.

---

# Part A — Autonomy

## 1. Plan Repair (FR-AS-001)

When a step fails, the agent does not just retry the step — it **re-plans from the
failure point**:

```
Step N fails
   │
   ▼
Diagnose (error class, impacted artifacts)
   │
   ▼
Repair decision (bounded):
   a. Retry step (transient)          — existing RetryPending path
   b. Repair step (same plan, new approach) — fix loop (FR-EL-013)
   c. Re-plan: re-sequence remaining steps (dependencies invalidated)
   d. Re-delegate: hand the task to a better-suited agent (skill mismatch)
   e. Escalate to user (unresolvable, or budget exhausted)
```

- Re-planning is **bounded**: max 3 repair cycles per task, then escalation (FR-AS-003).
- Each repair cycle is recorded in execution history (`plan_repair` event) so the
  final report explains *what changed and why*.

## 2. Agent Heartbeat & Watchdog (FR-AS-002)

| Aspect | Rule |
|--------|------|
| **Heartbeat** | The agent loop publishes a `heartbeat` event every iteration (or every N seconds for long tool calls) |
| **Watchdog** | A runtime coroutine watches heartbeats; no heartbeat within timeout (default 120 s) → suspect hang |
| **Action** | Suspend the loop, capture stack/state, save checkpoint, restart from checkpoint (bounded restarts, default 2) |
| **Escalation** | If the loop hangs again after restarts → escalate to user with diagnostics |
| **Interaction** | Extends sandbox process watchdog (SANDBOX_DEPTH §3.4) to the **agent loop** itself |

## 3. Budget Escalation — Never Silent Stop (FR-AS-003)

| Budget | On exhaustion |
|--------|---------------|
| Tokens (per session) | Pause → notify user → offer: raise budget, switch provider, or continue with summarization (CONTEXT_MANAGEMENT §3) |
| Steps (per task) | Pause → notify → offer: continue with checkpoint, or mark incomplete |
| Wall-clock time | Same — never kill silently |
| Cost (per task) | **Not an autonomous-stop gate** (ADR-0009). Cost notifications remain informational only; execution continues until a semantic progress failure, a safety violation, or explicit user interruption. |

Every exhaustion path ends in a **user-visible state** (notification + task status),
never a silent stop. Cost is intentionally out of scope as a termination signal —
resource pressure is observable (PERFORMANCE_BUDGET.md) and the user may interrupt
at any time, but the agent never stops purely because a token or cost limit was
reached while genuine progress is still being made.

## 4. Closed-Loop Learning (FR-AS-004)

After each task, the agent runs a short learning pass:

```
Reflect (what worked / what failed / what was surprising)
   │
   ▼
Store lesson → memory_lessons (TOOL-409) — tagged, retrievable
   │
   ▼
Propose skill refinement:
   - adjust an existing skill's tool set, or
   - propose a new LEARNED skill (ADR-0007, FR-SK-002)
   │
   ▼
User or policy approves → skill updated/created
```

Lessons are also retrieved during planning (Context Builder pulls relevant lessons for
similar tasks), so the application literally gets smarter with use.

## 5. Trust Growth (FR-AS-005)

Autonomy expands with a **trust score** instead of jumping straight to autopilot:

| Input | Effect |
|-------|--------|
| Successful low-risk calls | + small increment |
| Successful milestone completions | + larger increment |
| Verified final results | + large increment |
| Failed steps, safety violations, denied approvals | − decrement; repeated → autonomy drops a mode (Autopilot → Assisted → Manual) |

- Trust is per agent + per workspace; resets are explicit (user can reset trust).
- Autonomy mode selection: `Manual / Assisted / Autopilot` (FR-S016) is *offered* by
  the trust score, *decided* by the user.

## 6. Verification Gates (FR-AS-006)

Milestones are **hard gates**, not soft checks:

- Each plan step declares validation criteria (FR-EL-008).
- The executor **blocks** the next step until the current step's criteria pass or the
  failure is classified (repair / escalate).
- The final gate re-checks the **acceptance criteria** (FR-EL-011) before the agent may
  report completion.
- Gate results are persisted with the checkpoint, so a resumed agent re-validates
  before continuing.

---

# Part B — Stability

## 7. Idempotency & Exactly-Once Recovery (FR-AS-007)

Resuming after a crash must never double-apply side effects.

| Aspect | Rule |
|--------|------|
| **Tool declaration** | Every tool declares `idempotent: true/false` in its definition (extends `Tool` interface) |
| **Idempotent tools** | Safe to re-run (reads, writes-by-content, upserts) — recovery replays them freely |
| **Non-idempotent tools** | (e.g. `http_post` with side effects, `terminal_run` with mutations) — recovery **does not replay**; effects are reconciled from tool history (FR-M011) instead |
| **Replay log** | A compact `execution_replay` log records completed tool calls (id + input hash + result); recovery replays only uncompleted calls |
| **Transactionality** | File/DB mutations use write-new + atomic swap; WAL for Room (NFR-REL-001) |

Outcome: after any crash/restart, the workspace state is identical to exactly-once
execution — no duplicate mutation, no lost progress, no stale result injection.

Recoverable interruptions before a terminal state resume the same `executionId` with
`version` incremented and `correlationId` stable. A terminal Execution is never
returned to `RUNNING`. Explicit retry after terminal status creates a new `executionId`
with `priorExecutionId` linking the terminal predecessor. Non-idempotent in-flight
calls are reconciled from durable history; idempotent incomplete calls may replay
safely under the replay policy (see [../architecture/RUNTIME.md](../architecture/RUNTIME.md) §ExecutionStatus Lifecycle).

## 8. Degradation Ladder (FR-AS-008)

Never a blank crash — degrade gracefully down the ladder, announcing each step:

```
1. Primary provider    → healthy (ProviderLifecycle)
2. Provider failover   → next profile (auto, health-based)
3. Local model         → Ollama / LM Studio / GGUF (offline-capable)
4. Offline mode        → read-only workspace access (NFR-REL-006)
5. Read-only + notify  → degrade features, never crash (NFR-REL-005)
```

Each descent is logged (`degradation_event`) and surfaced in the activity feed. The
ladder is per-workspace configurable (some workspaces may prefer "fail fast" for
critical tasks).

## 9. Timeout & Concurrency Discipline

- **Every** external call (provider, network, sandbox process) has a deadline; no
  unbounded waits.
- Timeouts are classified retryable/non-retryable (NFR-REL-003) and feed plan repair (§1).

### 9.2 Retry Policy (NFR-REL-003)

Transient failures (NFR-REL-003 retryable class) MUST retry with exponential
backoff + full jitter:

```
interval = base × 2^attempt × random(0.5…1.5)
```

**Attempt semantics:**
- Initial execution is NOT a retry attempt.
- `attempt=0` = first retry; `attempt=1` = second retry; `attempt=2` = third retry.
- `maxAttempts = 3` means exactly 3 retry iterations (1 initial execution + 3 retries = 4 total executions maximum).
- Total possible executions = 1 initial + 3 retries = 4.
- The retry attempt index is zero-based and corresponds to the retry iteration index.
- The existing `retries < max` TaskLifecycle guard is mathematically consistent with this contract: after the initial execution, `retries` counts `0, 1, 2` and stops at `3`, matching `attempt` values `0, 1, 2`.

- **base**: 1 s for provider calls, 5 s for sandbox process calls (FR-TL005)
- **attempts**: capped at 3 retries (attempt=0, attempt=1, attempt=2) per [NFR-REL-003](../requirements/NFR.md) (NFR-REL-003 row)
- **No max interval cap**: the retry interval policy does not impose a ceiling beyond the exponential jitter formula. Provider-stream liveness timers (`firstByteTimeout`, `interTokenTimeout`) are a separate, unconstrained timer domain and do not bound retry backoff delays.
- After all retries exhausted: route through plan repair (§1 item **b**) or task-scoped
  failure ledger `BLACKLISTED_UNTIL_TASK_END` (§9.5); never an unconditional retry.
- Non-retryable timeouts commit terminal `FAILED` with `latestError` and surface to
  the degradation ladder (§8) for visibility — no silent continuation.
- **Cancellation**: A task in `RetryPending` MAY cancel per TaskLifecycle `cancel()` semantics.
- **Determinism**: Retry jitter MUST be deterministic when seeded for reproducible testing.

## 9.5 Semantic Progress & Anti-Replay (new, mandated by ADR-0009)

**Acceptance-Criterion Progress Vector.** Semantic progress is evaluated against the
active task's declared acceptance criteria. Each criterion has monotonic status
`UNASSESSED`, `IN_PROGRESS`, `PASSED`, or `FAILED`, and the vector is checkpointed
with evidence references. Activity unrelated to an acceptance criterion does not by
itself reset the bounded-progress detector. The Agent Runtime remains the canonical
owner of this vector; this section mirrors its stability obligation.

**State-Delta Evaluation — the "Treadmill" Detector.** Syntactic loop detection
(n=2 identical action+argument repeat) is necessary but insufficient: an agent can
alternate between different-but-equally-ineffective tools and still make zero real
progress. Agent Runtime MUST additionally evaluate a **semantic `ProgressSignal`**
over each iteration, computed by the Context Builder from the `ContextSnapshot`
working-state lineage:

- Test-suite pass count delta (FR-EL-008 verification gates)
- Workspace file change delta (non-equivalence hash of changed paths)
- New evidence / artifact count delta (CONTEXT_MANAGEMENT §7)
- Error category shift (is the failure *different*, or just the same one rehashed?)

If `ProgressSignal == 0` over **N=3 consecutive iterations** — even when the actions
differ — Agent Runtime MUST classify the run as escalated and route through §3's
escalation path (`e. Escalate to user`) OR apply a strategy mutation, never an
unconditionally silent retry. This closes the "treadmill" class of infinite loop.

**Task-Scoped Failure Ledger.** Each task's working context carries a compact,
durable failure ledger: `{toolId, errorSignature, count, firstSeenAt, blacklistedUntilTaskEnd}`. After
**K=3 identical signature repetitions** on the same tool within one task, Agent
Runtime **MUST** enforce **strategy mutation**: the next invocation **MUST select a
different `toolId`** (not merely different arguments); the blocked `toolId` is
recorded in the ledger as `BLACKLISTED_UNTIL_TASK_END`. It is **forbidden** to re-issue
the blacklisted tool (regardless of parameter changes) on any subsequent turn within
the same task. The ledger is **task-scoped only**; global `Tool` registry descriptors
and `ToolStatus` are never mutated (`TOOL_SYSTEM.md` §ToolStatus Lifecycle owns
descriptor health, explicitly excluding per-call failures — see NXR-2004 recovery).
This prevents tool-immutability violations while still forcing the agent off a
failing tool within the task — and the `ToolReplaced` history entry records the
substitution for the final report.

## 10. Fault-Injection Testing (FR-AS-009)

Scripted chaos scenarios, runnable in CI and locally:

| Scenario | Verifies |
|----------|----------|
| Kill app mid-task → restart | Resume reconstruction (CONTEXT_MANAGEMENT §3) + checkpoint fidelity |
| Kill during a non-idempotent tool call → restart | Exactly-once recovery (no double side-effect) |
| Network loss mid-task | Degradation ladder descent + graceful notification |
| Provider 500s / rate-limit storm | Failover + retry backoff (ProviderLifecycle) |
| Disk-full during write | Quota handling + partial results (NXR-7xxx) + snapshot restore |
| OOM / memory pressure | Resource limits, LRU eviction, `onTrimMemory` |
| Double restart (kill → resume → kill → resume) | Idempotent recovery across repeated interruptions |
| Summarization churn | Progressive summarization under token pressure (no context loss) |

Additions to [testing/E2ETests.md](../testing/E2ETests.md) (resilience journeys) and
unit/integration coverage for replay-log and watchdog logic.

## Phase Mapping

- **Phase 2**: Verification gates (FR-AS-006), budget escalation (FR-AS-003),
  heartbeat/watchdog (FR-AS-002), idempotency declarations + replay log (FR-AS-007).
- **Phase 4**: Plan repair (FR-AS-001), degradation ladder (FR-AS-008), closed-loop
  learning (FR-AS-004), trust growth (FR-AS-005), fault-injection suite (FR-AS-009).
- **Phase 6**: Learning-driven skill refinement at scale.
