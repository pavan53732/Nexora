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
