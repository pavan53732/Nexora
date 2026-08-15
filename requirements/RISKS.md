> **Status: SUPPORTING** for RISKS requirements.
> This document records focused requirements for RISKS; canonical subsystem definitions remain in the owning architecture documents.


# Risk Register — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|------------|--------|-----------|-------|
| RISK-001 | Android API deprecation removes sandbox or filesystem APIs | Medium | High | Pin to stable APIs; abstract behind own interfaces; monitor Android developer previews | Core Team |
| RISK-002 | AI provider API breaking changes break agent execution | High | High | Provider abstraction layer; versioned protocol adapters; integration test suite per provider | Core Team |
| RISK-003 | Sandbox escape vulnerability exposes user data | Low | Critical | Defense in depth; code review; external security audit before launch; bug bounty program | Security Lead |
| RISK-004 | Performance degradation on low-end devices (< 4GB RAM) | Medium | Medium | Lazy loading; resource limits; performance profiling on reference low-end device | Performance Lead |
| RISK-005 | Minimal-foundation APK exceeds its 50MB target | Medium | Low | ProGuard/R8 obfuscation; tree-shaking unused resources; keep Full Environment assets outside the minimal-foundation variant | Build Lead |
| RISK-006 | Plugin API instability forces frequent plugin rewrites | Medium | High | Semantic versioning; deprecation warnings; compatibility shims; plugin API review board | Platform Lead |
| RISK-007 | Memory pressure from concurrent agent execution causes OOM | Medium | High | Per-agent memory budgets; LRU eviction for cached data; monitoring with `MemoryInfo` thresholds | Runtime Lead |
| RISK-008 | Cloud AI provider rate limiting blocks user workflows | High | Medium | Exponential backoff with jitter; alternate eligible cloud-provider profile chain; cached/non-inference workspace operations; read-only notification | Provider Lead |
| RISK-009 | Google Play policy changes restrict agent/tool capabilities | Low | High | Monitor policy updates; design features to comply; maintain direct APK distribution channel | Product Lead |
| RISK-010 | User data loss due to corruption or unintended deletion | Low | High | WAL journaling; encrypted backup/restore; undo for destructive operations; crash recovery tests | Data Lead |
| RISK-011 | Multi-agent coordination deadlock | Medium | Medium | Timeout on delegation handoff; cycle detection in dependency graph; deadlock monitor coroutine | Agent Lead |
| RISK-012 | Third-party library vulnerabilities (OkHttp, Room, etc.) | Medium | Medium | Dependabot / Renovate for auto-updates; lockfile auditing in CI; minimal dependency surface | Security Lead |



| RISK-013 | GPL-2.0/3.0 license exposure from bundled Debian-slim rootfs in APK | Medium | High | Bundle rootfs as a data asset; include source offer in `licenses/`; provide in-app OSS attribution; legal review before Play Store submission | Legal/Product |
| RISK-014 | Architecture-specific Full Environment delivery exceeds the DEC-38 80MB gate or device storage expectations | Medium | Medium | Use xz compression, ABI-specific packaging, Android App Bundles, per-ABI measurement, and installed-size monitoring | Build Lead |
| RISK-015 | Rootfs extraction failure on devices with low free storage | Medium | High | Pre-flight storage check; clear user guidance; cleanup incomplete extraction state; support environment reset | Runtime Lead |
| RISK-016 | proot ptrace blocked by SELinux or device security software | Low | High | Detect denial, report clearly, and document incompatible device classes; evaluate platform-specific mitigations | Security Lead |
| RISK-017 | Binary/package compatibility gaps remain despite glibc baseline | Low | Medium | Maintain compatibility matrix, test common packages, and document unsupported cases | Platform Lead |
| RISK-018 | JIT-dependent guest programs (PyPy, numba, unpatched V8) fail under Android W^X with the current `targetSdk=34` baseline | Low | Medium | Pre-patch rootfs with `--jitless` Node.js; document unsupported runtimes; detect and report clear error messages when JIT is requested | Platform Lead |
| RISK-019 | High-frequency or oversized provider stream events exhaust memory/UI capacity | Medium | High | Bounded channels, event-size limits, semantic-event no-drop rules, overflow failure, performance tests | Provider Lead |
| RISK-020 | Mid-stream provider failover produces duplicated or contradictory output | Medium | High | New stream identity with priorStreamId; prohibit silent output splicing; lineage tests | Runtime Lead |
| RISK-021 | Stored reasoning artifacts leak secrets, system prompts, or private model reasoning | Medium | Critical | Persist only redacted ReasoningSummary; retention/export controls; security tests | Security Lead |
| RISK-022 | Tool-call fragments are executed before complete schema validation | Low | Critical | ToolCallCommitted barrier; discard incomplete fragments; protocol/security tests | Tooling Lead |
| RISK-023 | Excessive reasoning/critic loops cause device-resource, latency, or battery runaway; cost impact remains observable but non-blocking | Medium | High | Bounded ReasoningPolicy with technical token/call/time/device/resource ceilings and technical-boundary escalation | Runtime Lead |
