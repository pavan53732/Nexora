# Performance Tests

## Scope

Performance tests validate latency, throughput, resource usage, background execution behavior, and scalability-sensitive contract paths.

## Suite IDs

- `PERF-START-*` — startup and navigation
- `PERF-EXEC-*` — task and execution paths
- `PERF-PROV-*` — provider streaming responsiveness
- `PERF-MEM-*` — memory retrieval and ranking
- `PERF-BG-*` — background execution stability

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
