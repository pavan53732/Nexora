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

1. **Authorization Gate**: The runtime executor validates that the calling agent holds sufficient permissions. If sensitive, the Security Engine suspends execution and requests human-in-the-loop approval.
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

## Protocol Rules

- **Correlation Tracing**: Every protocol message MUST propagate `correlationId` and `toolCallId`.
- **At-Least-Once Delivery**: Outbound events MUST be deduplicated by downstream orchestrators using `(toolCallId, version)`.
- **Termination Signalling**: Processes MUST cleanly emit an exit code. A non-zero exit code or an unhandled signal (like OOM Kill `137`) MUST be converted into `NXR-2004` or `NXR-7004` error envelopes.
