> **Status: DERIVED** for Workspace domain model.
> This document defines the shape and semantics of Workspace in the data model.
>
> Depends on: the canonical runtime and workspace architecture sources.
> Referenced by: tasks, sessions, files, tools, memory, and orchestration implementations.

# Domain Model: Workspace

```kotlin
data class Workspace(
    val id: String,
    val ownerId: String,
    val status: WorkspaceStatus,
    val createdAt: Instant,
    val updatedAt: Instant,
    val archivedAt: Instant? = null
)

enum class WorkspaceStatus {
    CREATED,
    ACTIVE,
    SUSPENDED,
    ARCHIVED,
    DELETED
}
```

## Lifecycle and Workspace Semantics

Workspace lifecycle authority is defined in [lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md). Workspace lifecycle governs durable availability and ownership context for contained sessions, tasks, files, tools, and memory operations.
