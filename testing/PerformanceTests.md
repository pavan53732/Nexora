# Performance Testing Strategy & Benchmarks — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [../docs/PERFORMANCE_BUDGET.md](../docs/PERFORMANCE_BUDGET.md)

---

## Overview

This document defines performance test strategies, benchmarking environments, and validation suites for measuring Nexora against the targets established in `docs/PERFORMANCE_BUDGET.md`.

## Suite IDs

- `PERF-START-*` — startup and navigation
- `PERF-EXEC-*` — task and execution paths
- `PERF-PROV-*` — provider streaming responsiveness
- `PERF-MEM-*` — memory retrieval and ranking
- `PERF-BG-*` — background execution stability
- `PERF-STREAM-*` — typed streaming latency, jitter, queue, cancellation, resume
- `PERF-REASON-*` — reasoning budget, verifier, and effort-level benchmarks
- `PERF-CONTEXT-*` — ContextSnapshot compilation and retrieval dedupe
- `PERF-MODEL-*` — model/provider comparison matrix
- `PERF-TOOLDISC-*` — bounded tool discovery
- `PERF-MA-*` — multi-agent coordination overhead
- `PERF-MM-*` — multimodal/audio/screen throughput
- `PERF-ESC-*` — capability-matrix, delegation, escalation, expiry, revocation, and cancellation benchmarks
- `PERF-LIVE-*` — stall/failover, timeout reconciliation, retry backoff, deadline, repair, and terminal-disposition benchmarks

The case inventory in [cases/PerformanceTestCases.md](./cases/PerformanceTestCases.md) is authoritative for individual case IDs; every suite above has at least one defined case there.

## Test Environment Specification

All official performance benchmarks MUST be executed under the following standard environment:
- **Device Class:** Reference mid-range Android device (8 CPU cores, 8GB RAM, UFS 3.1 storage) or official Android Emulator running API 34 (Android 14) x86_64 image.
- **Thermal State:** Normal thermal baseline (no active throttling).
- **Network Condition:** Simulated stable broadband (50 Mbps down / 20 Mbps up, 30ms latency) or offline local mode where applicable.
- **Battery State:** Unplugged, 100% -> 80% discharge window for battery historian profiling.

Performance environments SHOULD additionally document load profile, data profile, device class, and measurement method per run.

## Benchmark Categories

### 1. Cold Start & UI Responsiveness (`PERF-START-*`)
- Measures app cold start time (target < 2s).
- Measures Compose UI frame rate (60fps steady, jank < 1%) and input latency during heavy workspace rendering.

### 2. Execution Loop & Provider Streaming (`PERF-STREAM-*`)
- Measures single agent loop iteration latency (< 500ms excluding provider).
- Measures first-token streaming latency (< 1s) and backpressure delivery under slow consumer simulation.

### 3. Agent Scalability & Resource Utilization (`PERF-EXEC-*`, `PERF-SCALE-*`)
- Measures memory footprint idle (< 512MB RSS), single agent active (< 512MB RSS), and concurrent agents (3+ agents).
- Measures database query latency for Room entities and semantic memory search across 10,000+ entries (< 200ms).

## Controlled Execution Escalation Benchmarks (`PERF-ESC-*`)

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

## Liveness Benchmarks (`PERF-LIVE-*`)

`PERF-LIVE-001..004` measure stalled-stream detection and bounded failover, timeout-to-reconciliation latency without unsafe retry of unknown non-idempotent outcomes, RetryPending queue delay under backoff/deadline guards, and bounded repair/verification/finalization latency under success and failure paths. They validate DEC-30 liveness bounds as performance evidence.

## Execution and Reporting

Benchmarks are executed via automated CI scripts and Gradle Macrobenchmark tasks. Results MUST be recorded as JSON documents matching the Benchmark Result Record schema defined in `docs/PERFORMANCE_BUDGET.md` (§Benchmark Result Record), with thresholds evaluated against the budget tables in that same document.

Reasoning benchmarks MUST compare effort levels and record reasoning-token usage, verifier passes, claim/evidence accuracy, contradiction detection, unsupported-claim rate, repair cycles, and end-state task success. Tool-discovery benchmarks MUST record candidate-set size, selected-tool accuracy, rejected-alternative reasons, schema-repair rate, duplicate selection rate, and task completion impact. Multi-agent benchmarks MUST record child count, parallel lanes, queue time, duplicate scope, artifact handoff, coordination overhead, partial-result utilization, conflict rate, and end-state success.

Model and provider claims remain evidence-scoped. Vendor-published capability or benchmark results may inform route selection and test design, but Nexora release gates require reproducible Nexora evidence under the declared device, provider, model, and fixture conditions.

## Regression Policy

Performance regressions are compared against the recorded baseline per `docs/PERFORMANCE_BUDGET.md` §Enforcement: a regression exceeding 20% from baseline blocks merge to the release branch, and any metric at or above its Critical threshold blocks release.

## Run Schedule

Run regularly for release candidates and performance-sensitive changes.
