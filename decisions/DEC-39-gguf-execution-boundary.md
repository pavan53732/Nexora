# DEC-39 — GGUF Provider Execution Boundary

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Execution boundary for local GGUF provider support.

## Problem

The requirements state that Ollama, LM Studio, and GGUF run as separate on-device processes and are not embedded. The provider specification separately describes `LOCAL_GGUF` as direct GGUF loading through llama.cpp or mlc-llm.

## Decision

Ollama and LM Studio remain separate local-server providers reached through their local HTTP endpoints. `LOCAL_GGUF` is implemented as a separate on-device worker process managed by Nexora’s provider/sandbox boundary; the GGUF model is not loaded into the main Android application process.

The worker process may use an approved native GGUF runtime such as llama.cpp or mlc-llm, but the runtime is an implementation dependency inside the worker boundary rather than a direct in-process dependency of the Android application. Provider System continues to expose the common `AIProvider` abstraction and typed stream contract.

## Boundary and recovery rules

The worker MUST be bound to the provider profile, workspace, task, execution, correlation, and effective deadline required by the existing provider and sandbox contracts. Requests, streaming events, cancellation, resource limits, health, and terminal outcomes cross the existing Provider protocol boundary. The worker MUST NOT gain host filesystem, unrestricted network, or permission bypasses through the GGUF path.

Worker failure, timeout, cancellation, stream interruption, and unknown completion use the existing ProviderStream, Tool, Execution, and Task recovery contracts. Failover to another provider creates the existing new stream lineage and MUST NOT replay incompatible provider-native continuation state.

## Invariants

No new ProviderStatus, ProviderHealth, ProviderStream, Task, Agent, Tool, or permission state is created. The decision preserves the existing provider capability negotiation, model-catalog identity, stream sequencing, cancellation, failover, privacy, sandbox, and audit rules. GGUF remains an on-device capability and does not become an embedded Android application feature.

## Required projections

requirements/CONSTRAINTS.md, requirements/ASSUMPTIONS.md, architecture/PROVIDER_SYSTEM.md, specs/AI_PROVIDERS.md, specs/FULL_ENVIRONMENT.md, architecture/SANDBOX.md, security/SandboxPolicy.md, and provider test plans MUST describe LOCAL_GGUF as a separate managed worker process. Only the worker may load llama.cpp/mlc-llm or equivalent GGUF runtime libraries.
