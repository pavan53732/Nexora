> **Status: DERIVED** for Session domain model.
> This document defines the shape and semantics of Session in the data model.
>
> Depends on: the canonical runtime and context-management sources.
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

enum class SessionStatus {
    CREATED,
    ACTIVE,
    IDLE,
    CLOSED,
    EXPIRED
}
```

## Lifecycle and Session Semantics

Session lifecycle authority is defined in [lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md). Session state is durable runtime context, not a substitute for task or execution lifecycle state. When a session is associated with a live execution, it SHOULD retain the active `correlationId` for observability and replay alignment.
