> **Status: SUPPORTING** for DATABASE focused behavior.
> This document explains focused behavior for DATABASE. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


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

### SQLite result and schema-state grounding

SQLite tool invocations inherit the existing Tool System authorization, schema-validation, idempotency, timeout, UNKNOWN_COMPLETION, reconciliation, SandboxPolicy, PermissionModel, and audit contracts. Query results, imported records, inspected schemas, migration output, and database files are tool-derived context and MUST be authority- and freshness-tagged before entering ContextSnapshot or supporting a user-facing claim. SQLite-discovered schema state MUST NOT silently redefine Nexora’s canonical persistence schema, requirements, decisions, lifecycle, or security policy. Mutating operations require their existing permission and side-effect rules; a timeout or transport interruption does not imply commit success. This is a cross-reference to existing authorities, not a new SQLite lifecycle, error, permission, or database schema.

## Phase Mapping

- **Phase 3**: SQLite available in sandbox.
- **Phase 6**: Memory system uses SQLite.


## Traceability Closure

- `requirements/FR.md` and `requirements/NFR.md` define the requirement layer.
- `specs/DATABASE_SCHEMA.md` defines the authoritative persistent storage shape.
- `architecture/RUNTIME.md` and `architecture/MEMORY_SYSTEM.md` define runtime and memory behavior that depend on persistence.
- `decisions/DEC-13-conversation-identity-persistence.md` and `decisions/DEC-14-session-conversation-relationship-semantic-status.md` through `decisions/DEC-21-session-conversation-continuation-recovery.md` define the conversation/session semantics that the schema must preserve.

This document does not choose storage technology beyond the repository’s existing SQLite/Room-oriented schema authority.
