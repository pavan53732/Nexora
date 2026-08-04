> **Status: CANONICAL** for workflow lifecycle states and transitions.
> This document owns the formal workflow state machine.
> It does NOT own workflow graph progression logic (see [../architecture/WORKFLOW_ENGINE.md](../architecture/WORKFLOW_ENGINE.md)).
>
> Depends on: [../architecture/WORKFLOW_ENGINE.md](../architecture/WORKFLOW_ENGINE.md).
> Referenced by: [../models/Workflow.md](../models/Workflow.md), [../docs/api/Runtime-API.md](../docs/api/Runtime-API.md).

# Workflow Lifecycle State Machine

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

A **Workflow** in Nexora is a directed acyclic graph (DAG) of steps that orchestrates multi-stage agent operations. The workflow-level lifecycle tracks overall progress, while each step maintains its own sub-state internally. Workflows support pause/resume semantics and propagate cancellation across all constituent steps.

## States

| State | Description |
|-------|-------------|
| **Defined** | Workflow DAG structure authored; steps and edges declared. |
| **Validated** | DAG has no cycles, all step inputs/outputs type-checked. |
| **Running** | At least one step is actively executing. |
| **Paused** | No steps executing; can be resumed from pause point. |
| **StepPending** | Next step(s) ready to execute but not yet started. |
| **StepRunning** | A step is actively executing within the workflow. |
| **StepCompleted** | A step has finished; downstream evaluation in progress. |
| **Completed** | Terminal state — all steps finished successfully. |
| **Failed** | Terminal state — a step failed with no fallback path. |
| **Cancelled** | Terminal state — user or system cancelled the workflow. |

## Transitions

| Trigger | From | To | Guard |
|---------|------|----|-------|
| `define()` | [*] | Defined | — |
| `validate()` | Defined | Validated | DAG is acyclic |
| `start()` | Validated | Running | — |
| `pause()` | Running | Paused | — |
| `resume()` | Paused | Running | Pending steps exist |
| `stepStart()` | Running | StepRunning | Upstream steps completed |
| `stepComplete()` | StepRunning | StepCompleted | Step result valid |
| `complete()` | StepCompleted | Completed | No pending steps remain |
| `stepStart()` | StepCompleted | StepRunning | Downstream step eligible |
| `fail(error)` | StepRunning | Failed | No error-handler edge |
| `cancel()` | * | Cancelled | — |

### Step Sub-States

Each step internally tracks: **Pending → Running → Completed / Failed / Skipped**. The workflow engine evaluates step readiness after every `stepComplete()` by walking the DAG for steps whose all upstream dependencies are in the Completed state.

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Defined

    Defined --> Validated : validate()
    Validated --> Running : start()
    Running --> Paused : pause()
    Paused --> Running : resume()
    Running --> StepPending : evaluateSteps()
    StepPending --> StepRunning : stepStart()
    StepRunning --> StepCompleted : stepComplete()
    StepCompleted --> StepPending : evaluateSteps()
    StepCompleted --> Completed : complete()
    StepRunning --> Failed : fail(error)
    Failed --> [*]
    Completed --> [*]

    Running --> Cancelled : cancel()
    Paused --> Cancelled : cancel()
    StepPending --> Cancelled : cancel()
    StepRunning --> Cancelled : cancel()
    StepCompleted --> Cancelled : cancel()
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

The `WorkflowEngine` class manages the DAG traversal and step dispatching. It uses a topological sort to determine execution order and maintains an in-memory `StepStatusMap`. Workflow state is persisted to the `workflow` table in Room; step sub-states are stored in the `workflow_step` table. The engine is coroutine-based — each `stepStart()` launches a child job so that independent parallel branches execute concurrently, with structured concurrency ensuring cancellation propagates to all children.
