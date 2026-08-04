> **Status: SUPPORTING** for WORKSPACE focused behavior.
> This document explains focused behavior for WORKSPACE. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# Workspace Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md) | [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)

---

## Overview

The Workspace is the **primary entity** in Nexora. It is not the chat screen — it is the project container that holds everything: agents, tasks, files, memory, terminal, plugins, logs, settings, and chats.

## Workspace Hierarchy

```
Workspace
    ├── Agents          -> Agent instances operating in this workspace
    ├── Tasks           -> Active, completed, and historical tasks
    ├── Files           -> Virtual file system (sandbox root)
    │   ├── src/
    │   ├── docs/
    │   └── ...
    ├── Memory          -> Workspace-scoped memory
    ├── Terminal        -> Embedded terminal sessions
    ├── Plugins         -> Workspace-installed plugins
    ├── Logs            -> Execution logs and audit trail
    ├── Settings        -> Per-workspace configuration
    └── Chats           -> Conversations (one artifact among many)
```

## Workspace Operations

| Operation | Description |
|-----------|-------------|
| **Create** | Create a new workspace with default configuration. |
| **Switch** | Switch the active workspace. |
| **Archive** | Archive a workspace (read-only, not deleted). |
| **Delete** | Delete a workspace and all its data. |
| **List** | List all workspaces with status. |
| **Configure** | Modify workspace settings (provider, model, permissions, limits). |
| **Export** | Export workspace as a zip file. |
| **Import** | Import a workspace from a zip file. |

## Workspace Configuration

```json
{
  "name": "My Project",
  "description": "Project description",
  "created_at": "2026-08-03T00:00:00Z",
  "updated_at": "2026-08-03T00:00:00Z",
  "settings": {
    "default_agent": "coder",
    "default_provider": "openai",
    "default_model": "gpt-4o",
    "sandbox_limits": {
      "max_memory_mb": 512,
      "max_disk_mb": 1024,
      "max_processes": 10,
      "network_allowed": true
    },
    "tool_permissions": {
      "network:http": "ask",
      "sandbox:write": "allow",
      "device:camera": "deny"
    }
  }
}
```

## Workspace Interface

```kotlin
data class Workspace(
    val id: String,
    val name: String,
    val description: String,
    val status: WorkspaceStatus,
    val settings: WorkspaceSettings,
    val createdAt: Instant,
    val updatedAt: Instant
)

enum class WorkspaceStatus { ACTIVE, ARCHIVED }

interface WorkspaceManager {
    suspend fun create(name: String, description: String = ""): Workspace
    suspend fun get(id: String): Workspace?
    suspend fun list(): List<Workspace>
    suspend fun switch(id: String)
    suspend fun archive(id: String)
    suspend fun delete(id: String)
    suspend fun updateSettings(id: String, settings: WorkspaceSettings)
    suspend fun export(id: String): ByteArray
    suspend fun import(data: ByteArray): Workspace
}
```

## Phase Mapping

- **Phase 1**: Workspace Manager, workspace creation, switching, configuration UI.
- **Phase 3**: Full sandbox integration, virtual file system, terminal sessions.
