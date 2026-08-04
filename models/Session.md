> **Status: DERIVED** for Session domain model.
> This document defines the shape and semantics of Session in the data model.
>
> Depends on: the canonical runtime and context-management sources, and [lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md).
> Referenced by: memory, execution, and orchestration implementations.

# Domain Model: Session

```kotlin
data class Session(
    val id: String,
    val workspaceId: String,
    val correlationId: String?,
    val status: SessionStatus,
    val activeTaskId: String?,
    val activeAgentId: String?,
    val createdAt: Instant,
    val updatedAt: Instant,
    val closedAt: Instant? = null
)
```

Session state is durable runtime context, not a substitute for task or execution lifecycle state. When a session is associated with a live execution, it SHOULD retain the active `correlationId` for observability and replay alignment. Lifecycle state authority is defined in [lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md).
