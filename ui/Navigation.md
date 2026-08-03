# UI: Navigation — Nexora

> Agent-first interaction model: see [ADR-0006](../docs/adr/ADR-0006-Agent-First-Interaction-Model.md).
> The terminal and sandbox are internal — no navigation entry for them.

## Bottom Navigation (3 items)

| Tab | Icon | Screen |
|-----|------|--------|
| **Workspace** | `folder_open` | Active workspace detail |
| **Tasks** | `task_alt` | Running and completed tasks |
| **Settings** | `settings` | App settings |

## Workspace Internal Tabs

| Tab | Content |
|-----|---------|
| **Chats** | Agent conversations — the primary interaction surface (goal entry, streaming, activity feed) |
| **Agents** | Agent dashboard for this workspace |
| **Files** | Workspace file explorer |
| **Memory** | Workspace-scoped memory browser |
| **Logs** | Execution logs and audit trail (terminal output appears here and in the chat activity feed) |

## Side Drawer

| Item | Screen |
|------|--------|
| **All Workspaces** | Workspace list |
| **Plugins** | Plugin Hub |
| **AI Providers** | Provider configuration |
| **Notifications** | Notification center |

## Deep Links

- Tap a file reference in chat → Opens Files tab at that file.
- Tap an agent name → Opens Agents tab showing that agent's status.
- Tap a tool call or terminal output card → Opens Logs filtered to that execution.
