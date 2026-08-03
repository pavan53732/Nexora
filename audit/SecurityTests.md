> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Security Tests

## Scope

Security tests validate that Nexora's defenses hold against known attack vectors. Coverage is aligned with the **OWASP Mobile Top 10 (2024)**.

| OWASP Category | Nexora Test Area |
|----------------|------------------|
| M1 — Improper Credential Storage | API keys stored in EncryptedSharedPreferences, not plaintext |
| M2 — Inadequate Supply Chain Security | Plugin signing verification, APK integrity checks |
| M3 — Insecure Communication | Provider API calls enforce TLS 1.3, certificate pinning |
| M4 — Insecure Authentication | Session tokens validated server-side, no client-side bypass |
| M5 — Insufficient Input Validation | Tool parameters sanitized, plan content validated |
| M6 — Insecure Authorization | PermissionManager enforced at every tool call boundary |
| M7 — Client Code Quality | No hardcoded secrets (detected via `detect-secrets`)
| M8 — Code Tampering | APK signature verification, runtime integrity check |
| M9 — Reverse Engineering | ProGuard/R8 obfuscation verified on release builds |
| M10 — Extraneous Functionality | Debug logs, hidden UI, test endpoints removed in release |

## Framework Stack

| Tool | Purpose |
|------|--------|
| JUnit 5 | Test runner |
| Custom security test helpers | `SandboxEscapeTestHelper`, `InjectionTestHelper` |
| OWASP ZAP (Docker) | Automated API security scan against local test server |
| `detect-secrets` | Static analysis for hardcoded credentials |
| ProGuard/R8 verifier | Confirm obfuscation on release APK |

## Penetration Test Scenarios

| # | Scenario | Expected Result |
|---|----------|----------------|
| 1 | Tool in sandbox attempts `File("/sdcard/data").readText()` | `SecurityException` — path outside sandbox root |
| 2 | Inject SQL via tool parameter into Room query | Query returns empty / sanitized result, no data leak |
| 3 | Load a plugin APK with an invalid or tampered signature | `PluginVerificationException`, plugin rejected |
| 4 | Exceed token budget by crafting a prompt that requests max tokens repeatedly | `InsufficientBudgetException` after first cycle |
| 5 | XSS payload injected into agent output displayed in WebView | Payload rendered as plain text, not executed |
| 6 | Agent in Workspace A attempts to read Workspace B's memory | `AccessDeniedException`, zero data returned |
| 7 | Audit log completeness — execute 10 actions, query audit log | All 10 actions present with correct timestamp and actor |
| 8 | EncryptedSharedPreferences — force-clear encryption key, restart app | API keys still accessible (re-encrypted on first boot) |

## Run Schedule

| Trigger | Scope |
|---------|--------|
| Every PR | Fast subset: scenarios 1–4 (no external tools, < 30 s) |
| Weekly | Full suite: all 8 scenarios + OWASP ZAP scan + `detect-secrets` |
| Pre-release | Full suite + manual penetration review by security team |