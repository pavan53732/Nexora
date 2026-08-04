> **Status: DERIVED** for Workspace domain model.
> This document defines the shape and semantics of Workspace in the data model.
>
> Depends on: the canonical runtime/workspace sources and [lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md).
> Referenced by: runtime, files, memory, tasks, and project ownership semantics.

# Domain Model: Workspace

```kotlin
data class Workspace(
    val id: String,
    val name: String,
    val status: WorkspaceStatus,
    val createdAt: Instant,
    val updatedAt: Instant,
    val archivedAt: Instant? = null
)
```

Workspace is the durable project boundary for tasks, memory, files, sessions, and execution ownership. Lifecycle state authority is defined in [lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md).
