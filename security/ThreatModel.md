# Threat Model — Nexora (STRIDE)

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

This document applies the **STRIDE** methodology to identify threats across Nexora's attack surface. Each threat is classified, assessed for severity, and mapped to a mitigation with its current implementation status.

## Trust Boundaries

```
┌─────────────────────────────────────────────────────┐
│                  Android OS / Hardware              │
│  ┌───────────────────────────────────────────────┐  │
│  │              Nexora App Process               │  │
│  │  ┌───────────┐  ┌────────┐  ┌──────────────┐ │  │
│  │  │   UI /    │  │ Runtime│  │   Global     │ │  │
│  │  │ Compose   │──│ Core   │──│   Memory     │ │  │
│  │  └───────────┘  └───┬────┘  └──────────────┘ │  │
│  │                    │                         │  │
│  │  ┌─────────────────▼───────────────────────┐  │  │
│  │  │         Workspace Isolation Layer       │  │  │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │  │
│  │  │  │  WS-1   │ │  WS-2   │ │  WS-N   │   │  │  │
│  │  │  │Sandbox  │ │Sandbox  │ │Sandbox  │   │  │  │
│  │  │  │ + Agent │ │ + Agent │ │ + Agent │   │  │  │
│  │  │  │ + Tools │ │ + Tools │ │ + Tools │   │  │  │
│  │  │  └─────────┘ └─────────┘ └─────────┘   │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
│              │                          │          │
│         ─────┘                          └─────     │
│     AI Providers (TLS)              Plugin Repos    │
└─────────────────────────────────────────────────────┘
```

**Boundaries**: Android sandbox → App process → Workspace isolation → External network.

## Data Flow Summary

| Flow | Data | Protocol | Trust Crossing |
|------|------|----------|----------------|
| User → UI | Touch, text input | Local | None (same boundary) |
| Runtime → Provider | Prompts, API keys | HTTPS / WSS | App → External |
| Agent → Tool | Parameters, file paths | IPC | Workspace → Sandbox |
| Plugin → Sandbox | Code, configs | IPC | Plugin boundary → Sandbox |
| Memory → SQLite | Vectors, entries | Room | Workspace → DB |

---

## STRIDE Threat Catalog

### Spoofing

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-001 | Malicious plugin package impersonates a trusted publisher | Plugin System | Critical | Signature verification against trusted author certs; checksum validation on install | Partial |
| TM-002 | API key theft via memory dump or insecure storage | Provider System | Critical | Android Keystore with hardware-backed encryption; keys never in plain text in app memory | Mitigated |
| TM-003 | Impersonated provider response (MITM) | Provider System | High | Certificate pinning for known provider endpoints; TLS 1.3 enforcement | Mitigated |
| TM-004 | Spoofed inter-agent message from untrusted workspace | Agent System | Medium | Message authentication tokens per workspace; workspace ID validation on every IPC call | Mitigated |

### Tampering

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-005 | Modified plugin binary post-install | Plugin System | Critical | Integrity check on every load (hash comparison with install-time manifest) | Partial |
| TM-006 | Sandbox escape via path traversal or symlink | Sandbox | Critical | Canonical path resolution; block all symlinks pointing outside workspace; chroot-style mount namespace | Partial |
| TM-007 | Configuration file manipulation by other apps on rooted device | Storage | High | App-private storage only (`/data/data/com.nexora.app`); no world-readable files | Mitigated |
| TM-008 | Tampered memory entries to mislead agent reasoning | Memory System | Medium | Write-intent logging; hash chain on memory entries; read-only archival | Open |

### Repudiation

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-009 | Agent action with no audit trail | Agent Runtime | High | Every tool invocation logged with timestamp, agent ID, tool, parameters, result, and permission decision | Mitigated |
| TM-010 | User denies having granted a permission | Permission System | Medium | Immutable permission grant log stored in Room database with creation timestamps | Mitigated |
| TM-011 | Plugin denies having performed a destructive action | Plugin System | Medium | Plugin operations logged in a separate append-only audit table | Partial |

### Information Disclosure

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-012 | Memory content leaked to other apps via IPC or content provider | Memory System | Critical | No content providers exposed; all inter-process communication via bound services with signature permission | Mitigated |
| TM-013 | API keys exposed in Logcat | Provider System | High | ProGuard/R8 stripping; `Log.wtf` for security events only; no key material in any log statement | Mitigated |
| TM-014 | Provider response leaking sensitive user content to logs | Provider System | Medium | Log level gating; prompt/response bodies logged at DEBUG only, stripped in release builds | Mitigated |
| TM-015 | Workspace files readable by other apps (backup) | Storage | High | `allowBackup=false` in manifest; Android auto-backup exclusion rules | Mitigated |
| TM-016 | Plugin reads workspace memory of a different workspace | Plugin System | High | Plugin loaded in caller's classloader; no cross-workspace file handles; path validation on every I/O call | Partial |

### Denial of Service

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-017 | Fork bomb inside sandbox exhausts device processes | Sandbox | Critical | Max 8 concurrent processes per workspace; `RLIMIT_NPROC` enforced | Partial |
| TM-018 | Agent fills sandbox disk, starving other workspaces | Sandbox | High | Per-workspace disk quotas (default 500 MB); alerts at 80 %/90 %/100 %; auto-cleanup of temp files | Partial |
| TM-019 | Memory pressure from large context or embeddings | Runtime | High | Per-workspace memory cap (default 256 MB); LRU eviction in memory store; OOM protection via `onTrimMemory` | Partial |
| TM-020 | Rapid agent spawning floods the event bus | Agent System | Medium | Max 5 concurrent agents globally; agent creation rate limit (10/min) | Partial |
| TM-021 | Background agent drains battery | Runtime | Medium | Foreground service with notification; Android Doze awareness; `JobScheduler` for non-urgent tasks | Partial |

### Elevation of Privilege

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-022 | Sandbox escape grants access to device filesystem | Sandbox | Critical | All file I/O mediated by `SandboxFileSystem`; no raw `java.io.File` access from plugins or tools | Partial |
| TM-023 | Plugin requests and receives excessive permissions | Plugin System | High | Least-privilege manifest; user reviews each scope at install; no `REQUEST_INSTALL_PACKAGES` ever granted | Mitigated |
| TM-024 | Agent exceeds granted permissions via tool chaining | Agent System | High | Permission check on every individual tool call, not just the first; no implicit permission inheritance across chain steps | Mitigated |
| TM-025 | Malicious provider response injects tool invocations | Provider System | Medium | Provider output is treated as data, not code; tool calls validated against registry before execution | Mitigated |

---

## Summary

| Category | Total | Mitigated | Partial | Open |
|----------|-------|-----------|---------|------|
| Spoofing | 4 | 2 | 1 | 0 |
| Tampering | 4 | 2 | 1 | 1 |
| Repudiation | 3 | 2 | 1 | 0 |
| Information Disclosure | 5 | 4 | 1 | 0 |
| Denial of Service | 5 | 0 | 5 | 0 |
| Elevation of Privilege | 4 | 3 | 1 | 0 |
| **Total** | **25** | **13** | **10** | **1** |
