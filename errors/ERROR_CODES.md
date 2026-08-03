# Nexora Error Catalog

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

All Nexora errors use the `NXR-` prefix and are grouped by subsystem. Each error carries an HTTP-like category indicating the responsible party and a recovery strategy for callers.

### Category Legend

| Category | Meaning | Example Cause |
|----------|---------|---------------|
| **Client** | Caller error — invalid input, missing config, permission denied | Bad parameters, unconfigured provider |
| **Server** | Internal fault — runtime crash, corrupt state, subsystem failure | Database corruption, null pointer in event bus |
| **Infrastructure** | External dependency failure — network, disk, OS limits | Provider timeout, disk full, foreground service denied |

---

## NXR-1xxx — Core Runtime

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-1001 | Sandbox init failed | Server | Could not initialise the sandbox virtual filesystem or runtime process | Retry after freeing storage; if persistent, reinstall |
| NXR-1002 | Event bus publish failed | Server | An event dispatched on the internal EventBus could not be delivered to one or more subscribers | Log undelivered event, continue; inspect subscriber health |
| NXR-1003 | Checkpoint save failed | Server | Agent checkpoint could not be serialised or written to disk | Retry once; if failed, mark workspace unhealthy |
| NXR-1004 | Checkpoint restore failed | Server | Stored checkpoint data is corrupt or incompatible with current version | Fall back to last-known-good checkpoint; alert user |
| NXR-1005 | Agent loop crash | Server | The main agent execution loop exited unexpectedly | Restart agent from last checkpoint; limit restarts to 3 |
| NXR-1006 | Context overflow | Client | Accumulated context window exceeds the provider's token limit | Trigger automatic context pruning; warn user |
| NXR-1007 | Token budget exceeded | Client | Operation consumed more tokens than the configured budget allows | Halt generation; present cost summary to user |
| NXR-1008 | Provider not configured | Client | No AI provider is set up for the requested capability | Prompt user to configure a provider in Settings |
| NXR-1009 | Workspace not found | Client | Referenced workspace ID does not exist on disk | Offer to create or select an existing workspace |
| NXR-1010 | Invalid configuration | Client | A settings value fails schema validation on load | Reset offending key to default; log warning |
| NXR-1011 | Service not bound | Infrastructure | Android service binding failed (e.g. foreground service) | Retry bind; check Android battery optimisation settings |
| NXR-1012 | Foreground service denied | Infrastructure | OS denied the foreground service notification permission | Request notification permission from user; fall back to in-process execution |
| NXR-1013 | Runtime not initialized | Server | Core runtime components were accessed before `NexoraRuntime.init()` completed | Ensure startup sequence completes before exposing UI |

---

## NXR-2xxx — Tool System

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-2001 | Tool not found | Client | Agent requested a tool name not present in the registry | Return error to agent so it can retry with a valid tool |
| NXR-2002 | Tool timeout | Infrastructure | Tool execution exceeded the configured timeout | Kill tool process; report partial output if available |
| NXR-2003 | Tool permission denied | Client | Current permission policy denies access to this tool | Prompt user for one-time or permanent grant |
| NXR-2004 | Tool execution failed | Server | Tool threw an unhandled exception during execution | Log stack trace; return structured error to agent |
| NXR-2005 | Tool invalid parameters | Client | Parameters supplied by the agent fail schema validation | Return validation errors to agent for self-correction |
| NXR-2006 | Tool not registered | Client | Tool class exists but was not registered in `ToolRegistry` | Register tool at startup; check module initialisation order |
| NXR-2007 | Tool chain broken | Server | Output of tool N does not match expected input schema of tool N+1 | Abort chain; report schema mismatch details |
| NXR-2008 | Tool result too large | Client | Tool returned data exceeding the max result size (default 1 MB) | Truncate or summarise result; log truncation |
| NXR-2009 | Tool sandbox error | Server | Tool violated sandbox policy during execution | Terminate tool; record policy violation in audit log |
| NXR-2010 | Tool version incompatible | Client | Installed tool version conflicts with the current runtime API version | Prompt user to update tool or runtime |
| NXR-2011 | Tool already executing | Client | A stateful tool was invoked while a prior invocation is still running | Queue or reject; prevent concurrent mutable access |

---

## NXR-3xxx — Agent System

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-3001 | Agent not found | Client | Referenced agent ID does not exist in the agent registry | Return 404-style error; suggest available agents |
| NXR-3002 | Agent creation failed | Server | Agent factory threw during instantiation | Validate agent config; check required dependencies |
| NXR-3003 | Agent configuration invalid | Client | Agent config JSON fails schema or semantic validation | Return field-level errors to caller |
| NXR-3004 | Agent timeout | Infrastructure | Agent did not produce a response within the configured timeout | Cancel task; offer to extend timeout or retry |
| NXR-3005 | Agent plan failed | Server | Planning phase produced no valid plan or an unparseable plan | Re-prompt with stricter constraints; fall back to single-step |
| NXR-3006 | Agent reflection failed | Server | Self-evaluation step threw or returned invalid scores | Skip reflection for this cycle; log anomaly |
| NXR-3007 | Agent deadlock detected | Server | Two or more agents are waiting on each other's output | Break deadlock by cancelling the lower-priority agent |
| NXR-3008 | Agent memory full | Infrastructure | Agent's working memory buffer has reached capacity | Prune oldest entries; persist to long-term memory |
| NXR-3009 | Agent checkpoint failed | Server | Agent could not save its state for later resumption | Retry once with reduced state; continue without checkpoint |
| NXR-3010 | Agent cancelled by user | Client | User explicitly cancelled the running agent task | Clean up resources; confirm cancellation |
| NXR-3011 | Agent coordination failed | Server | Inter-agent message passing or task delegation failed | Retry delivery; fall back to independent execution |

---

## NXR-4xxx — Provider System

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-4001 | Provider connection failed | Infrastructure | TCP/TLS handshake to provider endpoint failed | Retry with exponential backoff; try fallback provider |
| NXR-4002 | Provider timeout | Infrastructure | Provider did not respond within the configured deadline | Retry; switch to alternative provider if available |
| NXR-4003 | Provider auth failed | Client | API key or OAuth token was rejected by the provider | Prompt user to re-authenticate; check key validity |
| NXR-4004 | Provider rate limited | Infrastructure | HTTP 429 received; rate limit quota exhausted | Wait for `Retry-After` header; queue pending requests |
| NXR-4005 | Provider model not found | Client | Requested model ID is not available on this provider | Suggest alternative models; update configuration |
| NXR-4006 | Provider response invalid | Server | Provider returned malformed JSON or unexpected schema | Retry once; if persistent, log and report to user |
| NXR-4007 | Provider streaming failed | Infrastructure | SSE/WebSocket stream broke mid-generation | Reconnect; regenerate from last complete message |
| NXR-4008 | Provider embedding failed | Server | Embedding API call returned empty or invalid vectors | Retry; fall back to different embedding model |
| NXR-4009 | Provider health check failed | Infrastructure | Pre-flight health check indicates provider is unreachable | Mark provider unhealthy; reroute to healthy fallback |
| NXR-4010 | Provider not configured | Client | No credentials or endpoint configured for this provider | Direct user to provider setup screen |
| NXR-4011 | Provider API key invalid | Client | Stored API key fails format validation or is expired | Prompt user to enter a new key |
| NXR-4012 | Provider quota exceeded | Infrastructure | Monthly or daily token quota is exhausted | Notify user; pause generation until quota resets |

---

## NXR-5xxx — Memory System

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-5001 | Memory store full | Infrastructure | Vector store or working memory reached configured capacity | Trigger LRU eviction; persist evicted entries to disk |
| NXR-5002 | Memory search failed | Server | Vector similarity search threw or returned empty unexpectedly | Retry; fall back to keyword search |
| NXR-5003 | Memory persist failed | Server | Flushing memory to Room/SQLite failed | Buffer writes in memory; retry on next cycle |
| NXR-5004 | Memory entry not found | Client | Requested memory ID does not exist in the store | Return null or empty; let caller handle gracefully |
| NXR-5005 | Memory prune failed | Server | Automatic pruning job threw an exception | Skip this cycle; log and reschedule |
| NXR-5006 | Memory export failed | Server | Exporting memory store to file or JSON failed | Retry with reduced batch size; check disk space |

---

## NXR-6xxx — Plugin System

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-6001 | Plugin install failed | Server | Plugin package could not be extracted or initialised | Verify plugin archive integrity; check dependencies |
| NXR-6002 | Plugin verification failed | Client | Plugin signature or checksum does not match the manifest | Reject installation; warn user of potential tampering |
| NXR-6003 | Plugin load failed | Server | Plugin classloader could not load the plugin's entry point | Check min SDK / runtime version compatibility |
| NXR-6004 | Plugin permission denied | Client | Plugin requests a permission the user has not granted | Prompt user with permission manifest; block until resolved |
| NXR-6005 | Plugin incompatible | Client | Plugin requires a newer Nexora runtime version | Show upgrade prompt; do not load plugin |
| NXR-6006 | Plugin update failed | Server | Downloading or applying a plugin update failed | Roll back to previous version; retry later |
| NXR-6007 | Plugin dependency missing | Client | Plugin requires another plugin that is not installed | Prompt user to install dependency first |
| NXR-6008 | Plugin sandbox error | Server | Plugin violated sandbox boundaries during execution | Terminate plugin; log violation; disable plugin |
| NXR-6009 | Plugin signing invalid | Client | Plugin APK/JAR signature does not match the trusted author | Reject plugin; display security warning to user |

---

## NXR-7xxx — Sandbox

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-7001 | Sandbox creation failed | Server | Could not create a new sandbox instance (missing dirs, perms) | Check internal storage availability; repair layout |
| NXR-7002 | Sandbox process spawn failed | Server | Forking or spawning a child process inside the sandbox failed | Check process limits; kill idle processes |
| NXR-7003 | Sandbox disk full | Infrastructure | Sandbox workspace exceeded its disk quota | Alert user; offer to clean up or expand quota |
| NXR-7004 | Sandbox memory exceeded | Infrastructure | Sandbox process exceeded the per-process memory cap | Kill offending process; log OOM event |
| NXR-7005 | Sandbox network denied | Client | Sandbox attempted a network call not on the whitelist | Block request; return `NXR-2003` to caller |
| NXR-7006 | Sandbox timeout | Infrastructure | Sandbox operation exceeded the wall-clock time limit | Terminate; return partial output to agent |
| NXR-7007 | Sandbox cleanup failed | Server | Post-execution cleanup (temp files, processes) did not complete | Schedule deferred cleanup; monitor for leaks |

---

## NXR-8xxx — UI

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-8001 | Navigation error | Client | Deep link or in-app navigation target does not exist | Fall back to home screen; log invalid route |
| NXR-8002 | Theme apply failed | Server | Dynamic theme data could not be applied to the Compose tree | Fall back to default theme; log error |
| NXR-8003 | Component render error | Server | A Composable threw during recomposition | Show error boundary placeholder; log stack trace |
| NXR-8004 | State restoration failed | Server | Saved state from `SavedStateHandle` was corrupt or missing | Re-initialise from defaults; log data loss |

---

## NXR-9xxx — Storage / Database

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-9001 | Database corruption | Server | Room/SQLite database file is corrupt and cannot be opened | Attempt `PRAGMA integrity_check`; restore from backup |
| NXR-9002 | Migration failed | Server | Schema migration threw or left the database in an inconsistent state | Roll back migration; alert user; do not proceed |
| NXR-9003 | Backup failed | Server | Scheduled or manual backup could not be written | Retry; check available disk space |
| NXR-9004 | Restore failed | Server | Restoring from a backup file failed | Verify backup integrity; try earlier backup |
| NXR-9005 | Export failed | Server | Exporting workspace or settings data failed | Retry with smaller batch; check write permissions |

---

## Error Handling Best Practices (Kotlin)

### 1. Sealed Class Hierarchy

```kotlin
sealed class NexoraError(val code: String, val message: String) {
    data class SandboxInitFailed(val detail: String) :
        NexoraError("NXR-1001", detail)
    data class ToolNotFound(val toolName: String) :
        NexoraError("NXR-2001", "Tool '$toolName' not found in registry")
    data class ProviderRateLimited(val retryAfterMs: Long) :
        NexoraError("NXR-4004", "Rate limited; retry after ${retryAfterMs}ms")
    // … one class per error code
}
```

### 2. Result Type

```kotlin
// Prefer Kotlin's built-in Result<T> for fallible operations
suspend fun executeTool(
    tool: Tool, params: Map<String, Any>
): Result<ToolOutput> = runCatching {
    // throws NexoraError on failure
    tool.execute(params)
}

// Caller
when (val result = executeTool(tool, params)) {
    is Result.Success -> processOutput(result.value)
    is Result.Failure -> handleError(result.exception as NexoraError)
}
```

### 3. Coroutine Exception Handling

```kotlin
val agentScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

agentScope.launch {
    runCatching {
        agent.runLoop() // may throw NexoraError
    }.onFailure { error ->
        when (error) {
            is NexoraError -> logger.warn("${error.code}: ${error.message}")
            is CancellationException -> logger.info("Agent cancelled")
            else -> logger.error("Unexpected error", error)
        }
    }
}
```

> **Rule**: Never swallow `CancellationException`. Always re-throw or handle it explicitly in coroutine scopes.
