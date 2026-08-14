# ADR-0008: Typed Inference Streaming and Structured Reasoning Artifacts

- **Status**: Accepted
- **Date**: 2026-08-06
- **Deciders**: Lead Architect, Runtime, Provider, Security
- **Related**: [ADR-0003](ADR-0003-Agent-Runtime.md) · [ADR-0005](ADR-0005-Provider-Abstraction.md) · [Agent Runtime](../../architecture/AGENT_RUNTIME.md) · [Provider System](../../architecture/PROVIDER_SYSTEM.md) · [Context Management](../../specs/CONTEXT_MANAGEMENT.md)

## Context

Nexora already requires streaming responses, provider-neutral routing, six reasoning-effort levels, context provenance, evidence gates, and exactly-once recovery. The existing provider layers expose incompatible stream shapes, while the canonical AgentLoop waits for a complete response. Stream ordering, backpressure, cancellation, resume, partial tool-call assembly, and mid-stream failover are not yet expressed as one contract. Raw reasoning-trace retention also creates privacy and provider-compatibility risks.

## Decision

1. Provider streaming uses one typed, sequenced `StreamEnvelope` and a closed `StreamEvent` set.
2. Every inference attempt has stable `requestId`, `streamId`, `correlationId`, provider profile, model, and monotonic sequence.
3. A per-stream state machine owns connecting, open, backpressured, reconnecting, terminal, failure, and cancellation behavior.
4. Exactly one terminal event commits success; socket close alone is never success.
5. Tool-call fragments are data until a complete schema-valid `ToolCallCommitted` event is assembled. Partial calls never execute.
6. Mid-stream failover never silently splices providers. A replacement attempt gets a new `streamId` and `priorStreamId` lineage.
7. Agent Runtime consumes typed stream events as the canonical inference path; non-streaming providers are adapted into the same event contract.
8. Reasoning effort resolves to a bounded `ReasoningPolicy` covering provider calls, reasoning tokens, Tool calls, repair cycles, verifier passes, time, and device/resource safety ceilings. Usage and provider-cost metadata remain observable and non-blocking under DEC-25.
9. Nexora persists a structured, redacted `ReasoningSummary` (approach, evidence, decisions, uncertainty, verification), not unrestricted private chain-of-thought.
10. Context compilation produces a versioned `ContextSnapshot` with inclusion/exclusion rationale and compaction lineage.

## Ownership

- `architecture/AGENT_RUNTIME.md` owns inference-turn orchestration.
- `architecture/PROVIDER_SYSTEM.md` owns routing and the canonical provider stream abstraction.
- `state-machines/ProviderStreamLifecycle.md` owns per-stream states and transitions.
- `specs/CONTEXT_MANAGEMENT.md` owns ReasoningPolicy, ContextSnapshot, reasoning-summary privacy, grounding, and verification.
- `protocols/Provider-Protocol.md` owns the wire/event projection.

No monolithic AI-pipeline owner is introduced.

## Consequences

### Positive

- Provider/API/SDK stream contracts become compatible.
- Ordering, cancellation, resume, failover, usage accounting, and terminal behavior become testable.
- Agent reasoning becomes bounded and checkpointable.
- Tool-call fragments cannot execute prematurely.
- User-visible reasoning remains useful without requiring disclosure of private model reasoning.

### Negative

- Adapters must map provider-native events to a richer canonical protocol.
- Additional stream state, sequence, lineage, and audit data must be persisted.
- Backpressure and reconnect behavior increase implementation complexity.
- Existing APIs and SDKs require a contract-version increment and migration guidance.
