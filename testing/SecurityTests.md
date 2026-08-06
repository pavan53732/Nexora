# Security Tests

## Scope

Security tests validate permission mediation, sandbox isolation, secret handling, integrity, and abuse resistance.

## Suite IDs

- `SEC-PERM-*` — permission enforcement (including multi-scope evaluation SEC-PERM-003..023, TOOL-408 regression SEC-PERM-018..022, audit trail SEC-PERM-023)
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
