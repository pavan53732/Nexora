# Terminal Session Lifecycle Authority — Nexora

## States

`Created`, `Attached`, `Running`, `Detached`, `Closed`, `Failed`

## Rules

Terminal session lifecycle governs terminal availability inside sandboxed execution. Tool-call or task lifecycle remains the authority for business-level execution state.

## Transition Minimums

Transitions SHOULD emit terminal session identity, workspace identity, sandbox identity, correlation reference when available, prior state, new state, version, and timestamp.

## Expanded Lifecycle Specification (S3 — Option A)

### States
`Created`, `Active`, `Background`, `Suspended`, `Restored`, `Terminated`

### Transitions
- `Created → Active`: Terminal session spawned (`FR-TE001`); process isolation activated (`FR-S002`).
- `Active → Background`: User backgrounds session (`FR-T011` scheduling; `FR-AS-002` heartbeat continues).
- `Background → Active`: User brings session to foreground.
- `Active/Background → Suspended`: Session paused; state preserved (`FR-AS-013`); process may be frozen (not killed unless budget exceeded `FR-AS-003`).
- `Suspended → Restored`: Session resumed from preserved state (checkpoint + terminal history); exactly-once recovery (`NFR-REL-012`).
- `Restored/Active/Background → Terminated`: User kills session (`FR-TE004`); process cleaned; sandbox released (`FR-S018`).

### Dependencies (S4 — terminal spec interdependency)
- `specs/TERMINAL.md` — terminal execution model (PTY vs subprocess, session state, working-dir boundary, output caps, timeouts, restore).
- `models/TerminalSession.md` — terminal session model (fields for state, process isolation, resource limits).
- `architecture/TOOL_SYSTEM.md` (§Terminal) + `registry/TOOLS.md` (`TOOL-020`..`023` + `run_command`, `run_script`, `run_background`, `kill_process`).
- `security/SandboxPolicy.md` (§sandbox isolation aligns with terminal execution).
- `specs/BACKGROUND_EXECUTION.md` (§FGS notification + checkpoint recovery references terminal state).
