# Provider Protocol — Nexora

> Communication contract between the runtime and AI providers.

## Request Flow

1. Runtime builds a `CompletionRequest` (messages + tools + model config).
2. Runtime calls `provider.complete(request)` or `provider.stream(request)`.
3. Provider translates to its native API format.
4. Provider makes the HTTP call.
5. Provider translates the response back to `CompletionResponse`.
6. Runtime receives the response.

## Streaming Protocol

Providers use Kotlin `Flow<StreamChunk>`. Each chunk contains:
- `content: String?` — Text delta (null for tool call chunks).
- `toolCalls: List<PartialToolCall>?` — Partial tool call deltas.
- `finishReason: FinishReason?` — Set on the final chunk.

## Error Handling

- **Network errors**: Provider throws `ProviderUnavailableException`. Runtime retries with backoff.
- **Auth errors**: Provider throws `ProviderAuthException`. Runtime notifies user to check API key.
- **Rate limits**: Provider throws `RateLimitException`. Runtime waits and retries.
- **Model errors**: Provider throws `ModelNotFoundException`. Runtime notifies user.
