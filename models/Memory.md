> **Status: DERIVED** for Memory entity shape.
> This document defines the data model for Memory. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Memory.
> Referenced by: APIs, SDKs, protocols, and tests that consume Memory.


# Domain Model: Memory

> Canonical domain model. See [architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md).

```kotlin
package com.nexora.app.memory.models

data class MemoryEntry(
    val id: String,
    val content: String,
    val embedding: FloatArray?,  // Vector representation
    val scope: MemoryScope,
    val workspaceId: String?,
    val tags: List<String>,
    val createdAt: Instant,
    val metadata: Map<String, String>
)

enum class MemoryScope { SESSION, WORKSPACE, LONG_TERM }
```
