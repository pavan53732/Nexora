# FR / NFR Placeholder-to-Actual Ledger Mapping

> **Status: CANONICAL** — mapping of placeholder IDs (`FR-TL-401`..`406`, `NFR-SEC-021`, etc.) to verified actual requirement IDs from `docs/REQUIREMENT_COVERAGE_LEDGER.md`.
> **Rule source:** `docs/TRACEABILITY_RULES.md` (Evidence Rule, Coverage Rule, Audit Rule).
> **Purpose:** Ensure no placeholder references remain unaligned; every reference points to a concrete, mapped requirement.

---

## Placeholder → Actual Mapping Table

| Placeholder ID | Actual Ledger ID | Category | Owner | Primary Artifact | Validation Case | Evidence Path | Status |
|---|---|---|---|---|---|---|---|
| `FR-TL-401` | `FR-TL001` | Tooling (MCP source) | Tooling | `architecture/TOOL_SYSTEM.md` | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-402` | `FR-TL002` | Tooling (MCP transport) | Tooling | `protocols/Tool-Protocol.md` | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-403` | `FR-TL003` | Tooling (MCP registry) | Tooling | `registry/TOOLS.md` | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-404` | `FR-TL004` | Tooling (MCP lifecycle) | Tooling | `architecture/TOOL_SYSTEM.md` (§Lifecycle) | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-405` | `FR-TL005` | Tooling (MCP security) | Tooling | `security/PermissionModel.md` (§MCP rules) | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-406` | `FR-TL006` | Tooling (MCP phase mapping) | Tooling | `specs/AI_PROVIDERS.md` (§Phase 5) | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `NFR-SEC-021` | `NFR-SEC-001` | Security (explicit risk-based defaults) | Security | `security/PermissionModel.md` (§Explicit Risk-Based Scope Defaults) | `SEC-PERM-001` | `evidence/security/SEC-PERM-001/` | MAPPED |

---

## Verification Notes

- **No placeholder patterns remain** in edited docs (`architecture/TOOL_SYSTEM.md`, `protocols/Tool-Protocol.md`, `registry/TOOLS.md`, `registry/TOOL_MATRIX.md`, `specs/BACKGROUND_EXECUTION.md`, `security/PermissionModel.md`, `security/SandboxPolicy.md`, `specs/BROWSER.md`, `specs/AI_PROVIDERS.md`, `docs/DECISION_LOG.md`). Verified with regex search (`FR-[A-Z]{2}-[4-9][0-9]{2}` etc.) — `0` matches.
- All edited documents reference **actual** ledger IDs (`FR-S016`, `FR-AS-009`, `FR-T011`, `FR-W005`, `FR-P011`, `FR-S014`/`015`, `FR-TL015`, `FR-EV-002`/`006`, `FR-S028`, `FR-P009`, `NFR-REL-002`/`003`).
- Mapping aligns with `docs/TRACEABILITY_RULES.md` (Evidence Rule, Coverage Rule, Audit Rule) and `docs/REQUIREMENT_COVERAGE_LEDGER.md` (authoritative inventory).

---

## References

- `docs/REQUIREMENT_COVERAGE_LEDGER.md` (authoritative inventory — `FR-TL001`..`015`, `NFR-SEC-001`..`013`).
- `docs/TRACEABILITY_RULES.md` (mapping rules — Evidence, Audit, Coverage).
- `docs/DECISION_LOG.md` (`DL-020` MCP, `DL-021` OEM, `DL-022` Security, `DL-023` Blocked-List, `DL-024` Voice/Camera — all mapped to actual `FR`/`NFR` IDs).
- `docs/CHANGELOG.md` (`v4.5.0` preserved; `G4–G5` entry present — no `v4.6` added per user instruction).

---

*No placeholders remain unmapped. All references point to verified ledger entries.*

## S1 — Dynamic Concurrency Cap (SA-3)
- `FR-MA-003` (parallel coordination) mapped to `MULTI_AGENT_SYSTEM.md` §SA-3.
- `FR-AS-003` (technical-boundary escalation) mapped to concurrency-cap and resource-safety feeds; financial cost/credit status remains informational and non-blocking.
- `FR-S018` (sandbox isolation) mapped to per-sub-agent isolation under cap.
- `NFR-REL-003` (reliability) preserved — cap prevents overload-induced failures.

## S4 — Terminal Specification (Fully Specified)
- `FR-TE001`..`005` (terminal execution/lifecycle/tools) → `specs/TERMINAL.md` (§Execution Model, §Lifecycle, §Security).
- `FR-S002`/`003`/`018` (sandbox/process/workspace isolation) → `specs/TERMINAL.md` (§Security & Isolation) + `security/SandboxPolicy.md`.
- `FR-AS-002`/`003`/`009`/`013` (heartbeat/technical-boundary escalation/degradation/recovery) → `specs/TERMINAL.md` (§Timeout Discipline, §Restore Behavior) + `specs/BACKGROUND_EXECUTION.md`; financial cost/credit is not a terminal gate.
- `FR-TL015` (audit trail) → `specs/TERMINAL.md` (§Audit).
- `FR-EV-002`/`006` (evidence/reviewer) → `specs/TERMINAL.md` (§Evidence & Validation Engine reference).
- `FR-M012`/`013` (file version/user preferences) → `specs/TERMINAL.md` (§Restore Behavior — checkpoint storage + retention).
- `FR-A010` (real-time monitoring) → `specs/TERMINAL.md` (§Audit — technical-limit/cap/timeout events).
- `FR-U005` (agent activity feed) → `specs/TERMINAL.md` (§Boundary Violation Response — denied actions surfaced).
- `FR-GT-001`..`006` (git grounding) preserved — terminal session does not affect git grounding rules.

## Agent Intelligence Deepening
- `FR-AS-004` → `specs/AUTONOMY_STABILITY.md` §4 and `models/AutonomyLearning.md`; lessons retain provenance/evidence, are validated before planning retrieval, and may promote/refine an existing `LEARNED` Skill through the existing deterministic policy or user path when trust, safety, scope, evidence, and lifecycle conditions pass. Validation `UT-AS-004` (Planned).
- `FR-AS-005` → `specs/AUTONOMY_STABILITY.md` §5 and `models/AutonomyLearning.md`; trust is scoped to agent/workspace and automatically selects `MANUAL` 0–39, `ASSISTED` 40–74, or `AUTOPILOT` 75–100. Existing user override may only downgrade immediately; security, permission, degraded-mode, and high-risk boundaries remain authoritative. Validation `UT-AS-005` (Planned).
- `NFR-CI-003` → `specs/CONTEXT_MANAGEMENT.md` §7, `models/Inference.md` (`ClaimRecord`), `specs/DATABASE_SCHEMA.md` (`claim_record`), `protocols/Agent-Protocol.md`, and `docs/api/Agent-API.md`; validation `UT-EV-007`, `E2E-REL-009` (Planned).
- `NFR-CI-004` → Agent Runtime final completion revalidates the acceptance vector after repair and answer synthesis; validation `UT-AS-010`, `E2E-REL-007` (Planned).

## S5 — Multi-Instance Pipes
- `FR-MI-001`..`010` (discovery, transport, same-machine orchestration, pairing, cross-instance delegation, heartbeats, broadcast, security gates, failure handling, settings surface) → `specs/PIPES.md` (canonical) + `state-machines/InstanceLifecycle.md` (canonical states) + `models/Instance.md` (derived).
- `FR-AG-001`/`002` (coordinator role, no direct agent calls) → preserved across pipes via `architecture/MULTI_AGENT_SYSTEM.md` §Cross-Instance Extension.
- `FR-S016` (autonomy modes) → per-pipe acceptance mode (PIPES.md §6).
- `FR-S018` (per-agent sandbox) → remote sub-agent runs in the remote instance's own sandbox (PIPES.md §6).
- `FR-P011`/`FR-P013` (provider profiles, provider isolation) → credentials never cross pipes; remote execution uses remote profiles (PIPES.md §2 rule 2, §8).
- `FR-S014`/`FR-S015` (egress policy, quarantine) → pipe egress confinement + inbound artifact quarantine (PIPES.md §8).
- `FR-TL015` (audit trail) → pipe events audited end-to-end (PIPES.md §2 rule 4).
- `FR-CM-006` (context trust tagging) → inbound payloads are untrusted segments (PIPES.md §8).
- `NFR-SEC-014` (pipe channel security) → `requirements/NFR.md`; validation `SEC-NET-001`.
- `NFR-REL-002`/`012` (resume fidelity, exactly-once) → mid-task pipe recovery (PIPES.md §6, §9).

## S6 — Reasoning Effort Scale
- `FR-RN-003` (effort levels) → amended to 6-level scale (OFF/LOW/MEDIUM/HIGH/X_HIGH/MAX) in `specs/CONTEXT_MANAGEMENT.md` §6.
- `FR-RN-004` (reasoning models) → amended: fail-fast at X_HIGH/MAX; graceful degradation at HIGH and below.
- `FR-RN-007` (reasoning disable OFF) → `specs/CONTEXT_MANAGEMENT.md` §6 (OFF semantics: gate bypass, params omitted, RG/EV gates unaffected).
- `FR-RN-008` (settings surface + override hierarchy) → `specs/CONTEXT_MANAGEMENT.md` §6 (task→agent→workspace→global→default MEDIUM; Settings → Model Config → Reasoning).
- Wire contract → `architecture/PROVIDER_SYSTEM.md` (`CompletionRequest.reasoningEffort: ReasoningEffort?`, OFF = null/omitted; per-model mapping owned by adapters).

## SB — Bypass and Self-Grant Authorization Paths (DEC-50)
- `FR-AG-005` → authorized Tool descriptors MAY declare bypassSafeguards, allowJailbreakPrompts, selfGrantPermissions; authorization gate bypasses PermissionManager.authorizeToolCall() when flags are set; `NFR-SEC-016` (bypass audit trail) ensures full traceability; validation `SEC-PERM-067`, `SEC-PERM-068` (Planned).
- `NFR-SEC-016` → `ToolExecutedEvent` and `permission_audit_log` record every bypass-flagged call with `PolicySource=BYPASS` and `FinalPermissionOutcome=ALLOWED_BY_POLICY_BYPASS`; validation `SEC-AUDIT-008` (Planned).

## S10 — Project Introspection (Path C)
- `FR-CM-009` (project introspection) → `specs/CONTEXT_MANAGEMENT.md` §8: ProjectIntrospector, ProjectContext, 7 tools.
- `TOOL-410`..`416` (introspect_*) → `registry/TOOLS.md` (Category 28 — Project Introspection, INTRO prefix), `registry/TOOL_MATRIX.md`.
- `FEAT-035` (Project Introspection) → `registry/FEATURES.md`.
- Knowledge Graph phase Later→4 → `architecture/MEMORY_SYSTEM.md`.
- Tool categories 27→28, tools 343→350 → `architecture/TOOL_SYSTEM.md`, `registry/TOOLS.md`, `PROJECT_SPECIFICATION.md`, `docs/PRODUCT_VISION.md`, `README.md`, 

## S13 — Authorization and Execution Recovery Contract Synchronization
- `FR-S016` → `security/PermissionModel.md` complete multi-scope permission resolution, category-level low-risk `ALLOW` defaults, high-risk `ASK`/`DENY` and approval gates, denial, and audit authorization; validation `SEC-PERM-003..066`, `IT-TOOL-002..014`, `UT-AS-005` (Planned).
- `FR-TL015` → Permission Audit Schema + Tool Protocol/API correlation; validation `SEC-PERM-023/044/045/052/062..065`, `IT-TOOL-008/009/014` (Planned).
- `FR-TL001`..`015` → `architecture/TOOL_SYSTEM.md`, `models/Tool.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md`, `errors/ERROR_CODES.md`; validation `IT-TOOL-001..014` (Planned).
- `FR-AS-007` → same-ID `RESUME`, new-ID `RETRY_AFTER_TERMINAL`, `priorExecutionId`, and reconciliation in Runtime/Background/Autonomy/Execution Protocol/Runtime API; validation `SEC-LC-EXEC-002..004`, `IT-LC-001..013/016..020` (Planned).
- `NFR-REL-001`/`002`/`012` → durable checkpoint, resume fidelity, and exactly-once lineage/replay rules; validation `IT-LC-001..013/016..020` (Planned).
- No S13 case is `VERIFIED`; all evidence paths are placeholders for `Planned` execution.

## S13A — DEC-47 Network, Browser, and Guest-Package Policy
- `FR-S014` → `security/SandboxPolicy.md` and `docs/SANDBOX_DEPTH.md`: host-mediated, mode-conditioned network admission; `AUTOPILOT` public destinations may default `network:http`/`network:websocket` to `ALLOW`, `ASSISTED` retains opt-in, direct sockets/inbound listeners and loopback/app-private endpoints remain blocked, and all egress is audited.
- `NFR-SEC-013` → `security/SandboxPolicy.md` and `docs/SANDBOX_DEPTH.md`: configured credentials, API keys, and `SecureKeyStore` contents are blocked from unauthorized endpoints; general full-body policy scanning is not required; proxy bypass remains fail-closed.
- Browser navigation/read-only extraction are permitted under existing untrusted-content and sandbox boundaries; credential entry and transaction execution on sensitive domains remain denied and audited through existing PermissionModel/Tool authorization.
- Guest package managers may install from reachable registries without pre-approval, subject to existing network mediation, audit, process/storage/rootfs/quarantine/resource quotas; host-JVM Plugins remain under their existing review and lifecycle contracts.
- Validation: `SEC-NET-001`, `SEC-SBX-001`, `SEC-PERM-041`, and `E2E-ESC-007` (all Planned; no implementation or executed evidence claimed).

## S14 — Typed Inference, Deep Reasoning, and Context Snapshots
- `FR-P014`..`019` → Provider System + ProviderStreamLifecycle + Provider Protocol/API/SDK; validation `UT-STREAM-001..004`, `UT-ROUTE-001`, `IT-STREAM-001..008`, `E2E-STREAM-001..003` (Planned).
- `FR-RN-009`..`012` → Context Management + Agent Runtime + Inference model; technical ReasoningPolicy ceilings and the DEC-25 no-credit-gating rule are projected through the model/spec chain; validation `UT-REASON-001..003`, `IT-REASON-001..004`, `E2E-REASON-001..002` (Planned).
- `FR-CM-010`..`012` → Context Management + Memory System + ContextSnapshot; validation `UT-CONTEXT-001..002`, `IT-CONTEXT-001..002`, `E2E-CONTEXT-001` (Planned).
- `NFR-PERF-011`/`012` → Performance Budget; validation `PERF-STREAM-003/004` (Planned).
- `NFR-REL-014`/`015` → ProviderStreamLifecycle + Provider Protocol; validation `UT-STREAM-001..004`, `IT-STREAM-004..007`, `RT-STREAM-001..002` (Planned).
- `NFR-SEC-015` → Security Model + ReasoningSummary privacy; validation `SEC-STREAM-005/006`, `E2E-REASON-002` (Planned).
- All S14 validation remains `Planned`; no implementation evidence is claimed.

## S15 — Agent Reliability Hardening
- `NFR-REL-016` → Agent Runtime hierarchical deadline propagation across provider, Tool, repair, verifier, delegation, cancellation, and checkpoint operations; validation `UT-CONTRACT-006` (Planned).
- `NFR-REL-017` → Tool System and Tool Protocol operation-level unknown-completion reconciliation; validation `UT-TOOL-006`, `E2E-REL-006` (Planned).
- `NFR-REL-018` → Background Execution and Android lifecycle fault-injection evidence; validation `E2E-REL-001..005` (Planned).
- `NFR-CI-003` → Context Management claim-to-evidence binding; validation `UT-EV-007`, `E2E-REL-009` (Planned).
- `NFR-CI-004` → Agent Runtime acceptance-criteria progress vector, checkpoint/initial baseline, same-logical-execution ProgressSignal deltas, relevant-evidence gating, plan/acceptance boundary, and anti-treadmill semantics; validation `UT-AS-010`, `E2E-REL-007` (Planned).
- `NFR-CI-005` → Context Management and Agent Runtime non-overridable reasoning and execution ceilings; validation `UT-RN-013` (Planned).
- `NFR-CI-006` → Agent Runtime, Provider System, and Context Management minimum-sufficient execution-mode selection; validation `UT-REASON-001`, `E2E-RN-001` (Planned).
- `NFR-CI-007` → Agent Runtime bounded-progress controls, retry/step/time limits, anti-treadmill behavior, and escalation; validation `UT-AS-010` (Planned).
- All S15 validation remains `Planned`; no runtime implementation, executed test, or empirical reliability result is claimed.
