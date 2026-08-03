# Database Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md)

---

## Overview

Nexora uses SQLite for structured data storage within the sandbox and for the memory system.

## Use Cases

| Use Case | Description |
|----------|-------------|
| **Sandbox Database** | Users can create and query SQLite databases in their workspace. |
| **Memory Store** | Session, project, and long-term memory backed by SQLite. |
| **Execution History** | All tool calls, agent actions, and results. |
| **Plugin Data** | Per-plugin structured storage. |
| **Vector Storage** | Embeddings stored in SQLite with vector extension. |

## SQLite Tools

| Tool | Description |
|------|-------------|
| `sqlite_query` | Execute a SELECT query. |
| `sqlite_execute` | Execute INSERT, UPDATE, DELETE. |
| `sqlite_create` | Create a new database file. |
| `sqlite_migrate` | Run schema migrations. |
| `sqlite_schema` | Inspect database schema. |

## Phase Mapping

- **Phase 3**: SQLite available in sandbox.
- **Phase 6**: Memory system uses SQLite.
