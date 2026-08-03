# Terminal Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md)

---

## Overview

Nexora includes an embedded terminal that agents can invoke automatically and users can open manually. It provides a Linux-like shell experience inside the sandbox.

## Requirements

- Multiple concurrent terminal sessions.
- AI-invocable (agent runs commands as tools) and user-invocable.
- Command history persistent across sessions.
- Session restore after app restart.
- All output captured for execution history.

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
- Color-coded output.
- Scrollable output buffer (configurable size).
- Copy/paste support.
- Pinch-to-zoom on output.

## Phase Mapping

- **Phase 1**: Terminal UI screen (empty shell stub).
- **Phase 3**: Full terminal implementation with shell, history, sessions.
