# Security Model — Nexora

> **Status: CANONICAL** for security architecture and threat model ownership.
> This document owns the overall security posture, threat model, defense strategy,
> and security principles. It does NOT own permission semantics (see
> [security/PermissionModel.md](../security/PermissionModel.md)), sandbox
> containment rules (see [security/SandboxPolicy.md](../security/SandboxPolicy.md)),
> or sandbox subsystem design (see [SANDBOX.md](SANDBOX.md)).
>
> Depends on: [security/ThreatModel.md](../security/ThreatModel.md).
> Referenced by: [security/PermissionModel.md](../security/PermissionModel.md), [security/SandboxPolicy.md](../security/SandboxPolicy.md), [SANDBOX.md](SANDBOX.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

Nexora enforces strict security boundaries. The AI never touches the host system. All execution is sandboxed, permission-gated, and audited.

## Security Measures

| Measure | Description |
|---------|-------------|
| **Sandboxed execution** | All code/commands execute inside the sandbox, never on the host. |
| **Workspace isolation** | Each workspace is isolated. No cross-workspace access. |
| **Permission-based tool access** | Each tool requires specific permissions. User approves per-tool. |
| **Encrypted API keys** | All API keys stored using Android Keystore encryption. |
| **Resource quotas** | Configurable limits on CPU, memory, disk, network per workspace. |
| **Process limits** | Maximum concurrent processes per workspace. |
| **Plugin permissions** | Plugins declare required permissions at install. User approves. |
| **Audit logs** | Every action logged with timestamp, agent, tool, parameters, result. |
| **Provider isolation** | Provider configs, API keys, and request data are isolated per provider; provider code cannot access other providers' credentials or data. |
| **Inference stream integrity** | Typed events are authenticated to stream identity, schema/size checked, sequence validated, and terminal committed exactly once. |
| **Reasoning artifact privacy** | Only redacted ReasoningSummary artifacts persist; raw private chain-of-thought, hidden prompts, credentials, and resume tokens are excluded from logs/exports. |

## Permission Scopes

| Scope | Access Level | Default |
|-------|-------------|---------|
| `sandbox:read` | Read files inside sandbox | allow |
| `sandbox:write` | Write/modify files inside sandbox | allow |
| `sandbox:execute` | Execute commands in sandbox | allow |
| `network:http` | Make HTTP/HTTPS requests | ask |
| `network:websocket` | Open WebSocket connections | ask |
| `device:camera` | Access device camera | deny |
| `device:storage` | Access device external storage | deny |
| `device:notifications` | Send system notifications | ask |
| `ai:complete` | Call AI provider for completions | allow |
| `ai:embed` | Call AI provider for embeddings | allow |
| `memory:read` | Read from memory stores | allow |
| `memory:write` | Write to memory stores | allow |
| `plugin:install` | Install new plugins | ask |
| `agent:create` | Create new agent instances | ask |
| `instance:pair` | Pair with a peer Nexora instance | ask |
| `instance:connect` | Open a pipe to a paired instance | ask |
| `instance:broadcast` | Broadcast to connected pipes | deny |
| `instance:delegate` | Delegate a task to a remote instance | ask |

## Permission Flow

> **Note:** PermissionModel (`security/PermissionModel.md`) owns authorization semantics,
> including multi-scope evaluation, aggregated ASK approval, classifier policy, and
> complete audit. This document projects the canonical behavior for the security-architecture
> view only. Any divergence is documentation drift — PermissionModel is authoritative.

Tool authorization, in order:

1. Resolves every declared required-permission scope against the canonical registry.
2. Denies unknown or effective-DENY scopes immediately (classifier not invoked).
3. Aggregates ASK scopes into one approval transaction.
4. Validates exact one-to-one approval outcomes (duplicate, missing, extra, or
   transaction-ID mismatch returns MALFORMED_APPROVAL).
5. If all scopes pass, applies ClassifierPolicy selection.
6. If selected, executes classifier; classifier DENY is final for the call.
7. Returns Allowed only after every gate passes; tool execution begins only then.

## API Key Encryption

```kotlin
class SecureKeyStore(context: Context) {
    // Uses Android Keystore System
    // Keys never leave the device's secure hardware
    // Biometric unlock optional for sensitive keys

    fun storeKey(providerId: String, apiKey: String)
    fun retrieveKey(providerId: String): String?
    fun deleteKey(providerId: String)
    fun listProviderIds(): List<String>
}
```

## Provider Isolation

Providers are isolated from each other and from workspace data (NFR-SEC-011/012).
The following guarantees apply to every provider and provider profile:

| Guarantee | Rule |
|-----------|------|
| **Credential isolation** | Each provider profile's API key is stored under its own `SecureKeyStore` alias. Only the matching provider client may retrieve its own key reference; no provider code can enumerate or read another provider's keys or profiles. |
| **Configuration isolation** | Provider configurations are scoped by provider ID and profile ID. `ProviderRegistry` returns a config only to the provider client that owns it. |
| **Data-flow isolation** | Context assembled for provider A is delivered only to provider A's endpoint. Every request is tagged with the active profile ID; delivery through any other provider is rejected by the router. |
| **Code isolation** | Provider implementations (Phase 8 plugins, e.g. PLG-018) run in isolated classloaders with no access to app internals, other provider instances, or workspace data — except through the permissioned `ToolContext` surface (same rule as plugin sandboxing, NFR-SEC-009). |
| **Network confinement** | Provider HTTP clients connect only to their configured `baseUrl` (defaults per PROV-001…009). No arbitrary outbound connections from provider code without an explicit `network:*` grant. TLS 1.3 + certificate pinning (NFR-SEC-004). |
| **Crash isolation** | A provider failure, timeout, or OOM cannot take down the host app or other providers — bounded retries with backoff and health-based routing (see ProviderLifecycle: Healthy → Degraded → Unhealthy → failover). |
| **Auditability** | Every provider call is recorded: profile, workspace, agent, model, token usage (observability, FR-P009). |

## Inference Stream Trust Boundary

Provider bytes are untrusted until the adapter maps them to the closed canonical event
set and the router validates event size, schema, stream/request/profile identity, and
monotonic sequence. Tool-call fragments cannot cross into Tool authorization before a
schema-valid `ToolCallCommitted` event. Resume tokens are opaque secrets. Cross-provider
failover creates a new stream lineage; output is never silently spliced. Stream and
reasoning artifacts follow NFR-SEC-015 redaction/retention rules.

Design rule (unchanged): the runtime sees only the `AIProvider` interface; all
provider-specific logic lives in provider plugins
(see [PROVIDER_SYSTEM.md](PROVIDER_SYSTEM.md) and [specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md)).

## Phase Mapping

- **Phase 1**: Permission Manager interface, basic permission checks.
- **Phase 3**: Sandbox isolation enforcement, resource quotas.
- **Phase 5**: API key encryption, provider-specific security, provider isolation enforcement.
- **Phase 8**: Plugin permission sandboxing, provider plugins.
