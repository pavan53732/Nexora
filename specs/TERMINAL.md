# Terminal Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md) | [../docs/adr/ADR-0006-Agent-First-Interaction-Model.md](../docs/adr/ADR-0006-Agent-First-Interaction-Model.md)

---

## Overview

Nexora includes an embedded terminal that provides a Linux-like shell experience inside
the sandbox. Per **ADR-0006 (Agent-First Interaction Model)**, the terminal is an
**internal implementation detail**: it is invoked automatically by agents as a tool —
never opened directly by the user. Terminal output is surfaced in the chat activity
feed and captured in execution logs. There is **no user-facing terminal screen or
navigation tab** (an optional developer mode may expose one later, but not as a primary
feature).

## Requirements

- Multiple concurrent terminal sessions (internal).
- Agent-invocable: the agent runs commands as tools (`terminal_run`, `terminal_run_script`, etc.).
- Command history persistent across sessions (agent-managed, internal).
- Session restore after app restart.
- All output captured for execution history and streamed into the agent activity feed.
- Not reachable from the primary UI: no terminal tab, no terminal screen, no shell prompt UI.

## Supported Operations

| Category | Commands |
|----------|----------|
| **Navigation** | ls, cd, pwd, tree |
| **File Ops** | cat, head, tail, touch, mkdir, rm, cp, mv, chmod |
| **Search** | grep, find, rg (ripgrep), fd |
| **Archive** | zip, unzip, tar |
| **Process** | ps, kill, jobs, fg, bg, & (background) |
| **Environment** | export, env, echo, which |
| **Git** | git (full support) |
| **Python** | python, python3, pip |
| **Node** | node, npm, npx, yarn, pnpm |
| **Database** | sqlite3 |

## Terminal Features

- Tab completion for commands and file paths.
- Color-coded output (preserved when rendered in activity cards).
- Scrollable output buffer (configurable size).
- Copy/paste support (via activity card interactions).

## Phase Mapping

- **Phase 1**: Terminal interface contracts only (`TerminalSession`, command execution interface). No terminal UI.
- **Phase 3**: Full terminal implementation with shell, history, sessions — internal, agent-invoked; activity feed integration.
- **Phase 8**: Optional developer mode exposing terminal views to advanced users.
