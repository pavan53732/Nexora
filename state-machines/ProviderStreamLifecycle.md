> **Status: CANONICAL** for individual provider inference-stream states and transitions.
> Provider administrative health remains owned by [ProviderLifecycle.md](ProviderLifecycle.md).
> Stream event shape is projected by [../protocols/Provider-Protocol.md](../protocols/Provider-Protocol.md).

# Provider Stream Lifecycle — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## States

| State | Meaning |
|---|---|
| `CREATED` | Stream identity and route plan allocated; no connection attempted. |
| `CONNECTING` | Adapter is establishing the provider transport. |
| `OPEN` | Typed events may be accepted and committed in sequence. |
| `BACKPRESSURED` | Consumer capacity reached; producer is suspended or deltas are safely coalesced. |
| `RECONNECTING` | Recoverable transport loss; bounded native resume is in progress. |
| `STALLED` | No semantic event received within the stalled-stream timeout (first-byte or inter-token). |
| `COMPLETED` | Exactly one successful terminal event committed; terminal. |
| `FAILED` | Canonical failure committed, including partial-output metadata; terminal. |
| `CANCELLED` | Cancellation committed and propagated; terminal. |

## Transitions

| Trigger | From | To | Guard / effect |
|---|---|---|---|
| `connect` | `CREATED` | `CONNECTING` | Route candidate is eligible and request budget is reserved. |
| `opened` | `CONNECTING` | `OPEN` | Transport authenticated; `StreamStarted` sequence committed. |
| `capacityExceeded` | `OPEN` | `BACKPRESSURED` | Buffer high-water mark reached; never drop terminal/tool events. |
| `capacityAvailable` | `BACKPRESSURED` | `OPEN` | Queue below low-water mark; ordering preserved. |
| `transportLost` | `OPEN` / `BACKPRESSURED` | `RECONNECTING` | Native resume supported, cursor valid, retry budget remains. |
| `stalled` | `CONNECTING` / `OPEN` / `BACKPRESSURED` / `RECONNECTING` | `STALLED` | No first-byte within deadline OR no semantic event within inter-token window. |
| `failover` | `STALLED` | `RECONNECTING` | Stalled-failover budget remains; create a new route/stream lineage or use the configured provider restart policy; preserve committed context and `priorStreamId`. |
| `resumed` | `RECONNECTING` | `OPEN` | Same `streamId`; next sequence follows last committed sequence. |
| `resumeRejected` | `RECONNECTING` | `FAILED` | Commit `NXR-4014`; partial output remains explicitly partial. |
| `terminal` | `OPEN` / `BACKPRESSURED` | `COMPLETED` | Terminal sequence contiguous; usage reconciled; no incomplete tool call. |
| `fail` | `CONNECTING` / `OPEN` / `BACKPRESSURED` / `RECONNECTING` / `STALLED` | `FAILED` | Canonical error and partial-output status committed. |
| `cancel` | Any nonterminal | `CANCELLED` | Cancellation propagates Agent → Router → Adapter within budget. |

## Invariants

1. `streamId` is immutable; replacement/failover creates a new stream with `priorStreamId`.
2. `sequence` is strictly monotonic from zero; duplicates are idempotently ignored and gaps block terminal commit.
3. Exactly one of `COMPLETED`, `FAILED`, or `CANCELLED` is committed.
4. Socket closure is not a successful terminal event.
5. `ToolCallCommitted` is emitted only after all fragments assemble and schema validation succeeds.
6. Partial tool-call state is discarded on failure/cancellation and never executes.
7. Text already displayed before failure remains marked provisional/partial until a successful terminal commit.
8. Provider failover never appends replacement output to the prior stream identity.
9. Cancellation is idempotent and terminal.
10. Stream events are at-least-once; consumers deduplicate by `(streamId, sequence)`.
11. Persisted sequence/cursor state is authoritative after restart.
12. Provider health changes may affect future routing but never rewrite committed stream history.
13. Stalled streams abandon without appending output to the prior `streamId`; failover emits a new stream with `priorStreamId`.
14. A different provider always uses `RESTART_WITH_LINEAGE`; cross-provider byte splicing is prohibited; stalled failover is one such lineage-bounded restart.

## Backpressure Contract

- Adapter-to-router channel is bounded and configurable per workspace/device class.
- Text/reasoning-summary deltas MAY be coalesced without changing byte order.
- Tool-call, citation, usage, failure, cancellation, and terminal events MUST NOT be dropped.
- Sustained overflow beyond the configured deadline fails with `NXR-4013` rather than exhausting memory.
- UI rendering MAY throttle frames, but the durable event stream remains ordered.

## Resume and Failover

- `NATIVE_CURSOR`: reconnect the same stream using the provider cursor/resume token.
- `RESTART_WITH_LINEAGE`: create a new request/stream; include committed context and `priorStreamId`; do not claim byte-continuation.
- `NONE`: fail explicitly with partial output.
- A different provider always uses `RESTART_WITH_LINEAGE`; cross-provider byte splicing is prohibited.
- Stalled failover is one such lineage-bounded restart: same committed context, same `priorStreamId`, new provider when configured.

## Stalled-Stream Timeouts

| Timeout | Applies from | Deadline | Effect |
|---|---|---|---|
| `firstByteTimeout` | Stream enter | 12s | Transition to `STALLED`; triggers `failover`. |
| `interTokenTimeout` | last semantic `StreamEvent` committed | 8s | Transition to `STALLED`; triggers `failover`. |
| `stalledFailoverBudget` | consecutive `STALLED` states | 2 attempts total | Exceeded consecutive stalls commit `FAILED` with `NXR-4015`. |
