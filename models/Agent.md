> **Status: DERIVED** for Agent domain model.
> This document defines the shape and semantics of Agent in the data model.
>
> Depends on: the canonical architecture document for Agent.
> Referenced by: protocols, APIs, SDKs, and storage implementations.

# Domain Model: Agent

```kotlin
data class Agent(
    val id: String,
    val version: Long,
    val name: String,
    val type: AgentType,
    val description: String,
    val declaredSkills: List<String>,
    val requiredPermissions: List<String>,
    val supportsDelegation: Boolean,
    val supportsBackgroundExecution: Boolean,
    val status: AgentStatus,
    val phase: AgentExecutionPhase,
    val createdAt: Instant,
    val updatedAt: Instant
)

enum class AgentType {
    PLANNER, RESEARCHER, CODER, REVIEWER, TESTER, DEBUGGER,
    DOCUMENTATION_WRITER, REFACTORING, DEPLOYMENT, SECURITY_AUDITOR,
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR, ARCHITECT, CUSTOM
}

enum class AgentStatus {
    CREATED,
    CONFIGURED,
    READY,
    RUNNING,
    PAUSED,
    WAITING_APPROVAL,
    REFLECTING,
    COMPLETING,
    COMPLETED,
    FAILED,
    CANCELLED
}

enum class AgentExecutionPhase {
    IDLE,
    PLANNING,
    THINKING,
    EXECUTING_TOOL,
    BUILDING_CONTEXT,
    WAITING,
    COMPLETING,
    TERMINATED
}
```

## Lifecycle and Execution Semantics

Agent identity (`id`) is stable across versions of the same registered agent. Runtime task execution uses `correlationId` and stable `taskId` values for execution tracking.

### Durable Status vs. Transient Phase

To eliminate semantic ambiguity and guarantee behavioral equivalence, Nexora strictly separates high-level lifecycle state from low-level loop activity:
- `status: AgentStatus` represents the durable lifecycle state persisted transactionally in the database.
- `phase: AgentExecutionPhase` represents the transient execution phase. During active running loops, phase transitions are held in transient memory, stored within execution checkpoints, and published to the Event Bus to drive real-time UI.

### State-to-Phase Mapping & Recovery Constraints

| Status (`AgentStatus`) | Valid Active Phases (`AgentExecutionPhase`) | Recovery Behavior |
|---|---|---|
| `CREATED` | `IDLE` | Non-executing; no recovery. |
| `CONFIGURED` | `IDLE` | Non-executing; no recovery. |
| `READY` | `IDLE` | Non-executing; no recovery. |
| `RUNNING` | `PLANNING`, `THINKING`, `EXECUTING_TOOL`, `BUILDING_CONTEXT`, `WAITING` | Active execution. Recoverable from the latest checkpoint. |
| `PAUSED` | `IDLE` | Suspended. Recoverable; resumes into `PAUSED` state. |
| `WAITING_APPROVAL` | `WAITING` | Human-in-the-loop block. Recoverable; resumes in `WAITING` phase. |
| `REFLECTING` | `THINKING` | Active self-review. Recoverable from latest checkpoint. |
| `COMPLETING` | `COMPLETING` | Finalizing execution. Recoverable. |
| `COMPLETED` | `TERMINATED` | Terminal state; no recovery. |
| `FAILED` | `TERMINATED` | Terminal state; no recovery. Can be retried (re-enters `READY`). |
| `CANCELLED` | `TERMINATED` | Terminal state; no recovery. |

During recovery from process death, if the database records `status` as `RUNNING`, `REFLECTING`, or `WAITING_APPROVAL`, the engine reads the latest checkpoint. This checkpoint contains the serialized memory, token budget, step history, and the exact `AgentExecutionPhase` at the time of the checkpoint. The execution resumes precisely at that phase boundary.
