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

## Phase Mapping

- **Phase 1**: VFS interface definition, basic CRUD.
- **Phase 3**: Full implementation with search, large file support.
