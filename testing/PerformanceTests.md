# Performance Tests

## Scope

Performance tests validate latency, throughput, resource usage, background execution behavior, and scalability-sensitive contract paths.

## Suite IDs

- `PERF-START-*` — startup and navigation
- `PERF-EXEC-*` — task and execution paths
- `PERF-PROV-*` — provider streaming responsiveness
- `PERF-MEM-*` — memory retrieval and ranking
- `PERF-BG-*` — background execution stability
- `PERF-ESC-*` — capability-matrix, delegation, escalation, expiry, revocation, and cancellation benchmarks
- `PERF-LIVE-*` — stall/failover, timeout reconciliation, retry backoff, deadline, repair, and terminal-disposition benchmarks

## Framework Stack

- benchmark harnesses
- profiling and tracing tools
- representative workload fixtures

## Test Setup

Performance environments SHOULD document load profile, data profile, device class, and measurement method.

## Profiling Workflow

Profile startup, task execution, tool invocation, provider streaming, memory retrieval, and background execution paths.

## Regression Policy

Performance regressions SHOULD be compared against explicit thresholds or baselines where available.

## Run Schedule

Run regularly for release candidates and performance-sensitive changes.

## Controlled Execution Escalation Benchmarks

The performance suite MUST measure bounded execution escalation without treating broader privilege as a performance optimization.

Required benchmark dimensions include:

- capability-matrix and delegation decision latency;
- temporary Terminal grant authorization and approval-round-trip latency;
- temporary Background grant startup, checkpoint, notification, and WorkManager handoff latency;
- cancellation propagation and descendant-drain latency after expiry or revocation;
- CPU, memory, disk, battery, thermal, process, and network impact of delegated and escalated work;
- queue wait and active time for eligible workers under concurrent escalation requests;
- duplicate-request suppression and transfer-rejection overhead;
- checkpoint persistence and recovery latency when a grant expires during active work;
- trace and audit write overhead without loss of correlation or security events.

Results MUST be reported by agent type, requested capability, device class, Android version, workspace limits, autonomy mode, provider/tool route, concurrency level, and outcome. The benchmark MUST include denial, delegation, approval, expiry, revocation, cancellation, degradation, and successful completion paths. These are planned evidence obligations until implementation and device measurements exist.

## Canonical Contract Evidence

Performance validation SHOULD tie back to measurable NFR-style concerns such as:

- startup and navigation latency
- task execution overhead
- provider stream responsiveness
- memory retrieval latency
- background execution stability under load

## Stream, Reasoning, and Context Benchmarks

`PERF-STREAM-001..005`, `PERF-REASON-001..002`, and `PERF-CONTEXT-001` enforce TTFB,
jitter, queue, cancellation, resume, reasoning budget, verifier, and snapshot budgets.

## Provider and Agent Benchmark Matrix

Performance results MUST be reported by provider profile, exact model identifier or pinned
snapshot, adapter contract version, reasoning effort, requested capability set, context
size, Tool count, device class, Android version, network condition, and build channel. A
single aggregate latency number is not sufficient to compare models or providers.

The benchmark record SHOULD distinguish time to first byte, time to first visible token,
inter-token latency, tokens per second where meaningful, Tool-call round-trip latency,
plan-to-first-action latency, plan-to-completion time, provider failover overhead,
checkpoint-resume latency, cancellation propagation, queue wait, CPU/memory/battery/thermal
impact, and concurrent-agent throughput. P50, P95, and P99 values SHOULD be retained for
latency-sensitive measures; quality and latency MUST be reported together so a faster but
less accurate route is not treated as universally better.

Reasoning benchmarks MUST compare effort levels and record reasoning-token usage, verifier
passes, claim/evidence accuracy, contradiction detection, unsupported-claim rate, repair
cycles, and end-state task success. Tool-discovery benchmarks MUST record candidate-set
size, selected-tool accuracy, rejected-alternative reasons, schema-repair rate, duplicate
selection rate, and task completion impact. Multi-agent benchmarks MUST record child count,
parallel lanes, queue time, duplicate scope, artifact handoff, coordination overhead,
partial-result utilization, conflict rate, and end-state success.

Model and provider claims remain evidence-scoped. Vendor-published capability or benchmark
results may inform route selection and test design, but Nexora release gates require
reproducible Nexora evidence under the declared device, provider, model, and fixture
conditions.
