# ADR-0003: Autonomous Agent Runtime Loop

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect
- **Related**: [ADR-0006-Agent-First-Interaction-Model](./ADR-0006-Agent-First-Interaction-Model.md) — user notification happens via chat activity feed, not generic OS notification

## Context

There are two approaches to building an AI agent application:

1. **Request-Response**: The user sends a message, the AI responds. The AI is stateless between messages. This is how chatbots work.

2. **Autonomous Loop**: The user gives a goal. The AI enters a loop: plan, execute, reflect, repeat. The AI maintains state across iterations. This is how Cursor, Cline, and Claude Code work.

Nexora's purpose is autonomous task execution. A request-response model cannot handle multi-step workflows, background execution, checkpointing, or resume-after-restart.

## Decision

Nexora implements an **autonomous agent runtime loop**:

```
WHILE goal_is_not_complete:
    1. REFLECT on current state
    2. PLAN next actions
    3. BUILD context
    4. CALL AI provider
    5. PARSE response (text + tool calls)
    6. EXECUTE tools in sandbox
    7. STORE results in memory
    8. EVALUATE completion
    9. SAVE checkpoint
    10. STREAM results to conversation activity feed (per ADR-0006; not a generic OS notification — tool output, file diffs, and execution logs surface as activity cards in the chat interface)
```

Key properties:
- The loop runs as an Android **Foreground Service** for background execution.
- State is periodically saved as **checkpoints** for crash recovery.
- The user can **cancel** at any iteration.
- **Token budgeting** prevents infinite loops.
- **Human approval gates** pause the loop for sensitive operations.

## Consequences

### Positive
- **True autonomy**: Agents complete complex multi-step tasks without human intervention.
- **Resilience**: Checkpoints allow recovery from crashes and restarts.
- **Transparency**: Every iteration is logged and observable.

### Negative
- **Resource consumption**: Long-running loops consume CPU, memory, and network.
- **Complexity**: Checkpointing, cancellation, and background execution add significant implementation complexity.
- **Token cost**: Each iteration consumes tokens. Without budgeting, costs can spiral.

### Mitigation
- Enforce configurable resource quotas per workspace.
- Use Android WorkManager for efficient background scheduling.
- Implement hard token budget limits with user-configurable thresholds.
