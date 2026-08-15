# DEC-41 — Cloud-Only AI Provider Scope and Degradation Policy

- **Status:** Accepted
- **Date:** 2026-08-15
- **Deciders:** Architecture Owner
- **Supersedes:** The active provider-scope effect of DEC-39; DEC-39 remains immutable historical authority for the previously selected local-provider boundary.

## Context

The published provider contract included cloud providers, Ollama, LM Studio, and LOCAL_GGUF. DEC-39 selected local-server Ollama/LM Studio support and a separate Nexora-managed GGUF worker. The product requirement is now cloud AI providers only: Nexora must not bundle, load, manage, or use local AI inference providers or local AI model files.

The existing provider abstraction, named profiles, API-key isolation, typed streaming, health checks, failover, embeddings, tool calling, reasoning-summary boundary, and Provider lifecycle remain valid independently of provider locality.

## Decision

Nexora supports cloud/external AI providers only. The active provider scope is:

- OpenAI-compatible external APIs.
- Anthropic external APIs.
- Gemini external APIs.
- Groq external APIs.
- OpenRouter external APIs.
- Custom external/cloud endpoints only.

Ollama, LM Studio, LOCAL_GGUF, GGUF files, and other local AI inference providers are out of active product scope. They must not be bundled, loaded, managed, or used as an inference fallback. A Custom endpoint is cloud/external only; a localhost, loopback, app-private, or on-device model endpoint is not an eligible provider under this decision.

## Degradation Policy

The active degradation path is:

`Primary cloud provider → alternate eligible cloud provider/profile → cached prior result or supported non-inference workspace operation → read-only workspace access + notification`.

Each descent is announced, audited, and represented by the existing degradation-event mechanism. No local-model tier and no offline agent-inference mode exists. When no eligible cloud provider is reachable, local workspace inspection, history, checkpoints, search over persisted data, file operations already permitted by the active workspace, and other non-inference features may remain available according to their existing contracts; planning, generation, embeddings, and provider-backed agent execution require network connectivity.

## Preserved Invariants

This decision does not create or remove Task, Agent, ProviderStatus, ProviderHealth, ProviderStream, Tool, permission, or lifecycle states. It does not change provider failover lineage, Retry-After bounds, deadlines, cancellation, unknown-completion handling, authorization, sandbox isolation, API-key storage, or no-side-effect rules.

The Provider abstraction remains implementation-independent. The runtime continues to depend on `AIProvider` rather than a concrete provider. Provider-specific behavior remains behind the provider adapter/plugin boundary.

## Required Projections

The canonical Provider System, FR/NFR requirements, assumptions and constraints, provider specifications, Provider API/Protocol/SDK, models, environment setup, product principles, roadmap, README, ADR projections, sandbox/network security wording, risks, test plans, traceability, canonical-source map, completeness inventory, and changelog must describe only the active cloud/external provider scope. Immutable DEC-39 and historical decision/changelog records must remain unchanged and be marked superseded where active scope is discussed.

## Acceptance Evidence

Documentation validation must demonstrate that no active document advertises, requires, routes to, or plans Ollama, LM Studio, GGUF, local model files, localhost AI endpoints, or offline agent inference. Historical DEC-39 references remain allowed only when explicitly identified as historical/superseded. Cloud provider profiles, external endpoint validation, failover, outage degradation, read-only offline behavior, and provider isolation remain planned implementation evidence.
