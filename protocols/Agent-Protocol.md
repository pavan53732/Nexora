> **Status: DERIVED** for Agent message contract.
> This document defines protocol messages for Agent. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Agent.
> Referenced by: models, APIs, SDKs, and tests.


# Agent Protocol — Nexora

> Communication contract between the runtime and agents.

## Flow

1. Runtime creates an `AgentTask` with a goal and workspace ID.
2. Runtime calls `agent.execute(task, context)`.
3. Agent enters the agent loop (reflect, plan, execute, repeat).
4. Agent publishes events to the Event Bus at each step.
5. Agent returns an `AgentResult` when the goal is complete (or fails).

## Events Published

| Event | When | Payload |
|-------|------|--------|
| `AgentStatusChanged` | Agent status changes | `{agentId, oldStatus, newStatus}` |
| `TaskProgress` | Agent completes a step | `{taskId, stepIndex, totalSteps, description}` |
| `ToolExecuted` | Agent invokes a tool | `{toolCallId, toolId, durationMs, success}` |
| `AgentError` | Agent encounters an error | `{agentId, taskId, message, recoverable}` |

## Cancellation

The runtime can set a `Job` cancellation flag. The agent loop checks this flag at each iteration and exits gracefully.
