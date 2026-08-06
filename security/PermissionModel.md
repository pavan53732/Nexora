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
    val scopes = tool.requiredPermissions

    // Empty permission list — allowed by default
    if (scopes.isEmpty()) {
        return PermissionResult.Allowed
    }

    val askScopes = mutableListOf<PermissionScope>()

    for (scope in scopes) {
        val decision = resolveDecision(
            scope = scope,
            workspaceId = workspaceId,
            agentId = agentId
        )

        // Audit every resolution
        auditResolution(tool, workspaceId, agentId, scope, decision)

        when (decision) {
            PermissionDecision.DENY ->
                return PermissionResult.Denied(scope)
            PermissionDecision.ASK ->
                askScopes.add(scope)
            PermissionDecision.ALLOW ->
                continue // evaluate remaining scopes
        }
    }

    // Present ASK scopes in one aggregated approval transaction
    if (askScopes.isNotEmpty()) {
        return requestApprovalForScopes(
            tool = tool,
            workspaceId = workspaceId,
            agentId = agentId,
            scopes = askScopes
        )
    }

    return PermissionResult.Allowed
}

/**
 * Resolves a single scope through the override hierarchy.
 * Unknown / undeclared scope identifiers resolve to DENY.
 */
private fun resolveDecision(
    scope: PermissionScope,
    workspaceId: String,
    agentId: String?
): PermissionDecision {
    // 1. Agent-level override
    if (agentId != null) {
        val agentDecision = agentPermissionStore.get(agentId, scope)
        if (agentDecision != null) return agentDecision
    }

    // 2. Workspace override
    val wsDecision = workspacePermissionStore.get(workspaceId, scope)
    if (wsDecision != null) return wsDecision

    // 3. Global policy
    val globalDecision = globalPermissionStore.get(scope)
    if (globalDecision != null) return globalDecision

    // 4. Scope default (falls back to DENY for unknown scopes)
    return scope.default
}

/**
 * Aggregated approval: presents all ASK scopes in one transaction.
 * Returns Allowed only if every scope is user-approved.
 * Any denial returns Denied for that scope.
 */
private suspend fun requestApprovalForScopes(
    tool: Tool,
    workspaceId: String,
    agentId: String?,
    scopes: List<PermissionScope>
): PermissionResult {
    val result = askUser(tool, scopes) // suspends; presents all scopes together
    return when (result) {
        is PermissionResult.Allowed -> PermissionResult.Allowed
        is PermissionResult.Denied -> result
    }
}

/**
 * Records the resolved decision for the permission audit trail
 * (immutable room table `permission_audit_log`).
 */
private fun auditResolution(
    tool: Tool,
    workspaceId: String,
    agentId: String?,
    scope: PermissionScope,
    decision: PermissionDecision
) {
    // Append-only entry: scope, decision, agentId, workspaceId, timestamp
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
> **Verified research reference:** `bitdoze.com` 2026-07-24 (`~93%` approval-fatigue); `aihackers.net` 2026-07-03; `blog.4sapi.com` 2026-07-07.  
> **Purpose:** User vigilance (`FR-S016` `Manual`/`Assisted` mode) cannot be the only safety mechanism — `~93%` of approvals become automatic (`approval fatigue`). The classifier provides an independent, non-user-dependent layer that can `DENY` obviously risky calls, reducing dependence on user attention.

### Design Constraints

- **Independent layer:** The classifier operates **after** the `Permission Manager` (`checkPermission()`) but **before** `execute()` (`protocols/Tool-Protocol.md` — Authorization Gate). It does **NOT** replace user approval (`FR-S016`); it is an additional `DENY` gate.
- **Optional:** User can disable the classifier in `Workspace Settings` (`FR-W005`); default is `ENABLED` (safety-by-default, aligned with deny-by-default principle above).
- **On-device (`TFLite`)**: No network dependency; no external service; classifier runs locally within the app process (`security/SandboxPolicy.md` — same process isolation rules apply). No `network:http` scope required for classifier operation (it uses the tool call parameters, not external data).
- **Scoping:** Only applies to scopes where `default` is `DENY` or `ASK` (`plugin:install`, `agent:create`, `device:*`, `sandbox:execute` when workspace override is `ALLOW` — the classifier can override to `DENY` if the call matches risky patterns). It does **not** apply to `ALLOW` scopes (`sandbox:read`, `memory:read`, `ai:complete`) unless explicitly configured by user (`Workspace Settings` — optional scope override for classifier sensitivity).
- **No redesign:** Uses existing `PermissionResult` enum (`Allowed` / `Denied` / `Ask`) — classifier produces `Denied` (not a new result type); `ToolResult.NeedsApproval` unchanged; `ToolResult.Success` unchanged; `ToolResult.Error` (`NXR-2003`) used for classifier denial (same error code as permission denial — no new error taxonomy).

### Classifier Behavior

- **Input**: `Tool` (`requiredPermissions`, `parameters` JSON Schema), `context` (`workspaceId`, `agentId`, `executionHistory` — `FR-T015` audit trail), `userAutonomyMode` (`FR-S016`: `Manual`/`Assisted`/`Autopilot`).
- **Output**: `PermissionResult.Denied` (auto-deny) or `PermissionResult.Allowed` (pass through to execution or user approval, depending on `FR-S016` mode).
- **Risk patterns** (verified by `FR-EV-002` structured confidence + `FR-EV-003` zero-assumption mode):
  - `plugin:install` + `network:http` + `sandbox:execute` combined = high risk (`plugin` installation with network access and sandbox execution — requires user review; classifier auto-denies if no explicit `ALLOW` workspace override exists).
  - `agent:create` + `network:http` + `device:*` = high risk (new agent with network + device access; classifier denies in `Manual` mode unless workspace override is `ALLOW`).
  - `sandbox:execute` + `device:*` + `plugin:install` = extreme risk (execution + device + plugin — never allowed by classifier; must be explicitly granted per scope by user through workspace/agent settings).
- **Evidence classification:** `VERIFIED` (research finding — approval fatigue); `ENGINEERING INFERENCE` (TFLite classifier design — standard on-device ML technique; no new architecture; uses existing `PermissionResult` and `ToolContext`); `UNKNOWN` (exact classifier model accuracy — not specified; the design specifies the mechanism, not the model weights; training/evaluation is future work — `Phase 5` or later).

### Traceability (G2 — Documentation Updates Only)

- `security/PermissionModel.md`: Updated (§Deny-By-Default + §Auto-Approval Classifier — see above).
- `specs/CONTEXT_MANAGEMENT.md`: Referenced (`FR-EV-002` structured confidence — `LOW` triggers `ASK`, which aligns with classifier behavior; `FR-EV-003` zero-assumption mode — classifier enforces zero-assumption by denying unverified high-risk calls).
- `FR.md`: References preserved (`FR-S016` autonomy modes; `FR-S001`..`FR-S028` sandbox isolation; `FR-EV-001`..`FR-EV-006` evidence engine).
- `docs/DECISION_LOG.md`: `DL-022` (see above) logs the decision.
- `docs/REQUIREMENT_COVERAGE_LEDGER.md`: No new requirement IDs added (G2 is documentation clarification of existing security posture — `FR-S016`, `FR-EV-001`..`FR-EV-006` already mapped; no new `FR-` or `NFR-` required since no new architecture or feature added).
- `docs/TRACEABILITY.md`: Not updated (no new contract or validation case — documentation clarification only).

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
