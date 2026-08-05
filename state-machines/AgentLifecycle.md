> **Status: CANONICAL** for agent lifecycle states and transitions.
> This document owns the formal agent state machine: Created, Configured, Ready, Running, Paused, WaitingApproval, Reflecting, Completing, Completed, Failed, Cancelled.
> It does NOT own the agent runtime loop (see [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md)).
>
> Depends on: [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md).
> Referenced by: [../models/Agent.md](../models/Agent.md), [../docs/api/Agent-API.md](../docs/api/Agent-API.md).

# Agent Lifecycle State Machine

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

The Agent Lifecycle governs the runtime state of every autonomous agent instance in Nexora. From creation through execution to termination, each agent follows a strict progression ensuring that agents are properly configured before execution and can safely recover from failures or user interventions.

## States

| State | Description |
|-------|-------------|
| **Created** | Agent instance allocated; no configuration applied. |
| **Configured** | System prompt, model binding, tools, and constraints set. |
| **Ready** | All prerequisites validated; awaiting execution signal. |
| **Running** | Actively executing a task loop (plan → act → observe). |
| **Paused** | Execution suspended by user or system policy. Resumable. |
| **WaitingApproval** | Blocked on a human-in-the-loop approval gate. |
| **Reflecting** | Performing self-evaluation or plan revision. |
| **Completing** | Finalizing results, persisting artifacts, releasing resources. |
| **Completed** | Terminal state — agent finished successfully. |
| **Failed** | Terminal state — unrecoverable error encountered. |
| **Cancelled** | Terminal state — explicitly cancelled by user or system. |

## Durable Status vs. Transient Execution Phase

To resolve semantic ambiguity and ensure behavioral equivalence, Nexora strictly separates the **durable agent lifecycle state** (`AgentStatus`) from the **transient runtime execution phase** (`AgentExecutionPhase`).

1. **Durable Lifecycle State (`AgentStatus`)**: Tracks governance, transactional boundaries, and persistence-readiness. Persisted in the database.
2. **Transient Execution Phase (`AgentExecutionPhase`)**: Tracks the exact operation of the autonomous agent loop at any millisecond. Memory-resident, saved in checkpoints, and streamed to the UI.

### Compatibility & Mapping Matrix

| Durable State (`AgentStatus`) | Allowed Transient Phases (`AgentExecutionPhase`) | Description / Meaning |
|---|---|---|
| **CREATED** | `IDLE` | Instance allocated; no configuration or goal applied. |
| **CONFIGURED** | `IDLE` | System prompt, tools, permissions, and provider bound. |
| **READY** | `IDLE` | Target goal validated, constraints cleared; ready to run. |
| **RUNNING** | `PLANNING`, `THINKING`, `EXECUTING_TOOL`, `BUILDING_CONTEXT`, `WAITING` | Loop active; executing planner, calling provider, running tool, or preparing context. |
| **PAUSED** | `IDLE` | Loop suspended. Retains memory and checkpoint. Resumable. |
| **WAITING_APPROVAL** | `WAITING` | Blocked waiting on a human permission decision or confirmation. |
| **REFLECTING** | `THINKING` | Active self-review, plan repair, or verification analysis. |
| **COMPLETING** | `COMPLETING` | Finalizing artifacts, updating memory systems, compiling report. |
| **COMPLETED** | `TERMINATED` | Terminal success. Resources released, execution frozen. |
| **FAILED** | `TERMINATED` | Terminal failure. Carries canonical error; ready for retry. |
| **CANCELLED** | `TERMINATED` | Terminal cancellation. Gracefully aborted; partial state saved. |

### Operational Semantics & Enforcement

- **Persistence Boundaries**:
  - `AgentStatus` transitions MUST be transactionally persisted in the local SQLite database. Transitions evaluate guards, acquire write locks, commit the state and increment the entity `version`, and then emit the event to the Event Bus.
  - `AgentExecutionPhase` is primarily memory-resident. To avoid database write-amplification during rapid loops, phase updates are published as lightweight events. However, the current phase MUST be persisted within the **Execution Checkpoint** (at least every 30s) to enable seamless crash recovery.
- **Checkpoint & Recovery Rules**:
  - Upon application crash or reboot, the system scans for agents with active status (`RUNNING`, `REFLECTING`, `WAITING_APPROVAL`).
  - Active agents are re-hydrated from their latest checkpoint, restoring their `AgentExecutionPhase` (e.g. restoring back to `PLANNING` or `WAITING` for approval) and resuming the loop at that exact phase boundary.
  - Terminal states (`COMPLETED`, `FAILED`, `CANCELLED`) are frozen and never recovered.
- **UI & Event Bus Projections**:
  - Event payloads (such as `AgentStatusChanged` or `TaskProgress`) carry both `AgentStatus` and `AgentExecutionPhase`.
  - The UI renders coarse controls (like Cancel/Pause action buttons) according to `AgentStatus`.
  - The UI displays real-time animation, spinners, and contextual text in the chat-embedded Agent Activity Feed (e.g. "Agent is thinking...", "Agent is running file-write tool") based on the active `AgentExecutionPhase`.

## Transitions

| Trigger | From | To | Guard |
|---------|------|----|-------|
| `configure()` | Created | Configured | Required fields non-null |
| `start()` | Ready | Running | Agent not disabled |
| `pause()` | Running | Paused | — |
| `resume()` | Paused | Running | — |
| `requestApproval()` | Running | WaitingApproval | Action exceeds autonomy level |
| `approve()` | WaitingApproval | Running | — |
| `deny()` | WaitingApproval | Paused | — |
| `reflect()` | Running | Reflecting | Reflection policy enabled |
| `complete()` | Reflecting / Running | Completing | — |
| `fail(error)` | * | Failed | Non-recoverable exception |
| `cancel()` | * | Cancelled | — |
| `retry()` | Failed | Ready | Max retries not exceeded |

### Invalid Transitions

- **Created → Running** — agent must be configured first.
- **Completed → Running** — terminal state; use a new instance or restart flow.
- **Cancelled → Running** — terminal state; create a fresh agent.
- **Configured → Reflecting** — agent must reach Running first.

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Created

    Created --> Configured : configure()
    Configured --> Ready : validate()
    Ready --> Running : start()
    Running --> Paused : pause()
    Paused --> Running : resume()
    Running --> WaitingApproval : requestApproval()
    WaitingApproval --> Running : approve()
    WaitingApproval --> Paused : deny()
    Running --> Reflecting : reflect()
    Reflecting --> Completing : complete()
    Running --> Completing : complete()
    Completing --> Completed : finalize()
    Completed --> [*]
    Failed --> [*] : fail(error)
    Cancelled --> [*] : cancel()
    Failed --> Ready : retry()

    Running --> Failed : fail(error)
    Configured --> Failed : fail(error)
    WaitingApproval --> Failed : fail(error)
    Paused --> Cancelled : cancel()
    Ready --> Cancelled : cancel()
    Configured --> Cancelled : cancel()
```

## Normative Transition Contract

Every transition in this state machine MUST be treated as an atomic command. The implementation MUST evaluate the guard against the current persisted version, apply the state change and side effects in one transaction, persist the resulting version, and emit the event only after durable persistence succeeds.

| Contract field | Requirement |
|---|---|
| Source and trigger | The trigger MUST be valid for the current state; unsupported triggers are rejected without mutation. |
| Guard | Guards are evaluated before mutation using current durable state and required authorization/context. |
| Target | The target is the only legal resulting state for the accepted trigger. |
| Side effects | Resource allocation/release, checkpointing, cleanup, routing, or child-operation changes MUST be listed by the owning subsystem. |
| Persistence | Durable state, transition version, actor, timestamp, correlation ID, and error context MUST be written before the event is published. |
| Event | One semantic transition event is emitted after commit; retries MUST NOT duplicate the committed transition event. |
| Idempotency | Repeating the same command with the same idempotency key returns the committed result; a conflicting version is rejected. |
| Failure | Guard failure and invalid transition return a canonical error and leave state unchanged. Side-effect failure MUST use the subsystem rollback or recovery rule. |
| Recovery | On restart, persisted state and transition version are authoritative; incomplete work resumes only through an explicitly listed recovery transition. |

### Transition Event Minimum

Each emitted lifecycle event MUST carry: `entityId`, `entityType`, `fromState`, `toState`, `trigger`, `transitionVersion`, `occurredAt`, `actor`, `correlationId`, and optional canonical error information. Consumers MUST treat events as at-least-once and deduplicate by `(entityType, entityId, transitionVersion)`.

### Invalid Transition Contract

An invalid transition MUST return a canonical error without changing persisted state, emitting a success event, or executing target-state side effects. The error MUST identify current state, requested trigger, entity ID, and correlation ID in redacted structured details.

## Implementation Notes

The lifecycle is enforced by `AgentStateMachine` in the core module. Every state transition fires an `AgentStateEvent` onto the shared event bus, enabling logging, metrics, and UI reactivity. Guards are evaluated synchronously on the caller thread; async validation should complete before invoking the trigger.
