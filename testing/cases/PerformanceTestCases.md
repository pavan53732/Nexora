# Performance Test Case Inventory — Nexora

> ADR-0010: case rows are `TEST DEFINED` until execution produces a result; `EXECUTED EVIDENCE` requires the common reproducible envelope in `testing/EVIDENCE_CONVENTIONS.md`. Deterministic controls are fixture-scoped and test-only.

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| PERF-START-001 | PERF-START | Measure startup and navigation latency | Performance | Planned | `evidence/performance/PERF-START-001/` | 2026-08-04 |
| PERF-EXEC-001 | PERF-EXEC | Measure task execution overhead | Performance | Planned | `evidence/performance/PERF-EXEC-001/` | 2026-08-04 |
| PERF-PROV-001 | PERF-PROV | Measure provider stream responsiveness | Performance + Provider Layer | Planned | `evidence/performance/PERF-PROV-001/` | 2026-08-04 |
| PERF-MEM-001 | PERF-MEM | Measure memory retrieval latency | Performance + Memory System | Planned | `evidence/performance/PERF-MEM-001/` | 2026-08-04 |
| PERF-BG-001 | PERF-BG | Measure background execution stability under load | Performance | Planned | `evidence/performance/PERF-BG-001/` | 2026-08-04 |
| PERF-STREAM-001 | PERF-STREAM | Measure first typed event and first visible text latency | Performance + Provider | Planned | `evidence/performance/PERF-STREAM-001/` | 2026-08-06 |
| PERF-STREAM-002 | PERF-STREAM | Measure inter-event jitter P50/P95/P99 | Performance + Provider | Planned | `evidence/performance/PERF-STREAM-002/` | 2026-08-06 |
| PERF-STREAM-003 | PERF-STREAM | Measure bounded queue wait and occupancy | Performance + Provider | Planned | `evidence/performance/PERF-STREAM-003/` | 2026-08-06 |
| PERF-STREAM-004 | PERF-STREAM | Measure cancellation propagation P95 | Performance + Provider | Planned | `evidence/performance/PERF-STREAM-004/` | 2026-08-06 |
| PERF-STREAM-005 | PERF-STREAM | Measure resume success and recovery latency | Performance + Provider | Planned | `evidence/performance/PERF-STREAM-005/` | 2026-08-06 |
| PERF-REASON-001 | PERF-REASON | Measure reasoning tokens/cost/latency by effort | Performance + Reasoning | Planned | `evidence/performance/PERF-REASON-001/` | 2026-08-06 |
| PERF-REASON-002 | PERF-REASON | Measure verifier and critic overhead | Performance + Reasoning | Planned | `evidence/performance/PERF-REASON-002/` | 2026-08-06 |
| PERF-CONTEXT-001 | PERF-CONTEXT | Measure ContextSnapshot compilation and retrieval dedupe | Performance + Context | Planned | `evidence/performance/PERF-CONTEXT-001/` | 2026-08-06 |
| PERF-MODEL-001 | PERF-MODEL | Compare P50/P95/P99 first-byte, first-visible-token, completion, failover, and resume latency by exact model snapshot, effort, context size, and device/network matrix | Performance + Provider | Planned | `evidence/performance/PERF-MODEL-001/` | 2026-08-15 |
| PERF-MODEL-002 | PERF-MODEL | Measure capability-negotiation and route-planning overhead, including catalog refresh and deprecated-model handling | Performance + Provider | Planned | `evidence/performance/PERF-MODEL-002/` | 2026-08-15 |
| PERF-REASON-003 | PERF-REASON | Compare effort levels using reasoning-token use, verifier passes, claim/evidence accuracy, unsupported-claim rate, repair cycles, and task success | Performance + Reasoning + Evidence | Planned | `evidence/performance/PERF-REASON-003/` | 2026-08-15 |
| PERF-TOOLDISC-001 | PERF-TOOLDISC | Measure bounded discovery latency, candidate-set size, selected-tool accuracy, schema-repair rate, and duplicate-selection rate | Performance + Tool | Planned | `evidence/performance/PERF-TOOLDISC-001/` | 2026-08-15 |
| PERF-MA-001 | PERF-MA | Measure coordination overhead, queue time, parallel lanes, artifact handoff, conflict rate, and end-state success by child count | Performance + Multi-Agent | Planned | `evidence/performance/PERF-MA-001/` | 2026-08-15 |
| PERF-MM-001 | PERF-MM | Measure multimodal/audio/screen event throughput, frame/audio latency, backpressure, cancellation, and device thermal impact under negotiated capability routes | Performance + Provider + Android | Planned | `evidence/performance/PERF-MM-001/` | 2026-08-15 |
| PERF-ESC-001 | PERF-ESC | Measure capability-matrix and delegation decision latency by agent type and requested capability | Performance + Multi-Agent | Planned | `evidence/performance/PERF-ESC-001/` | 2026-08-15 |
| PERF-ESC-002 | PERF-ESC | Measure Terminal escalation authorization, approval round-trip, and startup overhead by device and policy | Performance + Terminal + Security | Planned | `evidence/performance/PERF-ESC-002/` | 2026-08-15 |
| PERF-ESC-003 | PERF-ESC | Measure Background escalation startup, checkpoint, notification, WorkManager handoff, and degradation latency | Performance + Background Runtime | Planned | `evidence/performance/PERF-ESC-003/` | 2026-08-15 |
| PERF-ESC-004 | PERF-ESC | Measure cancellation propagation and descendant drain time after grant expiry or revocation under concurrency | Performance + Recovery | Planned | `evidence/performance/PERF-ESC-004/` | 2026-08-15 |
| PERF-ESC-005 | PERF-ESC | Measure CPU, memory, disk, battery, thermal, process, network, audit, and trace overhead of delegated/escalated work | Performance + Runtime + Security | Planned | `evidence/performance/PERF-ESC-005/` | 2026-08-15 |
| PERF-LIVE-001 | PERF-LIVE | Measure stalled-stream detection, bounded failover decision, new-lineage startup, and terminal-failure latency | Performance + Provider | Planned | `evidence/performance/PERF-LIVE-001/` | 2026-08-15 |
| PERF-LIVE-002 | PERF-LIVE | Measure timeout-to-reconciliation latency and verify no unsafe retry while non-idempotent outcome is unknown | Performance + Tool + Recovery | Planned | `evidence/performance/PERF-LIVE-002/` | 2026-08-15 |
| PERF-LIVE-003 | PERF-LIVE | Measure RetryPending queue delay and confirm no start before backoff/deadline guard | Performance + Task Scheduler | Planned | `evidence/performance/PERF-LIVE-003/` | 2026-08-15 |
| PERF-LIVE-004 | PERF-LIVE | Measure bounded repair, verification, finalization, and terminal event latency under success and failure paths | Performance + Agent Runtime | Planned | `evidence/performance/PERF-LIVE-004/` | 2026-08-15 |
