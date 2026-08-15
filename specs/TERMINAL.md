# Terminal Specification — Nexora

> **Status: CANONICAL** for terminal execution behavior inside the sandboxed environment.
> Defines terminal session execution model (PTY vs subprocess), session state management,
> working-directory boundary enforcement, output caps, timeout discipline, session restore,
> and isolation rules.
> This document owns terminal behavior; lifecycle authority remains `lifecycle/TerminalSessionLifecycle.md` (S3 — expanded).

---

## Scope

Terminal execution operates within the sandboxed runtime (`security/SandboxPolicy.md`, `architecture/SANDBOX.md`). Every terminal session is isolated (`FR-S002` process isolation, `FR-S018` workspace isolation), resource-capped (`FR-AS-003` technical-boundary escalation), and observable (`FR-A010` real-time monitoring, `FR-TL015` audit trail, `FR-EV-002` structured confidence).

---

## Execution Model (S4 — fully specified)

### Subprocess vs PTY

| Mode | Use case | Isolation | Working-dir boundary | Restore behavior |
|------|----------|-----------|----------------------|-------------------|
| **Subprocess** (`run_command`, `run_script`) | Short-lived commands, scripts | Full sandbox isolation (`FR-S002`); inherits workspace limits (`FR-S018`) | Confined to workspace root; `sandbox_limits.workingDir` applies (`models/Workspace.md`); `chdir` outside workspace is denied (`security/SandboxPolicy.md`) | Not restorable (stateless); checkpoint only if `run_background` (`FR-T011`) |
| **PTY** (`terminal_run` interactive, `terminal_session_create`) | Interactive terminal sessions, long-running background tasks (`run_background`) | Process-level isolation (`FR-S002`); session-level isolation (`FR-S018`); PTY master/slave pair isolated per session | Workspace root bound (`workspace.getWorkingDirectory()`); relative paths resolved against workspace; absolute path access (`/etc`, `/home/user`) blocked by sandbox policy (`FR-S014` network egress + `FR-S015` quarantine rules applied to file-system access) | Full session restore (`FR-AS-007` idempotent recovery + `NFR-REL-012` exactly-once): session state snapshot (`lifecycle/TerminalSessionLifecycle.md` `Restored` state) + process restart + working-dir reconstruction + input buffer replay (if `sessionRestoreBuffer` enabled) |

### Session State Machine (canonical — `state-machines/TerminalSessionLifecycle.md`)

Terminal session lifecycle is governed by the canonical state machine
[`state-machines/TerminalSessionLifecycle.md`](../state-machines/TerminalSessionLifecycle.md):
`Created → Attached → Running → Detached → Closed / Failed`.
The state set `Active`, `Background`, `Suspended`, `Restored` used in earlier drafts is
retired; durable status is the canonical enum only.

Timeout-driven suspension and crash recovery are modeled as checkpoint + state, not as
new durable states:

- **Timeout / suspension**: when an interactive PTY exceeds `timeoutMs`, the session is
  **checkpointed** (`restoreCheckpoint` set, `FR-AS-007`) and the foreground I/O detaches
  — the durable status becomes `Detached` with a `suspended=true` flag, not a `Suspended`
  state. The process stays alive; output continues buffered.
- **Restore**: a `Detached` (suspended) session resumes by `reattach()` → `Attached` →
  `Running`; the checkpoint is reloaded and (if `sessionBufferReplay`) input buffer is
  replayed. There is no separate `Restored` status — restore is a transition, recorded as a
  lifecycle event, not a durable state.
- **Background**: `run_background` is simply a `Running`/`Detached` session with no
  interactive timeout; it lives until the process exits or the workspace shuts down
  (technical timeout, resource, or liveness handling under `FR-AS-003` applies; financial cost or internal credits do not kill it).

State fields (`models/TerminalSession.md` — updated for S4):

```kotlin
data class TerminalSession(
    val id: String,
    val workspaceId: String,
    val correlationId: String?,
    val status: TerminalSessionStatus,  // CREATED, ATTACHED, RUNNING, DETACHED, CLOSED, FAILED (canonical — state-machines/TerminalSessionLifecycle.md)
    val sandboxId: String,
    val executionMode: ExecutionMode,   // SUBPROCESS or PTY (S4 — new field)
    val workingDirBoundary: String?,     // workspace root or sandbox overlay (S4 — new field)
    val outputCapBytes: Long,            // max output bytes (S4 — new field; links FR-AS-003 technical output safety)
    val timeoutMs: Long,                // session timeout (S4 — new field; links FR-AS-002 heartbeat)
    val startedAt: Instant,
    val updatedAt: Instant,
    val endedAt: Instant? = null,
    val restoreCheckpoint: String? = null,  // checkpoint reference for FR-AS-007 restore (S4 — new field)
    val sessionBufferReplay: Boolean = false  // input replay after restore (S4 — new field)
)
```

### Working-Directory Boundary Enforcement

Every terminal session enforces a working-directory boundary (`models/Workspace.md` `workspace.getWorkingDirectory()`; `security/SandboxPolicy.md` §sandbox isolation):

- **Subprocess mode**: process working directory set to workspace root; `chdir` outside workspace denied at OS level (sandbox `rootfs` + `chroot`/`proot` isolation; `FULL_ENVIRONMENT.md`).
- **PTY mode**: terminal session working directory initialized to workspace root; user `cd` commands resolve relative to workspace root; absolute path access (`/etc`, `/home/user`) blocked by sandbox policy (`FR-S014` network egress + `FR-S015` quarantine rules applied to file-system access).
- **Boundary violation response**: `PermissionResult.DENY` (`security/PermissionModel.md`) + audit log entry (`FR-TL015` audit trail) + user-facing notice (`FR-U005` agent activity feed surfaces denied actions).

### Output Caps (S4 — new discipline)

Every terminal session applies an output cap (`FR-AS-003` technical safety-boundary mechanism):

- **Default cap**: `outputCapBytes = 1_048_576` (1 MB) for interactive PTY; `262_144` (256 KB) for subprocess (`run_command`).
- **Configurable per workspace** (`models/Workspace.md` `sandboxLimits.outputCapBytes`): user can set lower cap for sensitive workspaces; cap cannot exceed the `FR-AS-003` technical workspace output-safety maximum.
- **Cap enforcement**: output buffer monitored by `TerminalSession` (`models/TerminalSession.md` `outputCapBytes`); when cap reached (`outputBuffer.size >= outputCapBytes`), new output is truncated; user receives truncated-output notice (`FR-U005`); execution continues (not killed) unless the user explicitly sets `truncateOnCap = false` (then output stops, session pauses for approval — `FR-AS-006` verification gate).
- **Cap audit**: every cap event (reached, exceeded, truncated) logged via `FR-TL015` execution audit + `FR-EV-002` structured confidence (output completeness tagged `TRUNCATED` when cap applies).

### Timeout Discipline (S4 — new discipline)

Every terminal session applies timeout rules (`FR-AS-002` heartbeat + `FR-AS-009` degradation ladder):

- **Interactive PTY (`terminal_run`)**: `timeoutMs = 300_000` (5 minutes) default; configurable per workspace (`models/Workspace.md` `sandboxLimits.sessionTimeoutMs`). If timeout reached, the session is **checkpointed** (`restoreCheckpoint` set, `FR-AS-007`) and the foreground I/O **detaches**: durable status becomes `Detached` with `suspended = true` (not a `Suspended` state). The process stays alive; output continues buffered. The user may `reattach()` → `Running` (restore) or `close()` (terminate).
- **Subprocess (`run_command`)**: `timeoutMs = 60_000` (60 seconds) default; non-configurable for security (`FR-S016` autonomy modes: `Manual` requires shorter timeout; `Assisted` allows longer with user confirmation). Timeout triggers bounded repair (`FR-AS-001`): process killed (`FR-TE004` `terminal_kill`); error returned (`NXR-*`); user notified (`FR-U011` chat feed).
- **Background (`run_background`)**: no interactive timeout; background session lives until process exits or workspace shutdown; technical timeout, resource, or liveness handling follows `FR-AS-003`, while financial cost or internal credits do not kill the task.
- **Timeout audit**: timeout events logged (`FR-TL015`); timeout-triggered kills recorded as `FR-AS-003` technical-boundary events (`FR-A010` real-time monitoring shows technical limit usage per request/session/provider/model).

### Restore Behavior (S4 — fully specified)

Session restore aligns with `FR-AS-007` (idempotent recovery) + `NFR-REL-012` (exactly-once) + `FR-M013` (user preferences for session persistence):

- **Checkpoint capture** (timeout/suspend transition): session state (`TerminalSession.status = Detached`, `suspended = true`, `restoreCheckpoint`), process snapshot saved to workspace snapshot (`FR-S013` workspace snapshots); working-dir state preserved; input buffer preserved (`sessionBufferReplay` flag set if replay enabled).
- **Checkpoint storage**: checkpoint stored in workspace snapshot directory (`FR-M012` file history + `FR-S013` workspace snapshots); retention follows workspace retention policy (`FR-M012` retention rules; `FR-S013` snapshot lifecycle).
- **Restore process** (reattach transition): checkpoint loaded; durable status set to `Running` (via `Attached`); process restarted (`TerminalSessionLifecycle.md` `Detached → Attached → Running`); working-dir reconstructed from checkpoint; input buffer replayed (`sessionBufferReplay`); user notified (`FR-U005` agent activity feed shows "resumed after interruption" event — `FR-AS-009` degradation ladder message). A `RESTORED` lifecycle event is emitted; there is no separate `Restored` status.
- **Exactly-once guarantee** (`NFR-REL-012`): checkpoint ID (`correlationId`) tracked; duplicate restore attempts for same checkpoint ID rejected (`FR-AS-001` bounded repair prevents replay loops); audit log confirms exactly-once (`FR-TL015` audit trail shows `RESTORED` event with checkpoint reference and timestamp).
- **Failure during restore**: if checkpoint is corrupt or incomplete, restore fails (`FR-AS-001` bounded repair: max 3 restore attempts; after 3 failures, session marked `FAILED`; user notified; no silent failure — `NFR-REL-002` fidelity preserved).

---

## Task-Scoped Terminal Capability Escalation

Terminal capability remains selective by agent type. A non-terminal-capable agent MUST delegate terminal work to an eligible agent or request a task-scoped escalation through the existing authorization flow. The escalation is bound to the requesting agent, task, workspace, execution lineage, declared purpose, affected canonical Tool IDs, required scopes, effective deadline, output/resource limits, cancellation rule, and revocation condition.

A temporary terminal grant does not create a new Tool, permission scope, agent type, lifecycle state, or permanent capability. It MUST still pass the agent matrix dispatch check, `sandbox:execute`, applicable `sandbox:read`/`sandbox:write`, workspace policy, approval, classifier, schema, sandbox, timeout, output-cap, and resource gates. It does not authorize host paths, unrestricted network/device access, plugin/MCP access, or sensitive-app interaction.

The grant expires on task completion, cancellation, effective deadline, explicit revocation, terminal failure, or runtime degradation. Expiry or revocation while a subprocess or PTY is active MUST use the existing cancellation/termination and checkpoint rules. An unresolved side effect remains `UNKNOWN_COMPLETION` until the declared reconciliation contract resolves it; escalation expiry MUST NOT silently retry or report success. Every request, decision, use, expiry, revocation, cancellation, timeout, restore, and final outcome is recorded in the existing execution history, permission audit trail, and correlated trace.

## Security & Isolation (S4 — terminal model aligns with sandbox)

- **Process isolation**: terminal process spawned as child of sandbox runtime (`FR-S002` process isolation; `FR-S018` workspace isolation; `FULL_ENVIRONMENT.md` `proot` isolation); process group isolated (`FR-S003` resource quotas apply to terminal process group).
- **Sandbox policy**: terminal execution governed by `security/SandboxPolicy.md` (§sandbox isolation); terminal-specific rules include: working-dir boundary enforcement (`models/Workspace.md`); output cap enforcement (`FR-AS-003` technical boundary); timeout enforcement (`FR-AS-002` heartbeat); session restore audit (`FR-AS-007`).
- **Permission scopes**: terminal execution is gated by existing scopes — there is no `device:terminal` scope:
  - `sandbox:execute` — required for every terminal command/script (`security/PermissionModel.md`).
  - `sandbox:read` / `sandbox:write` — required for terminal working-directory access; terminal working-dir access inherits workspace settings (`FR-S001` sandbox security; `security/PermissionModel.md`).
  - `device:microphone` (`DENY` default; `ASK` for voice input — links `S2` MCP + `G5` real-time voice) — required only when the session captures microphone audio, not for ordinary terminal I/O.
  - `device:storage` (`DENY` default; `ASK` for workspace file access outside the sandbox VFS) — see `security/PermissionModel.md`.
- **Audit trail**: every terminal session event (start, background, suspend, restore, terminate, timeout, cap reached) logged via `FR-TL015` execution audit + `FR-EV-002` structured confidence; audit log entry includes session ID, workspace ID, correlation ID, checkpoint reference (for restore), permission scope, output cap status, timeout status.

---

## References (S4 — full spec dependencies)

- `state-machines/TerminalSessionLifecycle.md` (canonical lifecycle authority — `Created/Attached/Running/Detached/Closed/Failed`). `lifecycle/TerminalSessionLifecycle.md` is the DERIVED narrative; in case of discrepancy the state machine wins.
- `models/TerminalSession.md` (updated: `executionMode`, `workingDirBoundary`, `outputCapBytes`, `timeoutMs`, `restoreCheckpoint`, `sessionBufferReplay`).
- `security/SandboxPolicy.md` (sandbox isolation aligns with terminal execution model).
- `architecture/TOOL_SYSTEM.md` (§Terminal category: `run_command`, `run_script`, `run_background`, `kill_process`, `terminal_session_create`/`list`/`kill`).
- `registry/TOOLS.md` (`TOOL-020`..`023` + new terminal session tools).
- `registry/TOOL_MATRIX.md` (terminal capability rows updated for `executionMode`, `outputCap`, `timeout`).
- `specs/BACKGROUND_EXECUTION.md` (§session restore references terminal state; `TaskProgress` events include session status).
- `protocols/Execution-Protocol.md` (terminal execution payload: session ID, working-dir, output cap, timeout, checkpoint reference — updated for S4).
- `docs/LIFECYCLES.md` (§terminal session lifecycle reference — updated S3).
- `docs/MODULE_BOUNDARIES.md` (§runtime terminal execution boundary — updated S3).
- `docs/DECISION_LOG.md` (`DL-028` — S4 terminal specification; `DL-025` — S1 concurrency cap; `DL-027` — S3 lifecycle; `DL-026` — S2 MCP canonical).
- `docs/CHANGELOG.md` (updated: S4 terminal spec note + S3 lifecycle note + S2 MCP note + S1 concurrency cap note).
- `docs/FR_NFR_MAPPING.md` (updated: S4 references — `FR-TE001`..`005`, `FR-S002`/`003`/`018`, `FR-AS-002`/`003`/`007`/`009`, `FR-TL015`, `FR-EV-002`/`006`, `FR-M012`/`013`, `FR-A010`, `FR-U005`).

---

*Terminal execution is now fully specified. All dependencies synchronized (S3 lifecycle filled; S2 MCP canonical; S1 concurrency cap applied to background terminal sessions; `ResourceManager` enforces cap + timeout + output cap + restore behavior).*
