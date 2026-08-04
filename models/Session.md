> **Status: DERIVED** for Session entity shape.
> This document defines the data model for Session. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Session.
> Referenced by: APIs, SDKs, protocols, and tests that consume Session.


# Domain Model: Session

> Canonical domain model.

```kotlin
package com.nexora.app.core.models

/**
 * A chat session within a workspace.
 */
data class Session(
    val id: String,
    val workspaceId: String,
    val title: String,
    val messages: List<Message>,
    val createdAt: Instant,
    val updatedAt: Instant
)

data class Message(
    val id: String,
    val role: MessageRole,
    val content: String,
    val toolCalls: List<ToolCall>?,
    val timestamp: Instant
)

enum class MessageRole { SYSTEM, USER, ASSISTANT, TOOL }
```
