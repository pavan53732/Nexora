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
    val status: MemoryStatus,
    val createdAt: Instant,
    val updatedAt: Instant
)

enum class MemoryScope {
    SESSION,
    WORKSPACE,
    LONG_TERM
}

enum class MemoryKind {
    CONVERSATION,
    TOOL_HISTORY,
    FILE_HISTORY,
    USER_PREFERENCE,
    KNOWLEDGE_GRAPH,
    EXECUTION_HISTORY,
    CONTEXT_SNAPSHOT,
    REASONING_SUMMARY,
    STREAM_LINEAGE,
    LESSON
}

enum class MemoryStatus {
    RECORDED,
    INDEXED,
    RETRIEVED,
    RETAINED,
    EXPIRED,
    DELETED
}
```

## Lifecycle and Execution Semantics

Memory lifecycle authority is defined in [state-machines/MemoryLifecycle.md](../state-machines/MemoryLifecycle.md). The supporting lifecycle narrative is [lifecycle/MemoryLifecycle.md](../lifecycle/MemoryLifecycle.md). Memory writes are durable records, not transient context projections. An `EXPIRED` record is non-revivable: it cannot be reindexed, return to `INDEXED`, or become searchable again. This lifecycle rule does not define replacement-identity behavior. Memory retrieval, scoring, and replay operations SHOULD preserve `correlationId` where available so retrieved evidence can be tied back to the originating execution path.

### Memory Storage Tiers and Pruning

- **Session**: Scoped to a single interactive chat session.
- **Workspace**: Tied to a workspace context; persists across sessions.
- **Long-Term**: System-wide global knowledge or cross-workspace preferences.
- **Eviction / Expiry**: High-volume records (like Tool/File histories) use LRU eviction policies, transitioning from `RETAINED` to `EXPIRED` or `DELETED` to honor configured storage quotas. An `EXPIRED` record remains non-revivable pending deletion.
