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

Every action in Nexora—tool invocation, network call, device access—requires a permission. The model defines **18 scopes**, three decision levels, a layered override hierarchy, and full auditability.

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
| `instance:pair` | Pair with a peer Nexora instance (fingerprint confirmation) | `ASK` | N/A (internal) |
| `instance:connect` | Open a pipe to a paired instance | `ASK` | `INTERNET` (LAN pipes) |
| `instance:broadcast` | Broadcast a typed message to connected pipes | `DENY` | N/A (internal) |
| `instance:delegate` | Delegate a task to a remote instance through a pipe (TOOL-408) | `ASK` | `INTERNET` (LAN pipes) |

## Decision Levels

| Level | Behaviour |
|-------|-----------|
| `ALLOW` | Proceed immediately; no user interaction required |
| `ASK` | Suspend execution; show a system dialog to the user; proceed only on approval |
| `DENY` | Block immediately; return `NXR-2003` to the agent |

## Hierarchy: Agent → Workspace → Global → scope default

Resolution order — first match wins:

1. **Agent override** — agent-level restrictions (e.g., a "read-only" research agent).
2. **Workspace override** — per-workspace policy stored in `workspace.json`.
3. **Global policy** — defined in app Settings, applies to all workspaces.
4. **Scope default** — the scope's own `default` from the table above (no tool-level policy layer exists; tools declare required scopes which feed into the agent/workspace/global resolution).

If no layer defines a decision, the scope's **default** (table above) is used.

## Runtime Permission Request Flow

```kotlin
suspend fun checkPermission(
    tool: Tool,
    workspaceId: String,
    agentId: String?
): PermissionResult {
    val scopeIds = tool.requiredPermissions

    // Empty permission list — allowed by default
    if (scopeIds.isEmpty()) {
        return PermissionResult.Allowed
    }

    val askScopes = mutableListOf<PermissionScope>()

    for (scopeId in scopeIds) {
        // Resolve scope ID through the canonical registry
        val scope = permissionScopeRegistry.resolve(scopeId)
            ?: run {
                auditDenial(
                    tool = tool, workspaceId = workspaceId, agentId = agentId,
                    scopeId = scopeId, reason = PolicySource.UNKNOWN_SCOPE
                )
                return PermissionResult.DeniedUnknownScope(scopeId)
            }

        val decision = resolveDecision(
            scope = scope,
            workspaceId = workspaceId,
            agentId = agentId
        )

        // Audit preliminary resolution (records policy source + prelim decision)
        auditPreliminaryResolution(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            scope = scope, decision = decision
        )

        when (decision) {
            PermissionDecision.DENY -> {
                auditFinalDenial(
                    tool = tool, workspaceId = workspaceId, agentId = agentId,
                    scope = scope, reason = PolicySource.OVERRIDE_DENIAL
                )
                return PermissionResult.Denied(scope)
            }
            PermissionDecision.ASK -> {
                askScopes.add(scope)
            }
            PermissionDecision.ALLOW -> {
                auditFinalAllow(
                    tool = tool, workspaceId = workspaceId, agentId = agentId,
                    scope = scope
                )
                continue // evaluate remaining scopes
            }
        }
    }

    // Aggregated approval — present all ASK scopes in one transaction
    if (askScopes.isNotEmpty()) {
        val txnId = generateApprovalTransactionId()
        val result = requestApprovalForScopes(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            scopes = askScopes, transactionId = txnId
        )
        // Audit final outcome per scope
        for (scope in askScopes) {
            auditFinalAskOutcome(
                tool = tool, workspaceId = workspaceId, agentId = agentId,
                scope = scope, transactionId = txnId,
                approved = result is PermissionResult.Allowed
            )
        }
        return result
    }

    return PermissionResult.Allowed
}

/**
 * Resolves a single scope through the override hierarchy.
 * Returns the effective decision from: Agent → Workspace → Global → scope default.
 */
private fun resolveDecision(
    scope: PermissionScope,
    workspaceId: String,
    agentId: String?
): PermissionDecision {
    // 1. Agent-level override
    if (agentId != null) {
        val agentDecision = agentPermissionStore.get(agentId, scope.id)
        if (agentDecision != null) return agentDecision
    }

    // 2. Workspace override
    val wsDecision = workspacePermissionStore.get(workspaceId, scope.id)
    if (wsDecision != null) return wsDecision

    // 3. Global policy
    val globalDecision = globalPermissionStore.get(scope.id)
    if (globalDecision != null) return globalDecision

    // 4. Scope default
    return scope.defaultDecision
}

/**
 * Aggregated approval: presents all ASK scopes in one transaction.
 * Returns Allowed only if every scope is user-approved.
 * Any denial returns Denied for the first denied scope.
 */
private suspend fun requestApprovalForScopes(
    tool: Tool,
    workspaceId: String,
    agentId: String?,
    scopes: List<PermissionScope>,
    transactionId: String
): PermissionResult {
    val result = askUser(tool, scopes, transactionId) // suspends; presents all scopes together
    return when (result) {
        is PermissionResult.Allowed -> PermissionResult.Allowed
        is PermissionResult.Denied -> result
    }
}

enum class PolicySource { AGENT_OVERRIDE, WORKSPACE_OVERRIDE, GLOBAL_POLICY, SCOPE_DEFAULT, UNKNOWN_SCOPE, OVERRIDE_DENIAL }
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

## Explicit Risk-Based Scope Defaults

> **Status:** CANONICAL policy (revised 2026-08-06 — resolves deny-by-default contradictions).

The scope default table in §Permission Scopes (lines 24-43) is the authoritative,
deterministic default for every declared Nexora permission scope. No prose overlay
reinterprets an `ALLOW` or `ASK` table value as `DENY`.

### Default Semantics

| Table default | Meaning |
|---|---:|
| `ALLOW` | Proceed unless an applicable higher-priority policy (Agent, Workspace, or Global) explicitly restricts the scope. |
| `ASK` | Explicit user approval is required unless a higher-priority policy already resolves the scope to `ALLOW` or `DENY`. |
| `DENY` | Blocked unless a higher-priority policy explicitly grants `ALLOW`. |

### Resolution Chain

The runtime resolves every scope independently:
```
Agent override
  → Workspace override
  → Global policy
  → declared scope default (from the scope table)
  → DENY (for unknown or undeclared scope identifiers)
```

- A Tool with multiple required permissions must satisfy **every** scope.
- Order of `requiredPermissions` does not affect the authorization result.
- An `ALLOW` for one scope does not implicitly authorize other scopes.
- Absence of an override is not the same as absence of a scope default — the table default always applies for known scopes.

### Scope Default Table Reference

The following defaults are the single authoritative values:

| Scope | Default | Notes |
|---|---|---|
| `sandbox:read`, `sandbox:write`, `sandbox:execute` | `ALLOW` | Trusted workspace execution |
| `network:http`, `network:websocket` | `ASK` | Outbound network |
| `device:camera`, `device:storage` | `DENY` | Hardware access |
| `device:notifications` | `ASK` | User-visible |
| `ai:complete`, `ai:embed` | `ALLOW` | AI provider calls |
| `memory:read`, `memory:write` | `ALLOW` | Memory store access |
| `plugin:install` | `ASK` | Irreversible; user review required |
| `agent:create` | `ASK` | Resource allocation; user approval required |
| `instance:pair`, `instance:connect` | `ASK` | Pipe discovery + connection |
| `instance:broadcast` | `DENY` | Broadcast requires explicit grant |
| `instance:delegate` | `ASK` | Cross-instance task delegation (TOOL-408) |
| Any undeclared scope | `DENY` | Unknown scopes denied unconditionally |

### Relationship to the Classifier

If the optional on-device classifier (see §Optional On-Device Auto-Approval Classifier) is enabled:

- The classifier may add an independent `DENY` gate after scope resolution.
- It does **not** change the declared scope default.
- Classifier `ALLOW` means "no classifier objection" — not automatic permission approval.
- The classifier cannot bypass `ASK` or `DENY` scopes.
- Classifier denial cannot be overridden by user approval alone unless the workspace policy explicitly permits override.

## Optional On-Device Auto-Approval Classifier (TFLite)

> **Status:** CANONICAL specification for independent safety layer (added G2 — 2026-08-06).  
> **Purpose:** User vigilance (`FR-S016` `Manual`/`Assisted` mode) cannot be the only safety mechanism — `~93%` of approvals become automatic (`approval fatigue`). The classifier provides an independent, non-user-dependent layer that can `DENY` obviously risky calls, reducing dependence on user attention.

### Design Constraints

- **Independent layer:** The classifier operates **after** the `Permission Manager` (`checkPermission()`) but **before** `execute()` (`protocols/Tool-Protocol.md` — Authorization Gate). It does **NOT** replace user approval (`FR-S016`); it is an additional `DENY` gate.
- **Optional:** User can disable the classifier in `Workspace Settings` (`FR-W005`); default is `ENABLED` (safety-by-default).
- **On-device (`TFLite`)**: No network dependency; no external service.

### Scope Selection

The classifier evaluates tool calls based on their effective permission decision and risk class, not on whether the scope default is ALLOW/ASK/DENY. The selection is:

| Condition | Classifier evaluates? |
|---|---|
| Any scope resolved to `ASK` or `DENY` | Yes — assesses risk patterns |
| All scopes resolved to `ALLOW` | No — unless workspace config explicitly opts in |
| Workspace config enables classifier for a specific scope | Yes — regardless of default |

This means the classifier **may** evaluate a call that includes `sandbox:execute` (default ALLOW) if the workspace configuration opts it in or if other scopes in the call are ASK/DENY. But the classifier does **not** imply that `sandbox:execute`'s default is DENY — the default remains ALLOW per the scope table.

### Classifier Behavior

- **Input**: `Tool` (`requiredPermissions`, `parameters` JSON Schema), `context` (`workspaceId`, `agentId`, `executionHistory` — `FR-T015` audit trail), `userAutonomyMode` (`FR-S016`: `Manual`/`Assisted`/`Autopilot`).
- **Output**: `PermissionResult.Denied` (auto-deny) or `PermissionResult.Allowed` (pass through — does not bypass ASK or DENY scopes).
- Classifier `ALLOW` means "no classifier objection" — not automatic permission approval.
- Classifier `DENY` cannot be overridden by user approval alone unless the workspace policy explicitly permits classifier override.
- The classifier does **not** change the declared scope default in the scope table.

### Relationship to Permission Resolution

```
checkPermission()  →  resolved scopes (ALLOW / ASK / DENY)
                         │
                         ▼
                   Classifier evaluation (independent DENY gate)
                         │
                         ▼
                   execute() or return Denied
```

The classifier reads the resolved permission decisions and the tool parameters. It operates after `checkPermission()` has resolved all scopes through the override hierarchy. It cannot bypass `ASK` or `DENY` scopes — those must still be approved per the normal permission flow.

### Traceability

- `security/PermissionModel.md`: Updated (§Explicit Risk-Based Scope Defaults + §Classifier).
- `specs/CONTEXT_MANAGEMENT.md`: `FR-EV-002` structured confidence — `LOW` triggers `ASK`, which aligns with classifier behavior; `FR-EV-003` zero-assumption mode — classifier enforces zero-assumption by denying unverified high-risk calls.
- `FR.md`: References preserved (`FR-S016` autonomy modes; `FR-S001`..`FR-S028` sandbox isolation; `FR-EV-001`..`FR-EV-006` evidence engine).
- `docs/DECISION_LOG.md`: `DL-022` logs the original decision (superseded by DL-034 for scope defaults).

---

## Permission Groups

Common permission bundles to reduce decision fatigue:

| Group | Scopes Included | Use Case |
|-------|----------------|----------|
| `full_sandbox` | `sandbox:read`, `sandbox:write`, `sandbox:execute` | Full workspace access agent |
| `network_access` | `network:http`, `network:websocket` | Web-scraping or API agent |
| `device_access` | `device:camera`, `device:storage`, `device:notifications` | Multimedia agent (always requires ASK) |
| `read_only` | `sandbox:read`, `memory:read`, `ai:complete` | Analysis-only research agent |
| `agent_operator` | `agent:create`, `ai:complete`, `ai:embed`, `memory:read`, `memory:write` | Multi-agent orchestration |
