# Permission Model — Nexora

> **Status: CANONICAL** for user approval semantics and permission grants.
> This document owns how users approve or deny agent actions, permission
> scopes, the ASK/ALLOW/DENY/REVOKE flow, and the permission audit trail.
> It does NOT own security architecture (see
> [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md)),
> sandbox containment (sandbox rules in SandboxPolicy.md) (see [SandboxPolicy.md](SandboxPolicy.md)), or runtime
> enforcement implementation (see [../architecture/SANDBOX.md](../architecture/SANDBOX.md)).
>
> Depends on: [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md).
> Referenced by: [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../docs/SANDBOX_DEPTH.md](../docs/SANDBOX_DEPTH.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

Every action in Nexora—tool invocation, network call, device access—requires a permission. The model defines **14 scopes**, three decision levels, a layered override hierarchy, and full auditability.

## Permission Scopes

| Scope | Description | Default | Android Equivalent |
|-------|-------------|---------|-------------------|
| `sandbox:read` | Read files inside the workspace sandbox | `ALLOW` | Internal storage (own) |
| `sandbox:write` | Write/modify/delete files inside the workspace sandbox | `ALLOW` | Internal storage (own) |
| `sandbox:execute` | Execute commands or scripts within the sandbox | `ALLOW` | N/A (managed by sandbox) |
| `network:http` | Make outbound HTTP/HTTPS requests | `ASK` | `INTERNET` |
| `network:websocket` | Open persistent WebSocket connections | `ASK` | `INTERNET` |
| `device:camera` | Access the device camera stream | `DENY` | `CAMERA` |
| `device:storage` | Access shared/external storage (`/sdcard`) | `DENY` | `READ/WRITE_EXTERNAL_STORAGE` |
| `device:notifications` | Post system notifications | `ASK` | `POST_NOTIFICATIONS` |
| `ai:complete` | Call an AI provider for text completions | `ALLOW` | `INTERNET` |
| `ai:embed` | Call an AI provider for vector embeddings | `ALLOW` | `INTERNET` |
| `memory:read` | Read from workspace or global memory stores | `ALLOW` | Internal storage (own) |
| `memory:write` | Write entries to memory stores | `ALLOW` | Internal storage (own) |
| `plugin:install` | Download and install a new plugin | `ASK` | `REQUEST_INSTALL_PACKAGES` (never granted) |
| `agent:create` | Spawn a new agent instance | `ASK` | N/A (internal) |

## Decision Levels

| Level | Behaviour |
|-------|-----------|
| `ALLOW` | Proceed immediately; no user interaction required |
| `ASK` | Suspend execution; show a system dialog to the user; proceed only on approval |
| `DENY` | Block immediately; return `NXR-2003` to the agent |

## Hierarchy: Global → Workspace → Agent → Tool

Resolution order — first match wins:

1. **Global policy** — defined in app Settings, applies to all workspaces.
2. **Workspace override** — per-workscope policy stored in `workspace.json`.
3. **Agent override** — agent-level restrictions (e.g., a "read-only" research agent).
4. **Tool declared scopes** — the tool's own `requiredPermissions` list.

If no layer defines a decision, the scope's **default** (table above) is used.

## Runtime Permission Request Flow

```kotlin
suspend fun checkPermission(
    tool: Tool,
    workspaceId: String,
    agentId: String?
): PermissionResult {
    val scopes = tool.requiredPermissions

    for (scope in scopes) {
        // 1. Agent-level override
        if (agentId != null) {
            val agentDecision = agentPermissionStore.get(agentId, scope)
            if (agentDecision != null) return decide(agentDecision, scope)
        }

        // 2. Workspace override
        val wsDecision = workspacePermissionStore.get(workspaceId, scope)
        if (wsDecision != null) return decide(wsDecision, scope)

        // 3. Global policy
        val globalDecision = globalPermissionStore.get(scope)
        if (globalDecision != null) return decide(globalDecision, scope)

        // 4. Scope default
        return decide(scope.default, scope)
    }
    return PermissionResult.Allowed
}

private fun decide(
    decision: PermissionDecision,
    scope: PermissionScope
): PermissionResult = when (decision) {
    PermissionDecision.ALLOW -> PermissionResult.Allowed
    PermissionDecision.DENY -> PermissionResult.Denied(scope)
    PermissionDecision.ASK -> askUser(scope) // suspends until user responds
}
```

## Persistence (DataStore)

```kotlin
// Global policy stored in PreferencesDataStore
val globalPermissionStore = PermissionDataStore(
    context = context,
    name = "global_permissions"
)

// Workspace overrides stored per-workspace
val workspacePermissionStore = PermissionDataStore(
    context = context,
    name = "permissions_${workspaceId}"
)
```

Each grant/deny decision is an append-only entry:

| Field | Type | Description |
|-------|------|-------------|
| `scope` | `String` | Permission scope identifier |
| `decision` | `Enum` | ALLOW / DENY |
| `grantedAt` | `Instant` | Timestamp of the decision |
| `grantedTo` | `String` | Agent or tool that triggered the request |
| `workspaceId` | `String` | Active workspace at time of decision |

## Permission Audit Trail

All permission decisions are written to an immutable Room table (`permission_audit_log`). This log cannot be edited or deleted by agents, tools, or plugins. It supports:

- Filtering by workspace, agent, or time range.
- Export for compliance review.
- Retention policy: 90 days, auto-purged.

## Plugin Permission Manifest

Every plugin declares its required scopes in `plugin.json`:

```json
{
  "id": "com.example.web-scraper",
  "permissions": [
    "network:http",
    "sandbox:write",
    "memory:write"
  ]
}
```

At install time, the user reviews the full manifest. Missing scopes are **not** auto-granted.

## Permission Groups

Common permission bundles to reduce decision fatigue:

| Group | Scopes Included | Use Case |
|-------|----------------|----------|
| `full_sandbox` | `sandbox:read`, `sandbox:write`, `sandbox:execute` | Full workspace access agent |
| `network_access` | `network:http`, `network:websocket` | Web-scraping or API agent |
| `device_access` | `device:camera`, `device:storage`, `device:notifications` | Multimedia agent (always requires ASK) |
| `read_only` | `sandbox:read`, `memory:read`, `ai:complete` | Analysis-only research agent |
| `agent_operator` | `agent:create`, `ai:complete`, `ai:embed`, `memory:read`, `memory:write` | Multi-agent orchestration |
