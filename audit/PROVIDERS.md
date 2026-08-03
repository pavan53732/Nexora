# Provider Registry — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See [specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) for provider details,
> [architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md) for the abstraction,
> and [state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md) for the lifecycle.

**Stable provider identifiers.** Users configure providers through named **profiles**
(API key, endpoint, model, streaming — see [Provider Profiles](../specs/AI_PROVIDERS.md#provider-profiles));
profiles are independent and switchable, with one default per workspace.

| ID | Provider | Protocol | Default Endpoint | Auth | Streaming | Phase | Status |
|----|----------|----------|------------------|------|-----------|-------|--------|
| PROV-001 | OpenAI | OpenAI-compatible REST + SSE | `https://api.openai.com/v1` | Bearer key | ✓ | 5 | Planned |
| PROV-002 | Anthropic | REST | `https://api.anthropic.com` | `x-api-key` | ✓ | 5 | Planned |
| PROV-003 | Gemini | Google AI REST | `https://generativelanguage.googleapis.com` | API key (query) | ✓ | 5 | Planned |
| PROV-004 | Groq | OpenAI-compatible REST + SSE | `https://api.groq.com/openai/v1` | Bearer key | ✓ | 5 | Planned |
| PROV-005 | OpenRouter | OpenAI-compatible REST + SSE | `https://openrouter.ai/api/v1` | Bearer key | ✓ | 5 | Planned |
| PROV-006 | Ollama | OpenAI-compatible (local) | `http://localhost:11434` | None (local) | ✓ | 5 | Planned |
| PROV-007 | LM Studio | OpenAI-compatible (local) | `http://localhost:1234` | None (local) | ✓ | 5 | Planned |
| PROV-008 | Local GGUF | Direct GGUF loading (llama.cpp / mlc-llm) | Local file | None (local) | ✓ | 5 | Planned |
| PROV-009 | Custom | User-defined (OpenAI-compatible or Anthropic format) | User-defined | User-defined | user | 5 | Planned |

**Notes**

- **OpenAI-compatible** covers OpenAI, DeepSeek, Together AI, Fireworks, and any
  OpenAI-API-compatible endpoint (configurable base URL).
- **Local providers** (Ollama, LM Studio, GGUF) run as separate on-device processes
  managed by the user — not embedded (per [CONSTRAINTS](../requirements/CONSTRAINTS.md)).
- **Phase 8**: providers installable as plugins (PLG-018).
