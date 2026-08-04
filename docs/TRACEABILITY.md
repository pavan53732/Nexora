# Requirement-to-Implementation Traceability Matrix

The matrix links each requirement family to its primary implementation and contract artifacts.

## Legend

- **Primary** — canonical owning document.
- **Derived** — contract or support document derived from the canonical owner.
- **Validation** — test or audit artifact expected to verify the contract.

## Maintenance Rule

When a canonical architecture or requirement changes, all derived APIs, SDKs, protocols, models, registries, and tests MUST be updated in the same change or explicitly deferred with a recorded gap.

## Contract Coverage

| Concern | Primary | Derived | Validation |
|---|---|---|---|
| Agent lifecycle and execution | `architecture/AGENT_RUNTIME.md` | `docs/api/Agent-API.md`, `protocols/Agent-Protocol.md`, `models/Agent.md`, `sdk/AgentSDK.md` | integration, lifecycle, and SDK conformance tests |
| Tool registration and invocation | `architecture/TOOL_SYSTEM.md` | `docs/api/Tool-API.md`, `protocols/Tool-Protocol.md`, `models/Tool.md`, `sdk/ToolSDK.md` | registry, protocol, security, and SDK conformance tests |
| Provider completion and streaming | `architecture/PROVIDER_SYSTEM.md` | `docs/api/Provider-API.md`, `protocols/Provider-Protocol.md`, `models/Provider.md`, `sdk/ProviderSDK.md` | streaming, lifecycle, and SDK conformance tests |
| Plugin lifecycle and capability export | `architecture/PLUGIN_SYSTEM.md` | `docs/api/Plugin-API.md`, `protocols/Plugin-Protocol.md`, `models/Plugin.md`, `sdk/PluginSDK.md` | lifecycle, rollback, security, and SDK conformance tests |
| Runtime orchestration and event guarantees | `architecture/RUNTIME.md` | `docs/api/Runtime-API.md`, `protocols/Execution-Protocol.md`, `models/Execution.md` | event bus, background execution, and orchestration tests |
| Canonical error envelope | `errors/ERROR_CODES.md` | all APIs, protocols, SDKs, and runtime projections | contract and regression tests |
| Correlation, idempotency, resume, and version semantics | owning architecture documents | API envelopes, protocols, runtime event streams, and SDK helpers | contract, replay, and retry tests |
