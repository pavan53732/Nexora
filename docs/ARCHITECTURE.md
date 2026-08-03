# System Architecture — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [architecture/](../architecture/)

---

## High-Level Architecture

```
Nexora Android AI Agent Platform
│
├── UI Layer (Android Activities/Fragments/Compose)
│   ├── Workspace Screen (PRIMARY)
│   ├── Chat Screen (inside workspace)
│   ├── Agent Dashboard
│   ├── Task Manager
│   ├── File Manager
│   ├── Terminal Screen
│   ├── Memory Browser
│   ├── Plugin Hub
│   ├── AI Providers Screen
│   ├── Logs Screen
│   └── Settings Screen
│
├── Core Runtime (Kotlin)
│   ├── Planner
│   ├── Executor
│   ├── Workflow Engine
│   ├── Context Builder
│   ├── Token Budget Manager
│   └── Event Bus
│
├── Sandbox Runtime
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
| 9 | **Terminal** | P0 |
| 10 | **Plugins** | P1 |
| 11 | **AI Providers** | P0 |
| 12 | **Logs** | P1 |
| 13 | **Settings** | P0 |
| 14 | **Notifications** | P2 |
| 15 | **Tool Permissions** | P1 |

## Navigation

- **Bottom nav**: Workspace, Tasks, Terminal, Settings.
- **Workspace internal tabs**: Agents, Files, Chats, Memory, Terminal, Logs.
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
