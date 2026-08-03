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

## Scoring

Recall uses embedding cosine similarity. Results are ranked by relevance score. The threshold (minimum similarity) is configurable per workspace.
