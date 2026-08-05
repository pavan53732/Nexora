# Sandbox Architecture — Nexora

> **Status: CANONICAL** for sandbox subsystem design and runtime integration.
> This document owns how the sandbox is structured, how proot executes guest
> binaries, how the VFS is layered, and how the sandbox integrates with the
> runtime. It does NOT own sandbox security policy (see
> [../security/SandboxPolicy.md](../security/SandboxPolicy.md)), permission
> semantics (see [../security/PermissionModel.md](../security/PermissionModel.md)),
> or security architecture (see [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md)).
>
> Depends on: [../security/SandboxPolicy.md](../security/SandboxPolicy.md), [../specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md).
> Referenced by: [RUNTIME.md](RUNTIME.md), [specs/TERMINAL.md](../specs/TERMINAL.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

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

## Full Environment

The sandbox uses a single bundled Full Environment based on a Debian-slim rootfs packaged inside the APK. See [specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md) for the full specification.

| Environment | Description | Default |
|---|---|---|
| **Full Environment** | **Debian-slim rootfs (~50–70 MB compressed) with glibc, apt, and broad Python/npm compatibility** | **Yes** |

### Full Environment Architecture

```text
┌─────────────────────────────────────────┐
│         Nexora Android App              │
│  ┌─────────────────────────────────┐    │
│  │      Sandbox Manager            │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │    proot (static)       │    │    │
│  │  │  ┌─────────────────┐    │    │    │
│  │  │  │ Debian-slim     │    │    │    │
│  │  │  │   rootfs        │    │    │    │
│  │  │  │  ┌───────────┐  │    │    │    │
│  │  │  │  │ Workspace │  │    │    │    │
│  │  │  │  │ VFS via   │  │    │    │    │
│  │  │  │  │ /workspace│  │    │    │    │
│  │  │  │  └───────────┘  │    │    │    │
│  │  │  └─────────────────┘    │    │    │
│  │  └─────────────────────────┘    │    │
│  └─────────────────────────────────┘    │
│         APK Assets: rootfs/.tar.xz     │
└─────────────────────────────────────────┘
```

**Bundled rootfs**: The Debian-slim rootfs is compressed (`tar.xz`) in APK `assets/rootfs/` and extracted to app-private storage on first launch. The base rootfs is read-only and workspace overlays provide write isolation (security policy in SandboxPolicy.md).

**proot execution**: Commands execute through proot with a rootfs and workspace bind mount, without requiring root privileges.

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


### Rootfs Storage (Full Environment)

```text
/data/data/com.nexora.app/
├── rootfs/                         # Shared read-only Debian base
│   ├── bin/, usr/, lib/, etc/      # Standard FHS layout
│   └── .manifest.json              # Checksums, version, signature
├── sandbox/
│   └── workspaces/
│       └── {workspace-id}/
│           ├── files/              # Workspace files
│           ├── rootfs-overlay/     # Private writable layer (tmp, var, usr/local, etc.)
│           └── env/
└── rootfs-cache/                   # Download cache for rootfs updates
    └── debian-slim-arm64-v1.2.3.tar.xz
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
