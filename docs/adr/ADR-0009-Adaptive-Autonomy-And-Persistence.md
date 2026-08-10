# ADR-0009: Adaptive Autonomy, Anti-Hang, and Resumable Escalation

- **Status**: Accepted
- **Date**: 2026-08-11
- **Deciders**: Lead Architect, Runtime, Provider, Agent, Security
- **Related**: [ADR-0003](ADR-0003-Agent-Runtime.md) · [ADR-0005](ADR-0005-Provider-Abstraction.md) · [ADR-0008](ADR-0008-Typed-Inference-Streaming.md) · [Agent Runtime](../../architecture/AGENT_RUNTIME.md) · [Provider System](../../architecture/PROVIDER_SYSTEM.md) · [Multi-Agent System](../../architecture/MULTI_AGENT_SYSTEM.md) · [Context Management](../../specs/CONTEXT_MANAGEMENT.md) · [Background Execution](../../specs/BACKGROUND_EXECUTION.md)

## Context

Nexora's agent loop, provider system, and background execution specs already define 3-tier syntactic loop detection, process-level timeouts, checkpointing, and provider failover on hard error responses. However, three real-world reliability gaps remain in autonomous runs:

1. **Silent Stream Stalls**: Network streams that open but stall (no bytes received) do not trigger immediate provider failover because `ProviderStreamLifecycle` only handles explicit stream failures or socket errors.
2. **Syntactic Loop Bypass ("Treadmill Execution")**: An agent can vary minor tool arguments or alternate between ineffective tools while producing zero progress (zero state-delta), avoiding the N=2 identical action-repeat rule.
3. **Terminal Escalation Dead-Ends**: When an agent hits an escalation boundary or requires human input (e.g. missing license or credential), execution transitions to a terminal error state rather than pausing for a resumable answer.
4. **Sub-Agent Deadlock & Retry Storms**: Delegation dependencies and parallel tool retries lack explicit waits-for cycle detection, delegation timeouts, and jittered backoff rules.

Furthermore, budget and token limits must not serve as artificial hard-stops when progress is actively occurring.

## Decision

1. **Unbounded Financial Budgeting for Autonomous Execution**: Token and cost ceilings are explicitly out of scope as execution termination gates. Agent Runtime termination is governed solely by semantic progress failure, safety policy violations, or explicit user cancellation.
2. **Stalled-Stream Failover**: `ProviderStreamLifecycle` introduces a `stalled_stream` trigger (first-byte timeout + inter-token stall timeout). Un-received or stalled streams are abandoned, creating a new stream attempt with `priorStreamId` lineage and triggering provider failover.
3. **Semantic Progress Evaluation (State-Delta)**: `ContextSnapshot` is extended with a `ProgressSignal` (evaluating test results, file modifications, new evidence, and error category shifts). Experiencing N=3 consecutive iterations with zero state-delta triggers loop escalation regardless of syntactic action variations.
4. **Task-Scoped Failure Ledger**: Agent Runtime maintains a task-scoped failure ledger in working context. After K=3 identical error signatures for a tool call within a task, the runtime enforces strategy mutation or alternate tool selection for that task without mutating global registry descriptors.
5. **Resumable Escalation (`BlockedAwaitingInput`)**: `TaskLifecycle` adds a canonical `BlockedAwaitingInput` state. When loop escalation or missing user capabilities occur, the agent formulates a targeted clarification query, persists an `ExecutionCheckpoint`, releases execution resources, and enters `BlockedAwaitingInput`. Receiving a user response resumes execution seamlessly from the checkpoint.
6. **Multi-Agent Deadlock Watchdog**: `MULTI_AGENT_SYSTEM.md` §SA-3 mandates a waits-for graph monitor over file write-locks and delegation futures. Graph cycles automatically abort the youngest sub-agent, release locks, and report to the Workflow Coordinator. Explicit delegation timeouts are required.
7. **Execution Liveness Heartbeat & ANR Recovery**: Coroutine execution streams emit a mandatory Liveness Heartbeat. Missed heartbeats or Android main-thread ANRs trigger an automated checkpoint commit and background recovery attempt.
8. **Canonical Jittered Backoff**: All tool invocation retries, sub-agent delegation handoffs, and network reconnects must apply randomized exponential backoff with jitter to eliminate retry storms.

## Ownership

- `architecture/AGENT_RUNTIME.md` owns task-scoped failure ledgers and progress-delta escalation rules.
- `architecture/PROVIDER_SYSTEM.md` and `state-machines/ProviderStreamLifecycle.md` own stalled-stream detection and failover lineage.
- `state-machines/TaskLifecycle.md` owns the `BlockedAwaitingInput` state and resume semantics.
- `architecture/MULTI_AGENT_SYSTEM.md` owns the deadlock waits-for watchdog and sub-agent timeouts.
- `specs/CONTEXT_MANAGEMENT.md` owns `ProgressSignal` computation inside `ContextSnapshot`.
- `specs/BACKGROUND_EXECUTION.md` owns execution liveness heartbeats and ANR checkpoint recovery.

## Consequences

### Positive

- Agents no longer hang silently on dead network connections.
- Treadmill loops (varying inputs with zero progress) are caught and broken early.
- Escalations become interactive and resumable instead of destructive task failures.
- Multi-agent deadlocks are detected and resolved automatically.
- Thundering herd retry storms across tools and sub-agents are eliminated.

### Negative

- Additional stream timers and heartbeat monitoring overhead.
- Maintaining task-scoped failure ledgers and progress-delta calculations increases context compilation state.
- `TaskLifecycle` state machine requires an extra non-terminal state handled across UI and API layers.
