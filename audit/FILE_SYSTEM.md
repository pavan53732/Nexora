# File System Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md)

---

## Overview

The Virtual File System (VFS) provides a complete file system inside Nexora's sandbox. It is the foundation for workspaces, projects, and all file-based operations.

## Requirements

- Full file CRUD: create, read, update, delete.
- Directory operations: create, list, delete, navigate.
- File metadata: size, type, modified time, permissions.
- Search: by name, by content (text and regex).
- Workspace isolation: each workspace has its own VFS root.
- Persistence: files survive app restarts.
- Large file support: streaming reads/writes for files > 10MB.

## Storage Path

```
/data/data/com.nexora.app/sandbox/workspaces/{workspace-id}/files/
```

## Operations

| Operation | Method | Description |
|-----------|--------|-------------|
| Read file | `readFile(path)` | Returns file content as string. |
| Write file | `writeFile(path, content)` | Creates or overwrites a file. |
| Append file | `appendFile(path, content)` | Appends to existing file. |
| Delete file | `deleteFile(path)` | Removes a file. |
| List directory | `listDirectory(path)` | Returns file info for all children. |
| Create directory | `createDirectory(path)` | Creates a directory (recursive). |
| Delete directory | `deleteDirectory(path)` | Removes empty directory or tree. |
| Move file | `moveFile(from, to)` | Moves/renames a file or directory. |
| Copy file | `copyFile(from, to)` | Copies a file or directory. |
| File exists | `fileExists(path)` | Returns boolean. |
| File info | `getFileInfo(path)` | Returns metadata. |
| Search files | `searchFiles(query, path)` | Searches by name pattern. |
| Search content | `searchContent(query, path)` | Searches file contents. |

## File Versioning (FR-M012)

The VFS keeps a **version history of files modified by agents** — the `File History`
memory type. Agents can inspect and revert changes; the user sees file changes in the
activity feed.

| Aspect | Rule |
|--------|------|
| **Capture** | On every agent-originated `writeFile`/`appendFile`/`deleteFile`/`moveFile`, the previous state is snapshotted before the change (content hash + diff). Read-only operations never create versions. |
| **Storage** | Version metadata (hash, timestamp, agent, task, diff) in Room `file_version` table; content blobs in the workspace sandbox under `files/.history/` (outside the user-visible tree, excluded from search). |
| **Diff** | Versions store a unified diff between the prior and new content (text files); binary files store full blobs with hash dedupe. |
| **Revert** | `revertFile(path, versionId)` restores the chosen version atomically (write-new + swap, never truncate-in-place), creating a new version entry recording the revert. |
| **Quota** | File history counts toward the workspace disk quota (SandboxPolicy §6). Retention: keep last 50 versions per file or 30 days, then prune oldest (configurable per workspace). |
| **Isolation** | `.history/` is per-workspace and cannot be read by other workspaces or plugins (same rules as the VFS). |
| **Tools** | `file_history` (TOOL-381), `file_restore` (TOOL-382) — see [registry/TOOLS.md](../registry/TOOLS.md). |

## Phase Mapping

- **Phase 1**: VFS interface definition, basic CRUD.
- **Phase 3**: Full implementation with search, large file support.
