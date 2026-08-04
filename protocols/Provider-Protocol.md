> **Status: DERIVED** for Provider message contract.
> This document defines protocol messages for Provider. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Provider.
> Referenced by: models, APIs, SDKs, and tests.


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


## Cross-Layer Contract Rules

Protocol messages MUST map to the normative operation contract of the corresponding API. A message MUST preserve correlation ID, operation ID, lifecycle effect, transition version when applicable, and the canonical error envelope fields defined in [../errors/ERROR_CODES.md](../errors/ERROR_CODES.md).

A protocol consumer MUST treat events as at-least-once, deduplicate by entity and transition version, and never infer success from transport completion alone. Stream and cancellation messages MUST include an explicit terminal outcome.
