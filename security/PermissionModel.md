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
data class ResolvedPermissionDecision(
    val decision: PermissionDecision,
    val source: PolicySource
)

data class PendingApproval(
    val scope: PermissionScope,
    val source: PolicySource
)

suspend fun checkPermission(
    tool: Tool,
    workspaceId: String,
    agentId: String?
): PermissionResult {
    val scopeIds = tool.requiredPermissions

    // Validate: no duplicate scope declarations
    if (scopeIds.size != scopeIds.toSet().size) {
        auditDuplicateScopes(tool, workspaceId, agentId, scopeIds)
        return PermissionResult.Denied(
            scopeId = "declaration",
            reason = DenialReason.MALFORMED_APPROVAL,
            errorCode = "NXR-2003"
        )
    }

    // Empty permission list — scopes pass; classifier may still apply
    if (scopeIds.isEmpty()) {
        return finalizeAuthorizationAfterScopes(
            tool, workspaceId, agentId,
            resolvedPermissions = emptyList()
        )
    }

    val pendingApprovals = mutableListOf<PendingApproval>()
    val resolvedPermissions = mutableListOf<ResolvedPermission>()

    for (scopeId in scopeIds) {
        // Resolve scope ID through the canonical registry
        val scope = permissionScopeRegistry.resolve(scopeId)
            ?: run {
                auditDenial(
                    tool = tool, workspaceId = workspaceId, agentId = agentId,
                    scopeId = scopeId, source = PolicySource.UNKNOWN_SCOPE
                )
                return PermissionResult.Denied(
                    scopeId = scopeId,
                    reason = DenialReason.UNKNOWN_SCOPE,
                    errorCode = "NXR-2003"
                )
            }

        val resolved = resolveDecision(
            scope = scope,
            workspaceId = workspaceId,
            agentId = agentId
        )

        // Audit preliminary resolution (policy source + prelim decision)
        auditPreliminaryResolution(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            scope = scope, resolved = resolved
        )

        when (resolved.decision) {
            PermissionDecision.DENY -> {
                auditFinalDenial(
                    tool = tool, workspaceId = workspaceId, agentId = agentId,
                    scope = scope, source = resolved.source
                )
                return PermissionResult.Denied(
                    scopeId = scope.id,
                    reason = DenialReason.POLICY_DENIAL,
                    errorCode = "NXR-2003"
                )
            }
            PermissionDecision.ASK -> {
                pendingApprovals.add(PendingApproval(
                    scope = scope,
                    source = resolved.source
                ))
            }
            PermissionDecision.ALLOW -> {
                auditFinalAllow(
                    tool = tool, workspaceId = workspaceId, agentId = agentId,
                    scope = scope, source = resolved.source
                )
                resolvedPermissions.add(ResolvedPermission(
                    scopeId = scope.id,
                    declaredDefault = scope.defaultDecision,
                    preliminaryDecision = PermissionDecision.ALLOW,
                    source = resolved.source,
                    finalOutcome = FinalPermissionOutcome.ALLOWED_BY_POLICY
                ))
                continue // evaluate remaining scopes
            }
        }
    }

    // Aggregated approval — present all ASK scopes in one transaction
    if (pendingApprovals.isNotEmpty()) {
        val txnId = generateApprovalTransactionId()
        val txnResult = requestApprovalForScopes(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            approvals = pendingApprovals, transactionId = txnId
        )
        val validated = try {
            validateApprovalTransaction(pendingApprovals, txnId, txnResult)
        } catch (e: SecurityException) {
            auditMalformedApproval(tool, workspaceId, agentId, txnId, e)
            return PermissionResult.Denied(
                scopeId = "transaction",
                reason = DenialReason.MALFORMED_APPROVAL,
                errorCode = "NXR-2003"
            )
        }
        // Audit final outcome per scope with authoritative PolicySource
        for (v in validated) {
            auditFinalAskOutcome(
                tool = tool, workspaceId = workspaceId, agentId = agentId,
                scopeId = v.scopeId, source = v.source,
                transactionId = txnId, approved = v.approved
            )
            resolvedPermissions.add(ResolvedPermission(
                scopeId = v.scopeId,
                preliminaryDecision = PermissionDecision.ASK,
                source = v.source,
                finalOutcome = if (v.approved)
                    FinalPermissionOutcome.APPROVED_BY_USER
                else
                    FinalPermissionOutcome.DENIED_BY_USER
            ))
        }
        val allApproved = validated.all { it.approved }
        if (!allApproved) {
            val firstDenied = validated.first { !it.approved }
            return PermissionResult.Denied(
                scopeId = firstDenied.scopeId,
                reason = DenialReason.USER_DENIED,
                errorCode = "NXR-2003"
            )
        }
        // Approved ASK scopes — continue to classifier evaluation
    }

    return finalizeAuthorizationAfterScopes(
        tool = tool, workspaceId = workspaceId, agentId = agentId,
        resolvedPermissions = resolvedPermissions
    )
}

private suspend fun finalizeAuthorizationAfterScopes(
    tool: Tool,
    workspaceId: String,
    agentId: String?,
    resolvedPermissions: List<ResolvedPermission>
): PermissionResult {
    val classifierSelection = if (classifierEnabled) {
        classifierPolicy.shouldEvaluate(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            resolvedPermissions = resolvedPermissions
        )
    } else {
        ClassifierSelection(evaluate = false, reason = ClassifierSelectionReason.CLASSIFIER_DISABLED)
    }

    if (classifierSelection.evaluate) {
        val eval = classifier.evaluate(tool, workspaceId, agentId)
        auditClassifierEvaluation(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            evaluation = eval, reason = classifierSelection.reason
        )
        if (eval.decision == ClassifierDecision.DENY) {
            return PermissionResult.Denied(
                scopeId = eval.primaryScopeId ?: "classifier",
                reason = DenialReason.CLASSIFIER_DENIAL,
                errorCode = "NXR-2003"
            )
        }
    } else {
        auditClassifierSkipped(
            tool = tool, workspaceId = workspaceId, agentId = agentId,
            reason = classifierSelection.reason,
            resolvedPermissions = resolvedPermissions
        )
    }

    return PermissionResult.Allowed
}

/**
 * Resolves a single scope through the override hierarchy.
 * Returns both the effective decision and the policy source.
 */
private fun resolveDecision(
    scope: PermissionScope,
    workspaceId: String,
    agentId: String?
): ResolvedPermissionDecision {
    // 1. Agent-level override
    if (agentId != null) {
        val agentDecision = agentPermissionStore.get(agentId, scope.id)
        if (agentDecision != null) return ResolvedPermissionDecision(agentDecision, PolicySource.AGENT_OVERRIDE)
    }

    // 2. Workspace override
    val wsDecision = workspacePermissionStore.get(workspaceId, scope.id)
    if (wsDecision != null) return ResolvedPermissionDecision(wsDecision, PolicySource.WORKSPACE_OVERRIDE)

    // 3. Global policy
    val globalDecision = globalPermissionStore.get(scope.id)
    if (globalDecision != null) return ResolvedPermissionDecision(globalDecision, PolicySource.GLOBAL_POLICY)

    // 4. Scope default
    return ResolvedPermissionDecision(scope.defaultDecision, PolicySource.SCOPE_DEFAULT)
}

/**
 * Aggregated approval result — per-scope outcome.
 * source is NOT stored in ScopeApprovalOutcome; it is derived from PendingApproval.
 */
data class ScopeApprovalOutcome(
    val scopeId: String,
    val approved: Boolean
)

data class ApprovalTransactionResult(
    val transactionId: String,
    val outcomes: List<ScopeApprovalOutcome>
)

/**
 * Validates that the approval result exactly matches requested approvals.
 * Returns validated outcomes (with authoritative PolicySource from PendingApproval)
 * or denies the call if incomplete/malformed.
 */
data class ValidatedApproval(
    val scopeId: String,
    val source: PolicySource,
    val approved: Boolean
)

fun validateApprovalTransaction(
    requested: List<PendingApproval>,
    expectedTransactionId: String,
    result: ApprovalTransactionResult
): List<ValidatedApproval> {
    if (result.transactionId != expectedTransactionId) {
        throw SecurityException("Approval transaction ID mismatch: " +
            "expected=$expectedTransactionId actual=${result.transactionId}")
    }

    val requestedIds = requested.map { it.scope.id }
    val outcomeIds = result.outcomes.map { it.scopeId }

    // No duplicate requested scopes
    if (requestedIds.size != requestedIds.toSet().size) {
        throw SecurityException("Duplicate requested scope in approval batch")
    }

    // No duplicate outcomes
    if (outcomeIds.size != outcomeIds.toSet().size) {
        throw SecurityException("Duplicate approval outcome")
    }

    // Empty result when approvals requested is invalid
    if (result.outcomes.isEmpty() && requested.isNotEmpty()) {
        throw SecurityException("Empty approval result for non-empty request")
    }

    // Exact one-to-one coverage
    if (requestedIds.toSet() != outcomeIds.toSet()) {
        throw SecurityException("Approval coverage mismatch: " +
            "requested=${requestedIds.toSet()} result=${outcomeIds.toSet()}")
    }

    return requested.map { pending ->
        val outcome = result.outcomes.first { it.scopeId == pending.scope.id }
        ValidatedApproval(
            scopeId = pending.scope.id,
            source = pending.source,
            approved = outcome.approved
        )
    }
}

/**
 * Aggregated approval: presents all ASK scopes in one transaction.
 * Returns per-scope outcomes; tool executes only if every scope is approved.
 */
private suspend fun requestApprovalForScopes(
    tool: Tool,
    workspaceId: String,
    agentId: String?,
    approvals: List<PendingApproval>,
    transactionId: String
): ApprovalTransactionResult {
    return askUserForScopes(tool, approvals, transactionId)
}

enum class PolicySource { AGENT_OVERRIDE, WORKSPACE_OVERRIDE, GLOBAL_POLICY, SCOPE_DEFAULT, UNKNOWN_SCOPE }

enum class DenialReason { UNKNOWN_SCOPE, POLICY_DENIAL, USER_DENIED, MALFORMED_APPROVAL, CLASSIFIER_DENIAL }

data class ResolvedPermission(
    val scopeId: String,
    val declaredDefault: PermissionDecision,
    val preliminaryDecision: PermissionDecision,
    val source: PolicySource,
    val finalOutcome: FinalPermissionOutcome
)

enum class FinalPermissionOutcome {
    ALLOWED_BY_POLICY,
    APPROVED_BY_USER,
    DENIED_BY_USER  // present in audit; classifier never receives denied outcomes
}

data class ClassifierEvaluation(
    val decision: ClassifierDecision,
    val modelVersion: String,
    val riskScore: Float?,
    val reasonCodes: List<String>,
    val primaryScopeId: String?
)

enum class ClassifierDecision { ALLOW, DENY }

interface ClassifierPolicy {
    fun shouldEvaluate(
        tool: Tool,
        workspaceId: String,
        agentId: String?,
        resolvedPermissions: List<ResolvedPermission>
    ): ClassifierSelection
}

data class ClassifierSelection(
    val evaluate: Boolean,
    val reason: ClassifierSelectionReason
)

enum class ClassifierSelectionReason {
    WORKSPACE_OPT_IN,
    SCOPE_RISK_POLICY,
    TOOL_RISK_POLICY,
    CLASSIFIER_DISABLED,
    NOT_SELECTED
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
> **Purpose:** User vigilance (`FR-S016` `Manual`/`Assisted` mode) cannot be the only safety mechanism — `~93%` of approvals become automatic (`approval fatigue`). The classifier provides an independent, non-user-dependent layer that can `DENY` obviously risky calls, reducing dependence on user attention.

### Design Constraints

- **Independent layer:** The classifier operates **after** the `Permission Manager` (`checkPermission()`) but **before** `execute()` (`protocols/Tool-Protocol.md` — Authorization Gate). It does **NOT** replace user approval (`FR-S016`); it is an additional `DENY` gate.
- **Optional:** User can disable the classifier in `Workspace Settings` (`FR-W005`); default is `ENABLED` (safety-by-default).
- **On-device (`TFLite`)**: No network dependency; no external service.

### Classifier Pipeline Position

The classifier evaluates **after** all permission scopes are satisfied — never after a canonical denial:

```
Resolve all scopes
    ↓
Unknown scope? → return Denied (classifier not invoked)
    ↓
Any policy DENY? → return Denied (classifier not invoked)
    ↓
Collect and resolve ASK approvals
    ↓
Any ASK rejected? → return Denied (classifier not invoked)
    ↓
All scopes satisfied → optional classifier evaluation
    ↓
Classifier DENY? → audit + return Denied
    ↓
Classifier ALLOW? → execute
```

### Scope Selection

| Condition | Classifier behavior |
|---|---|
| Unknown scope | Permission denial; classifier not invoked |
| Any effective policy decision is DENY | Permission denial; classifier not invoked |
| Any ASK scope is rejected | Permission denial; classifier not invoked |
| All ASK scopes approved | Classifier evaluates if risk policy/config selects the call |
| All scopes ALLOW | Classifier evaluates only if risk policy/config selects the call |
| Classifier disabled | Skip classifier after permissions pass |

### Classifier Behavior

- **Input**: `Tool` (`requiredPermissions`, `parameters` JSON Schema), `context` (`workspaceId`, `agentId`, `executionHistory` — `FR-T015` audit trail), `userAutonomyMode` (`FR-S016`: `Manual`/`Assisted`/`Autopilot`).
- **Output**: `PermissionResult.Denied` (auto-deny) or `PermissionResult.Allowed` (pass through — does not bypass ASK or DENY scopes).
- Classifier `ALLOW` means "no classifier objection" — not automatic permission approval.
- Classifier `DENY` is final for the current tool call and cannot be overridden by ordinary user approval.
- The classifier does **not** change the declared scope default in the scope table.

### Relationship to Permission Resolution

The classifier is invoked **after** the complete permission authorization flow
(`checkPermission` in this document), but before `ToolExecutor.execute()`.
Conceptually:

```
authorizeToolCall()
  = permission resolution (checkPermission)
  + ASK approval
  + optional classifier (ClassifierPolicy.shouldEvaluate → Classifier.evaluate)

ToolExecutor.execute() runs only after authorizeToolCall() returns Allowed.
```

The classifier is part of the authorization gate, not a separate module boundary.
It operates on the resolved permission state and cannot retroactively change
permission decisions.

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
