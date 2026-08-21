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
| Root path | `/data/data/com.nexora.app/sandbox/workspaces/{id}/files/` |
| Accessible storage | App-private only; never `/sdcard`, `/system`, or `/data/data/other-app/` |
| Inter-workspace access | Prohibited — each workspace's VFS root is an isolated directory |
| Host IPC | Not available — no AIDL, no content providers, no broadcasts from sandbox |

## 2. Filesystem Restrictions

All file I/O is mediated by `SandboxFileSystem`. Direct `java.io.File` or `java.nio.file` usage from plugin/tool code is blocked at classloader level.

| Rule | Detail |
|------|--------|
| **No `/sdcard`** | Any path resolving outside the workspace root is rejected. A path escape by a Tool during execution returns `NXR-2009`; a path escape by a Plugin during execution returns `NXR-6008`. |
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
            "Path escapes workspace: $userPath"  // Tool execution: NXR-2009; Plugin execution: NXR-6008
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
| **Default** | In an `AUTOPILOT` workspace, `network:http` and `network:websocket` default to `ALLOW` for public, routable destinations when no higher-priority restriction applies; `ASSISTED` retains the existing opt-in grant behavior |
| **Destination scope** | No per-workspace Allowed-Domains enrollment is required for the `AUTOPILOT` public-destination default; localhost, loopback, app-private, and other existing higher-priority restrictions remain blocked |
| **Transport** | HTTP port 80 is permitted under the applicable effective mode and grant; HTTPS-only is not an active requirement for the `AUTOPILOT` public-destination default |
| **DNS** | DNS resolution restricted to system DNS resolver; no custom DNS to prevent DNS exfiltration |
| **No inbound** | Sandbox processes never open listening sockets |
| **Egress enforcement boundary** | All guest egress is forced through the host-side workspace egress proxy (`docs/SANDBOX_DEPTH.md` §2.4). proot is launched with `http_proxy`/`https_proxy`/`all_proxy` set to `127.0.0.1:{perWorkspacePort}`; guest processes cannot create direct outbound sockets. The proxy — not an in-guest interceptor — is the sole authority for mode-conditioned admission, secret-material blocking, audit, and grant enforcement |
| **Secret-material protection** | Configured credentials, API keys, and `SecureKeyStore` contents are blocked from transmission to any endpoint except their declared service. The proxy may terminate guest TLS with a workspace-scoped CA (private key in `SecureKeyStore`, never exported to the guest) to enforce this rule; no general full-body policy scan is required |
| **Encrypted egress** | Pinned/foreign-certificate traffic or any attempt to bypass the proxy is denied — fail-closed, with no silent path |
| **Provider & pipe clients** | Host-side provider HTTP clients and pipe transports are *not* guest processes; they remain host-managed and confined by `NFR-SEC-012` / `NFR-SEC-014`. Their outbound payloads are subject to deterministic secret-material blocking before transport encryption, so they do not traverse the guest egress proxy; no general full-body classifier is required |

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
| Path escape attempt | Tool execution: terminate tool, return `NXR-2009`, and record the policy violation in the audit log. Plugin execution: terminate plugin, return `NXR-6008`, record the boundary violation, and disable the plugin. |
| Network rule breach | Connection terminated; `NXR-2003` returned; violation counted toward workspace risk score. A direct guest socket attempt (bypassing the egress proxy) is also terminated and denied — there is no allowlist path for non-proxied egress |
| Resource limit exceeded | Graceful termination with partial output; `NXR-7xxx` error returned to agent |
| Repeated violations (3+ in 1 hour) | Workspace locked to read-only; user must manually unlock via Settings |

## 11. Sensitive Domains & Restricted Action Classes (DEC-47; narrows G3)

> **Status:** CANONICAL sensitive-action specification selected by DEC-47.
> **Purpose:** Browser and UI automation may navigate and perform read-only research on any domain subject to the existing network, permission, sandbox, and untrusted-content contracts. On sensitive banking, payment, trading, cryptocurrency, and insurance domains, credential entry and transaction execution remain denied and audited.

### Sensitive App Action Classes (UI/Browser Automation)

| Class | Example Apps / Services | Block Action | Evidence Classification |
|-------|------------------------|--------------|------------------------|
| Banking | `Bank of America`, `Chase Mobile`, `Wells Fargo`, `HSBC`, `Deutsche Bank` | Deny credential entry and transaction execution through existing PermissionModel/Tool authorization and audit contracts; read-only navigation and extraction are allowed. No local classifier is invoked. | `DECIDED` (DEC-47) |
| Payment / Wallet | `PayPal`, `Venmo`, `Apple Pay`, `Google Pay`, `Stripe Dashboard` | Deny credential entry and transaction execution through existing PermissionModel/Tool authorization and audit contracts; read-only navigation and extraction are allowed. No local classifier is invoked. | `DECIDED` (DEC-47) |
| Trading / Investment | `Robinhood`, `E*TRADE`, `Fidelity`, `Charles Schwab`, `Bloomberg Terminal` | Deny credential entry and transaction execution through existing PermissionModel/Tool authorization and audit contracts; read-only navigation and extraction are allowed. No local classifier is invoked. | `DECIDED` (DEC-47) |
| Insurance | `Geico`, `Progressive`, `Allstate`, `State Farm` | Deny credential entry and transaction execution through existing PermissionModel/Tool authorization and audit contracts; read-only navigation and extraction are allowed. No local classifier is invoked. | `DECIDED` (DEC-47) |

### Sensitive Domains and Restricted Action Classes (Network Egress / Browser)

| Domain Pattern | Category | Restricted action classes | Evidence Classification |
|---------------|----------|--------------------------|------------------------|
| `*.bank*`, `*.banking*`, `*.pay*` (subdomain-level) | Banking / Payment | Credential entry and transaction execution are denied and audited; navigation and read-only extraction are allowed | `DECIDED` (DEC-47) |
| `*.crypto*`, `*.bitcoin*`, `*.blockchain*` | Cryptocurrency / High-risk trading | Credential entry and transaction execution are denied and audited; navigation and read-only extraction are allowed | `DECIDED` (DEC-47) |
| `*.insurance*`, `*.claims*` | Insurance | Credential entry and transaction execution are denied and audited; navigation and read-only extraction are allowed | `DECIDED` (DEC-47) |

### Sensitive Action Denial and Audit (`specs/BROWSER.md`)

When browser or UI automation attempts credential entry or transaction execution on a sensitive domain/app class:

1. **Existing authorization denies.** Navigation and read-only extraction are not denied solely by the domain. Credential entry and transaction execution are denied through existing PermissionModel/Tool authorization; no local classifier is invoked.
2. **Audit log entry** (`FR-TL015`) records `workspaceId`, `agentId`, sensitive domain/app, timestamp, attempted action, and denial reason.
3. **User notification** uses the existing `agent_error` boundary when a user-visible explanation is required.
4. **Continuation status:** The denied action does not execute or automatically resume. A later attempt remains subject to existing authorization, approval, audit, and lifecycle contracts. This rule does not create or reinterpret a TaskLifecycle state or transition.

**Traceability (DEC-47 documentation update):**
- `security/SandboxPolicy.md`: DEC-47 mode-conditioned network defaults, secret-material blocking, and sensitive-domain action floor.
- `specs/BROWSER.md`: free public navigation, resource preferences, loopback floors, untrusted-content wrapping, and restricted sensitive actions.
- `requirements/FR.md`: FR-S014 remains the network-policy owner.
- `docs/DECISION_LOG.md`: DL-087 records DEC-47.
- `docs/REQUIREMENT_COVERAGE_LEDGER.md` and `docs/TRACEABILITY.md`: existing FR-S014/FR-S015/FR-TL015 mappings and security/browser validation projections are synchronized.

**Phase mapping:** `Phase 3` (`security/SandboxPolicy.md` — sandbox security is Phase 3 per `docs/ROADMAP.md`); `Phase 4` (`specs/BROWSER.md` — browser automation is Phase 4); no phase change required (documentation update to existing specs).


> **S4 — Terminal isolation:** Terminal execution governed by `specs/TERMINAL.md` (§Execution Model, §Security & Isolation). Process isolation (`FR-S002`), workspace isolation (`FR-S018`), sandbox policy (`FULL_ENVIRONMENT.md` `proot`/`chroot` isolation) align with terminal mode (subprocess vs PTY). Working-dir boundary (`models/Workspace.md`), technical output cap (`FR-AS-003`), timeout (`FR-AS-002` heartbeat), and restore audit (`FR-AS-007` idempotent + `NFR-REL-012` exactly-once) enforced; these are safety/liveness controls and not financial or credit budgets. See `docs/DECISION_LOG.md` DL-028.
