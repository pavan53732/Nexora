# Security Model — Nexora

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

## Permission Flow

```kotlin
enum class PermissionDecision { ALLOW, ASK, DENY }

class PermissionManager(
    private val globalPolicy: Map<PermissionScope, PermissionDecision>,
    private val workspaceOverrides: Map<String, Map<PermissionScope, PermissionDecision>>
) {
    suspend fun check(tool: Tool, workspaceId: String): PermissionResult {
        val scope = tool.requiredPermissions
        val workspacePolicy = workspaceOverrides[workspaceId] ?: emptyMap()

        for (s in scope) {
            val decision = workspacePolicy[s] ?: globalPolicy[s] ?: PermissionDecision.DENY
            when (decision) {
                PermissionDecision.DENY -> return PermissionResult.Denied(s)
                PermissionDecision.ASK -> return askUser(tool, s)
                PermissionDecision.ALLOW -> continue
            }
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

## Phase Mapping

- **Phase 1**: Permission Manager interface, basic permission checks.
- **Phase 3**: Sandbox isolation enforcement, resource quotas.
- **Phase 5**: API key encryption, provider-specific security.
- **Phase 8**: Plugin permission sandboxing.
