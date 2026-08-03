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
