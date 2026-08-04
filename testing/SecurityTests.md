# Security Tests

## Scope

Security tests validate permission mediation, sandbox isolation, secret handling, integrity, and abuse resistance.

## Framework Stack

- security-focused test harnesses
- device/emulator and sandbox validation tools
- adversarial fixtures where appropriate

## Penetration Test Scenarios

- unauthorized tool invocation
- sandbox escape attempts
- secret leakage through provider/plugin boundaries
- permission bypass during plugin activation
- invalid approval or cancellation sequencing

## Run Schedule

Run on security-sensitive changes and before release gating.

## Canonical Contract Evidence

Security validation SHOULD explicitly assert:

- permissions are enforced before side effects
- canonical error-envelope redaction rules are preserved
- credentials never cross caller-visible boundaries
- cancellation and retries do not bypass authorization
- plugin activation rollback preserves isolation guarantees
