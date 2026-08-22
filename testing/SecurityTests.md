# Security Tests

## Scope

Security tests validate permission mediation, sandbox isolation, secret handling, integrity, and abuse resistance.

## Suite IDs

- `SEC-PERM-001..023` — foundational permission, multi-scope, TOOL-408, and audit behavior
- `SEC-PERM-024..034` — malformed/duplicate declaration and approval validation
- `SEC-PERM-035..052` — ResolvedPermission and canonical authorization outcomes
- `SEC-PERM-053..066` — declared defaults, scope/Tool precedence, descriptor activation, and final audit rules; classifier-era rows are retained for traceability only under DEC-42
- `SEC-SBX-*` — sandbox isolation
- `SEC-SECRET-*` — secret handling and redaction
- `SEC-PLUGIN-*` — plugin integrity and rollback
- `SEC-LC-*` — lifecycle enforcement (Session SEC-LC-SESSION-001..006, Execution SEC-LC-EXEC-001..004, ToolStatus SEC-LC-TOOL-001..002)

## Framework Stack

- security-focused test harnesses
- device/emulator and sandbox validation tools
- adversarial fixtures where appropriate

## Penetration Test Scenarios

- `SEC-PERM-001` unauthorized tool invocation
- `SEC-SBX-001` sandbox escape attempts
- `SEC-SECRET-001` secret leakage through provider/plugin boundaries
- `SEC-PLUGIN-001` permission bypass during plugin activation
- `SEC-PERM-002` invalid approval or cancellation sequencing
- `SEC-DOS-001` fork bomb and process limiting
- `SEC-DOS-002` disk and memory quota exhaustion
- `SEC-FLOW-001` cross-provider credential leakage
- `SEC-NET-001` network egress domain bypass

## Run Schedule

Run on security-sensitive changes and before release gating.

## Canonical Contract Evidence

Security validation SHOULD explicitly assert:

- known low-risk category `ALLOW` defaults proceed without an ASK transaction only when no higher-priority restriction applies, and high-risk `ASK`/`DENY` gates remain authoritative
- permissions are enforced before side effects
- canonical error-envelope redaction rules are preserved
- credentials never cross caller-visible boundaries
- cancellation and retries do not bypass authorization
- plugin activation rollback preserves isolation guarantees
- AI Settings Test Connection and capability refresh do not expose API keys, grant permissions, invoke Tools, create Task/Execution state, or bypass provider/sandbox/security gates
- automatic autonomy-mode selection, downgrade-only override, category-default authorization, and policy-approved skill promotion do not invoke a local classifier or bypass PermissionModel, SandboxPolicy, audit, or high-risk approval gates

## Inference Stream and Reasoning Security

`SEC-STREAM-001..010` validate terminal/sequence integrity, Tool fragment isolation,
audit lineage, reasoning redaction, resume-token security, failover confinement,
bounded buffering, and reasoning-budget enforcement (TM-038..047).

## ADR-0010 Evidence and Deterministic Controls

Security cases MUST use the common evidence envelope in `testing/EVIDENCE_CONVENTIONS.md` and retain permission, workspace, task, execution, tool-call, correlation, audit, fixture, environment, expected owner decision, observed result, and artifact metadata where applicable. Deterministic controls may vary test clock, seed/jitter, provider/stream, resource, permission, storage/lock, scheduler, or process/device conditions only inside the fixture boundary. They MUST NOT bypass PermissionModel, SandboxPolicy, egress, redaction, audit, lifecycle, idempotency, or unknown-completion rules.

For a case exercising automatic security-intent routing, the evidence MUST identify or explicitly mark unavailable the security intent, authorized target/scope and its source, selected existing agent roles and distinct objectives, omitted capabilities and selection reason, provider capability and Tool route, applicable PermissionModel/SandboxPolicy/network/audit/deadline/resource/evidence decisions, any attempted self-grant or bypass and its no-execution result, residual risk, unresolved uncertainty, and final disposition. These fields are projections over existing identities and do not authorize offensive action or establish execution success.

A security case is `TEST DEFINED` until execution produces a result; only the retained reproducible result is `EXECUTED EVIDENCE`. Fault-injection categories are selected by the affected security contract and release gate. Security owners remain authoritative; the evidence envelope and deterministic controls create no new policy or production authority.
