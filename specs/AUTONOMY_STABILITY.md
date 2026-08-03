# Autonomy & Stability Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See also [../specs/CONTEXT_MANAGEMENT.md](./CONTEXT_MANAGEMENT.md) · [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md) · [../docs/LIFECYCLES.md](../docs/LIFECYCLES.md) · [../security/SandboxPolicy.md](../security/SandboxPolicy.md)

---

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
| Cost (per task) | Notify with spent/remaining; require explicit confirmation to continue |

Every exhaustion path ends in a **user-visible state** (notification + task status),
never a silent stop.

## 4. Closed-Loop Learning (FR-AS-004)

After each task, the agent runs a short learning pass:

```
Reflect (what worked / what failed / what was surprising)
   │
   ▼
Store lesson → memory_lessons (TOOL-397) — tagged, retrievable
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
similar tasks), so the platform literally gets smarter with use.

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
execution of the completed steps.

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

Already strong (TOOL_SYSTEM `timeout`, FR-TL002/005, FR-A015, NXR-2002, crash
isolation). Reinforced here:

- **Every** external call (provider, network, sandbox process) has a deadline; no
  unbounded waits.
- Timeouts are classified retryable/non-retryable (NFR-REL-003) and feed plan repair (§1).

## 10. Fault-Injection Testing (FR-AS-009)

Scripted chaos scenarios, runnable in CI and locally:

| Scenario | Verifies |
|----------|----------|
| Kill app mid-task → restart | Resume reconstruction (CONTEXT_MANAGEMENT §4) + checkpoint fidelity |
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
