> **Status: DERIVED** typed provider-stream sequence derived from Provider System,
> Provider Protocol, and ProviderStreamLifecycle.

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Provider Streaming Flow

```mermaid
sequenceDiagram
    participant Agent as Agent Runtime
    participant Router as ProviderRouter
    participant Account as Token Accounting
    participant Adapter as Provider Adapter
    participant Validate as StreamValidator
    participant Assemble as InferenceAssembler
    participant Bus as EventBus/UI

    Agent->>Router: planRoute(ContextSnapshot, ReasoningPolicy)
    Router->>Account: reserve(requestId, budget)
    Account-->>Router: validated
    Router->>Adapter: stream(request, bounded policy)
    Adapter-->>Validate: native event
    Validate->>Validate: normalize + identity + sequence + size/schema
    Validate-->>Assemble: StreamEnvelope
    Validate-->>Bus: provisional typed event

    alt Text/citation/reasoning summary
        Assemble->>Assemble: append/coalesce in order
    else Tool-call fragment
        Assemble->>Assemble: isolate by toolCallId
        Assemble->>Agent: ToolCallCommitted only after JSON/schema validation
    else Backpressure
        Validate->>Adapter: suspend producer / safe coalescing
    else Transport loss with native resume
        Router->>Adapter: resume(last sequence, opaque cursor)
        Adapter-->>Validate: same streamId, next sequence
    else Failover/restart
        Router->>Adapter: new request/stream with priorStreamId
        Bus-->>Agent: prior output remains partial; no splice
    else Cancel
        Agent->>Router: cancel(streamId, idempotencyKey)
        Router->>Adapter: cancel
        Adapter-->>Validate: Cancelled terminal
    end

    Adapter-->>Validate: Terminal / Failed / Cancelled
    Validate->>Account: reconcile authoritative usage
    Validate-->>Assemble: commit exactly one terminal
    Assemble-->>Agent: committed response or explicit partial failure
```

## Diagram Invariants

- Every durable event is deduplicated by `(streamId, sequence)`.
- Socket closure without terminal is failure.
- Tool fragments never execute.
- Control/semantic events are never dropped by backpressure.
- Cross-provider continuation always creates new stream lineage.
