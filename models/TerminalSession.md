> **Status: DERIVED** for TerminalSession entity shape.
> This document defines the data model for TerminalSession. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for TerminalSession.
> Referenced by: APIs, SDKs, protocols, and tests that consume TerminalSession.


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
