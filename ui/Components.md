> **Status: SUPPORTING** for Components focused behavior.
> This document explains focused behavior for Components. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# UI: Components — Nexora

## Core Components

| Component | Description | Priority |
|-----------|-------------|----------|
| `NexoraAppBar` | Top app bar with workspace name and actions. | P0 |
| `WorkspaceTabs` | Tabbed navigation within a workspace. | P0 |
| `ChatBubble` | AI and user message bubbles with streaming support. | P0 |
| `ToolCallCard` | Expandable card showing tool invocation and result — core of the agent activity feed. | P0 |
| `ActivityCard` | Streamed terminal output, file changes, and progress events rendered inline in chat. | P0 |
| `TaskCard` | Task status card with progress indicator. | P0 |
| `TerminalView` | Terminal emulator — internal only (agent activity / developer mode). Not a primary screen. | P2 |
| `FileExplorer` | Tree-view file browser for the virtual file system. | P0 |
| `AgentCard` | Agent status and capabilities display. | P1 |
| `MemorySearchBar` | Semantic search input for memory recall. | P1 |
| `PluginCard` | Plugin info with install/uninstall button. | P1 |
| `ProviderCard` | Provider config card with health indicator. | P0 |
| `PermissionDialog` | Permission approval/deny dialog. | P1 |
| `StreamingText` | Text view that animates token-by-token. | P0 |
| `EmptyState` | Placeholder for empty workspaces, no tasks, etc. | P0 |

All components use Jetpack Compose.
