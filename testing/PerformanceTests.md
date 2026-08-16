# Performance Testing Strategy & Benchmarks — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [../docs/PERFORMANCE_BUDGET.md](../docs/PERFORMANCE_BUDGET.md)

---

## Overview

This document defines performance test strategies, benchmarking environments, and validation suites for measuring Nexora against the targets established in `docs/PERFORMANCE_BUDGET.md`.

## Test Environment Specification

All official performance benchmarks MUST be executed under the following standard environment:
- **Device Class:** Reference mid-range Android device (8 CPU cores, 8GB RAM, UFS 3.1 storage) or official Android Emulator running API 34 (Android 14) x86_64 image.
- **Thermal State:** Normal thermal baseline (no active throttling).
- **Network Condition:** Simulated stable broadband (50 Mbps down / 20 Mbps up, 30ms latency) or offline local mode where applicable.
- **Battery State:** Unplugged, 100% -> 80% discharge window for battery historian profiling.

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

## Execution and Reporting

Benchmarks are executed via automated CI scripts and Gradle Macrobenchmark tasks. Results must output JSON metrics matching the schema defined in `docs/PERFORMANCE_BUDGET.md`.

Reasoning benchmarks MUST compare effort levels and record reasoning-token usage, verifier passes, claim/evidence accuracy, contradiction detection, unsupported-claim rate, repair cycles, and end-state task success. Tool-discovery benchmarks MUST record candidate-set size, selected-tool accuracy, rejected-alternative reasons, schema-repair rate, duplicate selection rate, and task completion impact. Multi-agent benchmarks MUST record child count, parallel lanes, queue time, duplicate scope, artifact handoff, coordination overhead, partial-result utilization, conflict rate, and end-state success.

Model and provider claims remain evidence-scoped. Vendor-published capability or benchmark results may inform route selection and test design, but Nexora release gates require reproducible Nexora evidence under the declared device, provider, model, and fixture conditions.
