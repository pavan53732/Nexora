> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Tool Execution Flow

This diagram shows the resolved path when an agent requests a tool invocation — from permission checks through sandboxed execution to result storage and event propagation.

```mermaid
sequenceDiagram
    participant Agent
    participant ToolManager
    participant PermissionManager
    participant User
    participant Tool
    participant Sandbox
    participant Memory
    participant EventBus

    Agent->>ToolManager: executeTool(toolCall)
    ToolManager->>ToolManager: resolve(toolCall.name)
    ToolManager-->>Agent: ToolDefinition

    ToolManager->>PermissionManager: checkPermission(tool, agent)

    alt Permission AUTO
        PermissionManager-->>ToolManager: GRANTED
    else Permission ASK
        PermissionManager-->>ToolManager: REQUIRE_USER_APPROVAL
        ToolManager-->>User: Show permission dialog
        User-->>ToolManager: Approve / Deny
        alt User denies
            ToolManager-->>Agent: PermissionDeniedResult
        end
    else Permission DENY
        PermissionManager-->>ToolManager: DENIED
        ToolManager-->>Agent: PermissionDeniedResult
    end

    ToolManager->>Sandbox: execute(tool, params)
    Sandbox->>Tool: invoke(params)
    Tool-->>Sandbox: raw result
    Sandbox->>Sandbox: sanitizeOutput(raw)
    Sandbox-->>ToolManager: ToolResult

    ToolManager->>Memory: storeResult(toolCall.id, result)
    Memory-->>ToolManager: stored

    ToolManager->>EventBus: publish(ToolExecutedEvent)
    ToolManager-->>Agent: ToolResult
```
