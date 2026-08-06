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

> **Note:** The following summarizes the canonical permission evaluation algorithm.
> `security/PermissionModel.md` owns the complete algorithm, multi-scope evaluation,
> and aggregated-approval semantics. This document projects the same behavior for
> the security-architecture view. Any divergence from PermissionModel is documentation
> drift — PermissionModel is authoritative.

```kotlin
enum class PermissionDecision { ALLOW, ASK, DENY }

class PermissionManager(
    private val globalPolicy: Map<PermissionScope, PermissionDecision>,
    private val workspaceOverrides: Map<String, Map<PermissionScope, PermissionDecision>>,
    private val agentOverrides: Map<String, Map<PermissionScope, PermissionDecision>>
) {
    suspend fun check(tool: Tool, workspaceId: String, agentId: String?): PermissionResult {
        val scopes = tool.requiredPermissions
        if (scopes.isEmpty()) return PermissionResult.Allowed

        val askScopes = mutableListOf<PermissionScope>()

        for (s in scopes) {
            // Agent override → Workspace override → Global policy → scope default → DENY
            val decision = agentOverrides[agentId]?.get(s)
                ?: workspaceOverrides[workspaceId]?.get(s)
                ?: globalPolicy[s]
                ?: s.default
                ?: PermissionDecision.DENY

            when (decision) {
                PermissionDecision.DENY -> return PermissionResult.Denied(s)
                PermissionDecision.ASK -> askScopes.add(s)
                PermissionDecision.ALLOW -> continue // evaluate remaining scopes
            }
        }

        if (askScopes.isNotEmpty()) {
            return askUser(tool, askScopes) // aggregated approval
        }

        return PermissionResult.Allowed
    }
}
```

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

Design rule (unchanged): the runtime sees only the `AIProvider` interface; all
provider-specific logic lives in provider plugins
(see [PROVIDER_SYSTEM.md](PROVIDER_SYSTEM.md) and [specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md)).

## Phase Mapping

- **Phase 1**: Permission Manager interface, basic permission checks.
- **Phase 3**: Sandbox isolation enforcement, resource quotas.
- **Phase 5**: API key encryption, provider-specific security, provider isolation enforcement.
- **Phase 8**: Plugin permission sandboxing, provider plugins.
