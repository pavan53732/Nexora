> **Status: SUPPORTING** for AI provider usage and configuration. This document explains focused usage and behavior but does not own the canonical definition. The canonical source is [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md), [../state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md).
>
> Depends on: [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md), [../state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md).

# AI Providers Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md)

---

## Overview

Detailed specification for each AI provider integration. All providers implement the `AIProvider` interface. The runtime never depends on any specific provider.

## Provider Details

### OpenAI-Compatible

- **Covers**: OpenAI, DeepSeek, Together AI, Fireworks, and any OpenAI-API-compatible endpoint.
- **Base URL**: Configurable (default: `https://api.openai.com/v1`)
- **Auth**: Bearer token (API key).
- **Capabilities**: Chat, Streaming, Tool Calling, Vision, Embeddings, Reasoning (e.g. o-series).
- **Models**: User-configurable. Default: `gpt-4o`.
- **Protocol**: REST API with JSON. Streaming via Server-Sent Events.

### Anthropic

- **Covers**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku.
- **Base URL**: `https://api.anthropic.com`
- **Auth**: `x-api-key` header.
- **Capabilities**: Chat, Streaming, Tool Calling, Vision.
- **Models**: `claude-sonnet-4-20250514`, `claude-3-opus-20240229`.
- **Protocol**: REST API. Anthropic-specific tool format.

### Gemini

- **Covers**: Gemini Pro, Gemini Flash, Gemini Ultra.
- **Base URL**: `https://generativelanguage.googleapis.com`
- **Auth**: API key as query parameter.
- **Capabilities**: Chat, Streaming, Tool Calling, Vision, Embeddings.
- **Models**: `gemini-1.5-pro`, `gemini-1.5-flash`.
- **Protocol**: Google AI REST API with `generateContent`.

### Groq

- **Base URL**: `https://api.groq.com/openai/v1`
- **Auth**: Bearer token.
- **Capabilities**: Chat, Streaming, Tool Calling.
- **Models**: `llama-3.1-70b-versatile`, `mixtral-8x7b-32768`.
- **Note**: Uses OpenAI-compatible protocol with Groq's endpoint.

### OpenRouter

- **Base URL**: `https://openrouter.ai/api/v1`
- **Auth**: Bearer token.
- **Capabilities**: Chat, Streaming, Tool Calling, Vision.
- **Models**: Access to 100+ models via unified API.
- **Note**: OpenAI-compatible protocol.

### Ollama

- **Base URL**: Configurable (default: `http://localhost:11434`)
- **Auth**: None (local).
- **Capabilities**: Chat, Streaming, Tool Calling, Vision, Embeddings.
- **Models**: Any model pulled via `ollama pull`.

### LM Studio

- **Base URL**: Configurable (default: `http://localhost:1234`)
- **Auth**: None (local).
- **Capabilities**: Chat, Streaming, Tool Calling.
- **Models**: Any GGUF model loaded in LM Studio.

### Local GGUF

- **Implementation**: Direct GGUF model loading via llama.cpp or mlc-llm.
- **Auth**: None (local).
- **Capabilities**: Chat, Streaming.
- **Models**: Any GGUF file.

### Custom

- **Base URL**: User-defined.
- **Auth**: User-defined (headers, query params, bearer).
- **Capabilities**: User-declared.
- **Protocol**: User selects OpenAI-compatible or Anthropic format.

## Provider Profiles

Users configure providers through **named profiles** — a profile is a complete,
switchable provider configuration:

| Field | Description |
|-------|-------------|
| **Name** | Human-readable profile name (e.g. "OpenAI Work", "Local Fast"). |
| **Provider type** | One of the 9 supported types (PROV-001…009). |
| **API key** | Per-profile key, stored encrypted via `SecureKeyStore` (never plaintext, never logged — NFR-SEC-005). |
| **Endpoint** | Configurable base URL (defaults per provider; required for custom endpoints). |
| **Model** | Default model for the profile; selectable from the provider model catalog (FR-P006). |
| **Streaming** | Per-profile streaming toggle (FR-P004); streamed via `Flow<StreamChunk>`. |
| **Parameters** | Temperature, max tokens, stop sequences, and other provider params. |
| **Capabilities** | The profile's declared `ProviderCapability` set (chat, streaming, tool calling, vision, embeddings). |

Rules:

- **Unlimited profiles per provider** — e.g. multiple OpenAI profiles with different
  keys, or a cloud profile and a local profile (Ollama/LM Studio/GGUF) side by side.
- **Profiles are independent** — create, edit, duplicate, delete, or switch without
  affecting other profiles.
- **Per-workspace default** — a workspace's `settings.default_provider` /
  `settings.default_model` reference a profile; agents route through the workspace's
  active profile.
- **A profile maps to a `ProviderConfig`** (see [models/Provider.md](../models/Provider.md))
  plus a SecureKeyStore key reference.

## Phase Mapping

- **Phase 1**: Profile model, configuration UI, encrypted key storage.
- **Phase 5**: All 9 providers implemented; streaming; health checks; profile switching.
- **Phase 8**: Providers installable as plugins.
