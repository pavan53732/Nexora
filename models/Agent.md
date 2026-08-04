> **Status: DERIVED** for Agent domain model.
> This document defines the shape and semantics of Agent in the data model.
>
> Depends on: the canonical architecture document for Agent.
> Referenced by: protocols, APIs, SDKs, and storage implementations.

# Domain Model: Agent

```kotlin
data class Agent(
    val id: String,
    val version: String,
    val name: String,
    val type: AgentType,
    val description: String,
    val declaredSkills: List<String>,
    val requiredPermissions: List<String>,
    val supportsDelegation: Boolean,
    val supportsBackgroundExecution: Boolean,
    val status: AgentStatus,
    val createdAt: Instant,
    val updatedAt: Instant
)

enum class AgentStatus {
    DISCOVERED,
    REGISTERED,
    READY,
    RUNNING,
    PAUSED,
    ERROR,
    DISABLED
}
```

## Lifecycle and Execution Semantics

Agent identity (`id`) is stable across versions of the same registered agent. Runtime task execution uses `correlationId` and stable `taskId` values for execution tracking, while durable lifecycle transitions use committed versioned projections rather than transient in-memory status alone.
