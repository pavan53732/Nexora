# Non-Functional Requirements — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## Performance

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-PERF-001 | App cold start time | < 2 seconds | Time from launch to interactive |
| NFR-PERF-002 | Agent loop iteration latency | < 500ms (excluding provider) | Wall-clock per plan→execute→reflect cycle |
| NFR-PERF-003 | Tool execution overhead | < 50ms internal latency | Time from invocation to sandbox dispatch |
| NFR-PERF-004 | UI rendering | 60fps consistent | Frame drops < 1% during interaction |
| NFR-PERF-005 | Memory footprint (idle) | < 512MB RSS | Profiler measurement on mid-range device |
| NFR-PERF-006 | Battery impact (active agent) | < 10% drain/hour | Battery historian on reference device |
| NFR-PERF-007 | Concurrent agent execution | >= 3 agents | No perceptible UI degradation |
| NFR-PERF-008 | Streaming first-token latency | < 1 second | From request to first visible token |
| NFR-PERF-009 | Search query response | < 200ms | Local search across workspace data |
| NFR-PERF-010 | Workspace switch time | < 300ms | Full context swap including UI refresh |

## Reliability

| ID | Requirement | Target | Strategy |
|----|-------------|--------|----------|
| NFR-REL-001 | Crash recovery | Zero data loss on crash | WAL journaling, periodic checkpoints |
| NFR-REL-002 | Checkpoint resume | 100% state fidelity | Serialize full agent state to disk |
| NFR-REL-003 | Error recovery | Automatic retry (configurable) | Exponential backoff, max 3 attempts |
| NFR-REL-004 | Data persistence | ACID-compliant | Room with WAL mode |
| NFR-REL-005 | Graceful degradation | Degrade features, not crash | Fallback providers, cached responses |
| NFR-REL-006 | Offline mode | Read-only workspace access | Local data available without network |
| NFR-REL-007 | Backup/restore | Full workspace export/import | Encrypted archive format |
| NFR-REL-008 | Data integrity | CRC/checksum verification | On every write to persistent storage |
| NFR-REL-009 | Android background compliance | Foreground service type declared (API 34+); dataSync 6-hour cap (API 35+) handled via WorkManager handoff or user-initiated jobs; Doze-aware | Per [specs/BACKGROUND_EXECUTION.md](../specs/BACKGROUND_EXECUTION.md) §7 |

## Security

| ID | Requirement | Standard | Implementation |
|----|-------------|----------|----------------|
| NFR-SEC-001 | Sandbox isolation | Process-level separation | No access outside designated paths |
| NFR-SEC-002 | Permission enforcement | Least-privilege | Runtime permission checks on every tool call |
| NFR-SEC-003 | Encryption at rest | AES-256-GCM | Android Keystore for key management |
| NFR-SEC-004 | Encryption in transit | TLS 1.3 | Certificate pinning for provider APIs |
| NFR-SEC-005 | API key security | Encrypted storage | Keys never logged or exposed in memory dumps |
| NFR-SEC-006 | Audit logging | Tamper-evident | Append-only log for all security events |
| NFR-SEC-007 | Input validation | Allowlist-based | All external inputs sanitized before use |
| NFR-SEC-008 | Output sanitization | Context-aware | Escape outputs based on target context |
| NFR-SEC-009 | Plugin sandboxing | Classloader isolation | Plugins cannot access host app classes directly |
| NFR-SEC-010 | Secure storage | Android Keystore + EncryptedSharedPreferences | All sensitive config values encrypted |
| NFR-SEC-011 | Provider isolation | Credential + data-flow separation per provider | Per-provider key aliases in Android Keystore; requests tagged with active profile; provider plugins in isolated classloaders |
| NFR-SEC-012 | Provider network confinement | Endpoint allowlist | Provider HTTP clients connect only to their configured baseUrl; TLS 1.3 + certificate pinning |

## Usability

| ID | Requirement | Guideline | Validation |
|----|-------------|----------|------------|
| NFR-USE-001 | Learnability | First task within 5 minutes | User testing with new users |
| NFR-USE-002 | Accessibility | WCAG 2.1 AA | Screen reader, contrast, touch targets |
| NFR-USE-003 | Error messages | Actionable, jargon-free | User comprehension testing |
| NFR-USE-004 | Onboarding | 3-step guided setup | First-launch wizard with provider config |
| NFR-USE-005 | Responsive design | 320dp–1920dp | Tested on phone, tablet, foldable |
| NFR-USE-006 | Material Design 3 | Full compliance | Dynamic color, motion, typography |

## Maintainability

| ID | Requirement | Target | Approach |
|----|-------------|--------|----------|
| NFR-MAINT-001 | Modular architecture | < 10% cross-module coupling | Feature modules with event bus communication |
| NFR-MAINT-002 | Test coverage | > 80% line coverage | Unit + integration tests enforced in CI |
| NFR-MAINT-003 | Documentation | Every public API documented | KDoc with examples |
| NFR-MAINT-004 | CI/CD | Automated build + test on PR | GitHub Actions with lint, test, build gates |
| NFR-MAINT-005 | Conventional commits | 100% compliance | Commitlint + husky pre-commit hook |

## Scalability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-SCALE-001 | Plugin count | 50+ concurrent | No startup degradation |
| NFR-SCALE-002 | Tool count | 100+ registered | Discovery and search remain responsive |
| NFR-SCALE-003 | Workspace count | 100+ workspaces | List rendering uses lazy loading |
| NFR-SCALE-004 | Memory entries | 10,000+ entries | Search remains < 200ms |
| NFR-SCALE-005 | Agent count | 20+ per workspace | Resource limits enforced per agent |

## Compatibility

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-COMPAT-001 | Android version | API 34+ (Android 14) | MinSdk in build.gradle |
| NFR-COMPAT-002 | Screen sizes | Phone, tablet, foldable | Multi-window and orientation support |
| NFR-COMPAT-003 | Theme support | Light, dark, dynamic | Material You dynamic color |
| NFR-COMPAT-004 | Accessibility | TalkBack, Switch Access | Semantic markup and content descriptions |

## Portability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-PORT-001 | Gradle build | Reproducible on any dev machine | Gradle wrapper, no local paths |
| NFR-PORT-002 | APK output | Single universal APK | No split APKs for MVP; consider App Bundle later |
