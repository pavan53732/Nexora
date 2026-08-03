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
