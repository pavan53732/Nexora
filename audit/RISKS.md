# Risk Register — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|------------|--------|-----------|-------|
| RISK-001 | Android API deprecation removes sandbox or filesystem APIs | Medium | High | Pin to stable APIs; abstract behind own interfaces; monitor Android developer previews | Core Team |
| RISK-002 | AI provider API breaking changes break agent execution | High | High | Provider abstraction layer; versioned protocol adapters; integration test suite per provider | Core Team |
| RISK-003 | Sandbox escape vulnerability exposes user data | Low | Critical | Defense in depth; code review; external security audit before launch; bug bounty program | Security Lead |
| RISK-004 | Performance degradation on low-end devices (< 4GB RAM) | Medium | Medium | Lazy loading; resource limits; performance profiling on reference low-end device | Performance Lead |
| RISK-005 | APK size exceeds 50MB target | Medium | Low | ProGuard/R8 obfuscation; tree-shaking unused resources; deferred feature download | Build Lead |
| RISK-006 | Plugin API instability forces frequent plugin rewrites | Medium | High | Semantic versioning; deprecation warnings; compatibility shims; plugin API review board | Platform Lead |
| RISK-007 | Memory pressure from concurrent agent execution causes OOM | Medium | High | Per-agent memory budgets; LRU eviction for cached data; monitoring with `MemoryInfo` thresholds | Runtime Lead |
| RISK-008 | AI provider rate limiting blocks user workflows | High | Medium | Exponential backoff with jitter; provider fallback chain; local model option for critical tasks | Provider Lead |
| RISK-009 | Google Play policy changes restrict agent/tool capabilities | Low | High | Monitor policy updates; design features to comply; maintain direct APK distribution channel | Product Lead |
| RISK-010 | User data loss due to corruption or unintended deletion | Low | High | WAL journaling; encrypted backup/restore; undo for destructive operations; crash recovery tests | Data Lead |
| RISK-011 | Multi-agent coordination deadlock | Medium | Medium | Timeout on delegation handoff; cycle detection in dependency graph; deadlock monitor coroutine | Agent Lead |
| RISK-012 | Third-party library vulnerabilities (OkHttp, Room, etc.) | Medium | Medium | Dependabot / Renovate for auto-updates; lockfile auditing in CI; minimal dependency surface | Security Lead |
