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
- **Capabilities**: Chat, Streaming, Tool Calling, Vision, Embeddings, Reasoning, and any additional capabilities advertised by the selected model descriptor.
- **Models**: User-configurable and selected from the provider catalog; examples must not be treated as pinned defaults because provider catalogs change.
- **Protocol**: REST API with JSON. Streaming via Server-Sent Events or the provider-declared stream transport.
- **Current capability examples**: OpenAI’s current catalog exposes model-specific reasoning levels, long context, Functions, Web search, File search, Computer use, realtime reasoning/tool-use, speech, transcription, and image models. Adapter support remains subject to the canonical model-catalog negotiation contract.

### Anthropic

- **Covers**: Anthropic Claude model families exposed by the current provider catalog; model names and availability are catalog data, not permanent architecture constants.
- **Base URL**: `https://api.anthropic.com`
- **Auth**: `x-api-key` header.
- **Capabilities**: Chat, Streaming, Tool Calling, Vision, and model-specific adaptive or extended thinking where advertised.
- **Models**: Selected from the provider catalog; current first-party documentation distinguishes Fable 5, Opus 5, Sonnet 5, and Haiku 4.5 tiers with different latency, context, output, and thinking characteristics.
- **Protocol**: REST API. Anthropic-specific tool and reasoning-state format; adapters MUST preserve opaque provider continuation artifacts only within the provider contract and MUST NOT expose private reasoning as durable user-visible content.

### Gemini

- **Covers**: Gemini model families exposed by the current provider catalog; model names and availability are catalog data, not permanent architecture constants.
- **Base URL**: `https://generativelanguage.googleapis.com`
- **Auth**: API key as query parameter.
- **Capabilities**: Chat, Streaming, Tool Calling, Vision, Embeddings, structured outputs, code execution, Search/URL grounding, multimodal function responses, and model-specific thinking levels where advertised.
- **Models**: Selected from the provider catalog; current first-party documentation describes Gemini 3.7 Flash as a 1M-context, 64K-output model with low/medium/high thinking levels and agentic multi-step execution.
- **Protocol**: Google AI REST/Interactions API. Adapters MUST preserve provider-required turn identifiers and thought signatures according to the selected model contract.

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
| **Streaming** | Per-profile streaming toggle (FR-P004); streamed via `Flow<StreamEnvelope>` (FR-P014, see [../models/Inference.md](../models/Inference.md)). |
| **Parameters** | Temperature, max tokens, stop sequences, and other provider params. |
| **Capabilities** | The profile's negotiated `ProviderCapability` set, including modalities, reasoning levels, tool families, search/file/code/computer-use, realtime I/O, citations, stream/resume behavior, and evidence requirements. |
| **Catalog snapshot** | Exact model identifier/version, retrieval time, provider catalog source, adapter contract version, and capability metadata used for the active route. |
| **Reasoning continuation** | Provider-specific adaptive-thinking or opaque continuation metadata, never raw private chain-of-thought; retained only under the provider adapter’s integrity, expiry, and privacy rules. |

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

## Model-Catalog and Capability Negotiation

A profile MUST NOT treat a provider name as proof that every model in that provider supports the same capabilities. Before a route is accepted, the adapter MUST resolve a model descriptor from the current provider catalog and negotiate the requested hard capabilities, modalities, context/output limits, reasoning effort, stream mode, cancellation, resume, data locality, and provider contract version.

Catalog refresh is separate from an in-flight route. A refreshed catalog may change new-route eligibility, deprecation status, or available model choices, but it MUST NOT mutate the model identity or capability snapshot already recorded on an active execution. Unsupported advanced capabilities MUST produce an explicit incompatibility outcome or a policy-approved fallback; they MUST NOT be silently discarded.

### Provider-Native Reasoning State

`ReasoningPolicy`, `ReasoningEffort`, `ReasoningSummary`, `ClaimRecord`, and provider-native continuation state are distinct. Provider adapters own mapping from the canonical policy to provider-specific thinking levels, effort parameters, reasoning-token budgets, thought signatures, or equivalent opaque continuation artifacts. Raw private chain-of-thought is not persisted or exposed. Provider-native continuation state is bound to provider/model/request/stream identity and is not replayed across provider failover unless a compatible translation contract exists.

## Typed Stream and Reasoning Adapter Requirements (ADR-0008)

Every provider/model profile declares context/output limits, tokenizer, Tool/citation/
reasoning capabilities, resume mode, data locality, provider usage/cost metadata, and
observed latency/reliability. Cost metadata is observational and does not create an
internal credit or financial-cost execution gate.
Adapters normalize native events to `StreamEnvelope`; providers without native
streaming emit a synthetic canonical Started/delta/Terminal sequence.

| Native behavior | Canonical projection |
|---|---|
| Provider thought signature or opaque continuation artifact | Adapter-owned provider state, bound to provider/model/request/stream identity; never raw private chain-of-thought |
| Adaptive or level-based thinking control | Canonical `ReasoningPolicy`/`ReasoningEffort` projection plus recorded provider mapping |
| Web/file search or code execution result | Tool/citation/evidence events with source and provenance metadata |
| Multimodal function response | Capability-negotiated typed payload; unsupported media is not silently reduced to text |
| Realtime audio/transcription event | Capability-negotiated audio event family with permission, cancellation, and terminal semantics |
| SSE/WebSocket text delta | `TextDelta` with monotonic sequence |
| Provider reasoning summary | Redacted `ReasoningSummaryDelta`; raw private reasoning excluded |
| Function/tool fragments | Started/ArgumentsDelta/Committed assembly contract |
| Usage update | `UsageDelta`; terminal usage reconciles totals |
| Native cursor | `NATIVE_CURSOR` same-stream resume |
| No cursor | `RESTART_WITH_LINEAGE` or explicit partial failure |
| Socket close without done marker | `NXR-4017`, never success |

Provider-specific reasoning parameters remain adapter-owned, but all adapters enforce the
resolved `ReasoningPolicy` technical token/call/time and safety ceilings and report
supported effort mapping. Provider usage and cost are reconciled as informational metadata;
adapters MUST NOT block or terminate a technically valid run because of internal credits or
financial cost.

## Phase Mapping

- **Phase 1**: Profile model, configuration UI, encrypted key storage.
- **Phase 5**: All 9 providers implemented; streaming; health checks; profile switching.
- **Phase 8**: Providers installable as plugins.

---

## Real-Time Voice & Live Camera — Roadmap / Optional (G5 — Added 2026-08-06)

> **Status:** ROADMAP / OPTIONAL feature specification (G5 — 2026-08-06).  
> **Verified research reference:** `aihackers.net` 2026-07-03; `flowtivity.ai` 2026-07-12 (`Grok` / `MiniMax Hailuo` patterns — voice and camera as native agent I/O modes, not just chat attachments).  
> **Gating:** Existing permission scopes (`security/PermissionModel.md`): `device:camera` (`DENY` default), `device:storage` (`DENY` default), `device:notifications` (`ASK` default). No new scopes added — G5 uses existing scopes.  
> **Mapping:** `Android Device` category (`architecture/TOOL_SYSTEM.md` §Category 18) extended with streaming behavior (not new category): `device_camera_stream` (`TOOL-403`) supports continuous camera stream (`Streaming` flag `✓`) for live agent observation; `device_audio_stream` (`TOOL-404`) supports real-time microphone-audio stream (`Streaming` flag `✓` — aligns with `ai_transcribe` `TOOL-101` which already supports streaming). The non-streaming capture tools remain `device_camera` (`TOOL-302`) and `device_audio` (`TOOL-303`).
> **Autonomy control (`FR-S016`):** Real-time device I/O requires `Manual` or `Assisted` autonomy mode (`FR-S016`); `Autopilot` mode cannot invoke `device:*` scopes without explicit user confirmation (`FR-AS-005` — trust growth requires successful history before `Autopilot` grants `device:*`).  
> **Security (`security/PermissionModel.md` — G2 deny-by-default):** `device:camera` and `device:microphone` remain `DENY` by default; user must explicitly grant (`ALLOW`) through workspace settings (`FR-W005`) or agent-level override; the optional `AutoApprovalClassifier` (`security/PermissionModel.md` §Auto-Approval Classifier) can `DENY` risky device calls even if `ALLOW` is granted (independent safety layer).
> **Phase:** Phase 5 or later (`docs/ROADMAP.md` — optional; does not change phase mapping; `Android Device` category exists; streaming support exists via `Streaming` capability in `registry/TOOL_MATRIX.md`).  
> **Evidence classification:** `VERIFIED` (`Grok` / `MiniMax Hailuo` voice/camera patterns — verified by public sources); `ENGINEERING INFERENCE` (extension of existing `Android Device` category with `Streaming` flag — standard capability mapping, no new interface); `UNKNOWN` (exact model accuracy for real-time voice transcription — future work; streaming mechanism exists, model selection is provider-level — `specs/AI_PROVIDERS.md` Phase 5 covers vision; real-time transcription aligns with `ai_transcribe` `TOOL-101` and `ai_speech` `TOOL-102`).  
> **Traceability (G5 — Documentation Updates Only):** `architecture/TOOL_SYSTEM.md` updated (§Category 18 — streaming note); `security/PermissionModel.md` unchanged (`device:*` scopes preserved, `DENY` default preserved, `AutoApprovalClassifier` applies); `docs/DECISION_LOG.md`: `DL-024` logs the decision; `docs/REQUIREMENT_COVERAGE_LEDGER.md`: no new `FR-` / `NFR-` IDs (G5 is optional roadmap extension of existing `FR-S001`..`FR-S028` — device access; `FR-P009` — token tracking includes streaming; `FR-A010` — real-time monitoring includes device events); `docs/TRACEABILITY.md`: not updated (optional feature; no new contract; existing device/access contracts sufficient).
