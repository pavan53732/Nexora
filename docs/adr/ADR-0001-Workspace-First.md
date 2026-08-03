# ADR-0001: Workspace-First Architecture

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect

## Context

Most AI chat applications center their UI around a conversation list. The user opens the app, sees a list of chats, and taps one to interact. This works for chatbots but fails for autonomous agent platforms.

In Nexora, the AI performs real tasks: it creates files, runs code, manages projects, and uses tools. A chat-only interface cannot represent these artifacts. If chat is the root entity, the user must navigate away from their conversation to see files, tasks, or terminal output, breaking the workflow.

Comparable products (Cursor, Cline, Claude Code) all organize around a **project** or **workspace**, not a chat list. The conversation is one component of the workspace.

## Decision

The **Workspace** is the primary entity in Nexora. Not the chat screen, not the app home.

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

- The bottom navigation shows: **Workspace, Tasks, Terminal, Settings**.
- Inside a workspace, tabs provide access to: Agents, Files, Chats, Memory, Terminal, Logs.
- A user can have multiple workspaces, each fully isolated.
- Chats are one artifact within a workspace.

## Consequences

### Positive
- **Scalability**: New artifact types (e.g., databases, deployments) are added as workspace children, not new top-level concepts.
- **Multi-project support**: Users naturally work on multiple projects without confusion.
- **Consistent with industry**: Matches how Cursor, Cline, and Claude Code organize work.
- **Clear scope**: All operations within a workspace are scoped to that workspace.

### Negative
- **More navigation depth**: Users must select a workspace before accessing any content.
- **Initial complexity**: A workspace-only app requires workspace creation before first use.

### Mitigation
- Provide a "Quick Start" workspace created automatically on first launch.
- Allow creating workspaces from templates.
- Cache the last active workspace for fast resume.
