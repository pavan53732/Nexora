# System Design — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Execution Flow

```
User Goal (entered in Chat, inside a Workspace)
    ↓
Planner → Task Decomposition
    ↓
Context Builder → Assemble Context (memory + files + history + system prompt)
    ↓
AI Provider → Generate Response (with tool calls)
    ↓
Tool Manager → Validate & Route Tools
    ↓
Permission Manager → Check / Prompt Approval
    ↓
Executor → Execute in Sandbox
    ↓
Memory Manager → Store Results
    ↓
Observability → Log Everything
    ↓
Loop (reflect, plan next step, or complete)
```

## Agent Loop

```
WHILE goal_is_not_complete:
    1. REFLECT on current state and progress
    2. PLAN next action(s)
    3. BUILD context (memory + files + history + system prompt)
    4. CALL AI provider with context
    5. PARSE response (text + tool calls)
    6. FOR EACH tool call:
        a. CHECK permissions
        b. EXECUTE in sandbox
        c. COLLECT results
        d. STORE in memory
        e. LOG to observability
    7. EVALUATE: is the goal complete?
    8. SAVE checkpoint
    9. NOTIFY user of progress
```

## Workspace Model

```
Workspace (primary entity)
│
├── Agents (Planner, Coder, Researcher, etc.)
├── Tasks (Active, Completed, History)
├── Files (Virtual file system)
├── Memory (Session, Project, Long-term)
├── Terminal (Multiple sessions)
├── Plugins (Installed + Config)
├── Logs (Execution + Audit)
├── Settings (Per-workspace config)
└── Chats (Conversations — one artifact among many)
```

## Workspace Configuration

```json
{
  "name": "My Project",
  "description": "Project description",
  "created_at": "2026-08-03T00:00:00Z",
  "updated_at": "2026-08-03T00:00:00Z",
  "settings": {
    "default_agent": "coder",
    "default_provider": "openai",
    "default_model": "gpt-4o",
    "sandbox_limits": {
      "max_memory_mb": 512,
      "max_disk_mb": 1024,
      "max_processes": 10,
      "network_allowed": true
    },
    "tool_permissions": {
      "network:http": "ask",
      "sandbox:write": "allow",
      "device:camera": "deny"
    }
  }
}
```

## Observability Data Model

```kotlin
data class ExecutionEvent(
    val id: String,
    val timestamp: Instant,
    val agentId: String,
    val taskId: String,
    val eventType: EventType,
    val data: JsonObject,
    val durationMs: Long?,
    val tokenUsage: TokenUsage?,
    val status: EventStatus
)
```

## Observability Components

| Component | Description |
|-----------|-------------|
| **Live logs** | Real-time streaming log viewer. |
| **Execution timeline** | Visual timeline of operations in a task. |
| **Tool invocations** | Every tool call: params, duration, result, errors. |
| **Terminal output** | Complete terminal session capture. |
| **Errors** | Centralized error tracking with stack traces. |
| **Performance metrics** | CPU, memory, disk, network over time. |
| **Token usage** | Per request, session, provider, model. |
| **API usage** | Call count, latency, success rate per provider. |
| **Execution history** | Complete history of all task executions. |
