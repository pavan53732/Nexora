# Memory System — Nexora

> **Status: CANONICAL** for memory storage tiers, retention, promotion, and summarization.
> This document owns how memories are stored, tiered (working → short-term → long-term → episodic),
> summarized, promoted between tiers, and retained/evicted. It does NOT own context assembly (context assembly at read time is defined in specs/CONTEXT_MANAGEMENT.md)
> at read time (see [../specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md)).
>
> Depends on: [../specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md) (read-time consumer).
> Referenced by: [AGENT_RUNTIME.md](AGENT_RUNTIME.md), [RUNTIME.md](RUNTIME.md), [../specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

Nexora remembers everything. The memory system provides persistent, searchable, semantic memory across sessions and workspaces.

## Memory Tiers

| Tier | Scope | MemoryKind(s) | Lifetime | Phase |
|------|-------|---------------|----------|-------|
| **Session Memory** | Single conversation | `CONVERSATION` | Cleared on session end (configurable) | 6 |
| **Project Memory** | Single workspace | `CONVERSATION`, `TOOL_HISTORY`, `FILE_HISTORY`, `USER_PREFERENCE`, `EXECUTION_HISTORY` | Persists across sessions, tied to workspace | 6 |
| **Long-Term Memory** | Global | `CONVERSATION`, `USER_PREFERENCE`, `KNOWLEDGE_GRAPH` | Survives app reinstalls (cloud backup optional) | 6 |
| **Knowledge Graph** | Global | `KNOWLEDGE_GRAPH` | Structured entities, relationships, facts | 4 |
| **Execution History** | Per task | `EXECUTION_HISTORY`, `CONTEXT_SNAPSHOT`, `REASONING_SUMMARY`, `STREAM_LINEAGE` | Full audit trail of every action | 6 |

## Memory Components

| Component | Description | MemoryKind |
|-----------|-------------|------------|
| **Embeddings** | Vector embeddings of conversations, files, and documents. | `CONVERSATION`, `FILE_HISTORY` |
| **Vector Database** | Local vector DB for storing and querying embeddings. | — |
| **Semantic Search** | Find relevant past information using natural language queries. | — |
| **Semantic Recall** | Automatically recall relevant past context for new tasks. | — |
| **Tool History** | Record of every tool invocation with parameters and results. | `TOOL_HISTORY` |
| **File History** | Version history of files modified by agents. | `FILE_HISTORY` |
| **User Preferences** | Learned preferences: coding style, preferred tools, patterns. | `USER_PREFERENCE` |
| **Knowledge Graph** | Structured entities, relationships, and facts. | `KNOWLEDGE_GRAPH` |
| **Execution History** | Full audit trail of every action. | `EXECUTION_HISTORY` |
| **Context Snapshots** | Versioned context with included/excluded segments. | `CONTEXT_SNAPSHOT` |
| **Reasoning Summaries** | Redacted structured reasoning artifacts. | `REASONING_SUMMARY` |
| **Stream Lineage** | Stream identity, committed sequence, terminal outcome. | `STREAM_LINEAGE` |

## Memory Backing Stores

| Memory type | Storage | Requirements |
|-------------|---------|--------------|
| Session / Project / Long-Term | Room `memory_entry` + vector index | FR-M001–003, FR-M010 |
| Tool History | Room `tool_record` (append-only) | FR-M011 |
| File History | Room `file_version` + sandbox `files/.history/` blobs | FR-M012, [specs/FILE_SYSTEM.md](../specs/FILE_SYSTEM.md) |
| User Preferences | DataStore (global + per-workspace) | FR-M013 |
| Knowledge Graph | Room `graph_entity` + `graph_edge` | FR-M014–015 |
| Execution History | Room `execution_event` | FR-M005 |
| Context Snapshots | Room `context_snapshot` + segment references | FR-CM-010..012 |
| Reasoning Summaries | Room `reasoning_summary` (redacted, retention-scoped) | FR-RN-011/012 |
| Stream Lineage | Room `inference_stream` + committed sequence/cursor | FR-P014..019 |

Protocol operations and payloads: [protocols/Memory-Protocol.md](../protocols/Memory-Protocol.md).

## Knowledge Graph

The Knowledge Graph stores structured **entities**, **relationships**, and **facts**
extracted from conversations, tool results, and files (FR-M014):

- **Extraction** — `graphExtract(sourceId, content)` runs entity extraction (via the
  AI provider) on new memories and tool outputs; results are merged by entity identity
  (dedupe/merge, no duplicate nodes).
- **Query** — `graphQuery(entityId, depth)` and `graphNeighbors(entityId)` support
  traversal; `graphSearch(query)` adds embedding-based semantic search over
  entities/facts (FR-M015).
- **Scope** — graph is workspace-scoped with a global layer for long-term entities
  (same isolation rules as other memory).
- **Storage** — Room `graph_entity` / `graph_edge` tables; indexes on entity name and
  embedding vector.
- **Tools** — `memory_graph_query` (TOOL-385), `memory_graph_build` (TOOL-386).

### Project Context

The `ProjectIntrospector` (specified in `specs/CONTEXT_MANAGEMENT.md` §8, FR-CM-009)
populates a lightweight ProjectContext in working memory before the Planner runs.
It reads API schemas, database schemas, configuration files, build definitions,
UI layouts, domain models, and infrastructure files — producing structured
summaries tagged with EV confidence (DERIVED/ESTIMATED). Seven introspection tools
(`TOOL-410`..`416`, Category 28) implement the readers. The Knowledge Graph is
queried **after** introspection so entity extraction can reference the fresh
ProjectContext.

## Inference Artifact Retention

- `ContextSnapshot` is immutable and retained with its task/execution evidence window.
- `ReasoningSummary` follows workspace execution-history retention; raw private reasoning is not persisted.
- Stream records persist identity, lineage, last committed sequence, terminal outcome,
  usage, and sanitized error—not every coalesced UI rendering delta indefinitely.
- Tool-call fragments are deleted after commit/failure; committed Tool calls remain in Tool History.
- Export/delete operations preserve workspace scope and redaction rules.

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

- **Phase 2**: Execution history, tool history (FR-M005, FR-M011).
- **Phase 3**: File history (FR-M012).
- **Phase 4**: Semantic memory, user preferences (FR-M006, FR-M013).
- **Phase 5**: Knowledge graph (FR-M014–015).
- **Phase 6**: Session, Project, Long-Term memory. Semantic search. Execution history.
- **Later**: Cloud sync. Advanced embeddings.
