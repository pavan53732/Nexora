> **Status: DERIVED** for TerminalSession domain model.
> This document defines the shape and semantics of TerminalSession in the data model.
>
> Depends on: the canonical sandbox and terminal specifications.
> Referenced by: tool execution, sandbox, and runtime implementations.

# Domain Model: TerminalSession

```kotlin
data class TerminalSession(
    val id: String,
    val workspaceId: String,
    val correlationId: String?,
    val status: TerminalSessionStatus,
    val sandboxId: String,
    val startedAt: Instant,
    val updatedAt: Instant,
    val endedAt: Instant? = null,
    val executionMode: String = "SUBPROCESS",  // SUBPROCESS or PTY (S4)
    val workingDirBoundary: String? = null,     // workspace root or sandbox overlay (S4)
    val outputCapBytes: Long = 262_144,         // default 256 KB (subprocess) / 1 MB (PTY interactive) (S4)
    val timeoutMs: Long = 60_000,              // 60s (subprocess) / 300s (PTY) default (S4)
    val restoreCheckpoint: String? = null,     // checkpoint ID for FR-AS-007 restore (S4)
    val sessionBufferReplay: Boolean = false  // replay input after restore (S4)
)

enum class TerminalSessionStatus {
    CREATED,
    ATTACHED,
    RUNNING,
    DETACHED,
    CLOSED,
    FAILED
}
```

## Terminal Session Semantics

Terminal session lifecycle authority is defined in [lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md). The canonical state machine is [state-machines/TerminalSessionLifecycle.md](../state-machines/TerminalSessionLifecycle.md). Terminal session lifecycle is subordinate to sandbox and tool execution policy. A terminal session MAY participate in a correlated task or tool-call execution, but it MUST NOT become the primary authority for task or execution lifecycle state.


> **S4 — Terminal specification fully specified:** Execution model (PTY vs subprocess), working-dir boundary, output caps, timeout discipline, restore behavior, isolation rules. See `specs/TERMINAL.md` (§Execution Model, §Security & Isolation). Lifecycle authority: `lifecycle/TerminalSessionLifecycle.md` (S3 — filled). Registry sync: `registry/TOOLS.md` (`TOOL-020`..`023`) + `TOOL_MATRIX.md` (terminal capabilities).
