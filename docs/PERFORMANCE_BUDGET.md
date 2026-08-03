# Performance Budget

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

Measurable performance targets for Nexora — an Android-native autonomous AI agent platform (Kotlin/Java, API 34+, targeting mid-range devices). These are **hard budgets**: if a metric exceeds its budget, it is a regression that must be fixed before release.

## Startup & Navigation

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Cold start (killed → first frame) | 2 000 ms | 3 000 ms | 5 000 ms | Macrobenchmark (`startupMode=COLD`) | Alpha |
| Warm start (background → foreground) | 500 ms | 800 ms | 1 500 ms | Macrobenchmark | Alpha |
| Screen navigation (tap → render) | 300 ms | 500 ms | 1 000 ms | Compose timing | Alpha |
| Workspace switch | 500 ms | 800 ms | 1 500 ms | Custom benchmark | Beta |

## Agent Runtime

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Agent loop cycle — local tools | 500 ms | 1 000 ms | 2 500 ms | `AgentLoop` timing logs | Alpha |
| Agent loop cycle — network tools | 2 000 ms | 4 000 ms | 10 000 ms | `AgentLoop` timing logs | Alpha |
| Tool invocation — local | 200 ms | 500 ms | 1 000 ms | `ToolManager` timing | Alpha |
| Tool invocation — network | 2 000 ms | 5 000 ms | 10 000 ms | `ToolManager` timing | Alpha |
| Context building (collect for AI call) | 100 ms | 200 ms | 500 ms | `ContextBuilder` timing | Alpha |

## AI Provider

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Streaming first token (TTFB) | 1 000 ms | 2 000 ms | 5 000 ms | `Flow<StreamChunk>` timing | Alpha |
| Inter-chunk latency | 100 ms | 300 ms | 1 000 ms | `Flow` timing | Alpha |
| Provider health check | 2 000 ms | 5 000 ms | 10 000 ms | `HealthCheck` coroutine | Beta |
| Provider failover time | 3 000 ms | 5 000 ms | — | `ProviderManager` timing | Beta |

## Memory & Resources

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| App memory — idle, no agents | 128 MB | 200 MB | 300 MB | Android Profiler / `Runtime.getRuntime()` | Alpha |
| App memory — single agent active | 256 MB | 384 MB | 512 MB | Android Profiler | Alpha |
| App memory — 3+ concurrent agents | 384 MB | 512 MB | 640 MB | Android Profiler | Beta |
| Sandbox disk usage per workspace | 100 MB quota | 80 MB alert | 100 MB hard limit | `VirtualFileSystem` stats | Alpha |

## Database & Storage

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Room query — single entity by ID | 10 ms | 20 ms | 50 ms | Room query callback timing | Alpha |
| Room query — filtered list (1 000 rows) | 50 ms | 100 ms | 200 ms | Room query callback timing | Alpha |
| Memory search — semantic (10 k entries) | 200 ms | 500 ms | 1 000 ms | `MemoryManager.search` timing | Beta |
| Checkpoint save | 100 ms | 200 ms | 500 ms | `AgentCheckpoint` timing | Alpha |

## UI Responsiveness

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Frame rate (scroll, animations) | 60 fps (16.6 ms/frame) | 55 fps (jank > 1 %) | 45 fps | FrameMetrics / Macrobenchmark | Alpha |
| Input latency (tap → visual response) | 100 ms | 200 ms | 500 ms | Choreographer callback | Alpha |
| List render — 100 items | 100 ms | 200 ms | 500 ms | `LazyColumn` timing | Alpha |

## Background & Battery

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Background agent CPU usage | 10 % avg | 20 % | 30 % | Android Battery Stats | Beta |
| Background agent battery impact | < 2 % / hr | 5 % / hr | — | `BatteryManager` | Beta |
| Checkpoint interval | 30 s default | — | — | `AgentLoop` timer | Alpha |

## APK Size

| Metric | Target | Warning | Critical | Measurement Method | Phase |
|---|---|---|---|---|---|
| Base APK (no providers, no plugins) | 30 MB | 40 MB | 50 MB | Gradle build output | Alpha |
| With all bundled resources | 45 MB | 55 MB | 60 MB | Gradle build output | Alpha |

---

## Enforcement

1. **CI Macrobenchmark** — Every PR targeting a release branch runs the Macrobenchmark suite. Results are compared against the recorded baseline.
2. **Benchmark suite** — The full benchmark catalog is defined in [`testing/PerformanceTests.md`](../testing/PerformanceTests.md).
3. **Merge gate** — Any regression exceeding **20 %** from the baseline blocks merge to the release branch. The author must either fix the regression or provide a documented exception with a remediation plan.
4. **Release gate** — Any metric at or above its **Critical** threshold blocks the release entirely. No exceptions without sign-off from the tech lead.
