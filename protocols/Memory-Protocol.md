# Memory Protocol — Nexora

> Communication contract for the memory system.

## Operations

| Operation | Description | Returns |
|-----------|-------------|--------|
| `store(entry)` | Store a new memory entry | `MemoryEntry` with ID |
| `recall(query, scope, limit)` | Semantically search memories | `List<MemoryEntry>` |
| `search(query, scope)` | Keyword search | `List<MemoryEntry>` |
| `delete(id)` | Delete a memory entry | Unit |
| `list(scope)` | List all in scope | `List<MemoryEntry>` |

### Tool History (FR-M011)

| Operation | Description | Returns |
|-----------|-------------|--------|
| `recordToolCall(toolCall, result)` | Persist a tool invocation (tool ID, params, result, duration, permission decision, agent, workspace) | `ToolRecord` |
| `getToolHistory(workspaceId, toolId?, taskId?, limit)` | Query tool invocation history | `List<ToolRecord>` |

### File History (FR-M012)

| Operation | Description | Returns |
|-----------|-------------|--------|
| `recordFileVersion(workspaceId, path, contentHash, diff)` | Snapshot a file version before/after a modification | `FileVersion` |
| `getFileHistory(workspaceId, path)` | List versions of a file (hash, timestamp, agent, diff) | `List<FileVersion>` |
| `revertFile(workspaceId, path, versionId)` | Restore a file to a previous version | `FileVersion` |

### User Preferences (FR-M013)

| Operation | Description | Returns |
|-----------|-------------|--------|
| `setPreference(key, value, scope)` | Store a preference (global or per workspace) | Unit |
| `getPreference(key, scope)` | Read a preference | `String?` |
| `listPreferences(scope)` | List preferences in scope | `Map<String, String>` |

### Knowledge Graph (FR-M014 / FR-M015)

| Operation | Description | Returns |
|-----------|-------------|--------|
| `graphExtract(sourceId, content)` | Extract entities + relationships and merge into the graph (dedupe by entity identity) | `List<GraphEntity>` |
| `graphQuery(entityId, depth)` | Query entities and relationships starting from an entity | `GraphSubgraph` |
| `graphNeighbors(entityId)` | Direct neighbors of an entity | `List<GraphEdge>` |
| `graphSearch(query)` | Semantic search over entities/facts | `List<GraphEntity>` |

## Backing Stores

| Memory type | Storage |
|-------------|---------|
| Session / Project / Long-term entries | Room `memory_entry` table + vector index |
| Tool History | Room `tool_record` table (append-only) |
| File History | Room `file_version` table; content blobs in sandbox `files/.history/` |
| User Preferences | DataStore (global + per-workspace files) |
| Knowledge Graph | Room `graph_entity` + `graph_edge` tables |
| Execution History | Room `execution_event` table (see [Execution Protocol](./Execution-Protocol.md)) |

## Scoring

Recall uses embedding cosine similarity. Results are ranked by relevance score. The threshold (minimum similarity) is configurable per workspace.
