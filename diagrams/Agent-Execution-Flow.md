> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Agent Execution Flow

This diagram illustrates the full lifecycle of a user goal from submission through the agent loop to UI update. The agent iterates — planning, calling the provider, executing tools, and storing results — until the task is complete.

> **Guard conditions:** every transition shown here is enforced by the
> [Agent Lifecycle state machine](../state-machines/AgentLifecycle.md) — e.g.
> terminal states (Completed/Failed/Cancelled) can never re-enter Running;
> `start()` requires `Ready`; `retry()` is bounded by max retries. The sequence
> below assumes those guards hold.

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant AgentManager
    participant AgentLoop
    participant Planner
    participant Provider
    participant Executor
    participant ToolManager
    participant Sandbox
    participant Memory
    participant EventBus

    User->>UI: Send goal ("Build a report")
    UI->>AgentManager: createAgent(goal, workspaceId)
    AgentManager->>AgentLoop: start(agent)
    AgentManager-->>UI: AgentCreated event
    EventBus-->>UI: AgentState.RUNNING

    loop Until task complete or max cycles
        AgentLoop->>Planner: createPlan(context, goal)
        Planner-->>AgentLoop: Plan(steps)

        AgentLoop->>Provider: generateResponse(messages, tools)
        Provider-->>AgentLoop: Response(toolCalls, text)

        AgentLoop->>Executor: execute(toolCalls)
        Executor->>ToolManager: resolve(toolCall)
        ToolManager-->>Executor: Tool instance

        Executor->>ToolManager: checkPermission(tool)
        ToolManager-->>Executor: Permission granted

        Executor->>Sandbox: execute(tool, params)
        Sandbox-->>Executor: ToolResult

        Executor-->>AgentLoop: ExecutionResult(results)

        AgentLoop->>Memory: store(results, context)
        Memory-->>AgentLoop: Updated context

        AgentLoop->>EventBus: publish(ToolExecutedEvent)
        EventBus-->>UI: Update output panel
    end

    AgentLoop->>EventBus: publish(TaskCompletedEvent)
    EventBus-->>UI: AgentState.COMPLETED
    UI-->>User: Display final result

    alt Error during execution
        AgentLoop->>EventBus: publish(TaskFailedEvent, error)
        EventBus-->>UI: AgentState.FAILED
        UI-->>User: Display error
    end

    opt User cancels
        User->>UI: Tap cancel
        UI->>AgentManager: cancelAgent(agentId)
        AgentManager->>AgentLoop: cancel()
        AgentLoop->>EventBus: publish(TaskCancelledEvent)
        EventBus-->>UI: AgentState.CANCELLED
    end
```