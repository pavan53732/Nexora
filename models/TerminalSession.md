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
    val taskId: String? = null,              // required for autonomous background sessions (DEC-34)
    val executionId: String? = null,        // required for autonomous background sessions (DEC-34)
    val effectiveDeadline: Instant? = null, // inherited parent deadline for background sessions (DEC-34)
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
    val sessionBufferReplay: Boolean = false,  // replay input after restore (S4)
    val suspended: Boolean = false             // timeout/suspend: Detached with suspended=true (S4; not a separate state)
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

Terminal session lifecycle authority is defined by the canonical [state-machines/TerminalSessionLifecycle.md](../state-machines/TerminalSessionLifecycle.md). The [lifecycle/TerminalSessionLifecycle.md](../lifecycle/TerminalSessionLifecycle.md) document is a derived narrative. Terminal session lifecycle is subordinate to sandbox and tool execution policy. A terminal session MAY participate in a correlated task or tool-call execution, but it MUST NOT become the primary authority for task or execution lifecycle state. Under DEC-34, every autonomous background session MUST carry `taskId`, `executionId`, `workspaceId`, `correlationId`, and the inherited `effectiveDeadline`; an unbound background request is rejected before process creation. Interactive foreground sessions may leave the parent fields null.


> **S4 — Terminal specification fully specified:** Execution model (PTY vs subprocess), working-dir boundary, output caps, timeout discipline, restore behavior, isolation rules. See `specs/TERMINAL.md` (§Execution Model, §Security & Isolation). Lifecycle authority: `state-machines/TerminalSessionLifecycle.md` (S3-E formal state machine); `lifecycle/TerminalSessionLifecycle.md` is derived. Registry sync: `registry/TOOLS.md` (`TOOL-020`..`023`) + `TOOL_MATRIX.md` (terminal capabilities).
