# Memory System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [AGENT_RUNTIME.md](AGENT_RUNTIME.md)

---

## Overview

Nexora remembers everything. The memory system provides persistent, searchable, semantic memory across sessions and workspaces.

## Memory Tiers

| Tier | Scope | Lifetime | Phase |
|------|-------|----------|-------|
| **Session Memory** | Single conversation | Cleared on session end (configurable) | 6 |
| **Project Memory** | Single workspace | Persists across sessions, tied to workspace | 6 |
| **Long-Term Memory** | Global | Survives app reinstalls (cloud backup optional) | 6 |
| **Knowledge Graph** | Global | Structured entities, relationships, facts | Later |
| **Execution History** | Per task | Full audit trail of every action | 6 |

## Memory Components

| Component | Description |
|-----------|-------------|
| **Embeddings** | Vector embeddings of conversations, files, and documents. |
| **Vector Database** | Local vector DB for storing and querying embeddings. |
| **Semantic Search** | Find relevant past information using natural language queries. |
| **Semantic Recall** | Automatically recall relevant past context for new tasks. |
| **Tool History** | Record of every tool invocation with parameters and results. |
| **File History** | Version history of files modified by agents. |
| **User Preferences** | Learned preferences: coding style, preferred tools, patterns. |

## Memory Flow

```
New Information
    |
    v
Embedding Generator -> Create Vector Representation
    |
    v
Memory Store -> Store in Appropriate Tier (Session/Project/Long-Term)
    |
    v
Knowledge Graph -> Extract and Link Entities
    |
    v
Index Update -> Update Search Indices
    |
    v
Query: User asks something
    |
    v
Semantic Search -> Find Relevant Memories
    |
    v
Context Builder -> Inject Relevant Memories into AI Context
```

## Interfaces

```kotlin
interface MemoryManager {
    suspend fun store(entry: MemoryEntry)
    suspend fun recall(query: String, scope: MemoryScope, limit: Int = 10): List<MemoryEntry>
    suspend fun search(query: String, scope: MemoryScope): List<MemoryEntry>
    suspend fun delete(entryId: String)
    suspend fun list(scope: MemoryScope): List<MemoryEntry>
}

enum class MemoryScope { SESSION, WORKSPACE, LONG_TERM }

data class MemoryEntry(
    val id: String,
    val content: String,
    val embedding: FloatArray?,
    val scope: MemoryScope,
    val workspaceId: String?,
    val tags: List<String>,
    val createdAt: Instant,
    val metadata: Map<String, String>
)
```

## Phase Mapping

- **Phase 6**: Session, Project, Long-Term memory. Semantic search. Execution history.
- **Later**: Knowledge graph. Cloud sync. Advanced embeddings.
