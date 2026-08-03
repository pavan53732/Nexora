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
- Agent-invocable: the agent runs commands as tools (`terminal_run` TOOL-020, `terminal_run_script` TOOL-021, `terminal_run_background` TOOL-022, `terminal_kill` TOOL-023 — see [registry/TOOLS.md](../registry/TOOLS.md)).
- Command history persistent across sessions (agent-managed, internal).
- Session restore after app restart.
- All output captured for execution history and streamed into the agent activity feed.
- Not reachable from the primary UI: no terminal tab, no terminal screen, no shell prompt UI.

## Supported Operations

Operations available depend on the active [Environment Tier](../specs/ENVIRONMENT_TIERS.md).

### Tier 0 — Embedded Shell (Always Available)

| Category | Commands |
|---|---|
| **Navigation** | `ls`, `cd`, `pwd`, `tree` |
| **File Ops** | `cat`, `head`, `tail`, `touch`, `mkdir`, `rm`, `cp`, `mv`, `chmod` |
| **Search** | `grep`, `find` (basic) |
| **Archive** | `zip`, `unzip`, `tar` |
| **Environment** | `export`, `env`, `echo`, `which` |
| **Git** | `git` (JGit implementation) |

### Tier 2 — Full Environment (Default, Debian-slim)

All Tier 0 commands plus full Linux userland:

| Category | Commands |
|---|---|
| **Shell** | `bash`, `sh`, `dash` |
| **System** | `ps`, `kill`, `top`, `htop`, `df`, `du`, `free` |
| **Search** | `grep`, `find`, `rg`, `fd`, `ag` |
| **Network** | `curl`, `wget`, `ping`, `netstat`, `ss` |
| **Process** | `ps`, `kill`, `jobs`, `fg`, `bg`, `&`, `nohup` |
| **Git** | Full native `git` |
| **Python** | `python3`, `python3.11`, `pip`, `pip3`, `venv` |
| **Node** | `node`, `npm`, `npx`, `corepack` |
| **Build** | `make`, `gcc`, `g++`, `ld` |
| **Package** | `apt`, `apt-get`, `dpkg` |
| **Database** | `sqlite3`, `psql` (client) |
| **Media** | `ffmpeg`, `ffprobe` (if installed via apt) |

### Tier 1 — Micro Environment (Optional, Alpine)

All Tier 0 commands plus Alpine userland:

| Category | Commands |
|---|---|
| **Shell** | `ash` (BusyBox) |
| **Package** | `apk` |
| **System** | BusyBox variants (`ps`, `top`, `df`) |

**Limitations**: musl libc; binary wheels often fail; limited package repository. See [ENVIRONMENT_TIERS.md §3](../specs/ENVIRONMENT_TIERS.md).

## Terminal Features

- Tab completion for commands and file paths.
- Color-coded output (preserved when rendered in activity cards).
- Scrollable output buffer (configurable size).
- Copy/paste support (via activity card interactions).

## Phase Mapping

- **Phase 1**: Terminal interface contracts only (`TerminalSession`, command execution interface). No terminal UI.
- **Phase 3**: Full terminal implementation with shell, history, sessions — internal, agent-invoked; activity feed integration.
- **Phase 8**: Optional developer mode exposing terminal views to advanced users.

## Environment Tier Awareness

### Command Routing

```kotlin
fun execute(command: String, tier: EnvironmentTier): ExecutionResult {
    return when (tier) {
        EMBEDDED -> embeddedShell.execute(command)
        MICRO -> proot.execute(command, alpineRootfs, overlay)
        FULL -> proot.execute(command, debianRootfs, overlay)
    }
}
```

### Auto-Promotion

| Scenario | Behavior |
|---|---|
| `apt install` in Tier 0/1 | Error: "Full Environment required. Enable?" → user tap → extract Tier 2 |
| `pip install numpy` in Tier 1 | Detect `manylinux` incompatibility → suggest Tier 2 with explanation |
| `npm install` with native dependencies in Tier 1 | Detect missing headers → suggest Tier 2 |

Promotion is non-blocking: the agent receives an error with context and can retry after the user enables the higher tier.

### Session Environment

```bash
export NEXORA_WORKSPACE_ID="ws-uuid"
export NEXORA_TIER="full"
export NEXORA_APP_VERSION="1.2.3"
export HOME="/workspace/home"
export PATH="/usr/local/bin:/usr/bin:/bin:/workspace/.local/bin"
```

These variables allow scripts to detect that they are running inside Nexora and adapt behavior.
