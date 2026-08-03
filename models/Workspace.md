# Domain Model: Workspace

> Canonical domain model. See [specs/WORKSPACE.md](../specs/WORKSPACE.md) for full spec.

```kotlin
package com.nexora.app.core.models

/**
 * A Workspace is the primary entity in Nexora.
 * It contains all artifacts for a project: files, tasks, memory, chats, etc.
 */
data class Workspace(
    val id: String,               // UUID
    val name: String,             // User-visible name
    val description: String,      // Optional description
    val status: WorkspaceStatus,  // ACTIVE or ARCHIVED
    val settings: WorkspaceSettings,
    val createdAt: Instant,
    val updatedAt: Instant
)

enum class WorkspaceStatus { ACTIVE, ARCHIVED }

data class WorkspaceSettings(
    val defaultAgent: String = "coder",
    val defaultProvider: String = "openai",
    val defaultModel: String = "gpt-4o",
    val sandboxLimits: SandboxLimits = SandboxLimits(),
    val toolPermissions: Map<PermissionScope, PermissionDecision> = emptyMap()
)

// Storage: /data/data/com.nexora.app/sandbox/workspaces/{id}/
// Schema version: 1.0
