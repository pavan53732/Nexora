> **Status: SUPPORTING** for Navigation focused behavior.
> This document explains focused behavior for Navigation. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


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
| **AI Providers** | Provider configuration and AI Settings |
| **Notifications** | Notification center |

## AI Provider Settings Surface

The existing AI Providers destination includes the product-level AI Settings behavior: provider/type, external base URL, API key, model name, `TEST CONNECTION`, capability refresh/detection where supported, connection status, validation result, and `SAVE`. The surface projects provider-owned configuration and observations; it MUST NOT authorize workspace execution, grant permissions, create Task/Execution state, invoke Tools, or expose secrets. Exact UI technology and layout remain outside this navigation document.

## Deep Links

- Tap a file reference in chat → Opens Files tab at that file.
- Tap an agent name → Opens Agents tab showing that agent's status.
- Tap a tool call or terminal output card → Opens Logs filtered to that execution.
