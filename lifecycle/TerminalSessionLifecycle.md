> **Status: DERIVED** for terminal session lifecycle narrative.
> This document describes terminal session lifecycle in prose. The canonical state
> machine definition is owned by
> [../state-machines/TerminalSessionLifecycle.md](../state-machines/TerminalSessionLifecycle.md).
> This file must not be treated as an alternate source of truth for any state enum.
>
> Depends on: [../state-machines/TerminalSessionLifecycle.md](../state-machines/TerminalSessionLifecycle.md).

# Terminal Session Lifecycle Authority — Nexora

## States

`Created`, `Attached`, `Running`, `Detached`, `Closed`, `Failed`

## Rules

Terminal session lifecycle governs terminal availability inside sandboxed execution. Tool-call or task lifecycle remains the authority for business-level execution state.

## Transition Minimums

Transitions SHOULD emit terminal session identity, workspace identity, sandbox identity, correlation reference when available, prior state, new state, version, and timestamp.

## Expanded Lifecycle Specification (S3 — Option A)

Narrative reference for the canonical state machine at
[../state-machines/TerminalSessionLifecycle.md](../state-machines/TerminalSessionLifecycle.md).
States defined there: `Created`, `Attached`, `Running`, `Detached`, `Closed`, `Failed`.

### Canonical State Alignment

The states and transitions below are descriptive prose mirroring the canonical
state machine. In case of discrepancy,
`state-machines/TerminalSessionLifecycle.md` wins.

#### States (from canonical source)
`Created`, `Attached`, `Running`, `Detached`, `Closed`, `Failed`

### Transitions
- `Created → Attached`: PTY/spawned process bound; session ready for I/O.
- `Attached → Running`: Command or interactive input accepted.
- `Attached / Running → Detached`: Process stays alive; disconnected from foreground I/O.
- `Detached → Attached`: Reattached; process still alive.
- `Attached / Running / Detached → Closed`: Process termination complete; resources released.
- `Attached / Running / Detached → Failed`: Unrecoverable error (crash, sandbox violation).

### Dependencies (S4 — terminal spec interdependency)
- `specs/TERMINAL.md` — terminal execution model (PTY vs subprocess, session state, working-dir boundary, output caps, timeouts, restore).
- `models/TerminalSession.md` — terminal session model (fields for state, process isolation, resource limits).
- `architecture/TOOL_SYSTEM.md` (§Terminal) + `registry/TOOLS.md` (`TOOL-020`..`023` + `run_command`, `run_script`, `run_background`, `kill_process`).
- `security/SandboxPolicy.md` (§sandbox isolation aligns with terminal execution).
- `specs/BACKGROUND_EXECUTION.md` (§FGS notification + checkpoint recovery references terminal state).
