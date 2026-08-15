> **Status: SUPPORTING** for NFR requirements.
> This document records focused requirements for NFR; canonical subsystem definitions remain in the owning architecture documents.


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
| NFR-PERF-011 | Stream backpressure | P95 queue wait < 100ms; zero dropped semantic/control events | Bounded-channel metrics under slow consumers |
| NFR-PERF-012 | Cancellation propagation | < 250ms P95 from user cancel to adapter cancellation request | End-to-end stream cancellation benchmark |

## Reliability

| ID | Requirement | Target | Strategy |
|----|-------------|--------|----------|
| NFR-REL-001 | Crash recovery | Zero data loss on crash | WAL journaling, periodic checkpoints |
| NFR-REL-002 | Checkpoint resume | 100% state fidelity | Serialize full agent state to disk |
| NFR-REL-003 | Error recovery | Automatic retry (configurable) | Exponential backoff, max 3 retries (attempt=0 is the first retry; 1 initial execution + 3 retries = 4 total executions maximum); each delay = `base × 2^attempt × random(0.5…1.5)` (jitter); retry across tool invocations, sub-agent delegation, and provider reconnects per [AUTONOMY_STABILITY.md §9.2](../specs/AUTONOMY_STABILITY.md#92-retry-policy) and [ADR-0009](../docs/adr/ADR-0009-Adaptive-Autonomy-And-Persistence.md) Decision #8. No maximum interval cap is imposed beyond the exponential formula. |
| NFR-REL-004 | Data persistence | ACID-compliant | Room with WAL mode |
| NFR-REL-005 | Graceful degradation | Degrade features, not crash | Alternate eligible cloud providers, cached responses, supported non-inference workspace operations, and read-only access |
| NFR-REL-006 | Offline workspace mode | Read-only and supported local-data operations only | Local data remains available without network; agent inference, planning, embeddings, and provider-backed execution are unavailable |
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
| NFR-SEC-013 | Egress data-loss prevention | Outbound body inspection | All sandbox egress scanned for secrets/keys; blocked or warned before transmission (per workspace policy). Egress is enforced at the boundary: guest processes cannot open direct outbound sockets; all traffic is forced through the workspace egress proxy (`docs/SANDBOX_DEPTH.md` §2.4), which terminates guest TLS with a workspace-scoped CA for inspectable DLP and fails closed on bypass attempts |
| NFR-SEC-014 | Pipe channel security | Mutual TLS 1.3 + pinned instance certificates | All inter-instance traffic encrypted and mutually authenticated; payloads schema-validated pre-parse; DLP scan (NFR-SEC-013) applies to outbound pipe bodies; provider credentials never cross pipes |
| NFR-SEC-015 | Reasoning and stream artifact privacy | Redacted structured artifacts only | Raw private chain-of-thought, credentials, system prompts, and resume tokens are excluded from logs/exports |
| NFR-REL-010 | Snapshot restore fidelity | 100% state fidelity + integrity | Workspace snapshots hash-verified at restore; tampered snapshots rejected (see [docs/SANDBOX_DEPTH.md](../docs/SANDBOX_DEPTH.md)) |
| NFR-REL-011 | Context resume fidelity | Structured state + summary + retrieval reconstruct the working context | Resume uses checkpoint + summary + retrieval; never raw history replay; context build < 500 ms after restart (see [specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md)) |
| NFR-REL-012 | Exactly-once recovery | No double-applied side effects after crash/resume | Idempotency declarations + replay log; non-idempotent calls reconciled from tool history (see [specs/AUTONOMY_STABILITY.md](../specs/AUTONOMY_STABILITY.md)) |
| NFR-REL-013 | Degradation continuity | App stays usable through provider outage | Cloud-only ladder (failover → cached/non-inference operation → read-only), each step announced and logged; no local AI inference fallback (NFR-REL-005) |
| NFR-REL-014 | Ordered stream delivery | No undetected duplicate/gap; exactly one terminal event | Monotonic `(streamId, sequence)` validation and durable terminal commit |
| NFR-REL-015 | Stream resume/failover lineage | No silent cross-stream/provider splice | Native cursor resume or new stream with `priorStreamId` |
| NFR-REL-016 | Hierarchical execution deadlines | No child operation outlives its parent deadline; exhaustion produces explicit incomplete/escalated status | Remaining-deadline propagation with cancellation and checkpoint reservation |
| NFR-REL-017 | Unknown-completion reconciliation | No unresolved non-idempotent side effect is silently retried, marked failed, or reported successful | Operation-level idempotency/status lookup, compensation, or manual reconciliation contract |
| NFR-REL-018 | Agent reliability evidence | Critical recovery and liveness controls are exercised by repeatable fault-injection journeys before release gating | Android device/emulator matrix and deterministic fault-injection suite |

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

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-COMP-001 | Preserve compatibility and explicit version semantics across documented API, SDK, protocol, registry, plugin, provider, and schema contracts | Backward-compatible changes remain interpretable; breaking changes are versioned, migrated, or explicitly rejected | Contract regression suite and compatibility-matrix review across affected artifacts |
| NFR-COMPAT-001 | Android version | API 34+ (Android 14) | MinSdk in build.gradle |
| NFR-COMPAT-002 | Screen sizes | Phone, tablet, foldable | Multi-window and orientation support |
| NFR-COMPAT-003 | Theme support | Light, dark, dynamic | Material You dynamic color |
| NFR-COMPAT-004 | Accessibility | TalkBack, Switch Access | Semantic markup and content descriptions |

## Portability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-PORT-001 | Gradle build | Reproducible on any dev machine | Gradle wrapper, no local paths |
| NFR-PORT-002 | APK output | Single universal APK | No split APKs for MVP; consider App Bundle later |


## Environment & Rootfs Reliability

| ID | Requirement | Target | Measurement |
|---|---|---:|---|
| NFR-ENV-001 | Rootfs extraction succeeds on devices with ≥ 2 GB free storage | 99.5% | Firebase Crashlytics |
| NFR-ENV-002 | Rootfs SHA-256 integrity verification completes within two seconds | < 2 s | Pixel 6 benchmark |
| NFR-ENV-003 | Full Environment supports `manylinux_2_28+` pip binary wheels | 100% | Top-100 PyPI package matrix |
| NFR-ENV-004 | proot execution overhead versus native shell | < 20% | `time` benchmark |
| NFR-ENV-005 | Rootfs reset to clean state | < 3 s | Wipe overlay without re-extraction |
| NFR-ENV-006 | Offline package installation from cache after seven days offline | 100% | Integration test |
| NFR-ENV-007 | Environment reset and upgrade preserve workspace files outside the overlay | 100% | VFS bind-mount test |


## Context Integrity and Bounded Execution

| ID | Requirement |
|---|---|
| NFR-CI-001 | Canonical conversation history must remain recoverable independently of summaries or compacted context views. |
| NFR-CI-002 | Read-time context assembly must preserve provenance and authority distinctions between conversation, memory, evidence, requirements, constraints, decisions, tool results, and execution state. |
| NFR-REL-004 | Iterative reasoning and execution loops must use bounded-progress controls with explicit retry, step, and time limits. |
| NFR-PERF-006 | The runtime must prefer the minimum sufficient execution mode (FAST, NORMAL, DEEP, VERIFY, RECOVER) rather than using deep reasoning by default. |
| NFR-CI-003 | Significant user-facing factual claims must retain one-to-one evidence, authority, freshness, contradiction, verifier, confidence, and disposition metadata. |
| NFR-CI-004 | Semantic progress must be evaluated against declared acceptance criteria; irrelevant changes must not reset zero-progress detection. |
| NFR-CI-005 | Reasoning and execution settings must not exceed non-overridable provider, device, and resource-class safety ceilings. |
