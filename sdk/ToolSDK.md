# Tool SDK — Nexora

The Tool SDK provides standard base classes, dependency injection utilities, and convenience adapters for developer-authored tool implementations.

---

## SDK Architecture

All developer-defined tools MUST extend the standard `BaseTool` class provided by the SDK. This guarantees that parameters schema validation, permission checks, timeouts, and execution logs are consistently structured and handled without boilerplate.

```kotlin
package com.nexora.app.sdk.tool

abstract class BaseTool(
    val descriptor: ToolDescriptor
) {
    /**
     * Executes the tool with the validated parameters.
     * Throws NexoraError exceptions on failures.
     */
    abstract suspend fun execute(
        parameters: JsonObject, 
        context: ToolContext
    ): ToolOutput
}

data class ToolContext(
    val correlationId: String,
    val workspaceId: String,
    val agentId: String,
    val sandboxDirectory: String,
    val limits: SandboxLimits
)

data class ToolOutput(
    val success: Boolean,
    val result: JsonObject?,
    val error: CanonicalErrorEnvelope? = null
)
```

## Lifecycle Alignment

When writing custom tools, authors MUST respect the platform's lifecycle boundaries:
- **Terminal Session Alignment**: Tools executing commands within bash or persistent consoles MUST register their process handles using the `TerminalSessionLifecycle` registry, allowing the watchdog to monitor for hangs.
- **Transactional Side-effects**: Stateful tools modifying workspace files MUST utilize the virtual filesystem (`VFS`) interface rather than raw Java IO, allowing automated per-file snapshots (`FR-M012`) and full workspace rollbacks (`FR-S013`).

## Error Wrapping & Conformance

Custom tools MUST NOT leak raw Java/Kotlin exceptions (like `FileNotFoundException` or `IOException`) across the SDK boundaries. The SDK wrapper automatically catches all exceptions and wraps them into:
- `NXR-2004` (Execution Failed) — for unhandled tool exceptions.
- `NXR-2005` (Invalid Parameters) — for parameters violating the tool's JSON schema.
- `NXR-2002` (Timeout) — when execution exceeds the declared `timeoutMs` threshold.
