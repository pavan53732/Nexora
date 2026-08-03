# Sandbox Architecture — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [RUNTIME.md](RUNTIME.md) | [TOOL_SYSTEM.md](TOOL_SYSTEM.md)

---

## Overview

The Sandbox is Nexora's isolated execution environment. The AI never directly executes commands on Android. Everything runs inside the sandbox, which lives in the app's private storage.

## Components

| Component | Description | Phase |
-----------|-------------|-------|
| **Virtual File System** | Complete file system inside app private storage. Directories, files, symlinks. | 3 |
| **Workspace Isolation** | Each workspace has isolated storage. No cross-workspace access. | 1 |
| **Temporary Workspaces** | Ephemeral workspaces for one-off tasks. | 3 |
| **Linux-like Shell** | Shell environment mimicking common Linux commands. | 3 |
| **Python Runtime** | Embedded Python interpreter for scripts and packages. | 3 |
| **Node Runtime** | Embedded Node.js runtime for JavaScript and npm. | 3 |
| **JavaScript Runtime** | Lightweight JS engine for quick scripts and plugin execution. | 3 |
| **Git** | Full Git support inside the sandbox. | 3 |
| **SQLite** | Embedded SQLite for databases. | 3 |
| **Package Managers** | pip, npm, yarn, pnpm for installing packages. | 3 |
| **Environment Variables** | Per-workspace and per-session env var management. | 3 |
| **Command History** | Persistent command history across terminal sessions. | 3 |
| **Session Restore** | Terminal sessions persist and restore after app restart. | 3 |
| **Resource Limits** | Configurable CPU, memory, disk, network quotas. | 3 |
| **Process Isolation** | Each execution runs in an isolated process. | 3 |
| **Log Capture** | All sandbox activity logged and accessible. | 3 |

## Storage Layout

```
/data/data/com.nexora.app/
├── sandbox/
│   ├── workspaces/
│   │   ├── {workspace-id-1}/
│   │   │   ├── workspace.json      # Workspace config
│   │   │   ├── files/              # Virtual file system root
│   │   │   │   ├── src/
│   │   │   │   ├── docs/
│   │   │   │   └── ...
│   │   │   ├── .git/               # Git repository
│   │   │   ├── memory/             # Workspace-scoped memory
│   │   │   ├── terminal/           # Terminal sessions and history
│   │   │   ├── tasks/              # Task state and checkpoints
│   │   │   ├── env/                # Environment config
│   │   │   └── logs/               # Workspace logs
│   │   └── {workspace-id-2}/
│   └── temp/                       # Temporary/ephemeral workspaces
├── global/
│   ├── memory/                     # Long-term memory
│   ├── plugins/                    # Installed plugins
│   ├── providers/                  # AI provider configs (encrypted keys)
│   └── settings/                   # Global app settings
└── cache/
    ├── embeddings/                 # Vector embedding cache
    └── models/                     # Cached local models
```

## Virtual File System Interface

```kotlin
interface VirtualFileSystem {
    // File operations
    suspend fun readFile(path: String): String
    suspend fun writeFile(path: String, content: String)
    suspend fun appendFile(path: String, content: String)
    suspend fun deleteFile(path: String)
    suspend fun fileExists(path: String): Boolean
    suspend fun getFileInfo(path: String): FileInfo

    // Directory operations
    suspend fun listDirectory(path: String): List<FileInfo>
    suspend fun createDirectory(path: String)
    suspend fun deleteDirectory(path: String)

    // Search
    suspend fun searchFiles(query: String, path: String): List<FileInfo>
}
```

## Process Isolation

Each tool execution runs in an isolated context:

- **Separate Process** — Where possible, commands spawn isolated processes.
- **Resource Limits** — CPU time, memory, and disk quotas per workspace.
- **Network Control** — Per-workspace network allow/deny.
- **Timeout Enforcement** — Maximum execution time per command.
- **Working Directory** — Each execution has a scoped working directory.

## Resource Quotas

```kotlin
data class SandboxLimits(
    val maxMemoryMb: Int = 512,
    val maxDiskMb: Int = 1024,
    val maxProcesses: Int = 10,
    val maxExecutionTimeSeconds: Long = 300,
    val networkAllowed: Boolean = true,
    val maxFileCount: Int = 10_000
)
```

## Phase Mapping

- **Phase 1**: Workspace isolation, virtual file system interface.
- **Phase 3**: Shell, runtimes (Python, Node), Git, SQLite, process isolation, resource limits.
- **Phase 8**: Plugin-managed sandbox extensions.