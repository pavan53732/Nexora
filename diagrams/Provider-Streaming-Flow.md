> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Provider Streaming Flow

This diagram shows how the agent requests a streamed LLM response, how chunks flow from the provider API through token tracking, and how the UI renders them incrementally.

```mermaid
sequenceDiagram
    participant Agent
    participant ProviderManager
    participant AIProvider
    participant HTTP
    participant ProviderAPI
    participant TokenTracker
    participant EventBus
    participant UI

    Agent->>ProviderManager: streamResponse(messages, tools, model)
    ProviderManager->>ProviderManager: selectProvider(model)
    ProviderManager->>AIProvider: stream(messages, tools, config)
    AIProvider->>HTTP: POST /chat/completions (stream: true)
    HTTP->>ProviderAPI: HTTPS request

    loop Stream chunks
        ProviderAPI-->>HTTP: SSE chunk (data: {...})
        HTTP-->>AIProvider: ResponseChunk
        AIProvider->>AIProvider: parse(chunk)
        AIProvider-->>ProviderManager: Flow<StreamChunk>
        ProviderManager->>TokenTracker: consume(chunk.tokens)

        alt Budget exceeded
            TokenTracker-->>ProviderManager: throw InsufficientBudgetException
            ProviderManager->>HTTP: cancel request
            ProviderManager-->>Agent: BudgetExceededResult
        end

        ProviderManager->>EventBus: publish(StreamChunkEvent)
        EventBus-->>UI: Append chunk to output
    end

    ProviderAPI-->>HTTP: [DONE]
    HTTP-->>AIProvider: Stream complete
    AIProvider-->>ProviderManager: StreamCompleted
    ProviderManager->>TokenTracker: getUsage()
    TokenTracker-->>ProviderManager: UsageStats(promptTokens, completionTokens)
    ProviderManager-->>Agent: ProviderResponse(fullText, toolCalls, usage)
```