> **Status: DERIVED** for memory pipeline visualization.
> Canonical source: [architecture/MEMORY_SYSTEM.md](../../architecture/MEMORY_SYSTEM.md) (§Memory Flow, lines 99-134).
> This diagram introduces no new terminology or architecture.

# Memory Pipeline — Nexora

```mermaid
flowchart TD
    A[New Information] --> B[Embedding Generator]
    B --> C[Memory Store]
    C --> D{Scope}
    D -->|Session| E[Session Memory]
    D -->|Workspace| F[Project Memory]
    D -->|Global| G[Long-Term Memory]
    E --> H[Knowledge Graph]
    F --> H
    G --> H
    H --> I[Index Update]
    I --> J[(Vector Index)]
    I --> K[(FTS Index)]
    J --> L[Semantic Search]
    K --> L
    L --> M[Recall Ranking]
    M --> N[Response Assembly]

    subgraph Tiers["Memory Tiers"]
        E
        F
        G
    end

    subgraph Graph["Knowledge Graph: graph_entity + graph_edge"]
        H
    end

    subgraph Retrieval["Retrieval Phase"]
        L
        M
    end
```
