> **Status: SUPPORTING** for security threat modeling. This document explains focused usage and behavior but does not own the canonical definition. The canonical source is [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md).
>
> Depends on: [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md).

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
| TM-026 | Context intended for provider A is delivered to provider B (data-flow leak) | Provider System | High | Every request tagged with the active profile ID; single routing path through `ProviderRouter`; cross-provider delivery rejected | Partial |
| TM-027 | Provider plugin reads another provider's API key or configuration | Provider System | Critical | Per-provider `SecureKeyStore` aliases; provider code receives only its own key reference; isolated classloaders | Partial |

### Denial of Service

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-017 | Fork bomb inside sandbox exhausts device processes | Sandbox | Critical | Max 8 concurrent processes per workspace; `RLIMIT_NPROC` enforced | Partial |
| TM-018 | Agent fills sandbox disk, starving other workspaces | Sandbox | High | Per-workspace disk quotas (default 500 MB); alerts at 80 %/90 %/100 %; auto-cleanup of temp files | Partial |
| TM-019 | Memory pressure from large context or embeddings | Runtime | High | Per-workspace memory cap (default 256 MB); LRU eviction in memory store; OOM protection via `onTrimMemory` | Partial |
| TM-020 | Rapid agent spawning floods the event bus | Agent System | Medium | Dynamic concurrency cap per SA-3 (`min(memory_budget/per_agent_est, cpu_cores, configurable_max)`; default 3, high-end 8–16 — see `architecture/MULTI_AGENT_SYSTEM.md` §SA-3, `ResourceManager`, `FR-MA-003`); agent creation rate limit (10/min) preserved independently | Partial |
| TM-021 | Background agent drains battery | Runtime | Medium | Foreground service with notification; Android Doze awareness; `JobScheduler` for non-urgent tasks | Partial |

### Elevation of Privilege

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-022 | Sandbox escape grants access to device filesystem | Sandbox | Critical | All file I/O mediated by `SandboxFileSystem`; no raw `java.io.File` access from plugins or tools | Partial |
| TM-023 | Plugin requests and receives excessive permissions | Plugin System | High | Least-privilege manifest; user reviews each scope at install; no `REQUEST_INSTALL_PACKAGES` ever granted | Mitigated |
| TM-024 | Agent exceeds granted permissions via tool chaining | Agent System | High | Permission check on every individual tool call, not just the first; no implicit permission inheritance across chain steps | Mitigated |
| TM-025 | Malicious provider response injects tool invocations | Provider System | Medium | Provider output is treated as data, not code; tool calls validated against registry before execution | Mitigated |
| TM-028 | Provider plugin performs arbitrary network calls to exfiltrate data | Provider System | High | Provider HTTP clients confined to their configured `baseUrl`; `network:*` grants enforced by `PermissionManager`; no raw sockets exposed to provider code | Partial |
| TM-029 | Rogue mDNS advertisement impersonates a legitimate Nexora instance | Pipe Discovery | High | Pairing requires user-confirmed fingerprint match (Ed25519 public key, QR or 6-word code); discovery is listener-only — no trust is derived from TXT record content before pairing (`specs/PIPES.md` §3, §4) | Partial |
| TM-030 | Unauthorized pairing to a hostile instance via spoofed fingerprint | Pipe Pairing | Critical | Fingerprint confirmed on both ends; `instance:pair` is `ASK` by default; pairing record binds fingerprint + alias + workspace set; `NXR-6009` on mismatch (`specs/PIPES.md` §3; `FR-MI-004`, `FR-MI-008`) | Partial |
| TM-031 | TLS identity substitution (MITM between paired instances) | Pipe Transport | Critical | Mutual TLS 1.3 using pinned `pipeKey` certificates — no CA, no self-signed prompts; `instance:connect` is `ASK` by default; DLP scan on outbound bodies per `NFR-SEC-013` (`specs/PIPES.md` §5, §8; `NFR-SEC-014`) | Partial |
| TM-032 | Malformed/forged pipe payload triggers parser exploitation | Pipe Transport | High | Closed payload type set; schema-validated pre-parse; 3 violations → auto-`Revoked`; audit `CRITICAL` per `FR-TL015` (`specs/PIPES.md` §5, §9; `FR-MI-008`) | Partial |
| TM-033 | Replay attack on pipe messages (duplicate delegation) | Pipe Transport | Medium | Every payload carries a monotonically increasing `pipeSeq`; receiver deduplicates by `(pipeId, pipeSeq)`; matches `NFR-REL-012` exactly-once discipline (`specs/PIPES.md` §5; `FR-MI-006`) | Partial |
| TM-034 | Cross-workspace privilege escalation via pipe routing misconfiguration | Pipe Delegation | Critical | A pipe is bound to exactly one exposed workspace; cross-workspace routing is rejected (`NXR-1002` variant); `FR-MI-008` gates enforced by `PermissionManager` (`specs/PIPES.md` §8; `NFR-SEC-012` network confinement) | Partial |
| TM-035 | Broadcast abuse — attacker floods workspace with broadcast messages | Pipe Broadcast | Medium | `instance:broadcast` is `DENY` by default; rate-limited (1/s, burst 5); recipients treat broadcasts as data, not instructions (`FR-CM-006`); `TM-020` analog applies (`specs/PIPES.md` §7; `FR-MI-007`) | Partial |
| TM-036 | Listener DoS / connection exhaustion on pipe transport ports | Pipe Transport | Medium | Bounded retry (3 attempts, exponential backoff, `NFR-REL-003`); pipe timeout (30 s connect, 120 s task-ack); `Degraded` → `Disconnected` state machine (`specs/PIPES.md` §5, §9; `FR-MI-009`) | Partial |
| TM-037 | LAN metadata leakage — device names, workspace counts exposed via mDNS | Pipe Discovery | Low | TXT records carry only non-sensitive fields (`instanceId`, `fingerprint`, `minContractVersion`, nonce); no workspace names, tool counts, or provider identifiers advertised (`specs/PIPES.md` §3, §4; `FR-MI-001`) | Open |

### Inference Streaming and Reasoning Artifacts

| ID | Threat | Component | Severity | Mitigation | Status |
|----|--------|-----------|----------|------------|--------|
| TM-038 | Forged terminal event marks a partial provider response successful | Provider Stream | Critical | Authenticated stream identity, monotonic sequence, exactly-one terminal state machine | Partial |
| TM-039 | Sequence replay/gap injects, duplicates, or removes streamed content | Provider Stream | High | `(streamId, sequence)` validation, deduplication, gap recovery/failure | Partial |
| TM-040 | Tool argument fragments execute before complete validation | Tool/Provider Boundary | Critical | `ToolCallCommitted` barrier; incomplete fragments discarded | Partial |
| TM-041 | Stream action cannot be attributed after reconnect/failover | Observability | High | request/stream/priorStream/correlation IDs in append-only audit | Partial |
| TM-042 | Raw reasoning artifact leaks credentials, system prompts, or private reasoning | Context/Memory | Critical | Redacted ReasoningSummary only; raw private trace excluded from persistence/export | Partial |
| TM-043 | Resume token theft permits stream/session continuation | Provider Stream | High | Opaque short-lived profile-scoped tokens; redacted logs; secure storage | Partial |
| TM-044 | Cross-provider failover sends context to an ineligible provider | Provider Router | Critical | RoutePlan capability/privacy constraints; new stream lineage; provider isolation | Partial |
| TM-045 | Oversized/high-frequency chunks exhaust memory or UI | Provider Stream | High | Event-size cap, bounded channel, semantic no-drop policy, overflow failure | Partial |
| TM-046 | Slow consumer causes unbounded buffering and app failure | Provider Stream | High | High/low watermarks, producer suspension, safe delta coalescing | Partial |
| TM-047 | Unbounded reasoning/critic loops exhaust cost, battery, or time | Agent Reasoning | High | Persisted ReasoningPolicy budgets and FR-AS-003 escalation | Partial |

---

## Comprehensive Security Controls & Threat-to-Test Mapping Ledger

To satisfy High Finding 11 and ensure complete cryptographic, permission, and isolation coverage, every identified STRIDE threat is mapped to its core mitigating control, active enforcement point, expected containment behavior, and validation test case.

| Threat ID | STRIDE Category | Mitigating Control & Specification Source | Platform Enforcement Point | Expected Denial / Containment Behavior | Validation Case ID |
|---|---|---|---|---|---|
| **TM-001** | Spoofing | JWK/APK signature check (`PluginLifecycle.md`) | `PluginManager.install` | Block ClassLoader load; raise `NXR-6009`; delete payload | `SEC-PLUGIN-001` |
| **TM-002** | Spoofing | Keystore AES hardware-backed transience (`ProviderSDK.md` / `SandboxPolicy.md`) | `SecureKeyStore` wrapper | Plaintext keys never persist on disk; unreadable via adb dumps | `SEC-SECRET-001` |
| **TM-003** | Spoofing | TLS 1.3 pinning (`Provider-API.md`) | `SanitizingHttpClient` | Block socket on certificate mismatch or untrusted root | `SEC-FLOW-001` |
| **TM-004** | Spoofing | Workspace ID token verification (`MULTI_AGENT_SYSTEM.md`) | `EventBus` boundary | Inter-agent messages outside caller's workspace scope are dropped | `SEC-PERM-001` |
| **TM-005** | Tampering | Post-install hash checking (`PluginLifecycle.md`) | `PluginManager.load` | Hash mismatch halts load; raise `NXR-6002`; disable plugin | `SEC-PLUGIN-001` |
| **TM-006** | Tampering | Canonical path validation (`SandboxPolicy.md`) | `SandboxFileSystem.resolve` | Block paths with parent traversal (`../`); throw `NXR-7005` | `SEC-SBX-001` |
| **TM-007** | Tampering | Private sandbox boundaries (`FULL_ENVIRONMENT.md`) | Android OS File System | Non-root processes or other apps cannot read app-private data | `SEC-SBX-001` |
| **TM-008** | Tampering | Write-intent verification log (`MEMORY_SYSTEM.md`) | `MemoryManager` WAL | Out-of-order writes are rejected on hash chain validation | `SEC-SECRET-001` |
| **TM-009** | Repudiation | Mandatory audit logging (`SandboxPolicy.md`) | `ToolManager.execute` | Every tool execution is recorded atomically to immutable Room DB | `SEC-PERM-001` |
| **TM-010** | Repudiation | Immutable permission grant logs (`PermissionModel.md`) | `PermissionManager.decide` | User grants are written atomically to `permission_audit_log` | `SEC-PERM-002` |
| **TM-011** | Repudiation | Append-only plugin audit trails (`protocols/Plugin-Protocol.md`) | `PluginManager` | Active operations and DEX execution are written to Room | `SEC-PLUGIN-001` |
| **TM-012** | Info Disclosure | Isolated bounds and signature perms (`SECURITY_MODEL.md`) | Android IPC boundary | Block external binders; expose only bound services with sig perms | `SEC-SBX-001` |
| **TM-013** | Info Disclosure | ProGuard/R8 symbol stripping (`standards/Security-Standard.md`) | Build Pipeline | Strip log calls containing sensitive keys in release builds | `SEC-SECRET-001` |
| **TM-014** | Info Disclosure | Log level gating and prompt sanitization (`ProviderSDK.md`) | `SanitizingHttpClient` | Redact API keys and prompt bodies from standard Logcat | `SEC-SECRET-001` |
| **TM-015** | Info Disclosure | Disable app backup manifest configuration (`specs/WORKSPACE.md`) | Android Manifest | `allowBackup=false` prevents adb extraction of workspace data | `SEC-SBX-001` |
| **TM-016** | Info Disclosure | Isolated classloaders per plugin (`PluginSDK.md`) | `DexClassLoader` | Plugins cannot read host memory or sibling workspace handles | `SEC-PLUGIN-001` |
| **TM-017** | DoS | Process spawn limiting (`SandboxPolicy.md`) | `ProcessManager` | Spawn exceeding 8 concurrent processes returns `NXR-7002` | `SEC-DOS-001` |
| **TM-018** | DoS | Workspace disk quotas (`SandboxPolicy.md`) | `SandboxFileSystem.write` | Block writes exceeding 500 MB quota; throw `NXR-7003` | `SEC-DOS-002` |
| **TM-019** | DoS | Aggregate workspace RSS memory monitoring (`SandboxPolicy.md`) | `ProcessManager` watchdog | Kill process tree exceeding 256 MB aggregate limit; raise `NXR-7004` | `SEC-DOS-002` |
| **TM-020** | DoS | Dynamic concurrency cap SA-3 (`MULTI_AGENT_SYSTEM.md` §SA-3, `ResourceManager`); 10/min creation rate | `AgentManager` | Block spawns exceeding dynamic cap (default 3, high-end 8–16); drop on bus flood | `SEC-DOS-001` |
| **TM-021** | DoS | Android Doze & WorkManager handoffs (`specs/BACKGROUND_EXECUTION.md`) | `AgentExecutionService` | Release wake lock on low battery; hand off to WorkManager | `SEC-DOS-001` |
| **TM-022** | Privilege Elev | Classloader-level file IO blocks (`SandboxPolicy.md`) | `SandboxFileSystem` | Tool/plugin calls to raw `java.io.File` are blocked; require VFS | `SEC-SBX-001` |
| **TM-023** | Privilege Elev | User-approved scope review at install (`PermissionModel.md`) | `PluginManager.install` | Only user-granted scopes are accessible; others blocked | `SEC-PLUGIN-001` |
| **TM-024** | Privilege Elev | Per-step individual permission validation (`PermissionModel.md`) | `PermissionManager.check` | No implicit inheritance across tool chains; block with `NXR-2003` | `SEC-PERM-001` |
| **TM-025** | Privilege Elev | Schema-enforced tool call validation (`Tool-API.md`) | `ToolManager.resolve` | Unregistered tool names are rejected with `NXR-2001` | `SEC-PERM-001` |
| **TM-026** | Info Disclosure | Active profile tagging and validation (`Provider-API.md`) | `ProviderRouter` | Block completion requests to unassigned profiles; throw `NXR-4010` | `SEC-FLOW-001` |
| **TM-027** | Info Disclosure | Key alias isolation in Keystore (`ProviderSDK.md`) | `SecureKeyStore` | Provider adapters receive alias tokens; direct key read is denied | `SEC-FLOW-001` |
| **TM-028** | Privilege Elev | Base URL network confinement (`ProviderSDK.md`) | `PermissionManager` | Intercept calls to unapproved endpoints; throw `NXR-7005` | `SEC-NET-001` |
| **TM-029** | Spoofing | Ed25519 fingerprint pairing + user confirmation (`specs/PIPES.md` §3-4) | `PipeManager.pair` | mDNS TXT records are listener-only; trust established only on confirmed fingerprint match; reject with `NXR-6009` on mismatch | `SEC-NET-001` |
| **TM-030** | Spoofing | Pairing record validation + instance:pair ASK gate (`specs/PIPES.md` §3; `FR-MI-004`) | `PipeManager.pair` | Unauthorized pairing blocked; `instance:pair` `ASK` keeps gate explicit; pairing binds fingerprint+alias+workspace set per-revocation | `SEC-PERM-001` |
| **TM-031** | Spoofing | Mutual TLS 1.3 with pinned pipeKey certificates + DLP egress scan (`specs/PIPES.md` §5, §8; `NFR-SEC-014`) | `PipeTransport` | No CA or self-signed fallback; identity mismatch drops connection; outbound body DLP scan blocks credential leak (`NFR-SEC-013`) | `SEC-NET-001` |
| **TM-032** | Tampering | Closed payload type set + schema validation pre-parse (`specs/PIPES.md` §5; `FR-MI-008`) | `PipeTransport` | Malformed/forged payloads rejected before parse; 3 violations auto-revoke pipe; audit `CRITICAL` (`FR-TL015`) | `SEC-NET-001` |
| **TM-033** | Tampering | PipeSeq deduplication + NFR-REL-012 exactly-once (`specs/PIPES.md` §5; `FR-MI-006`) | `PipeTransport` | Duplicate `(pipeId, pipeSeq)` dropped; replay of delegation payloads harmless (idempotent-safe target) | `SEC-NET-001` |
| **TM-034** | Elevation | Per-pipe workspace scoping + PermissionManager routing (`specs/PIPES.md` §8; `NFR-SEC-012`) | `PipeManager.route` | Cross-workspace routing rejected (`NXR-1002` variant); pipe bound to exactly one workspace | `SEC-PERM-001` |
| **TM-035** | DoS | Broadcast rate limiting + data-not-instruction rule (`specs/PIPES.md` §7; `FR-MI-007`) | `PipeManager.broadcast` | Rate limit 1/s burst 5; `instance:broadcast` `DENY` default; recipients treat broadcasts as data (`FR-CM-006`) | `SEC-DOS-001` |
| **TM-036** | DoS | Bounded reconnect + pipe timeout discipline (`specs/PIPES.md` §5, §9; `NFR-REL-003`) | `PipeTransport` | 3 retry attempts with exponential backoff; 30 s connect / 120 s task-ack deadlines; `Degraded` → `Disconnected` state machine | `SEC-DOS-001` |
| **TM-037** | Info Disclosure | Minimal mDNS TXT record set (`specs/PIPES.md` §3, §4; `FR-MI-001`) | `NsdManager` service record | Non-sensitive fields only (instanceId, fingerprint, contract version, nonce); no workspace names or provider identifiers advertised | `SEC-NET-001` |
| **TM-038** | Spoofing | ProviderStreamLifecycle terminal invariant | `StreamValidator` | Reject terminal with invalid identity/sequence or second terminal | `SEC-STREAM-001` |
| **TM-039** | Tampering | Monotonic stream sequence and replay protection | `StreamValidator` | Deduplicate replay; recover/fail on gap | `SEC-STREAM-002` |
| **TM-040** | Tampering | ToolCallCommitted assembly barrier | `InferenceAssembler` | Discard incomplete/invalid fragments; no Tool invocation | `SEC-STREAM-003` |
| **TM-041** | Repudiation | Stream/request/lineage/correlation audit fields | `Observability` | Preserve reconnect/failover attribution | `SEC-STREAM-004` |
| **TM-042** | Info Disclosure | ReasoningSummary redaction and retention | `ContextBuilder` / `MemoryManager` | Reject raw private reasoning persistence/export | `SEC-STREAM-005` |
| **TM-043** | Info Disclosure | Opaque scoped resume tokens | `ProviderRouter` | Reject expired/mismatched token; redact logs | `SEC-STREAM-006` |
| **TM-044** | Info Disclosure | ProviderRoutePlan privacy/capability constraints | `ProviderRouter` | Block ineligible failover; new lineage only | `SEC-STREAM-007` |
| **TM-045** | DoS | Event-size cap and bounded channel | `ProviderAdapter` | Fail `NXR-4013`; no unbounded allocation | `SEC-STREAM-008` |
| **TM-046** | DoS | Backpressure high/low watermarks | `StreamProcessor` | Suspend/coalesce safe deltas; preserve semantic events | `SEC-STREAM-009` |
| **TM-047** | DoS | Bounded ReasoningPolicy | `AgentLoop` | Stop/clarify/escalate at call/token/time/cost budget | `SEC-STREAM-010` |

---

## Summary

| Category | Total | Mitigated | Partial | Open |
|----------|-------|-----------|---------|------|
| Spoofing | 8 | 3 | 5 | 0 |
| Tampering | 8 | 1 | 6 | 1 |
| Repudiation | 4 | 2 | 2 | 0 |
| Information Disclosure | 11 | 4 | 6 | 1 |
| Denial of Service | 10 | 0 | 10 | 0 |
| Elevation of Privilege | 6 | 3 | 3 | 0 |
| **Total** | **47** | **13** | **32** | **2** |
