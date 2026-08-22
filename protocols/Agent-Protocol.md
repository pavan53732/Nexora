> **Status: DERIVED** for Agent message contract.
> This document defines protocol messages for Agent. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Agent; [../state-machines/AgentLifecycle.md](../state-machines/AgentLifecycle.md) for Agent lifecycle transitions; and [../state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md) for Task lifecycle transitions.
> Referenced by: models, APIs, SDKs, and tests.


# Agent Protocol — Nexora

> Communication contract between the runtime and agents.


> **DEC-7 (2026-08-11):** `RetryPending` is EPHEMERAL (does not survive process death). Idempotency scope is per-Execution. RetryPending retry (PATH A) preserves the same `executionId` and idempotency boundary; explicit retry after a committed terminal state via `retryExecution` (PATH B) creates a new `executionId` (with `priorExecutionId`) and a new idempotency boundary. See [../decisions/DEC-7-retry-attempt-state.md](../decisions/DEC-7-retry-attempt-state.md).

## Flow

1. Runtime creates a `StartTaskRequest` with `requestId`, `correlationId`, workspace identity, caller identity, and task goal.
2. Runtime calls the Agent API to start work; the agent runtime materializes or reuses a stable `taskId`.
3. The existing runtime classifies the user goal or intent and automatically selects the minimum sufficient existing agent, skill, Tool, provider capability, execution mode, and evidence target. The selection rationale is derived planning/observability data and does not authorize execution.
4. When the intent is security-related, the coordinator MAY compose existing Security Auditor, Researcher, Architect, Tester, and Reviewer roles within the declared authorized scope and existing permission, sandbox, network, audit, deadline, resource, and evidence gates. No unrestricted offensive mode or new agent type is implied.
5. Agent enters the agent loop (reflect, plan, execute, repeat) and emits lifecycle-safe progress events.
6. Runtime publishes events only after durable state transitions are committed.
7. Agent returns a terminal `TaskProjection` or canonical error outcome.

When a Tool approval transaction is denied or expires, the protocol preserves one correlated outcome: Tool `NXR-2003` denial with its subreason and no side effect; Task `Failed`; and, when the participating Agent remains available, Agent `Paused`. The Agent pause does not resume or alter the failed Task. Any later operation requires a new approval transaction and is not an automatic retry.

## Intent-Driven Routing Events

When automatic routing applies, the existing task and agent trace SHOULD expose selected agent IDs, skill IDs, Tool IDs, provider capabilities, bounded selection rationale, evidence target, and omitted or unavailable capability. These fields are derived planning and observability projections over the existing task/execution lineage. Missing values MUST remain unknown or unavailable; generated confidence MUST NOT substitute for evidence.

Routing and delegation results MUST preserve the existing `workspaceId`, `taskId`, `executionId` when assigned, `agentId`, `correlationId`, acceptance criteria, provenance, verification state, and final disposition. A selected role or capability MUST NOT self-authorize a Tool, permission, lifecycle transition, capability escalation, external side effect, or claim of successful execution.

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
| `AgentStatusChanged` | Agent status or execution phase changes | `{correlationId, agentId, workspaceId, oldStatus, newStatus, phase, version}` |
| `TaskProgress` | Agent completes a step | `{correlationId, taskId, workspaceId, stepIndex, totalSteps, description, version}` |
| `ToolExecuted` | Agent invokes a tool | `{correlationId, taskId, toolCallId, toolId, durationMs, success, version}` |
| `AgentError` | Agent encounters a terminal or surfaced error | `{correlationId, agentId, taskId, code, retryability, lifecycleEffect, recoverable, version}` |
| `TaskSuspended` | Execution/checkpoint subsystem suspends active work for an existing platform/runtime trigger | `{correlationId, taskId, executionId, checkpointId, cause, version}`; owned by `Execution-Protocol`, not an Agent or Task lifecycle state |
| `CheckpointSaved` | Execution checkpoint transaction commits successfully | `{correlationId, executionId, checkpointId, version}`; owned by `Execution-Protocol` and emitted only after durable commit |

Events are at-least-once and MUST be deduplicated by `(entityId, version, transition)`.

- `AgentStatusChanged` events carry both the durable lifecycle state (`oldStatus`/`newStatus`) and the transient execution phase (`phase`).

## Cancellation

Cancellation MUST propagate from runtime to the active agent loop, child tasks, delegated work, and in-flight tool/provider operations. A cancelled task is terminal only after the durable cancellation state is committed and the terminal lifecycle event is published.

## Inference Stream Events

Agent progress projects provider events without redefining provider wire semantics:

| Event | Meaning |
|---|---|
| `InferenceStarted` | Route/context/reasoning policy committed; contains requestId and streamId. |
| `InferenceDelta` | Provisional text, citation, or redacted reasoning-summary update. |
| `ToolCallReady` | Fully assembled, schema-valid Tool call is ready for authorization. |
| `InferenceReconnecting` | Native resume attempt in progress; provisional output remains partial. |
| `InferenceRestarted` | New stream attempt with priorStreamId lineage; never byte-spliced. |
| `InferenceTerminal` | Final committed response, usage, claim-level evidence records, and finish reason; no claim crosses the user boundary without its required ClaimRecord disposition. |
| `InferenceFailed` | Canonical error and explicit partial-output state. |
| `InferenceCancelled` | Cancellation committed across Agent, Provider, and Tool children. |

Every inference event carries `requestId`, `streamId`, `correlationId`, `taskId`,
`sequence`, and provisional/terminal status. An `InferenceTerminal` payload MUST carry
or reference the `ClaimRecord` entries produced by the Evidence & Validation Engine.
Agent consumers deduplicate by `(streamId, sequence)`; durable task lifecycle events
continue using entity version.
