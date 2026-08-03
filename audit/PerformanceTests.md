> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Performance Tests

## Scope

Performance tests establish and guard against regressions in Nexora's runtime characteristics across startup, agent execution, UI responsiveness, and resource usage.

| Metric | Measurement Method | Baseline | Alert Threshold |
|--------|--------------------|----------|-----------------|
| Cold start time | Macrobenchmark (`startupMode=COLD`) | **< 2 s** | > 2.4 s (+20%) |
| Warm start time | Macrobenchmark (`startupMode=WARM`) | < 800 ms | > 960 ms |
| Agent loop cycle | Microbenchmark (plan → provider → execute → memory) | **< 500 ms** | > 600 ms |
| Local tool execution | Microbenchmark (file write in sandbox) | **< 1 s** | > 1.2 s |
| UI frame rate | Macrobenchmark (`FrameMetrics`) | **≥ 60 fps** | < 48 fps (20% drop) |
| Peak memory (single agent) | Macrobenchmark (`MemoryUsageMetric`) | **< 512 MB** | > 614 MB |
| Room DB query (agents list) | Microbenchmark (50 agents) | **< 50 ms** | > 60 ms |
| Concurrent agents (3) overhead | Microbenchmark (3 parallel agent loops) | < 1.2 s cycle | > 1.44 s cycle |

## Framework Stack

| Tool | Purpose |
|------|--------|
| AndroidX Benchmark (Macrobenchmark) | Startup, UI jank, frame rate, memory profiling |
| AndroidX Benchmark (Microbenchmark/JMH) | Hot-path function timing with nanosecond precision |
| Android Studio Profiler | CPU, memory, network waterfall during manual investigation |
| simpleperf | Native-layer CPU profiling for sandbox IPC |
| ProfilHP | Heap dump analysis for leak detection |

## Test Setup

- **Device**: Pixel 7 (API 34), no background apps, airplane mode (network-dependent tests use local mock).
- **Iterations**: Macrobenchmark = 10 iterations; Microbenchmark = 50 iterations after 10 warmup.
- **Locks**: CPU locked to max frequency, screen on, charger connected.

## Profiling Workflow

1. Run baseline benchmarks on `main` branch — results committed to `benchmarks/baseline.json`.
2. Each PR runs the benchmark suite; results compared against baseline.
3. If any metric exceeds the **alert threshold** (> 20% degradation), CI fails with a detailed diff.

## Regression Policy

| Condition | Action |
|-----------|--------|
| Single metric > 20% regression | CI fails, blocking merge |
| Two or more metrics > 10% regression | CI fails, requires investigation |
| Memory leak detected (heap growth > 50 MB over 100 loops) | CI fails, critical |

## Run Schedule

| Trigger | Scope |
|---------|--------|
| Every PR | Startup, agent loop, DB query (fast subset) |
| Nightly | Full benchmark suite + profiling captures |
| Pre-release | Full suite with device matrix (Pixel 7, Samsung S23, Pixel Tablet) |