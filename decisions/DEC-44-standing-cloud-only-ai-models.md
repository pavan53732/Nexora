# DEC-44 — Standing Cloud-Only AI Models Rule

- **Status:** Accepted
- **Date:** 2026-08-17
- **Deciders:** Architecture Owner / Product Owner
- **Supersedes:** The active provider-scope effect of DEC-41 and the active
  local-model effect of DEC-42; DEC-41 and DEC-42 remain immutable historical
  authority for the previously selected cloud-only and no-local-classifier
  boundaries.

## Context

DEC-41 established that Nexora supports cloud/external AI providers only and
that Ollama, LM Studio, LOCAL_GGUF, GGUF files, and localhost AI endpoints are
out of active product scope. DEC-42 removed the optional on-device TFLite
auto-approval classifier and prohibited bundling, loading, executing, or
managing TFLite, ONNX, GGUF, or other local AI model files for any AI-model
function.

The product owner has now confirmed that this is a **standing, non-revisit
rule**: Nexora uses cloud/external AI models only, and it must never bundle,
load, execute, or manage any local AI model or local AI inference runtime. This
decision elevates the combined DEC-41/DEC-42 boundary into a permanent
repository rule (Rule 9 of `AGENTS.md`) so that no future agent, builder, or
decision can reintroduce local models, localhost AI endpoints, or offline
agent-inference modes without an explicit, recorded override.

## Decision

Nexora uses **cloud/external AI models only**. The standing rule is:

- All agent inference, planning, embeddings, routing, and provider-backed
  execution go through eligible cloud providers: OpenAI-compatible external
  APIs, Anthropic external APIs, Gemini external APIs, Groq external APIs,
  OpenRouter external APIs, and custom external/cloud endpoints only.
- Nexora must not bundle, load, execute, manage, or use any local AI model or
  local AI inference runtime. Prohibited: Ollama, LM Studio, LOCAL_GGUF, GGUF
  files, TFLite, ONNX, and any on-device model of any kind, for authorization,
  inference, embeddings, routing, or any other AI-model function.
- A Custom endpoint is cloud/external only. A localhost, loopback,
  app-private, or on-device model endpoint is not an eligible provider under
  this decision.
- When no eligible cloud provider is reachable, the only permitted degradation
  path is: alternate eligible cloud provider → cached prior result or supported
  non-inference workspace operation → read-only workspace access + notification.
  No local-model tier and no offline agent-inference mode exists.

## Preserved Invariants

This decision does not create or remove Task, Agent, ProviderStatus,
ProviderHealth, ProviderStream, Tool, permission, or lifecycle states. It does
not change provider failover lineage, Retry-After bounds, deadlines,
cancellation, unknown-completion handling, authorization, sandbox isolation,
API-key storage, or no-side-effect rules.

The Provider abstraction remains implementation-independent. The runtime
continues to depend on `AIProvider` rather than a concrete provider.
Provider-specific behavior remains behind the provider adapter/plugin boundary.

Local non-AI execution remains allowed. Sandboxed terminal/process execution,
filesystem operations, Git, SQLite/Room persistence, checkpoints, local workspace
search, and read-only offline workspace access are not AI-model execution and
are unaffected.

## Explicit non-decisions

This decision does not require unlimited provider capacity, unlimited model
context, unlimited device resources, or successful execution after a provider
or platform failure. It does not select a concrete billing display, accounting
schema, cost-estimation algorithm, provider pricing source, or routing-
preference UI. It does not introduce a cloud safety-classification service;
that would require a separate decision covering data handling, latency,
availability, error mapping, privacy, egress, and fail-closed behavior.

## Required Projections

The canonical Provider System, FR/NFR requirements, assumptions and constraints,
provider specifications, Provider API/Protocol/SDK, models, environment setup,
product principles, roadmap, README, ADR projections, sandbox/network security
wording, risks, test plans, traceability, canonical-source map, completeness
inventory, and changelog must describe only the active cloud/external provider
scope. Immutable DEC-39, DEC-41, and DEC-42 historical records remain unchanged
and must be marked superseded where active scope is discussed.

## Acceptance Evidence

Documentation validation must demonstrate that no active document advertises,
requires, routes to, or plans Ollama, LM Studio, GGUF, local model files,
localhost AI endpoints, TFLite, ONNX, or offline agent-inference. Historical
DEC-39, DEC-41, and DEC-42 references remain allowed only when explicitly
identified as historical/superseded. Cloud provider profiles, external endpoint
validation, failover, outage degradation, read-only offline behavior, and
provider isolation remain planned implementation evidence.

## Canonical ownership

This decision owns the standing cloud-only AI-models rule at the repository
level. `AGENTS.md` (Rule 9) owns the agent-facing restatement.
`requirements/FR.md` and `requirements/NFR.md` own the requirement projection.
`architecture/PROVIDER_SYSTEM.md` owns provider route behavior.
`security/PermissionModel.md` owns the classifier boundary.
`docs/PRODUCT_PRINCIPLES.md` owns the product-principle projection.
`docs/CANONICAL_SOURCES.md` owns the canonical-source map entry.
`docs/CHANGELOG.md` and `docs/DECISION_LOG.md` own the historical record.

## References

- `decisions/DEC-41-cloud-only-ai-provider-scope.md`
- `decisions/DEC-42-no-local-ai-models-and-classifier-boundary.md`
- `decisions/DEC-39-gguf-execution-boundary.md` (historical, superseded)
- `AGENTS.md` Rule 9
- `docs/PRODUCT_PRINCIPLES.md` (PP-014, PP-016, PP-017)
- `requirements/CONSTRAINTS.md`
- `requirements/ASSUMPTIONS.md`
- `specs/AI_PROVIDERS.md`
- `security/PermissionModel.md`
