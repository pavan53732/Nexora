# Task Lifecycle State Machine

> **Status: CANONICAL.** This document is the single authoritative source for Task
> states and transitions across Nexora. Every other document (domain model, runtime,
> API, SDK, protocol, lifecycle narrative, diagrams, tests) MUST reference the
> `TaskStatus` enum defined here and MUST NOT redefine, rename, or subset it.
>
> Depends on: none (root of the Task-state hierarchy).
> Referenced by: [../models/Task.md](../models/Task.md), [../architecture/RUNTIME.md](../architecture/RUNTIME.md), [../docs/LIFECYCLES.md](../docs/LIFECYCLES.md), [../specs/EXECUTION_LIFECYCLE.md](../specs/EXECUTION_LIFECYCLE.md), [../docs/api/Runtime-API.md](../docs/api/Runtime-API.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

A **Task** is the fundamental unit of work assigned to an agent in Nexora. The Task Lifecycle tracks each task from initial authoring through execution to final resolution, supporting blocking on dependencies, human approval gates, and retry semantics for transient failures.

## States

| State | Description |
|-------|-------------|
| **Draft** | Task defined locally; not yet submitted to the task manager. |
| **Pending** | Submitted; awaiting dependency resolution before enqueue. |
| **Queued** | Dependencies satisfied; placed in the agent's execution queue. |
| **Running** | Agent is actively executing the task. |
| **Blocked** | Execution stalled due to an unresolved dependency or resource lock. |
| **BlockedAwaitingInput** | Stalled due to loop escalation or missing capability; awaiting user clarification/input. |
| **WaitingApproval** | Task produced an action requiring human approval. |
| **Completed** | Terminal state — task finished successfully. |
| **Failed** | Terminal state — non-retryable failure. |
| **Cancelled** | Terminal state — cancelled by user or parent workflow. |
| **RetryPending** | Failure was retryable; queued for re-execution after backoff. |

## Transitions

| Trigger | From | To | Guard |
|---------|------|----|-------|
| `submit()` | Draft | Pending | Task schema valid |
| `enqueue()` | Pending | Queued | All dependencies completed |
| `start()` | Queued / RetryPending | Running | Agent available |
| `block(dependency)` | Running | Blocked | Dependency not yet completed |
| `unblock()` | Blocked | Running | Dependency resolved |
| `requestEscalation(question)` | Running | BlockedAwaitingInput | Loop escalation triggered or capability gap identified |
| `resolveEscalation(answer)` | BlockedAwaitingInput | Running | User input received; resumes from checkpoint |
| `requestApproval()` | Running | WaitingApproval | Action exceeds autonomy scope |
| `approve()` | WaitingApproval | Running | — |
| `complete()` | Running | Completed | Result validated |
| `fail(error)` | Running | Failed | Error is non-retryable |
| `fail(error)` | Running | RetryPending | Error is retryable && retries < max |
| `cancel()` | * | Cancelled | — |
| `retry()` | RetryPending | Queued | Backoff elapsed |

### Invalid Transitions

- **Draft → Running** — must submit and enqueue first.
- **Completed → Running** — terminal state; create a new task.
- **Queued → Completed** — task must pass through Running.
- **BlockedAwaitingInput → Completed** — task must resolve escalation input and return to Running first.
- **Pending → RetryPending** — task has never attempted execution.

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> Pending : submit()
    Pending --> Queued : enqueue()
    Queued --> Running : start()
    Running --> Blocked : block(dependency)
    Blocked --> Running : unblock()
    Running --> BlockedAwaitingInput : requestEscalation(question)
    BlockedAwaitingInput --> Running : resolveEscalation(answer)
    Running --> WaitingApproval : requestApproval()
    WaitingApproval --> Running : approve()
    Running --> Completed : complete()
    Completed --> [*]
    Running --> Failed : fail(non-retryable)
    Failed --> [*]
    Running --> RetryPending : fail(retryable)
    RetryPending --> Queued : retry()
    RetryPending --> Running : start()

    Draft --> Cancelled : cancel()
    Pending --> Cancelled : cancel()
    Queued --> Cancelled : cancel()
    Running --> Cancelled : cancel()
    Blocked --> Cancelled : cancel()
    BlockedAwaitingInput --> Cancelled : cancel()
    WaitingApproval --> Cancelled : cancel()
    RetryPending --> Cancelled : cancel()
    Cancelled --> [*]
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

Task state is persisted in the local Room database via the `TaskEntity` table. The `TaskScheduler` service drives transitions automatically — it watches dependency completions to trigger `enqueue()` and applies exponential backoff for `RetryPending` tasks. Approval requests surface through the `ApprovalGateway`, which blocks the agent loop until the user responds.
