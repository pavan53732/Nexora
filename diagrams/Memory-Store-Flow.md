> **Status: DERIVED** for Memory Store Flow visual flow.
> This diagram illustrates Memory Store Flow flow. The canonical definition is in the relevant architecture or state-machine document.
>
> Depends on: the relevant canonical architecture or state-machine document.


> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Memory Store Flow

This diagram shows how the agent reads from and writes to the multi-tier memory system — session memory for short-term context, project memory for workspace-scoped data, long-term memory for cross-session persistence, and the knowledge graph for entity relationships.

```mermaid
sequenceDiagram
    participant Agent
    participant MemoryManager
    participant SessionMemory
    participant ProjectMemory
    participant LongTermMemory
    participant KnowledgeGraph
    participant VectorEmbedding
    participant SemanticSearch

    Agent->>MemoryManager: store(result, scope, metadata)

    alt scope = SESSION
        MemoryManager->>SessionMemory: put(key, result)
        SessionMemory-->>MemoryManager: stored
    else scope = PROJECT
        MemoryManager->>ProjectMemory: put(key, result, workspaceId)
        MemoryManager->>VectorEmbedding: embed(result.text)
        VectorEmbedding-->>MemoryManager: float[]
        MemoryManager->>ProjectMemory: index(embedding, metadata)
        ProjectMemory-->>MemoryManager: stored + indexed
    else scope = LONG_TERM
        MemoryManager->>LongTermMemory: put(key, result)
        MemoryManager->>VectorEmbedding: embed(result.text)
        VectorEmbedding-->>MemoryManager: float[]
        MemoryManager->>LongTermMemory: index(embedding, metadata)
        MemoryManager->>KnowledgeGraph: upsertEntities(entities from result)
        KnowledgeGraph-->>MemoryManager: graph updated
    end

    Agent->>MemoryManager: recall(query, scope, limit)
    MemoryManager->>VectorEmbedding: embed(query)
    VectorEmbedding-->>MemoryManager: float[]
    MemoryManager->>SemanticSearch: search(embedding, scope, limit)

    alt scope = SESSION
        SemanticSearch->>SessionMemory: scan()
    else scope = PROJECT
        SemanticSearch->>ProjectMemory: vectorSearch(embedding, limit)
    else scope = LONG_TERM
        SemanticSearch->>LongTermMemory: vectorSearch(embedding, limit)
        SemanticSearch->>KnowledgeGraph: traverseRelated(entities)
    end

    SemanticSearch-->>MemoryManager: List<MemoryEntry>
    MemoryManager-->>Agent: recallResults
```
