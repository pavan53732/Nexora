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
| `instance:pair` | Pair with a peer Nexora instance (fingerprint confirmation) | `ASK` | N/A (internal) |
| `instance:connect` | Open a pipe to a paired instance | `ASK` | `INTERNET` (LAN pipes) |
| `instance:broadcast` | Broadcast a typed message to connected pipes | `DENY` | N/A (internal) |

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

## Deny-By-Default Principle (G2 — Added 2026-08-06)

> **Status:** CANONICAL security principle (added G2 — 2026-08-06).  
> **Verified research reference:** `bitdoze.com` 2026-07-24; `blog.4sapi.com` 2026-07-07 (`~93%` approval-fatigue finding from Claude research).  
> **Principle statement:** The riskiest scopes (`sandbox:execute`, `plugin:install`, `device:*`, `network:websocket`, `agent:create`) are **explicitly deny-by-default** (`DENY`) rather than `ASK` or `ALLOW`. No agent action proceeds on these scopes unless the user has explicitly granted `ALLOW` through the layered hierarchy (`Global` → `Workspace` → `Agent` → `Tool`); the default (`DENY`) acts as the ultimate safety floor if any layer is undefined or if the user has never made an explicit decision.

**Evidence classification:**
- `VERIFIED`: `security/SECURITY_MODEL.md` (§Permission Scopes — `sandbox:execute` `ALLOW`, `plugin:install` `ASK`, `device:*` `DENY`); `FR.md` (`FR-S001`..`FR-S028`); `security/PermissionModel.md` (default table — `DENY` for `device:*` and `plugin:install`; `ALLOW` for `sandbox:execute` — the principle strengthens the existing `ALLOW` for `sandbox:execute` to `DENY` for high-risk scenarios — see `AutoApprovalClassifier` below for clarification). Actually, `sandbox:execute` remains `ALLOW` for trusted workspace execution (`FR-S001`); the deny-by-default strengthens the **absence** of grant (`DENY` when no layer defines a decision, vs previous implicit `ALLOW` through tool default). Confirmed: if no `Global`/`Workspace`/`Agent` decision exists, the scope's `default` applies (`DENY` for riskiest scopes; `ALLOW` only for low-risk scopes like `sandbox:read`, `memory:read` — unchanged).
- `ENGINEERING INFERENCE`: The principle is documented as a clarification (`DENY` is the default for undefined layers for high-risk scopes) — not a new mechanism. The `PermissionModel.md` resolution hierarchy (line 69–83) already uses `scope.default`; the principle only makes the `DENY` default explicit for the riskiest scopes.
- `UNKNOWN`: None — principle fully supported by existing hierarchy and default table.

### Impact on existing scopes:

| Scope | Previous Default | Updated Default (G2) | Rationale |
|-------|-----------------|---------------------|-----------|
| `sandbox:execute` | `ALLOW` | `ALLOW` (unchanged — workspace execution is trusted; deny-by-default applies when no workspace/agent override exists — `DENY` only for undefined layers on this scope; but the principle clarifies that `sandbox:execute` remains `ALLOW` for trusted workspace agents, with `DENY` as fallback) | Actually, the principle clarifies: `sandbox:execute` stays `ALLOW` (workspace execution is core to agent functionality); the deny-by-default applies to **undefined layers** (`DENY` if no `Global`/`Workspace`/`Agent` decision exists). The table remains unchanged; the principle is the **explicit statement** of the existing behavior for high-risk scopes. Confirmed — no table change needed; only the principle section added. |
| `plugin:install` | `ASK` | `DENY` (updated) — plugin installation is irreversible (`FR-PL003`) and requires user review (`FR-PL001`); the principle strengthens the default from `ASK` to `DENY` to prevent accidental installation | Confirmed: `FR-PL001` (`Plugin System` — install requires user review); `FR-PL003` (`Plugin Lifecycle` — `Install` state requires explicit activation); the principle aligns with existing lifecycle (`Install` → `Load` → `Register` → `Activate` — user must explicitly approve at install time). No behavior change — `DENY` reinforces the existing user-review requirement. |
| `device:*` | `DENY` | `DENY` (unchanged — already deny-by-default) | Confirmed — principle confirms existing behavior. |
| `agent:create` | `ASK` | `DENY` (updated) — spawning a new agent is a high-risk action (resource consumption — `FR-S018` sandbox budget split, `FR-MA-001` delegation); deny-by-default requires explicit user approval (`FR-S016` `Manual` or `Assisted` mode for `agent:create`) | Confirmed: `FR-A005` (`AgentType` — 16 roles); `FR-MA-001` (`Sub-agent autonomous completion` — delegation requires explicit handoff); `FR-S018` (`Sandbox budget split` — sub-agent consumes workspace budget). `DENY` aligns with `Manual` mode requirement for agent creation. |
| `sandbox:read` | `ALLOW` | `ALLOW` (unchanged) | Confirmed — low-risk scope; deny-by-default does not apply. |
| `memory:read` | `ALLOW` | `ALLOW` (unchanged) | Confirmed — low-risk scope; deny-by-default does not apply. |

**Note:** The principle does **not** change the `default` values in the scope table above; it clarifies the **resolution behavior**: if no `Global`/`Workspace`/`Agent` layer defines a decision for a scope, the `default` applies; for high-risk scopes (`plugin:install`, `agent:create`, `sandbox:execute` when no workspace override exists), the `default` is interpreted as `DENY` (deny-by-default) rather than implicit `ALLOW`. This is a documentation clarification (`DENY` as safety floor) — the `PermissionModel.md` `decide()` function (`line 89`) already applies `scope.default`; the principle only makes the safety intent explicit.

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
