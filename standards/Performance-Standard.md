> **Status: SUPPORTING** for Performance Standard coding standard.
> This document defines conventions for Performance Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Performance Standard — Nexora

## Targets

| Metric | Target |
|--------|--------|
| Cold start (app launch) | < 2 seconds (canonical per NFR-PERF-001) |
| Workspace switch | < 500ms |
| File read (tool) | < 100ms |
| Terminal command | < 500ms |
| First AI token (streaming) | < 500ms (network-dependent) |
| APK size (base) | < 50 MB |
| Memory (idle) | < 512 MB RSS (canonical per NFR-PERF-005) |
| Memory (active agent) | < 1 GB |
| ANR rate | < 0.05% |
| Crash rate | < 0.1% |

## Rules
- Never block the main thread. All I/O is suspend functions.
- Use `Lazy` for heavy initializations.
- Profile before optimizing. Measure, don't guess.
- Use `constrained_layout` in matplotlib (if generating charts).
- Pagination for large lists (files, logs, history).
