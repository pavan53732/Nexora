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

---

## Real-Time Voice & Live Camera — Roadmap / Optional (G5 — Added 2026-08-06)

> **Status:** ROADMAP / OPTIONAL feature specification (G5 — 2026-08-06).  
> **Verified research reference:** `aihackers.net` 2026-07-03; `flowtivity.ai` 2026-07-12 (`Grok` / `MiniMax Hailuo` patterns — voice and camera as native agent I/O modes, not just chat attachments).  
> **Gating:** Existing permission scopes (`security/PermissionModel.md`): `device:camera` (`DENY` default), `device:storage` (`DENY` default), `device:notifications` (`ASK` default). No new scopes added — G5 uses existing scopes.  
> **Mapping:** `Android Device` category (`architecture/TOOL_SYSTEM.md` §Category 18) extended with streaming behavior (not new category): `device_camera` (`TOOL-403`) supports continuous stream (`Streaming` flag `✓`) for live agent observation; `device_audio` (`TOOL-404`) supports real-time transcription stream (`Streaming` flag `✓` — aligns with `ai_transcribe` `TOOL-101` which already supports streaming).  
> **Autonomy control (`FR-S016`):** Real-time device I/O requires `Manual` or `Assisted` autonomy mode (`FR-S016`); `Autopilot` mode cannot invoke `device:*` scopes without explicit user confirmation (`FR-AS-005` — trust growth requires successful history before `Autopilot` grants `device:*`).  
> **Security (`security/PermissionModel.md` — G2 deny-by-default):** `device:camera` and `device:audio` remain `DENY` by default; user must explicitly grant (`ALLOW`) through workspace settings (`FR-W005`) or agent-level override; the optional `AutoApprovalClassifier` (`security/PermissionModel.md` §Auto-Approval Classifier) can `DENY` risky device calls even if `ALLOW` is granted (independent safety layer).  
> **Phase:** Phase 5 or later (`docs/ROADMAP.md` — optional; does not change phase mapping; `Android Device` category exists; streaming support exists via `Streaming` capability in `registry/TOOL_MATRIX.md`).  
> **Evidence classification:** `VERIFIED` (`Grok` / `MiniMax Hailuo` voice/camera patterns — verified by public sources); `ENGINEERING INFERENCE` (extension of existing `Android Device` category with `Streaming` flag — standard capability mapping, no new interface); `UNKNOWN` (exact model accuracy for real-time voice transcription — future work; streaming mechanism exists, model selection is provider-level — `specs/AI_PROVIDERS.md` Phase 5 covers vision; real-time transcription aligns with `ai_transcribe` `TOOL-101` and `ai_speech` `TOOL-102`).  
> **Traceability (G5 — Documentation Updates Only):** `architecture/TOOL_SYSTEM.md` updated (§Category 18 — streaming note); `security/PermissionModel.md` unchanged (`device:*` scopes preserved, `DENY` default preserved, `AutoApprovalClassifier` applies); `docs/DECISION_LOG.md`: `DL-024` logs the decision; `docs/REQUIREMENT_COVERAGE_LEDGER.md`: no new `FR-` / `NFR-` IDs (G5 is optional roadmap extension of existing `FR-S001`..`FR-S028` — device access; `FR-P009` — token tracking includes streaming; `FR-A010` — real-time monitoring includes device events); `docs/TRACEABILITY.md`: not updated (optional feature; no new contract; existing device/access contracts sufficient).
