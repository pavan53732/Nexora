> **Status: DERIVED** for Agent entity shape.
> This document defines the data model for Agent. The explicit lifecycle/behavior authority is [state-machines/AgentLifecycle.md](../state-machines/AgentLifecycle.md).
>
> Depends on: the canonical architecture and lifecycle sources for Agent.
> Referenced by: APIs, SDKs, protocols, and tests that consume Agent.


# Domain Model: Agent

> Canonical domain model. See [architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md).

```kotlin
package com.nexora.app.runtime.agents

/**
 * An agent instance running in a specific workspace.
 */
data class AgentInstance(
    val id: String,            // UUID
    val type: AgentType,        // Planner, Coder, etc.
    val name: String,           // Display name
    val workspaceId: String,    // Which workspace this agent belongs to
    val status: AgentStatus,    // IDLE, THINKING, EXECUTING, WAITING, ERROR
    val currentTaskId: String?, // Task being executed
    val createdAt: Instant,
    val lastActiveAt: Instant
)

enum class AgentType {
    PLANNER, RESEARCHER, CODER, REVIEWER, TESTER, DEBUGGER,
    DOCUMENTATION_WRITER, REFACTORING, DEPLOYMENT, SECURITY_AUDITOR,
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR, ARCHITECT,
    CUSTOM  // CUSTOM = user-defined agents, NOT a built-in type (16 built-ins: AGT-001..AGT-016)
}

enum class AgentStatus { IDLE, THINKING, EXECUTING, WAITING, ERROR, CANCELLED }
```

## Lifecycle and Execution Semantics

`lifecycleState` is the durable state-machine value defined by [state-machines/AgentLifecycle.md](../state-machines/AgentLifecycle.md). `executionPhase` is transient runtime activity and MUST NOT replace lifecycle state.

```kotlin
enum class AgentLifecycleState { CREATED, CONFIGURED, READY, RUNNING, PAUSED, WAITING_APPROVAL, REFLECTING, COMPLETING, COMPLETED, FAILED, CANCELLED }
enum class AgentExecutionPhase { NONE, PLANNING, ACTING, OBSERVING, REFLECTING, FINALIZING }
```

The legacy `status` field is not a second authority. If retained for compatibility, it MUST be a projection: `IDLE` for `CREATED`, `CONFIGURED`, or `READY`; `THINKING` for `PLANNING` or `REFLECTING`; `EXECUTING` for `ACTING` or `OBSERVING`; `WAITING` for `PAUSED` or `WAITING_APPROVAL`; `ERROR` for `FAILED`; and `CANCELLED` for `CANCELLED`. `COMPLETING` and `COMPLETED` require an explicit API representation and MUST NOT be silently collapsed.
