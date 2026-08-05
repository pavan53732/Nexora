> **Status: DERIVED** for Workspace domain model.
> This document defines the shape and semantics of Workspace in the data model.
>
> Depends on: the canonical runtime and workspace architecture sources.
> Referenced by: tasks, sessions, files, tools, memory, and orchestration implementations.

# Domain Model: Workspace

```kotlin
// S1 — Dynamic concurrency cap: enforced by ResourceManager using
// min(memory_budget/per_agent_est, cpu_cores, configurable_max)
// Default: 3; High-end: 8–16 (see MULTI_AGENT_SYSTEM.md SA-3)
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

Workspace lifecycle authority is defined in [lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md). The canonical state machine is [state-machines/WorkspaceLifecycle.md](../state-machines/WorkspaceLifecycle.md). Workspace lifecycle governs durable availability and ownership context for contained sessions, tasks, files, tools, and memory operations.
