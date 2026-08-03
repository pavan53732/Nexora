# ADR-0006: Agent-First Interaction Model (Infrastructure Is Internal)

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect, Product
- **Supersedes**: DL-018 (bottom navigation) — amended; ADR-0001 navigation example — amended
- **Related**: [ADR-0003-Agent-Runtime](./ADR-0003-Agent-Runtime.md) · [ADR-0004-Sandbox](./ADR-0004-Sandbox.md) · [specs/TERMINAL.md](../../specs/TERMINAL.md) · [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md)

## Context

Earlier Nexora documentation positioned the **infrastructure** as user-facing product
features: the embedded terminal had a bottom-navigation tab, a "Terminal Screen" in the
UI layer, and terminal sessions were "user-invocable". Sandbox, runtimes, and the
execution engine were described as surfaces the user would open and operate.

In practice, modern agent platforms do not work this way. The user interacts with the
**AI agent** through a conversation; the agent plans, then **automatically triggers**
terminals, runtimes, file operations, Git, and other tools inside an isolated sandbox
created on demand. The user sees the *results* — tool-call cards, output excerpts, file
diffs — not the plumbing. This is how assistant-style agent products behave, and it is
the model Nexora should follow on a phone screen, where there is no room for
infrastructure UI anyway.

## Decision

**Chat with agents is the single primary interaction surface. The sandbox, internal
terminal, runtimes, and execution engine are internal implementation details.**

1. The user enters a **goal** in chat; the agent plans and executes autonomously.
2. The agent **auto-invokes** the embedded terminal, Python/Node runtimes, VFS, Git,
   SQLite, and network tools inside an **isolated sandbox** — the user never opens
   these directly.
3. Results stream back into the **conversation** as activity cards (tool calls, output,
   file changes, logs), with permission prompts for sensitive operations.
4. **No primary user-facing screens** for sandbox, terminal, runtimes, or the execution
   engine. The bottom navigation becomes **Workspace, Tasks, Settings** (Terminal tab
   removed). Workspace tabs are **Agents, Files, Chats, Memory, Logs** (Terminal tab
   removed).
5. Observability (logs, execution history) remains a user-facing *read-only* surface
   for trust and debugging; a **developer mode** may later expose the terminal and
   sandbox internals, but never as primary features.
6. The **workspace-first** model (ADR-0001) is unchanged — the workspace remains the
   primary entity; the terminal is one of its internal artifacts.

## Consequences

### Positive

- **Simpler UX**: one mental model — "tell the agent what you want".
- **Smaller UI surface**: fewer screens, tabs, and components to build and maintain.
- **Matches user expectations**: mirrors how agent assistants behave; lower learning
  curve.
- **Better security posture**: no user-facing shell means no direct host/FS exposure;
  everything already flows through the permission manager.
- **APK budget friendly**: terminal/sandbox UI components are not shipped as features.

### Negative

- Users cannot manually drive the shell or sandbox without developer mode.
- Debugging requires trusting the observability/activity feed (mitigated by full
  execution logs and audit trail).
- Documentation and tests referencing a "Terminal screen" must be updated.

### Mitigation

- Rich **agent activity feed** in chat (tool-call cards, streaming output, file diffs).
- Full **execution history + logs** screen for auditability.
- Optional **developer mode** (P2+) exposing terminal/sandbox views to advanced users.

## Affected Documents

`README.md`, `PROJECT_SPECIFICATION.md`, `docs/PRODUCT_VISION.md`, `docs/ARCHITECTURE.md`,
`docs/ROADMAP.md`, `docs/DECISION_LOG.md` (DL-019), `requirements/FR.md`, `backlog/MVP.md`,
`backlog/V1.md`, `specs/TERMINAL.md`, `ui/Navigation.md`, `ui/Components.md`,
`ui/Icons.md`, `registry/FEATURES.md`, `docs/ENVIRONMENT_SETUP.md`, and ADR-0001
(amendment note) — all updated to the agent-first model.
