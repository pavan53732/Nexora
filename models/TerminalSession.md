> **Status: DERIVED** for TerminalSession domain model.
> This document defines the shape and semantics of TerminalSession in the data model.
>
> Depends on: the canonical sandbox and terminal specifications.
> Referenced by: tool execution, sandbox, and runtime implementations.

# Domain Model: TerminalSession

```kotlin
data class TerminalSession(
    val id: String,
    val workspaceId: String,
    val correlationId: String?,
    val status: TerminalSessionStatus,
    val sandboxId: String,
    val startedAt: Instant,
    val updatedAt: Instant,
    val endedAt: Instant? = null
)
```

Terminal session lifecycle is subordinate to sandbox and tool execution policy. A terminal session MAY participate in a correlated task or tool-call execution, but it MUST NOT become the primary authority for task or execution lifecycle state.
