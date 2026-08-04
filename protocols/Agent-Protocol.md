> **Status: DERIVED** for Agent message contract.
> This document defines protocol messages for Agent. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Agent.
> Referenced by: models, APIs, SDKs, and tests.


# Agent Protocol — Nexora

> Communication contract between the runtime and agents.

## Flow

1. Runtime creates a `StartTaskRequest` with `requestId`, `correlationId`, workspace identity, caller identity, and task goal.
2. Runtime calls the Agent API to start work; the agent runtime materializes or reuses a stable `taskId`.
3. Agent enters the agent loop (reflect, plan, execute, repeat) and emits lifecycle-safe progress events.
4. Runtime publishes events only after durable state transitions are committed.
5. Agent returns a terminal `TaskProjection` or canonical error outcome.

## Message Rules

Every protocol message tied to task execution MUST include:

- `correlationId`
- `workspaceId`
- `agentId`
- `taskId` once assigned
- durable `version` on lifecycle events
- canonical error envelope on terminal failure

Client retries MUST preserve the same `idempotencyKey` when resubmitting the same logical start request. Long-running or resumable streams MUST use opaque `resumeToken` values rather than transport-specific offsets.

## Events Published

| Event | When | Required payload |
|-------|------|--------|
| `AgentStatusChanged` | Agent status changes | `{correlationId, agentId, workspaceId, oldStatus, newStatus, version}` |
| `TaskProgress` | Agent completes a step | `{correlationId, taskId, workspaceId, stepIndex, totalSteps, description, version}` |
| `ToolExecuted` | Agent invokes a tool | `{correlationId, taskId, toolCallId, toolId, durationMs, success, version}` |
| `AgentError` | Agent encounters a terminal or surfaced error | `{correlationId, agentId, taskId, code, retryability, lifecycleEffect, recoverable, version}` |

Events are at-least-once and MUST be deduplicated by `(entityId, version, transition)`.

## Cancellation

Cancellation MUST propagate from runtime to the active agent loop, child tasks, delegated work, and in-flight tool/provider operations. A cancelled task is terminal only after the durable cancellation state is committed and the terminal lifecycle event is published.
