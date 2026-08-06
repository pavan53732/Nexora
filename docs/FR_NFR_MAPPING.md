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
| `NFR-SEC-021` | `NFR-SEC-001` | Security (deny-by-default) | Security | `security/PermissionModel.md` (§Deny-by-Default) | `SEC-PERM-001` | `evidence/security/SEC-PERM-001/` | MAPPED |

---

## Verification Notes

- **No placeholder patterns remain** in edited docs (`architecture/TOOL_SYSTEM.md`, `protocols/Tool-Protocol.md`, `registry/TOOLS.md`, `registry/TOOL_MATRIX.md`, `specs/BACKGROUND_EXECUTION.md`, `security/PermissionModel.md`, `security/SandboxPolicy.md`, `specs/BROWSER.md`, `specs/AI_PROVIDERS.md`, `docs/DECISION_LOG.md`). Verified with regex search (`FR-[A-Z]{2}-[4-9][0-9]{2}` etc.) — `0` matches.
- All edited documents reference **actual** ledger IDs (`FR-S016`, `FR-AS-009`, `FR-T011`, `FR-W005`, `FR-P011`, `FR-S014`/`015`, `FR-T015`, `FR-EV-002`/`006`, `FR-S028`, `FR-P009`, `NFR-REL-002`/`003`).
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
- `FR-AS-003` (budget escalation) mapped to concurrency cap budget feed.
- `FR-S018` (sandbox isolation) mapped to per-sub-agent isolation under cap.
- `NFR-REL-003` (reliability) preserved — cap prevents overload-induced failures.

## S4 — Terminal Specification (Fully Specified)
- `FR-TE001`..`005` (terminal execution/lifecycle/tools) → `specs/TERMINAL.md` (§Execution Model, §Lifecycle, §Security).
- `FR-S002`/`003`/`018` (sandbox/process/workspace isolation) → `specs/TERMINAL.md` (§Security & Isolation) + `security/SandboxPolicy.md`.
- `FR-AS-002`/`003`/`009`/`013` (heartbeat/budget/degradation/recovery) → `specs/TERMINAL.md` (§Timeout Discipline, §Restore Behavior) + `specs/BACKGROUND_EXECUTION.md`.
- `FR-T015` (audit trail) → `specs/TERMINAL.md` (§Audit).
- `FR-EV-002`/`006` (evidence/reviewer) → `specs/TERMINAL.md` (§Evidence & Validation Engine reference).
- `FR-M012`/`013` (file version/user preferences) → `specs/TERMINAL.md` (§Restore Behavior — checkpoint storage + retention).
- `FR-A010` (real-time monitoring) → `specs/TERMINAL.md` (§Audit — budget/cap/timeout events).
- `FR-U005` (agent activity feed) → `specs/TERMINAL.md` (§Boundary Violation Response — denied actions surfaced).
- `FR-GT-001`..`006` (git grounding) preserved — terminal session does not affect git grounding rules.

## S5 — Multi-Instance Pipes
- `FR-MI-001`..`010` (discovery, transport, same-machine orchestration, pairing, cross-instance delegation, heartbeats, broadcast, security gates, failure handling, settings surface) → `specs/PIPES.md` (canonical) + `state-machines/InstanceLifecycle.md` (canonical states) + `models/Instance.md` (derived).
- `FR-AG-001`/`002` (coordinator role, no direct agent calls) → preserved across pipes via `architecture/MULTI_AGENT_SYSTEM.md` §Cross-Instance Extension.
- `FR-S016` (autonomy modes) → per-pipe acceptance mode (PIPES.md §6).
- `FR-S018` (per-agent sandbox) → remote sub-agent runs in the remote instance's own sandbox (PIPES.md §6).
- `FR-P011`/`FR-P013` (provider profiles, provider isolation) → credentials never cross pipes; remote execution uses remote profiles (PIPES.md §2 rule 2, §8).
- `FR-S014`/`FR-S015` (egress policy, quarantine) → pipe egress confinement + inbound artifact quarantine (PIPES.md §8).
- `FR-T015` (audit trail) → pipe events audited end-to-end (PIPES.md §2 rule 4).
- `FR-CM-006` (context trust tagging) → inbound payloads are untrusted segments (PIPES.md §8).
- `NFR-SEC-014` (pipe channel security) → `requirements/NFR.md`; validation `SEC-NET-001`.
- `NFR-REL-002`/`012` (resume fidelity, exactly-once) → mid-task pipe recovery (PIPES.md §6, §9).

## S6 — Reasoning Effort Scale
- `FR-RN-003` (effort levels) → amended to 6-level scale (OFF/LOW/MEDIUM/HIGH/X_HIGH/MAX) in `specs/CONTEXT_MANAGEMENT.md` §6.
- `FR-RN-004` (reasoning models) → amended: fail-fast at X_HIGH/MAX; graceful degradation at HIGH and below.
- `FR-RN-007` (reasoning disable OFF) → `specs/CONTEXT_MANAGEMENT.md` §6 (OFF semantics: gate bypass, params omitted, RG/EV gates unaffected).
- `FR-RN-008` (settings surface + override hierarchy) → `specs/CONTEXT_MANAGEMENT.md` §6 (task→agent→workspace→global→default MEDIUM; Settings → Model Config → Reasoning).
- Wire contract → `architecture/PROVIDER_SYSTEM.md` (`CompletionRequest.reasoningEffort: ReasoningEffort?`, OFF = null/omitted; per-model mapping owned by adapters).

## S10 — Project Introspection (Path C)
- `FR-CM-009` (project introspection) → `specs/CONTEXT_MANAGEMENT.md` §8: ProjectIntrospector, ProjectContext, 7 tools.
- `TOOL-410`..`416` (introspect_*) → `registry/TOOLS.md` (Category 28 — Project Introspection, INTRO prefix), `registry/TOOL_MATRIX.md`.
- `FEAT-035` (Project Introspection) → `registry/FEATURES.md`.
- Knowledge Graph phase Later→4 → `architecture/MEMORY_SYSTEM.md`.
- Tool categories 27→28, tools 343→350 → `architecture/TOOL_SYSTEM.md`, `registry/TOOLS.md`, `PROJECT_SPECIFICATION.md`, `docs/PRODUCT_VISION.md`, `README.md`, `docs/research/EMBEDDED_RUNTIME_STRATEGY.md`.
