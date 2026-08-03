# Domain Model: TerminalSession

> Canonical domain model. See [specs/TERMINAL.md](../specs/TERMINAL.md).

```kotlin
package com.nexora.app.sandbox.terminal

data class TerminalSession(
    val id: String,
    val workspaceId: String,
    val workingDirectory: String,
    val env: Map<String, String>,
    val history: List<String>,
    val createdAt: Instant,
    val lastActiveAt: Instant
)
```
