# Sandbox Security Policy — Nexora

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