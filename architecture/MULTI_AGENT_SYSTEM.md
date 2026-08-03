# Multi-Agent System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [AGENT_RUNTIME.md](AGENT_RUNTIME.md) | [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md)

---

## Overview

Nexora supports multiple collaborating agents within a workspace. Each agent has a specialized role. Agents share memory, workspace, tasks, and execution context.

## Built-in Agent Roles

| Agent | Role | Phase |
|-------|------|-------|
| **Planner** | Decomposes goals into structured execution plans. | 7 |
| **Researcher** | Gathers information, searches, reads documentation. | 7 |
| **Coder** | Writes, modifies, and refactors code. | 7 |
| **Reviewer** | Reviews code changes for correctness and quality. | 7 |
| **Tester** | Writes and executes tests. | 7 |
| **Debugger** | Diagnoses and fixes bugs and errors. | 7 |
| **Documentation Writer** | Generates docs, comments, READMEs. | 7 |
| **Refactoring Agent** | Restructures code for maintainability. | 7 |
| **Deployment Agent** | Handles build, packaging, deployment. | 7 |
| **Security Auditor** | Scans for vulnerabilities. | 7 |
| **Browser Agent** | Automates browser interactions. | 7 |
| **Database Agent** | Manages database operations. | 7 |
| **File Manager** | Handles file operations and organization. | 7 |
| **Git Agent** | Manages version control workflows. | 7 |
| **Workflow Coordinator** | Orchestrates multi-agent task delegation. | 7 |

## Agent Interface

```kotlin
interface Agent {
    val id: String
    val type: AgentType
    val name: String
    val description: String
    val capabilities: List<String>
    val defaultTools: List<String>

    suspend fun execute(task: AgentTask, context: AgentContext): AgentResult
}

enum class AgentType {
    PLANNER, RESEARCHER, CODER, REVIEWER, TESTER, DEBUGGER,
    DOCUMENTATION_WRITER, REFACTORING, DEPLOYMENT, SECURITY_AUDITOR,
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR
}
```

## Shared Context

Agents within a workspace share:

- **Memory** — Access to same memory stores (scoped permissions).
- **Workspace** — Same project files and directories.
- **Tasks** — Shared task queue for delegation and handoff.
- **Execution Context** — Can see each other's recent activity.
- **Artifacts** — Can produce and consume shared artifacts.

## Communication Flow

```
Workflow Coordinator
    |
    v
Delegates to Planner Agent -> Produces execution plan
    |
    v
Delegates to Coder Agent -> Implements code
    |
    v
Delegates to Tester Agent -> Writes and runs tests
    |
    v
Delegates to Reviewer Agent -> Reviews changes
    |
    v
Results aggregated -> Workflow Coordinator combines results
    |
    v
Report to user
```

## Agent Registry

```kotlin
class AgentRegistry {
    private val agentTypes = mutableMapOf<AgentType, Agent>()

    fun register(agent: Agent)
    fun create(type: AgentType, workspaceId: String): AgentInstance
    fun listAvailable(): List<AgentType>
    fun getInstance(agentId: String): AgentInstance?
}
```

## Phase Mapping

- **Phase 7**: All 15 agent types, agent registry, task delegation.
- **Phase 8**: Community agent plugins.
