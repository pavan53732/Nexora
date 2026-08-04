> **Status: DERIVED** for Task domain model.
> This document defines the shape and semantics of Task in the data model.
>
> Depends on: the canonical architecture and task lifecycle sources.
> Referenced by: protocols, APIs, SDKs, and storage implementations.

# Domain Model: Task

```kotlin
data class Task(
    val id: String,
    val workspaceId: String,
    val agentId: String,
    val correlationId: String,
    val parentTaskId: String?,
    val status: TaskStatus,
    val phase: ExecutionPhase,
    val version: Long,
    val goal: String,
    val input: JsonObject,
    val output: JsonObject?,
    val childTaskIds: List<String>,
    val delegatedAgentIds: List<String>,
    val createdAt: Instant,
    val updatedAt: Instant,
    val completedAt: Instant? = null,
    val latestError: CanonicalErrorEnvelope? = null
)
```

## Lifecycle and Execution Semantics

`status` is a durable lifecycle projection aligned to [state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md). `phase` represents transient execution phase and MUST NOT replace lifecycle state. Task identity and `correlationId` remain stable throughout retries of the same logical task once assigned.
