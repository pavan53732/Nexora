> **Status: DERIVED** for Tool message contract.
> This document defines protocol messages for Tool operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical tool architecture document (`architecture/TOOL_SYSTEM.md`).
> Referenced by: APIs, SDKs, sandbox, and tests.

# Tool Protocol — Nexora

> Communication and wire contract between the runtime executor, security policy engine, and sandbox tool runners.

## Execution Flow

```text
Runtime Executor         Security Engine           Sandbox Runner
       │                         │                        │
       ├─────── check() ────────>│                        │
       │                         │                        │
       │<──── ALLOW / ASK ───────┤                        │
       │                                                  │
       ├───────────────── execute() ─────────────────────>│
       │                                                  │
       │<─────────────── ToolExecuted ────────────────────┤
```

1. **Authorization Gate**: The complete authorization gate (see `security/PermissionModel.md`) validates the Tool descriptor, resolves every required scope through PermissionScopeRegistry, denies unknown/effective-DENY scopes, aggregates ASK into validated approval transaction, applies ClassifierPolicy, and optionally evaluates the Classifier. Denial returns `NXR-2003` with authoritative subreason (`POLICY_DENIAL`, `USER_DENIED`, `MALFORMED_APPROVAL`, `CLASSIFIER_DENIAL`, `INVALID_SCOPE_DECLARATION`). No Tool side effect occurs before complete authorization.
2. **Process Spawn**: The sandbox manager allocations sandbox memory/disk slices and spawns the tool runner inside proot.
3. **Execution & Stream**: The tool runs, streams real-time stdout/stderr into the activity feed (for long-running terminal scripts), and commits file snapshot modifications.
4. **Outcome Publication**: The sandbox manager collects exit codes, transforms exceptions into `CanonicalErrorEnvelope` records, and dispatches the `ToolExecuted` event onto the Event Bus.

## Message Shapes

### Tool Execution Command

```kotlin
data class ToolExecutionMessage(
    val correlationId: String,
    val workspaceId: String,
    val toolCallId: String,
    val toolId: String,
    val executablePath: String,
    val arguments: List<String>,
    val environmentVariables: Map<String, String>,
    val limits: SandboxLimits
)
```

### Tool Executed Event

```kotlin
data class ToolExecutedEvent(
    val eventId: String,
    val correlationId: String,
    val workspaceId: String,
    val toolCallId: String,
    val toolId: String,
    val exitCode: Int,
    val output: String,
    val errorEnvelope: CanonicalErrorEnvelope?,
    val durationMs: Long,
    val version: Long
)
```

## MCP Tool Mapping (Added G4)

> **Status:** DERIVED protocol clarification (added G4 — 2026-08-06).  
> **Verified research:** `bitdoze.com` 2026-07-24; `mcp.directory` 2026-07-09; `aihackers.net` 2026-07-03.  
> **Mapping rule:** Every MCP primitive (`mcp_call_tool`, `mcp_read_resource`, `mcp_get_prompt`) produces a standard `ToolExecutionMessage` (same `correlationId`, `workspaceId`, `toolCallId`, `limits`) and returns through the standard `ToolResult.Success` / `.Error` / `.NeedsApproval` pipeline.  
> **Transport isolation:** `mcp_connect_stdio` (`TOOL-397`) and `mcp_connect_http` (`TOOL-398`) are registered as `Tool` instances in the registry (`registry/TOOLS.md`) with `requiredPermissions` (`network:http` for HTTP transport; `sandbox:execute` for stdio subprocess execution) and `requiresSandbox` (`true` — sandbox isolation applies per `security/SandboxPolicy.md`).  
> **Negotiation event:** `mcp_list_caps` (`TOOL-399`) produces a `ToolResult.Success` with `output` containing the negotiated capability set; the workspace settings (`FR-W005`) persist the active server profile. No separate event type required — standard `ToolExecutedEvent` covers negotiation outcomes.  
> **Reference:** `architecture/TOOL_SYSTEM.md` (§MCP Client); `security/PermissionModel.md` (`DENY` default for undeclared scopes — G2); `protocols/Provider-Protocol.md` (provider isolation rules extended to MCP servers).

## Protocol Rules

- **Correlation Tracing**: Every protocol message MUST propagate `correlationId` and `toolCallId`.
- **At-Least-Once Delivery**: Outbound events MUST be deduplicated by downstream orchestrators using `(toolCallId, version)`.
- **Termination Signalling**: Processes MUST cleanly emit an exit code. A non-zero exit code or an unhandled signal (like OOM Kill `137`) MUST be converted into `NXR-2004` or `NXR-7004` error envelopes.
