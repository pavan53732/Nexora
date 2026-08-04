> **Status: DERIVED** for Memory domain model.
> This document defines the shape and semantics of Memory in the data model.
>
> Depends on: the canonical memory architecture document.
> Referenced by: protocols, storage, ranking, and context-management implementations.

# Domain Model: Memory

```kotlin
data class MemoryRecord(
    val id: String,
    val workspaceId: String?,
    val sessionId: String?,
    val correlationId: String?,
    val scope: MemoryScope,
    val kind: MemoryKind,
    val content: JsonObject,
    val embeddingRef: String?,
    val score: Double?,
    val createdAt: Instant,
    val updatedAt: Instant
)
```

Memory writes are durable records, not transient context projections. Memory retrieval, scoring, and replay operations SHOULD preserve `correlationId` where available so retrieved evidence can be tied back to the originating execution path.
