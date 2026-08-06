# Sandbox Security Policy — Nexora

> **Status: CANONICAL** for sandbox containment, egress, isolation, and resource rules.
> This document owns the sandbox security policy: process isolation, filesystem
> restrictions, network egress rules, resource quotas, and quarantine behavior.
> It does NOT own the sandbox subsystem design (see
> [../architecture/SANDBOX.md](../architecture/SANDBOX.md)), security architecture
> (see [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md)),
> or permission semantics (see [PermissionModel.md](PermissionModel.md)).
>
> Depends on: [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md), [PermissionModel.md](PermissionModel.md).
> Referenced by: [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

The Nexora sandbox confines all agent and tool execution to the app's private storage. No code running inside the sandbox may access the host filesystem, device hardware, or other workspaces without an explicit, audited permission grant.

## 1. Sandbox Boundaries

| Property | Value |
|----------|-------|
| Root path | `/data/data/com.nexora.app/sandbox/workspaces/{id}/files/`
| Accessible storage | App-private only; never `/sdcard`, `/system`, or `/data/data/other-app/` |
| Inter-workspace access | Prohibited — each workspace's VFS root is an isolated directory |
| Host IPC | Not available — no AIDL, no content providers, no broadcasts from sandbox |

## 2. Filesystem Restrictions

All file I/O is mediated by `SandboxFileSystem`. Direct `java.io.File` or `java.nio.file` usage from plugin/tool code is blocked at classloader level.

| Rule | Detail |
|------|--------|
| **No `/sdcard`** | Any path resolving outside the workspace root is rejected with `NXR-7005` |
| **No `/system`** | Blocklisted at canonical-path check |
| **No sibling workspace access** | Paths containing `../` are canonicalised and validated against the workspace root |
| **No symlinks out** | Symlinks are resolved and re-validated; creation of outbound symlinks is denied |
| **Max file size** | 50 MB per file; writes exceeding this return `NXR-7003` |

```kotlin
class SandboxFileSystem(private val workspaceRoot: Path) {

    fun resolve(userPath: String): Path {
        val canonical = workspaceRoot.resolve(userPath).toRealPathOrNull()
            ?: throw NexoraError.SandboxPathInvalid(userPath)
        require(canonical.startsWith(workspaceRoot.normalize())) {
            "Path escapes workspace: $userPath"  // NXR-7005
        }
        return canonical
    }

    fun openForRead(userPath: String): InputStream {
        val resolved = resolve(userPath)
        return resolved.toFile().inputStream()
    }
}
```

## 3. Network Policy

| Aspect | Rule |
|--------|------|
| **Default** | All outbound connections denied unless `network:http` or `network:websocket` is granted |
| **Whitelist** | When granted, only HTTPS (port 443) is allowed; HTTP is blocked unless explicitly opted in per-domain |
| **DNS** | DNS resolution restricted to system DNS resolver; no custom DNS to prevent DNS exfiltration |
| **No inbound** | Sandbox processes never open listening sockets |

## 4. Process Restrictions

| Limit | Default | Enforcement |
|-------|---------|-------------|
| Max concurrent processes per workspace | 8 | `ProcessManager` counter; reject spawn beyond limit with `NXR-7002` |
| Max CPU time per process | 120 seconds wall-clock | `Handler.postDelayed` cancellation; non-critical processes killed at limit |
| No fork bombs | `RLIMIT_NPROC` equivalent via process counter | Process spawn returns `NXR-7002` when limit reached |
| Process hierarchy | All child processes are children of the sandbox manager service | On workspace destroy, entire process tree is killed via `Process.killProcess` | 

## 5. Memory Restrictions

| Limit | Default | Enforcement |
|-------|---------|-------------|
| Per-process RSS | 128 MB | `android.os.Process` RSS check every 500 ms; kill on exceed (`NXR-7004`) |
| Per-workspace total | 256 MB | Aggregate RSS across all processes in workspace; deny new spawns if at cap |
| Embedding cache cap | 64 MB | LRU eviction in `EmbeddingCache` |

## 6. Disk Quotas

| Threshold | Action |
|-----------|--------|
| 80 % | Warning notification to user; log event |
| 90 % | Read-only mode for non-essential writes; agent warned |
| 100 % | All writes blocked; return `NXR-7003`; auto-cleanup of `temp/` and `logs/` |

Default quota per workspace: **500 MB**. Configurable in workspace settings.

## 7. Environment Variable Restrictions

- Only pre-approved env var names are passed to sandbox processes.
- Blocklist: `PATH` must not contain host paths; `HOME`, `USER`, `SHELL` are overridden to sandbox-safe values.
- No env var may contain an absolute path outside the workspace root.

## 8. Inter-Workspace Isolation

- Workspace A's `SandboxFileSystem` instance cannot resolve a path belonging to Workspace B.
- Agent messages are tagged with `workspaceId`; the `EventBus` drops cross-workspace messages (`NXR-1002` variant).
- Memory stores are scoped: `workspaceMemoryStore` keys are prefixed with `{workspaceId}:`.

## 9. Plugin Execution

Plugins execute inside the calling workspace's sandbox. A plugin receives the same filesystem, network, and process limits as any tool. Plugin code is loaded in an isolated `DexClassLoader` with no parent classloader access to Nexora internals.

## 10. Violation Response

| Violation | Response |
|-----------|----------|
| Path escape attempt | Immediate process kill; audit log entry with severity `CRITICAL`; user notification |
| Network rule breach | Connection terminated; `NXR-2003` returned; violation counted toward workspace risk score |
| Resource limit exceeded | Graceful termination with partial output; `NXR-7xxx` error returned to agent |
| Repeated violations (3+ in 1 hour) | Workspace locked to read-only; user must manually unlock via Settings |

## 11. Blocked Domains & Sensitive App Classes (G3 — Added 2026-08-06)

> **Status:** CANONICAL blocked-list specification (added G3 — 2026-08-06).  
> **Verified research reference:** `aihackers.net` 2026-07-03; `digitalapplied.com` 2026-07-03 (`Kimi Claw` pattern: sensitive accounts must be isolated to prevent fraud/regulatory exposure).  
> **Purpose:** Browser automation (`specs/BROWSER.md`) and any UI-based agent interaction (`AgentType.BROWSER` — `architecture/MULTI_AGENT_SYSTEM.md`) must not interact with banking, payment, trading, or insurance interfaces. The blocked-list protects both the user (accidental exposure of sensitive accounts) and the agent (regulatory/fraud liability).  

### Blocked App Classes (UI/Browser Automation)

| Class | Example Apps / Services | Block Action | Evidence Classification |
|-------|------------------------|--------------|------------------------|
| Banking | `Bank of America`, `Chase Mobile`, `Wells Fargo`, `HSBC`, `Deutsche Bank` | `NXR-7005` (sandbox path/network denial) + audit log (`FR-T015` — `CRITICAL` severity) + user notification (`agent_error`) + isolation warning (`specs/BROWSER.md` — `BlockedListWarning`) | `VERIFIED` (`aihackers.net` 2026-07-03; `digitalapplied.com` 2026-07-03) |
| Payment / Wallet | `PayPal`, `Venmo`, `Apple Pay`, `Google Pay`, `Stripe Dashboard` | Same (`NXR-7005` + audit + isolation warning) | `VERIFIED` (same sources) |
| Trading / Investment | `Robinhood`, `E*TRADE`, `Fidelity`, `Charles Schwab`, `Bloomberg Terminal` | Same (`NXR-7005` + audit + isolation warning) | `VERIFIED` (same sources) |
| Insurance | `Geico`, `Progressive`, `Allstate`, `State Farm` | Same (`NXR-7005` + audit + isolation warning) | `VERIFIED` (same sources) |

### Blocked High-Risk Domains (Network Egress / Browser)

| Domain Pattern | Category | Block Action | Evidence Classification |
|---------------|----------|------------|------------------------|
| `*.bank*`, `*.banking*`, `*.pay*` (subdomain-level) | Banking / Payment | Network connection denied (`NXR-2003`) + sandbox audit (`FR-T015`) + isolation warning (`specs/BROWSER.md` — `BlockedListWarning`) | `ENGINEERING INFERENCE` (domain-pattern blocklists — standard web-security practice; `security/SandboxPolicy.md` §Network Policy already defines `DENY` default for `network:http` unless granted; blocking specific domains is a documentation-level extension, not a new mechanism) |
| `*.crypto*`, `*.bitcoin*`, `*.blockchain*` | Cryptocurrency / High-risk trading | Same (`NXR-2003` + audit + isolation warning) | `ENGINEERING INFERENCE` (same rationale) |
| `*.insurance*`, `*.claims*` | Insurance | Same (`NXR-2003` + audit + isolation warning) | `ENGINEERING INFERENCE` (same rationale) |

### Isolation Warning (`specs/BROWSER.md` — Added G3)

When browser automation (`AgentType.BROWSER`) attempts to navigate to a blocked domain or interact with a blocked app class:

1. **Sandbox denies** (`NXR-7005` for filesystem/network escape attempts; `NXR-2003` for network connections to blocked domains).
2. **Audit log entry** (`FR-T015`) with severity `CRITICAL`: includes `workspaceId`, `agentId`, `blockedDomainOrApp`, `timestamp`, `attemptedAction` (`navigate`/`click`/`fill`/`extract`), and `isolationWarning` (`true`).
3. **User notification** (`agent_error` — `NotificationHelper`) with isolation instruction: "Sensitive account detected. Please isolate this account in a separate workspace (`FR-W005`) with a separate provider profile (`FR-P011`) before attempting automation. See `docs/DECISION_LOG.md` (`DL-023`)."
4. **Agent loop stops** (`AgentLoop` pauses at `Blocked` state — `state-machines/TaskLifecycle.md` `Blocked` — until user explicitly resolves isolation via workspace settings or provides explicit `ALLOW` for the specific scope + domain combination — `security/PermissionModel.md` `Workspace override` layer).

**Traceability (G3 — Documentation Updates Only):**
- `security/SandboxPolicy.md`: Updated (§Blocked Domains and Sensitive Apps — above).
- `specs/BROWSER.md`: Updated (`BlockedListWarning` section — isolation instruction + audit + notification reference).
- `FR.md`: References preserved (`FR-S014` network egress policy; `FR-S015` quarantine; `FR-T015` audit trail; `FR-W001` workspace isolation; `FR-P011` provider profile isolation).
- `docs/DECISION_LOG.md`: `DL-023` (see above) logs the decision with evidence (`Kimi Claw` pattern — `VERIFIED` research; domain-pattern blocklist — `ENGINEERING INFERENCE`).
- `docs/REQUIREMENT_COVERAGE_LEDGER.md`: No new `FR-` / `NFR-` IDs added (G3 extends existing `FR-S014`, `FR-S015`, `FR-T015` — no new architecture; documentation clarification of existing sandbox/network rules).
- `docs/TRACEABILITY.md`: Not updated (no new contract — existing `SandboxPolicy.md` and `BROWSER.md` contracts extended with blocked-list; no new validation case needed — `SEC-SBX-001` covers sandbox violations; blocked-list is a documentation-level specification of existing denial behavior).

**Phase mapping:** `Phase 3` (`security/SandboxPolicy.md` — sandbox security is Phase 3 per `docs/ROADMAP.md`); `Phase 4` (`specs/BROWSER.md` — browser automation is Phase 4); no phase change required (documentation update to existing specs).


> **S4 — Terminal isolation:** Terminal execution governed by `specs/TERMINAL.md` (§Execution Model, §Security & Isolation). Process isolation (`FR-S002`), workspace isolation (`FR-S018`), sandbox policy (`FULL_ENVIRONMENT.md` `proot`/`chroot` isolation) align with terminal mode (subprocess vs PTY). Working-dir boundary (`models/Workspace.md`), output cap (`FR-AS-003` budget), timeout (`FR-AS-002` heartbeat), and restore audit (`FR-AS-007` idempotent + `NFR-REL-012` exactly-once) enforced. See `docs/DECISION_LOG.md` DL-028.
