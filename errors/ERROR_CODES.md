> **Status: CANONICAL** for the cross-subsystem error identity and recovery contract.
> Architecture documents own subsystem behavior; this document owns the stable error identity, envelope, categories, and recovery metadata shared by protocols, APIs, SDKs, persistence, audit, and tests.
>
> Depends on: subsystem architecture documents for error causes and lifecycle effects.


# Nexora Error Catalog

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---


> **DEC-7 (2026-08-11):** Provider `Retry-After` handling and Task `RetryPending` have independent scopes. Provider throttling does not create, advance, cancel, or otherwise redefine Task retry lifecycle; Task retry identity and durability semantics remain defined in [../decisions/DEC-7-retry-attempt-state.md](../decisions/DEC-7-retry-attempt-state.md).

## Overview

All Nexora errors use the `NXR-` prefix and are grouped by subsystem. Each error carries an HTTP-like category indicating the responsible party and a recovery strategy for callers.

## Canonical Error Envelope

Every error crossing a subsystem, persistence, protocol, API, SDK, background-worker, or audit boundary MUST use the same semantic envelope. Transport-specific representations MAY differ, but they MUST preserve these fields:

| Field | Responsibility | Required meaning |
|---|---|---|
| `code` | Error catalog | Stable `NXR-####` identity; callers MUST branch on this value, not message text |
| `category` | Error catalog | `Client`, `Server`, or `Infrastructure` responsibility |
| `message` | Boundary adapter | Safe human-readable explanation; never the compatibility key |
| `retryability` | Recovery owner | `NEVER`, `SAFE`, or `CONDITIONAL`; conditional errors MUST include a condition |
| `idempotency` | Operation owner | Whether repeating the failed operation is safe, unsafe, or requires an idempotency key |
| `lifecycleEffect` | Owning state machine | State transition or `NO_CHANGE`; failures MUST NOT silently invent a state |
| `recoveryOwner` | Subsystem owner | Component responsible for retry, rollback, cleanup, checkpoint restore, or user action |
| `correlationId` | Runtime boundary | Identifier connecting logs, events, API responses, and audit records |
| `details` | Subsystem adapter | Structured, redacted context; MUST NOT expose credentials or secrets |

A protocol, API, or SDK adapter MUST preserve `code`, `category`, `retryability`, `idempotency`, `lifecycleEffect`, `correlationId`, and redacted `details`. It MAY rename fields for transport conventions, but the mapping MUST be documented and tested.

## Error Responsibility Rules

- The error catalog owns identity and shared recovery metadata.
- The subsystem lifecycle owns the legal lifecycle effect of an error.
- The operation owner owns idempotency and retry conditions.
- The boundary adapter owns serialization and redaction, not reinterpretation.
- Tests MUST assert the canonical code and semantic fields, not only message text or HTTP-like category.


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
| NXR-1014 | Task dependency invalid | Client | Task contains an unknown dependency reference or a dependency cycle discovered before queueing | Correct the dependency graph; do not queue or mutate the Task |
| NXR-1015 | Task dependency unsatisfied | Server | A referenced dependency reached terminal `FAILED` or `CANCELLED`, making the dependent Task unsatisfiable | Fail the dependent Task; do not automatically retry the failed dependency |
| NXR-1016 | Task deadline expired | Infrastructure | Task effective deadline was reached while waiting, blocked, awaiting approval, or awaiting provider retry | Commit the existing `Failed` effect, checkpoint recoverable state where applicable, and do not renew the deadline or retry budget |

---

## NXR-2xxx — Tool System

| Code | Name | Category | Description | Recovery |
|------|------|----------|-------------|----------|
| NXR-2001 | Tool not found | Client | Agent requested a tool name not present in the registry | Return error to agent so it can retry with a valid tool |
| NXR-2002 | Tool timeout | Infrastructure | Tool execution exceeded the configured timeout | Kill tool process; report partial output if available |
| NXR-2003 | Tool authorization denied | Client | A valid Tool call failed a permission, approval, or classifier gate; see subreason table below | Recover according to subreason; never execute before authorization succeeds |
| NXR-2004 | Tool execution failed | Server | Tool threw an unhandled exception during execution | Log stack trace; return structured error to agent |
| NXR-2005 | Tool validation failed | Client | Tool descriptor or invocation parameters fail canonical schema/semantic validation | Repair descriptor before registration, or return parameter validation details to the caller |
| NXR-2006 | Tool not registered | Client | Tool class exists but was not registered in `ToolRegistry` | Register tool at startup; check module initialisation order |
| NXR-2007 | Tool chain broken | Server | Output of tool N does not match expected input schema of tool N+1 | Abort chain; report schema mismatch details |
| NXR-2008 | Tool result too large | Client | Tool returned data exceeding the max result size (default 1 MB) | Truncate or summarise result; log truncation |
| NXR-2009 | Tool sandbox error | Server | Tool violated sandbox policy during execution | Terminate tool; record policy violation in audit log |
| NXR-2010 | Tool version incompatible | Client | Installed tool version conflicts with the current runtime API version | Prompt user to update tool or runtime |
| NXR-2011 | Tool already executing | Client | A stateful tool was invoked while a prior invocation is still running | Queue or reject; prevent concurrent mutable access |

### NXR-2003 Authorization Subreasons

| Subreason | Meaning | Prompt? | Recovery |
|---|---|---|---|
| `UNKNOWN_SCOPE` | Tool declares an unregistered scope ID | No | Repair descriptor; reject registration/invocation |
| `POLICY_DENIAL` | Effective Agent/Workspace/Global/default policy is `DENY`, or an approval transaction expires before a valid authorization outcome is committed under DEC-36; an expiry is not an explicit user rejection and does not alter the direct policy-DENY meaning | No automatic prompt | Change policy only through authorized settings, or require a new approval transaction after expiry |
| `USER_DENIED` | User rejected an `ASK` approval | No | Stop; retry only through a new user action |
| `MALFORMED_APPROVAL` | Approval transaction is missing, duplicate, extra, empty, or mismatched | No | Reject, security-audit, never execute |
| `CLASSIFIER_DENIAL` | Selected classifier denied the authorized call | No | Final for this attempt; a later attempt re-runs authorization |

`INVALID_SCOPE_DECLARATION` is descriptor validation, not NXR-2003: it maps to
`NXR-2005`, prevents `DISCOVERED → REGISTERED`, and is never user-prompted.

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
| NXR-4013 | Stream backpressure overflow | Infrastructure | Bounded event queue stayed over capacity beyond deadline | Cancel stream, retain partial output, tune consumer/buffer policy |
| NXR-4014 | Stream resume rejected | Infrastructure | Resume cursor is unsupported, expired, or mismatched | Keep partial result; restart with lineage only when policy permits |
| NXR-4015 | Stream sequence gap | Infrastructure | Stalled stream over failover budget (ProviderStreamLifecycle `stalledFailoverBudget`); missing sequence cannot be recovered | Fail stream; never synthesize missing content |
| NXR-4016 | Incomplete streamed Tool call | Client | Tool fragments ended before schema-valid commit | Discard fragments; never execute |
| NXR-4017 | Stream terminal missing | Infrastructure | Transport closed without canonical terminal event | Commit failure and reconcile usage; never report success |

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

---

## Public Operation to Canonical Error Mapping Matrix

To eliminate responsibility gaps and satisfy Critical Finding 2, every public interface, API, and SDK operation is mapped to its canonical error-handling and recovery behaviors. Implementations MUST enforce these mapping constraints end-to-end.

| Service / Interface | Operation | Canonical Code | Category | Idempotency Rule | Retryability Strategy | Subsystem Lifecycle Effect | Recovery Owner & Action |
|---|---|---|---|---|---|---|---|
| **`AgentApi`** | `registerAgent` | `NXR-3002` | Server | Safe (Idempotent) | Safe | `NO_CHANGE` | Registry: validate manifest/incompatible SDK; reject if duplicate |
| | `startTask` | `NXR-1008` | Client | Safe (Idempotent Key) | Safe | `NO_CHANGE` | User Action: prompt configuration of active provider profile |
| | `startTask` | `NXR-7001` | Server | Unsafe | Conditional (storage-full) | Transition to `FAILED` | Sandbox: wipe temp / clean up workspace caches, retry sandbox creation |
| | `cancelTask` | `NXR-3010` | Client | Safe (Idempotent) | Safe | Transition to `CANCELLED` | Orchestration: commit cancel projection, release CPU wake lock & child tasks |
| | `getTaskStatus`| `NXR-1009` | Client | Safe | Safe | `NO_CHANGE` | Storage: return standard empty/404 projection |
| **`ToolManager`** | `registerTool` | `NXR-2005` | Client | Safe | Never until descriptor repaired | Remains `DISCOVERED` | Tool Registry: reject duplicate/unknown scope IDs, invalid risk level, or invalid schema before registration |
| **`ToolManager`** | `executeTool` | `NXR-2001` | Client | Safe | Never | `NO_CHANGE` | Agent Runtime: report tool not found so agent can self-correct parameters |
| | `executeTool` | `NXR-2002` | Infrastructure | Safe (Idempotent Key) | Conditional (retry counts) | `NO_CHANGE` | Sandbox: kill process, return partial result or trigger exponential backoff |
| | `executeTool` | `NXR-2003` | Client | Safe only with operation idempotency key | Conditional by subreason | `WAITING_APPROVAL` only while an `ASK` transaction is open; otherwise `NO_CHANGE` | Security: follow NXR-2003 subreason table; never execute on denial |
| | `executeTool` | `NXR-2004` | Server | Unsafe | Conditional (retries) | `NO_CHANGE` | Developer Action: log stack trace, run agent bounded self-correction loop |
| | `executeTool` | `NXR-7004` | Infrastructure | Unsafe | Never | Transition to `FAILED` | Sandbox: terminate offending process, record policy breach in audit |
| **`ProviderManager`**| `complete` / `stream` | `NXR-4003` | Client | Safe | Never | `NO_CHANGE` | User Action: prompt to update API credentials in settings |
| | `stream` | `NXR-4013` | Infrastructure | Conditional | Never without policy change | Stream → `FAILED` | Provider Router: cancel transport, retain partial output, audit queue state |
| | `resumeStream` | `NXR-4014` | Infrastructure | Conditional (lineage restart) | Conditional | Stream → `FAILED` or new lineage | Provider Router: keep prior partial; restart only with explicit policy |
| | `stream` | `NXR-4015` / `NXR-4017` | Infrastructure | Unsafe to infer success | Never | Stream → `FAILED` | Stream Validator: fail on unrecoverable gap or missing terminal |
| | `stream` | `NXR-4016` | Client | Conditional regeneration | Never execute partial call | `NO_CHANGE` for Tool | Inference Assembler: discard fragments; optionally retry generation |
| | | `NXR-4004` | Infrastructure | Safe | Conditional (rate-limit backoff)| `NO_CHANGE` | Provider Layer: parse `Retry-After` header, delay request execution |
| | | `NXR-4009` | Infrastructure | Safe | Safe (Automatic fallback) | `NO_CHANGE` | Provider Layer: switch to next Healthy provider in priority queue, emit alert |
| **`PluginManager`** | `installPlugin` | `NXR-6002` | Client | Safe | Never | Transition to `FAILED` | Plugin System: checksum/signature check failed, delete partial files, notify user |
| | `activatePlugin`| `NXR-6003` | Server | Unsafe | Conditional (re-check SDK) | Rollback to `INACTIVE` | Plugin System: rollback exported capability registrations to prior state |
| **`WorkspaceManager`**| `createWorkspace` | `NXR-7001` | Server | Unsafe | Safe | `NO_CHANGE` | Sandbox: wipe temp / clean up workspace caches, retry sandbox creation |
| | `deleteWorkspace` | `NXR-7007` | Server | Safe (Idempotent) | Conditional | `NO_CHANGE` | Sandbox: queue deferred background purge of workspace directories; Workspace deletion may be retried after cleanup succeeds |
| **`WorkflowEngine`** | `executeWorkflow` | `NXR-1002` | Server | Unsafe | Safe | Transition to `FAILED` | Orchestration: cancel downstream tasks, release locks, report failure |

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
