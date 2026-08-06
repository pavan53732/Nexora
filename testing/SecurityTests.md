# Security Tests

## Scope

Security tests validate permission mediation, sandbox isolation, secret handling, integrity, and abuse resistance.

## Suite IDs

- `SEC-PERM-001..023` — foundational permission, multi-scope, TOOL-408, and audit behavior
- `SEC-PERM-024..034` — malformed/duplicate declaration and approval validation
- `SEC-PERM-035..052` — ResolvedPermission and classifier behavior
- `SEC-PERM-053..066` — declared defaults, classifier precedence, descriptor activation, and final audit rules
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

- permissions are enforced before side effects
- canonical error-envelope redaction rules are preserved
- credentials never cross caller-visible boundaries
- cancellation and retries do not bypass authorization
- plugin activation rollback preserves isolation guarantees

## Inference Stream and Reasoning Security

`SEC-STREAM-001..010` validate terminal/sequence integrity, Tool fragment isolation,
audit lineage, reasoning redaction, resume-token security, failover confinement,
bounded buffering, and reasoning-budget enforcement (TM-038..047).
