# System Architecture — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [architecture/](../architecture/) | [ADR-0003 Agent Runtime](adr/ADR-0003-Agent-Runtime.md) | [ADR-0006 Agent-First](adr/ADR-0006-Agent-First-Interaction-Model.md)

---

## High-Level Architecture

```
Nexora Android AI Agent Platform
│
├── UI Layer (Android Activities/Fragments/Compose)
│   ├── Workspace Screen (PRIMARY)
│   ├── Chat Screen (inside workspace) — agent-first interaction surface
│   ├── Agent Activity Feed (tool calls, terminal output, file changes)
│   ├── Agent Dashboard
│   ├── Task Manager
│   ├── File Manager
│   ├── Memory Browser
│   ├── Plugin Hub
│   ├── AI Providers Screen
│   ├── Logs Screen
│   └── Settings Screen
│
├── Core Runtime (Kotlin)  # simplified — full 17 modules in architecture/RUNTIME.md
│   ├── Planner
│   ├── Executor
│   ├── Workflow Engine
│   ├── Context Builder
│   ├── Token Budget Manager
│   └── Event Bus
│
├── Sandbox Runtime  # depth roadmap: docs/SANDBOX_DEPTH.md (FR-S011..S018)
│   ├── Virtual File System
│   ├── Shell (Linux-like)
│   ├── Python Runtime
│   ├── Node Runtime
│   └── Process Isolation
│
├── Tool System
├── Plugin System
├── AI Provider Manager
├── Memory System
├── Multi-Agent System
├── Security Model
├── Observability
└── Background Services
```

## Workspace-First Design

The **Workspace** is the primary entity. Not chat.

```
Workspace
    ├── Agents
    ├── Tasks
    ├── Files
    ├── Memory
    ├── Terminal
    ├── Plugins
    ├── Logs
    ├── Settings
    └── Chats
```

Chats are contextual to a workspace, not the application root. This scales because users create multiple workspaces, each with isolated files, memory, and configuration.

## UI Layer

| # | Screen | Priority |
|---|--------|----------|
| 1 | **Workspace** | P0 |
| 2 | **Chat** | P0 |
| 3 | **Agent Dashboard** | P0 |
| 4 | **Running Tasks** | P0 |
| 5 | **Projects** | P0 |
| 6 | **Workspace Explorer** | P0 |
| 7 | **Files** | P1 |
| 8 | **Memory** | P1 |
| 9 | **Agent Activity Feed** (tool calls, terminal output — the terminal itself is internal, ADR-0006) | P0 |
| 10 | **Plugins** | P1 |
| 11 | **AI Providers** | P0 |
| 12 | **Logs** | P1 |
| 13 | **Settings** | P0 |
| 14 | **Notifications** | P2 |
| 15 | **Tool Permissions** | P1 |

## Agent-First Interaction

Users interact with AI agents through chat (ADR-0006). The sandbox, embedded terminal,
runtimes, and execution engine are internal implementation details: the agent invokes
them automatically in an isolated environment, and the user sees tool calls, terminal
output, and file changes as activity cards in the conversation. There are no
user-facing screens for infrastructure.

## Navigation

- **Bottom nav**: Workspace, Tasks, Settings. (No infrastructure tabs — the terminal and sandbox are internal; see ADR-0006.)
- **Workspace internal tabs**: Agents, Files, Chats, Memory, Logs. (Terminal is not a tab; its activity appears in the chat activity feed and in Logs.)
- **Side drawer**: Plugins, Providers, Notifications.

## Inter-Module Communication

All modules communicate through the **Event Bus**. No direct coupling.

```
Module A → Event Bus → [Module B, Module C, Module D]
```

Event types: `ToolExecuted`, `AgentStateChanged`, `TaskProgress`, `FileChanged`, `MemoryStored`, `ProviderResponse`, `PluginInstalled`, `PermissionRequested`.

## Design Principles

- **Android-native** — Material Design 3 / Material You.
- **Dark mode first** — Developer tool default.
- **Information-dense** — Power users need to see a lot.
- **Real-time updates** — Streaming text, live terminal, animated progress.
- **Gesture-friendly** — Swipe, pull-to-refresh, long-press context menus.
