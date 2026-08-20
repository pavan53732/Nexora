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

Every action in Nexora—tool invocation, network call, device access—requires a permission. The model defines **19 scopes**, three decision levels, a layered override hierarchy, and full auditability.

## Permission Scopes

| Scope | Description | Default | Android Equivalent |
|-------|-------------|---------|-------------------|
| `sandbox:read` | Read files inside the workspace sandbox | `ALLOW` | Internal storage (own) |
| `sandbox:write` | Write/modify/delete files inside the workspace sandbox | `ALLOW` | Internal storage (own) |
| `sandbox:execute` | Execute commands or scripts within the sandbox | `ALLOW` | N/A (managed by sandbox) |
| `network:http` | Make outbound HTTP/HTTPS requests | `ASK` | `INTERNET` |
| `network:websocket` | Open persistent WebSocket connections | `ASK` | `INTERNET` |
| `device:camera` | Access the device camera stream | `DENY` | `CAMERA` |
| `device:microphone` | Capture microphone audio input (e.g., terminal voice input, real-time transcription) | `DENY` | `RECORD_AUDIO` |
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

## Task-Scoped Execution Capability Escalation

The permission model does not grant Terminal or Background access universally. The static agent capability matrix is evaluated before authorization, and a capability absent from the current agent profile MUST be delegated to an eligible agent or requested through a task-scoped escalation handled by the existing authorization flow.

An escalation request is not a permission scope, permanent agent override, lifecycle state, or Tool identity. It is a bounded authorization projection tied to `workspaceId`, `taskId`, execution lineage, requesting `agentId`, requested capability, purpose, affected Tool IDs or operation class, required scopes, effective deadline, resource/concurrency limits, cancellation policy, and revocation condition. It MUST be rejected when the request exceeds the task acceptance criteria, workspace policy, autonomy mode, sandbox limits, or remaining execution deadline.

A temporary grant does not bypass scope resolution. Terminal use still requires `sandbox:execute` and applicable `sandbox:read`/`sandbox:write`; background use still requires the existing notification, checkpoint, resource, cancellation, and Android lifecycle contracts. Network, device, plugin, MCP, browser, and sensitive-action scopes remain independent. Permission scope resolution and explicit `DENY` remain final for the current authorization attempt.

A grant is valid only for the identified task and execution lineage. It expires at task completion, cancellation, effective deadline, explicit revocation, or terminal failure, whichever occurs first. It cannot be transferred to another task or agent, and it cannot be reused as a durable agent override. Revocation or expiry while a child operation is active MUST propagate cancellation through the existing runtime path and preserve checkpoint, audit, and non-success classification rules.

Every request, delegation, approval, grant, denial, use, expiry, revocation, and final disposition MUST be appended to the existing permission audit trail and correlated execution trace. The audit projection MUST identify the requester, delegated worker when applicable, capability, scope decisions, approval transaction, lifetime, and resulting Tool/execution outcome. This section changes no scope default and introduces no new scope identifier.

## Derived Cross-Policy Eligibility Report (ADR-0010)

Nexora MAY compute a derived eligibility report before a side-effecting operation by joining the existing owner decisions for PermissionModel authorization, Task/Execution deadline and recovery, ResourceManager budgets, ContextSnapshot/evidence eligibility, Tool risk and unknown-completion status, Workflow readiness, Sandbox/Security rules, and cancellation state. The report is diagnostic and evaluative; the owner of each input remains authoritative.

A stateless evaluator MAY compute the composite result from an explicit immutable set of owner outputs, versions/timestamps, operation identity, approval transaction, context/evidence references, resource snapshot, and unknown-completion classification. It MUST be deterministic for the same inputs and MUST report the contributing owner, source version, decision, and conflict for every dimension. Missing, stale, contradictory, or unavailable owner input MUST produce an explicit non-eligible or unresolved outcome; it MUST NOT be silently treated as eligible.

The report or evaluator MUST NOT grant or deny a PermissionModel scope, transition Task/Execution/Workflow/Tool state, reset a deadline or retry budget, resolve `UNKNOWN_COMPLETION`, bypass audit/sandbox/context checks, or declare completion. It has no persisted policy identity, policy lifecycle, precedence rule, override authority, scheduler, recovery authority, or production veto authority. An authoritative Policy Engine or policy god-object requires a separate ADR demonstrating that the existing owners and stateless evaluator are insufficient.

Environment diagnostics MAY be included as an input to this report when they concern ABI, asset, mount, storage, quota, integrity, permission, battery, network, or scheduling readiness. Such diagnostics are observed evidence only; they MUST preserve applicable existing task/execution/workspace/correlation/checkpoint/evidence references and MUST classify unavailable or contradictory inputs explicitly. They MUST NOT grant a permission, convert an unresolved condition into `ALLOW`, bypass approval or audit, mutate Task/Execution/Workspace state, or authorize repair or side effects. Fail-closed authorization and the existing Runtime, Sandbox, Full Environment, Background, and Workspace recovery paths remain authoritative.

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

suspend fun authorizeToolCall(
    call: ToolCall,
    state: AgentState
): PermissionResult {
    val tool = toolRegistry.requireActive(call.toolId)
    return checkPermission(tool, state.workspace.id, state.agentId)
}

suspend fun checkPermission(
    tool: Tool,
    workspaceId: String,
    agentId: String?
): PermissionResult {
    val scopeIds = tool.requiredPermissions

    // Validate: no duplicate scope declarations (invalid Tool descriptor)
    if (scopeIds.size != scopeIds.toSet().size) {
        auditInvalidDescriptor(tool, workspaceId, agentId, scopeIds)
        return PermissionResult.Denied(
            scopeId = "declaration",
            reason = DenialReason.INVALID_SCOPE_DECLARATION,
            errorCode = "NXR-2005"
        )
    }

    // Empty permission list — authorization proceeds without a local AI classifier.
    if (scopeIds.isEmpty()) {
        return PermissionResult.Allowed
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
                scopeId = v.scope.id, source = v.source,
                transactionId = txnId, approved = v.approved
            )
            if (v.approved) {
                resolvedPermissions.add(ResolvedPermission(
                    scopeId = v.scope.id,
                    declaredDefault = v.scope.defaultDecision,
                    preliminaryDecision = PermissionDecision.ASK,
                    source = v.source,
                    finalOutcome = FinalPermissionOutcome.APPROVED_BY_USER
                ))
            }
        }
        val allApproved = validated.all { it.approved }
        if (!allApproved) {
            val firstDenied = validated.first { !it.approved }
            return PermissionResult.Denied(
                scopeId = firstDenied.scope.id,
                reason = DenialReason.USER_DENIED,
                errorCode = "NXR-2003"
            )
        }
        // Approved ASK scopes continue directly to execution authorization.
        // DEC-36: an approval transaction that expires before a valid
        // authorization outcome is committed is classified as POLICY_DENIAL;
        // an explicit user rejection remains USER_DENIED.
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
    val scope: PermissionScope,
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
            scope = pending.scope,
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

enum class DenialReason { UNKNOWN_SCOPE, POLICY_DENIAL, USER_DENIED, MALFORMED_APPROVAL, CLASSIFIER_DENIAL, INVALID_SCOPE_DECLARATION }

The PermissionModel owns resolution of these denial reasons and approval-transaction validity. Under [DEC-35](../decisions/DEC-35-approval-denial-cross-layer-projection.md), it does not own the resulting Task or Agent lifecycle projection: the Tool boundary returns `NXR-2003` without side effects, TaskLifecycle commits the Task failure effect, and AgentLifecycle may project availability as `Paused`.

data class ResolvedPermission(
    val scopeId: String,
    val declaredDefault: PermissionDecision,
    val preliminaryDecision: PermissionDecision,
    val source: PolicySource,
    val finalOutcome: FinalPermissionOutcome
)

enum class FinalPermissionOutcome {
    ALLOWED_BY_POLICY,
    APPROVED_BY_USER
}

```

## Permission Audit Schema

The permission audit log (`permission_audit_log`) is an append-only, agent/plugin-immutable
Room table. Every authorization event records:

| Field | Description |
|---|---|
| `auditEventId` | Unique event identity |
| `eventType` | One of: `SCOPE_RESOLVED`, `SCOPE_ALLOWED`, `SCOPE_DENIED`, `APPROVAL_REQUESTED`, `APPROVAL_APPROVED`, `APPROVAL_DENIED`, `APPROVAL_MALFORMED`, `AUTHORIZATION_ALLOWED`, `AUTHORIZATION_DENIED`, `INVALID_TOOL_DESCRIPTOR` |
| `toolId` | Tool descriptor ID |
| `toolCallId` | Per-call identity |
| `correlationId` | Cross-system correlation |
| `workspaceId` | Active workspace |
| `agentId` | Active agent (nullable) |
| `scopeId` | Permission scope ID (nullable for non-scope events) |
| `declaredDefault` | Canonical scope default |
| `preliminaryDecision` | Effective policy decision |
| `policySource` | `AGENT_OVERRIDE`, `WORKSPACE_OVERRIDE`, `GLOBAL_POLICY`, `SCOPE_DEFAULT`, `UNKNOWN_SCOPE` |
| `finalOutcome` | `ALLOWED_BY_POLICY`, `APPROVED_BY_USER` |
| `denialReason` | `UNKNOWN_SCOPE`, `POLICY_DENIAL`, `USER_DENIED`, `MALFORMED_APPROVAL`, `CLASSIFIER_DENIAL`, `INVALID_SCOPE_DECLARATION` |
| `approvalTransactionId` | ASK transaction ID when applicable |
| `occurredAt` | Timestamp |
| `sanitizedDetails` | Redacted additional context |

Rules:
- Agents, tools, and plugins cannot mutate audit records.
- Authorized retention purge is a system maintenance operation.
- Sensitive inputs and secrets are redacted in `sanitizedDetails`.
- `toolCallId` and `correlationId` are preserved across all related events.


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

Policy stores contain mutable authorization configuration. They are distinct from the
append-only `permission_audit_log`, whose canonical event schema is defined above.

## Permission Audit Trail

All permission and authorization-gate events are written to `permission_audit_log`
(canonical schema: `specs/DATABASE_SCHEMA.md`). This log cannot be edited or deleted by
agents, tools, or plugins. It supports:

- Filtering by workspace, agent, or time range.
- Export for compliance review.
- **Retention:** `permission_audit_log` is the authoritative, **non-evictable** audit
  trail retained for legal/compliance review. A separate *operational* audit view MAY
  surface a 90-day rolling window for UX filtering and routine review, but that derived
  view MUST NOT delete or mutate the canonical rows — any purge path preserves the source
  (copy-to-cold-storage or a `purgeEligible` flag on the derived view, never `DELETE` from
  `permission_audit_log`). This reconciles the earlier "90-day auto-purged" text with the
  schema's "legal retention / non-evictable" rule.
- Exactly-once recovery depends on a separate append-only `execution_replay` log
  (`specs/DATABASE_SCHEMA.md`) that records completed tool calls; it is distinct from the
  permission audit trail.

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

## Security Classifier Boundary (DEC-42)

The optional on-device TFLite auto-approval classifier is retired from the active architecture. Nexora does not bundle, load, execute, or manage TFLite, ONNX, GGUF, or other local AI model files for authorization or any other AI-model function.

Authorization remains fail-closed through the existing PermissionModel scope hierarchy, explicit `DENY`, `ASK` approval transactions, user decisions, policy evaluation, and audit logging. `ToolExecutor.execute()` runs only after the existing permission and approval flow returns `Allowed`. No classifier `ALLOW` override, bypass, or new permission state is introduced.

A future cloud safety-classification service requires a separate decision covering privacy, egress, latency, availability, error mapping, and fail-closed behavior. It is not part of the current contract.

Historical DL-022/DL-034 classifier wording is preserved as historical decision record; it is not active implementation authority after DEC-42.

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
