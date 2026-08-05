# Terminal Specification — Nexora

> **Status: CANONICAL** for terminal execution behavior inside the sandboxed environment.
> Defines terminal session execution model (PTY vs subprocess), session state management,
> working-directory boundary enforcement, output caps, timeout discipline, session restore,
> and isolation rules.
> This document owns terminal behavior; lifecycle authority remains `lifecycle/TerminalSessionLifecycle.md` (S3 — expanded).

---

## Scope

Terminal execution operates within the sandboxed runtime (`security/SandboxPolicy.md`, `architecture/SANDBOX.md`). Every terminal session is isolated (`FR-S002` process isolation, `FR-S018` workspace isolation), resource-capped (`FR-AS-003` budget escalation), and observable (`FR-A010` real-time monitoring, `FR-T015` audit trail, `FR-EV-002` structured confidence).

---

## Execution Model (S4 — fully specified)

### Subprocess vs PTY

| Mode | Use case | Isolation | Working-dir boundary | Restore behavior |
|------|----------|-----------|----------------------|-------------------|
| **Subprocess** (`run_command`, `run_script`) | Short-lived commands, scripts | Full sandbox isolation (`FR-S002`); inherits workspace limits (`FR-S018`) | Confined to workspace root; `sandbox_limits.workingDir` applies (`models/Workspace.md`); `chdir` outside workspace is denied (`security/SandboxPolicy.md`) | Not restorable (stateless); checkpoint only if `run_background` (`FR-T011`) |
| **PTY** (`terminal_run` interactive, `terminal_session_create`) | Interactive terminal sessions, long-running background tasks (`run_background`) | Process-level isolation (`FR-S002`); session-level isolation (`FR-S018`); PTY master/slave pair isolated per session | Workspace root bound (`workspace.getWorkingDirectory()`); relative paths resolved against workspace; absolute path access (`/etc`, `/home/user`) blocked by sandbox policy (`FR-S014` network egress + `FR-S015` quarantine rules applied to file-system access) | Full session restore (`FR-AS-013` exactly-once recovery): session state snapshot (`lifecycle/TerminalSessionLifecycle.md` `Restored` state) + process restart + working-dir reconstruction + input buffer replay (if `sessionRestoreBuffer` enabled) |

### Session State Machine (S3 — filled lifecycle authority)

Terminal session lifecycle is governed by `lifecycle/TerminalSessionLifecycle.md` (S3 — Option A, filled): `Created → Active → Background → Suspended → Restored → Terminated`.

State fields (`models/TerminalSession.md` — updated for S4):

```kotlin
data class TerminalSession(
    val id: String,
    val workspaceId: String,
    val correlationId: String?,
    val status: TerminalSessionStatus,  // CREATED, ACTIVE, BACKGROUND, SUSPENDED, RESTORED, TERMINATED
    val sandboxId: String,
    val executionMode: ExecutionMode,   // SUBPROCESS or PTY (S4 — new field)
    val workingDirBoundary: String?,     // workspace root or sandbox overlay (S4 — new field)
    val outputCapBytes: Long,            // max output bytes (S4 — new field; links FR-AS-003 budget)
    val timeoutMs: Long,                // session timeout (S4 — new field; links FR-AS-002 heartbeat)
    val startedAt: Instant,
    val updatedAt: Instant,
    val endedAt: Instant? = null,
    val restoreCheckpoint: String? = null,  // checkpoint reference for FR-AS-013 restore (S4 — new field)
    val sessionBufferReplay: Boolean = false  // input replay after restore (S4 — new field)
)
```

### Working-Directory Boundary Enforcement

Every terminal session enforces a working-directory boundary (`models/Workspace.md` `workspace.getWorkingDirectory()`; `security/SandboxPolicy.md` §sandbox isolation):

- **Subprocess mode**: process working directory set to workspace root; `chdir` outside workspace denied at OS level (sandbox `rootfs` + `chroot`/`proot` isolation; `FULL_ENVIRONMENT.md`).
- **PTY mode**: terminal session working directory initialized to workspace root; user `cd` commands resolve relative to workspace root; absolute path access (`/etc`, `/home/user`) blocked by sandbox policy (`FR-S014` network egress + `FR-S015` quarantine rules applied to file-system access).
- **Boundary violation response**: `PermissionResult.DENY` (`security/PermissionModel.md`) + audit log entry (`FR-T015` audit trail) + user-facing notice (`FR-U005` agent activity feed surfaces denied actions).

### Output Caps (S4 — new discipline)

Every terminal session applies an output cap (`FR-AS-003` budget escalation mechanism):

- **Default cap**: `outputCapBytes = 1_048_576` (1 MB) for interactive PTY; `262_144` (256 KB) for subprocess (`run_command`).
- **Configurable per workspace** (`models/Workspace.md` `sandboxLimits.outputCapBytes`): user can set lower cap for sensitive workspaces; cap cannot exceed `FR-AS-003` workspace budget maximum.
- **Cap enforcement**: output buffer monitored by `TerminalSession` (`models/TerminalSession.md` `outputCapBytes`); when cap reached (`outputBuffer.size >= outputCapBytes`), new output is truncated; user receives truncated-output notice (`FR-U005`); execution continues (not killed) unless the user explicitly sets `truncateOnCap = false` (then output stops, session pauses for approval — `FR-AS-006` verification gate).
- **Cap audit**: every cap event (reached, exceeded, truncated) logged via `FR-T015` execution audit + `FR-EV-002` structured confidence (output completeness tagged `TRUNCATED` when cap applies).

### Timeout Discipline (S4 — new discipline)

Every terminal session applies timeout rules (`FR-AS-002` heartbeat + `FR-AS-009` degradation ladder):

- **Interactive PTY (`terminal_run`)**: `timeoutMs = 300_000` (5 minutes) default; configurable per workspace (`models/Workspace.md` `sandboxLimits.sessionTimeoutMs`). If timeout reached, session state changes to `SUSPENDED` (`lifecycle/TerminalSessionLifecycle.md`); checkpoint saved (`FR-AS-013`); user may resume (`Restored` state) or terminate (`Terminated`).
- **Subprocess (`run_command`)**: `timeoutMs = 60_000` (60 seconds) default; non-configurable for security (`FR-S016` autonomy modes: `Manual` requires shorter timeout; `Assisted` allows longer with user confirmation). Timeout triggers bounded repair (`FR-AS-001`): process killed (`FR-TE004` `terminal_kill`); error returned (`NXR-*`); user notified (`FR-U011` chat feed).
- **Background (`run_background`)**: no interactive timeout; background session lives until process exits or workspace shutdown (`FR-AS-003` budget exhaustion kills background tasks with checkpoint restart).
- **Timeout audit**: timeout events logged (`FR-T015`); timeout-triggered kills recorded as `FR-AS-003` budget events (`FR-A010` real-time monitoring shows budget usage per request/session/provider/model).

### Restore Behavior (S4 — fully specified)

Session restore aligns with `FR-AS-013` (exactly-once recovery) + `FR-M013` (user preferences for session persistence):

- **Checkpoint capture** (`SUSPENDED` transition): session state (`TerminalSession.status`, `restoreCheckpoint`, process snapshot) saved to workspace snapshot (`FR-S013` workspace snapshots); working-dir state preserved; input buffer preserved (`sessionBufferReplay` flag set if replay enabled).
- **Checkpoint storage**: checkpoint stored in workspace snapshot directory (`FR-M012` file history + `FR-S013` workspace snapshots); retention follows workspace retention policy (`FR-M012` retention rules; `FR-S013` snapshot lifecycle).
- **Restore process** (`Restored` transition): checkpoint loaded; session state set to `Restored`; process restarted (`TerminalSessionLifecycle.md` `Restored → Active`); working-dir reconstructed from checkpoint; input buffer replayed (`sessionBufferReplay`); user notified (`FR-U005` agent activity feed shows "resumed after interruption" event — `FR-AS-009` degradation ladder message).
- **Exactly-once guarantee** (`NFR-REL-012`): checkpoint ID (`correlationId`) tracked; duplicate restore attempts for same checkpoint ID rejected (`FR-AS-001` bounded repair prevents replay loops); audit log confirms exactly-once (`FR-T015` audit trail shows `RESTORED` event with checkpoint reference and timestamp).
- **Failure during restore**: if checkpoint is corrupt or incomplete, restore fails (`FR-AS-001` bounded repair: max 3 restore attempts; after 3 failures, session marked `FAILED`; user notified; no silent failure — `NFR-REL-002` fidelity preserved).

---

## Security & Isolation (S4 — terminal model aligns with sandbox)

- **Process isolation**: terminal process spawned as child of sandbox runtime (`FR-S002` process isolation; `FR-S018` workspace isolation; `FULL_ENVIRONMENT.md` `proot` isolation); process group isolated (`FR-S003` resource quotas apply to terminal process group).
- **Sandbox policy**: terminal execution governed by `security/SandboxPolicy.md` (§sandbox isolation); terminal-specific rules include: working-dir boundary enforcement (`models/Workspace.md`); output cap enforcement (`FR-AS-003`); timeout enforcement (`FR-AS-002`); session restore audit (`FR-AS-013`).
- **Permission scopes**: terminal execution requires `device:*` scopes (`FR-S001` sandbox security; `security/PermissionModel.md`): `device:terminal` (default `ASK` for interactive; `ALLOW` for background when workspace policy permits), `device:microphone` (for voice input — links `S2` MCP + `G5` real-time voice), `device:storage` (`DENY` default; `ASK` for workspace file access; terminal working-dir access inherits workspace settings).
- **Audit trail**: every terminal session event (start, background, suspend, restore, terminate, timeout, cap reached) logged via `FR-T015` execution audit + `FR-EV-002` structured confidence; audit log entry includes session ID, workspace ID, correlation ID, checkpoint reference (for restore), permission scope, output cap status, timeout status.

---

## References (S4 — full spec dependencies)

- `lifecycle/TerminalSessionLifecycle.md` (canonical lifecycle authority — filled S3).
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
- `docs/FR_NFR_MAPPING.md` (updated: S4 references — `FR-TE001`..`005`, `FR-S002`/`003`/`018`, `FR-AS-002`/`003`/`009`/`013`, `FR-T015`, `FR-EV-002`/`006`, `FR-M012`/`013`, `FR-A010`, `FR-U005`).

---

*Terminal execution is now fully specified. All dependencies synchronized (S3 lifecycle filled; S2 MCP canonical; S1 concurrency cap applied to background terminal sessions; `ResourceManager` enforces cap + timeout + output cap + restore behavior).*
