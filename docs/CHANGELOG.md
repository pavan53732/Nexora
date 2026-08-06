# Changelog — Nexora

All notable changes to the Nexora project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Reasoning effort control (S6) — 6-level reasoning effort scale replacing the 3-level classification: `OFF` (reasoning disabled — deliberation gate bypassed, reasoning params omitted from provider requests, REASONING models never selected, RG/EV evidence gates remain active) / `LOW` / `MEDIUM` (default) / `HIGH` / `X_HIGH` / `MAX`; override hierarchy task → agent → workspace → global → default, mirroring PermissionModel layering; Settings → Model Config → Reasoning surface with effective-level indicator (no chat-embedded toggle, ADR-0006). Amended: `specs/CONTEXT_MANAGEMENT.md` §6 (+Reasoning Effort Scale), `requirements/FR.md` (FR-RN-003/004 amended; FR-RN-007/008 added), `architecture/PROVIDER_SYSTEM.md` (`ReasoningEffort` enum, `CompletionRequest.reasoningEffort` nullable — OFF = omitted, per-model mapping owned by adapters), `docs/TRACEABILITY.md` (+FR-RN-007 row), `docs/REQUIREMENT_COVERAGE_LEDGER.md` (+FR-RN-007/008 MAPPED), `docs/FR_NFR_MAPPING.md` (+S6), `docs/DECISION_LOG.md` (DL-031).
- Multi-Instance Pipes (S5) — new canonical capability closing the instance-to-instance collaboration gap: `specs/PIPES.md` (zero-config same-machine + LAN discovery via rendezvous directory + mDNS, Ed25519 pairing with QR/6-word confirmation, mTLS pipe transport with closed payload set, cross-instance SA-1..SA-5 delegation with per-pipe acceptance modes, heartbeat/reconnect discipline, broadcast routing, deny-by-default security gates, Settings → Pipes surface per ADR-0006); new canonical `state-machines/InstanceLifecycle.md` (Unpaired/Paired/Connected/Degraded/Disconnected/Revoked); new derived `models/Instance.md` (RemoteInstance + Pipe); `FR-MI-001..010`; `NFR-SEC-014` (pipe channel security); tools `TOOL-405..408` (pipe_list/pipe_connect/pipe_broadcast/pipe_delegate — catalog now 343 tools); `FEAT-034`; `instance:pair`/`instance:connect`/`instance:broadcast` scopes in `security/PermissionModel.md`; `architecture/MULTI_AGENT_SYSTEM.md` §Cross-Instance Extension (+ stale "15-agent registry" → 16 fixed); governance synchronized: `docs/CANONICAL_SOURCES.md` (+2 rows; malformed S3-E table rows repaired), `docs/TRACEABILITY.md` (+FR-MI-005 row), `docs/REQUIREMENT_COVERAGE_LEDGER.md` (+FR-MI-001..010, +NFR-SEC-014 — all MAPPED), `docs/FR_NFR_MAPPING.md` (+S5 section), `docs/DECISION_LOG.md` (DL-030). Registry count drift fixed in the same pass: `registry/TOOLS.md` header 339 → 343 (correct sum), `registry/FEATURES.md` FEAT-014 "(26 categories, 333 tools)" → "(27 categories, 343 tools)"; tool total now consistent across TOOLS.md, TOOL_SYSTEM.md, FEATURES.md. Pre-existing ID collision resolved: `TOOL-397` was double-assigned (`memory_lessons` from the context-management commit AND `mcp_connect_stdio` from S2's "preserved 397-402" range); `memory_lessons` renumbered to `TOOL-409` in `registry/TOOLS.md` + referencing spec `specs/AUTONOMY_STABILITY.md` §4 (MCP keeps `397..402` — that range is cited across TOOL_SYSTEM.md, Tool-Protocol.md, CANONICAL_SOURCES.md, ROADMAP.md, DECISION_LOG.md DL-020/026).
- ENVIRONMENT_SETUP.md — complete Linux development environment documentation: installed software & versions, SDK/Java/Python locations, environment variables, PATH configuration, verification results, Android library compatibility (Step 3), AI provider readiness (Step 4), embedded runtime research (Step 5), issues & resolutions, recommendations.
- ADR-0006 — Agent-First Interaction Model: the sandbox, internal terminal, runtimes, and execution engine are internal implementation details; users interact with AI agents through chat.
- FR-U011 — Chat as the single primary interaction surface (goal entry, streaming, tool-call cards, permission prompts, results).
- FEAT-013 — Agent-First Chat Interaction feature registry entry.
- PRODUCT_PRINCIPLES.md — 15 codified product principles (PP-001–015): autonomous agents, provider-agnostic, tool-based execution, persistent memory, agent-driven execution, plugin/skill system, background execution, multi-agent orchestration, dashboard & session management, sandboxed execution, checkpoint & resume, observability, token/cost control, offline-capable, onboarding — plus guardrails and a principle→documentation map.
- Full tool catalog — registry/TOOLS.md expanded from 69 to **316 tools** across all 25 categories (stable TOOL-IDs, descriptions, phases); registry/TOOL_MATRIX.md regenerated to cover every registered tool (legacy capability values preserved, legacy tool names reconciled, e.g. shell_execute→terminal_run, db_query→sqlite_query); generator script scripts/generate_tool_catalog.py; FEAT-014 added.
- Plugin registry — registry/PLUGINS.md expanded: per-plugin registration, install source (bundled vs marketplace), user operations ↔ lifecycle mapping (install/enable/disable/update/remove), and PLG-018 AI Providers plugin added.
- AI provider profiles — new user-facing configuration model: named, switchable profiles per provider (API key, endpoint, model, streaming, params), one default per workspace. Added ProviderProfile model (models/Provider.md), Provider Profiles spec (specs/AI_PROVIDERS.md), architecture note (PROVIDER_SYSTEM.md), FR-P011/FR-P012, and enriched registry/PROVIDERS.md (protocol, default endpoint, auth, streaming).
- Provider isolation — first-class security boundary: architecture/SECURITY_MODEL.md Provider Isolation section (credential, config, data-flow, code, network, crash isolation, auditability) + measures-table row; threat model TM-026..TM-028 (cross-provider data leak, cross-provider key access, provider exfiltration); NFR-SEC-011 (provider isolation) + NFR-SEC-012 (provider network confinement); FR-P013. Threat summary updated (28 total).
- Background execution spec — new specs/BACKGROUND_EXECUTION.md codifying task queue (priority ordering), scheduled jobs (WorkManager, constraints, dedupe), resumable execution, notifications (running/progress/completed/failed/approval), progress updates, checkpoint recovery, and Android platform rules (foreground service types API 34+, dataSync 6-hour cap API 35+, Doze). New FR-T011 (scheduled execution), FR-T012 (priority queue ordering), FR-T013 (global background control); NFR-REL-009 (Android background compliance); FEAT-015 (scheduled jobs), FEAT-016 (rich background notifications); linked from PROJECT_SPECIFICATION.md, README.md, RUNTIME.md.
- Memory system depth — FR-M011 (tool history), FR-M012 (file history), FR-M013 (user preferences), FR-M014/FR-M015 (knowledge graph extraction + query); Memory Protocol extended with Tool History, File History, User Preferences, and Knowledge Graph operation sets plus backing-stores table; File versioning mechanism in specs/FILE_SYSTEM.md (capture, storage, diff, revert, quota, retention); architecture/MEMORY_SYSTEM.md gains Memory Backing Stores + Knowledge Graph sections and phase mapping; new tools TOOL-381..TOOL-386 (file_history, file_restore, memory_tool_history, memory_preferences, memory_graph_query, memory_graph_build) — catalog now 322 tools with unchanged existing IDs; FEAT-017/018/019.
- Sandbox depth & autonomy roadmap — new docs/SANDBOX_DEPTH.md with 3 tiers (core depth Phase 3: telemetry, lifecycle autonomy + templates, snapshots & rollback, egress policy + DLP, quarantine & scanning, encryption at rest; autonomy depth Phases 4–6: adaptive approval modes, per-agent sandboxes, prompt-injection containment, resource economy, checkpoint integrity; advanced Phase 7–8: WASM micro-sandboxes, isolatedProcess, template marketplace, offline autonomy, export governance). New FR-S011..FR-S018; NFR-SEC-013 (egress DLP), NFR-REL-010 (snapshot fidelity); FEAT-020..026; tools TOOL-387..TOOL-393 (sandbox_info/reset/snapshot/restore/templates/network_rules/quarantine_review) — catalog now 329 tools with explicit phases; linked from PROJECT_SPECIFICATION.md, SANDBOX.md, ROADMAP.md, backlog/V1.md. ENVIRONMENT_SETUP.md: Node.js 20.20.2 + SQLite 3.50.6 documented as present in the dev image.
- Runtime naming alignment — architecture/RUNTIME.md "Security Policies" renamed to **Security Manager** (module `com.nexora.app.runtime.security`); docs/MODULE_BOUNDARIES.md security module re-scoped to security services (SecureKeyStore, AuditLogger, PermissionPolicyStore, secure storage — no longer claims PermissionManager) and a clarifying note added distinguishing `PermissionManager` (runtime per-call enforcement, `com.nexora.app.runtime.permissions`) from the `security` module (encryption, audit, policy persistence — never gates tool execution).
- Web search & extraction requirements — FR-WS-001..005 (web search via configured provider, page extraction with text/markdown/structured/screenshot modes, provider configuration, quarantine-gated content safety per FR-S015); FEAT-030.
- Sub-agent autonomous completion — amended existing architecture/MULTI_AGENT_SYSTEM.md with SA-1..SA-5 (autonomous completion contract: delegate → spawn → execute → verify → report, interruptions limited to approval gates/budget escalation/heartbeat failure; complete handoff context so sub-agents never interrupt for basics; parallel orchestration with per-workspace concurrency limit, per-file write locks, sandbox budget splitting, dependency-order merging; explicit inheritance of zero-assumption/grounding/reasoning/EV policies; plan-vs-actual sub-agent reporting with Reviewer pass for important subtasks); requirements/FR.md FR-MA-001..005; testing/UnitTests.md 6 multi-agent unit tests; testing/E2ETests.md 5 multi-agent journeys (full autonomous delegation, parallel file conflict, incomplete handoff blocked, ambiguity resolved once, important-subtask reviewer pass). No new files.
- Evidence & Validation Engine (adopting the ChatGPT-proposed pattern) — amended existing architecture/RUNTIME.md (+17th module com.nexora.app.runtime.evidence: evidence collection, source attribution, statement classification, confidence scoring, assumption detection, plan validation, output verification, self-review, completion validation, audit logging); docs/MODULE_BOUNDARIES.md runtime row (EvidenceEngine, Statement, Confidence); specs/CONTEXT_MANAGEMENT.md §11 EV-1..EV-6 (5-way statement classification VERIFIED/DERIVED/ESTIMATED/UNKNOWN/USER_PROVIDED as structured metadata, structured HIGH/MEDIUM/LOW confidence driving autonomy behavior, zero-assumption mode, consolidated 7 guardrails, fact-vs-recommendation labeling, completion validation + mandatory reviewer handoff for important tasks); architecture/MULTI_AGENT_SYSTEM.md mandatory review rule (Coder → Tester → Reviewer → User); requirements/FR.md FR-EV-001..006; testing/UnitTests.md 6 evidence unit tests; testing/E2ETests.md 5 evidence journeys. No new files.
- Reasoning before answering — amended existing specs/CONTEXT_MANAGEMENT.md with §10 RB-1..RB-6 (deliberation gate answer-now/reasoning-pass/clarify-first, reasoning pipeline retrieve-first, effort levels fast/balanced/thorough, reasoning-capable model routing via new ProviderCapability.REASONING, collapsible reasoning trace in the activity feed, answer-quality gates + meta-cognition + self-consistency); architecture/PROVIDER_SYSTEM.md + docs/api/Provider-API.md ProviderCapability enum REASONING; models/Skill.md + specs/AI_PROVIDERS.md reasoning notes; architecture/AGENT_RUNTIME.md deliberate-then-answer / reasoning-routing / answer-quality-gates capabilities; requirements/FR.md FR-RN-001..006; testing/UnitTests.md 6 reasoning unit tests; testing/E2ETests.md 5 reasoning journeys (ambiguous clarifies, complex reasons visibly, thorough uses reasoning model, contradictory premise flagged, fast stays fast). No new files.
- Response grounding & attribution (anti-hallucination in chat & coding) — amended existing specs/CONTEXT_MANAGEMENT.md with §9 RG-1..RG-6 (tool-before-claim, citations & sources, uncertainty disclosure, refuse-unsupported, code-claim grounding via code-intelligence tools, plan-vs-actual honesty) + enforcement/observability (grounding_missing_source log, trust-score decrement); requirements/FR.md FR-GND-001..006; architecture/AGENT_RUNTIME.md grounded-responses + code-claim verification capabilities; testing/UnitTests.md 5 grounding unit tests; testing/E2ETests.md 5 grounding journeys (non-existent API, cited fact, out-of-context, unsupported capability, plan-vs-actual mismatch). No new files.
- Git grounding rules (anti-hallucination) — amended existing specs/GIT.md with GR-1..GR-6 (structured results + repo snapshot, read-before-write gate, path grounding, SHA grounding, verify-after-write, repo content as untrusted data); requirements/FR.md FR-GT-001..006; testing/UnitTests.md 6 grounding unit tests; testing/E2ETests.md 5 hallucination journeys (non-existent file, fabricated SHA, dirty-tree merge, malicious README, stale repo). No new files.
- Context management spec — new specs/CONTEXT_MANAGEMENT.md: context-as-pipeline (structured state never compressed · working set · progressive summaries · retrieval layer); token budget allocation (priority order, truncation only after summarization); progressive summarization (thresholds, summary-of-summaries, fidelity check); resume reconstruction (checkpoint + summary + retrieval, never raw replay); freshness checks; context tagging & trust (untrusted isolation); milestone memory curation; observability. FR-CM-001..008; NFR-REL-011 (context resume fidelity); FEAT-031; tools TOOL-396 context_stats (OBS), TOOL-397 memory_lessons (MEM) — catalog now 333 tools; linked from PROJECT_SPECIFICATION v4.5.0 and README.
- Autonomy & stability spec — new specs/AUTONOMY_STABILITY.md Part A (plan repair with bounded repair cycles, agent heartbeat & watchdog with checkpoint restart, budget escalation never silent-stop, closed-loop learning via memory_lessons, trust growth adjusting autonomy modes, verification gates as hard gates) and Part B (idempotency & exactly-once recovery with replay log, degradation ladder provider→local→offline→read-only, timeout discipline, fault-injection testing). FR-AS-001..009; NFR-REL-012 (exactly-once recovery), NFR-REL-013 (degradation continuity); FEAT-032/033; E2E resilience journeys added (kill on non-idempotent call, network loss, provider storm, disk-full, double restart, summarization churn).
- Skills as first-class capability (ADR-0007) + complete execution lifecycle — new ADR-0007 (Agent=WHO, Skill=WHAT, Tool=HOW; skill registry; agents acquire skills); models/Skill.md (Skill, AgentSkillBinding, SkillRegistry); registry/SKILLS.md (24 built-in skills, SKL-001..024); specs/EXECUTION_LIFECYCLE.md (24-stage generic lifecycle + software-engineering pipeline with pass gates and bounded auto-fix loop); requirements FR-EL-001..013 (goal analysis, task decomposition, agent/skill/tool/model/plugin selection, ordering & parallelism, validation criteria, error recovery, reflection, E2E verification, completion reporting, SE pipeline) and FR-SK-001..005 (skill registry, acquisition, tool mapping, skill-aware planning, discovery); AGENT_RUNTIME.md capabilities (agent/skill selection, validation criteria, objective verification, follow-up); RUNTIME.md Skill Registry module (16 modules); MODULE_BOUNDARIES runtime row (Skill, SkillRegistry); new tool category Skills (SKL, TOOL-394 skill_list, TOOL-395 skill_acquire) — catalog now 331 tools / 26 categories; FEAT-027..029; linked from PROJECT_SPECIFICATION.md (v4.4.0), README.md, PRODUCT_PRINCIPLES.md PP-006, AGENTS.md; TOOL_SYSTEM.md 26th category row.
- S1 concurrency cap (SA-3): dynamic `min(memory_budget/per_agent_est, cpu_cores, configurable_max)`; default 3, high-end 8–16; `FR-MA-003` mapped; `DECISION_LOG.md` DL-025 added; `FR_NFR_MAPPING.md` verified (0 placeholders).
- S2 MCP adapter contract canonical (`docs/CANONICAL_SOURCES.md` new row; `ROADMAP.md` Phase 5 note; `DECISION_LOG.md` DL-026; registry `397-402` preserved; no new FR/NFR needed — existing `FR-TL001..015` + `NFR-SEC-001` cover interop).
- G4–G5 documentation hardening (non-redesigning, spec-level only): architecture/TOOL_SYSTEM.md (§MCP Client — TOOL-397..402, `mcp_connect_stdio/http`, `mcp_list_caps/call_tool/read_resource/get_prompt`; §Real-Time Voice & Camera — `TOOL-AUD-101`, `TOOL-CAM-201`/`202`, streaming pipeline, consent, Phase Later); protocols/Tool-Protocol.md (§MCP Tool Invocation — `mcp://` adapter, `NXR-*` error mapping); registry/TOOLS.md (+Category 27 MCP — `TOOL-397`..`402`); registry/TOOL_MATRIX.md (MCP capability rows); specs/BACKGROUND_EXECUTION.md (§OEM Battery-Optimization & Auto-Start — `FR-AS-009` degradation ladder, `FR-T011` scheduling, `FR-S016` autonomy); security/PermissionModel.md (§Deny-by-Default + Optional TFLite Auto-Approval Classifier — `FR-S016` autonomy, `FR-EV-002` structured confidence, `FR-AS-006` verification gates, advisory-only downward blocking); security/SandboxPolicy.md (§Sensitive-App & High-Risk-Domain Blocked-List — `FR-W005`, `FR-S014`/`015`, `FR-T015` audit); specs/BROWSER.md (§BlockedListWarning); specs/AI_PROVIDERS.md (§Real-Time Voice & Camera — `FR-S028`, `FR-P009` token tracking, `FR-A010` real-time monitoring, `FR-W005`, `FR-S001` sandbox). Registry updated (`TOOL-397`..`402`); `DECISION_LOG.md` updated (`DL-020` MCP, `DL-021` OEM, `DL-022` Security, `DL-023` Blocked-List, `DL-024` Voice/Camera); `docs/research/NEXORA_VS_ZCODE_CAPABILITY_GAP.md` (816 lines) preserved; audit supplement (`NEXORA_VS_ZCODE_AUDIT_SUPPLEMENT.md`) deleted after consolidation; embedded runtime strategy (planned, never committed — see `docs/ENVIRONMENT_SETUP.md` §Step 5); no Android source (`android/` absent); no Kotlin/Java (`.kt`/`.java`: 0); commit `8e1e937` pushed (`docs(research): implement G4/G1/G2/G3/G5 hardening changes`).
- S3-E lifecycle state machines — 3 new canonical state-machine companions for Workspace, Memory, and TerminalSession under `state-machines/`: `WorkspaceLifecycle.md` (Created/Active/Suspended/Archived/Deleted), `MemoryLifecycle.md` (Recorded/Indexed/Retrieved/Retained/Expired/Deleted), `TerminalSessionLifecycle.md` (Created/Attached/Running/Detached/Closed/Failed). Lifecycle stubs (`lifecycle/*.md`) reclassified as DERIVED with governance headers pointing to canonical state machines. All cross-references synchronized: `docs/CANONICAL_SOURCES.md` (3 new rows), `ARCHITECTURE.md` (links updated), `MODULE_BOUNDARIES.md` (3 new state machines in runtime), `LIFECYCLES.md` (references), `models/Workspace.md`, `models/Memory.md`, `models/TerminalSession.md` (links added). `DL-029` added; `DL-027` retained as narrative fill.

### Changed
- PROJECT_SPECIFICATION.md → v4.3.0: agent-first interaction quick reference, ADR-0006 index entry, locked interaction rule, Phase 1 deliverable, Product Principles index entry (v4.2 → v4.3).
- README.md, docs/PRODUCT_VISION.md — agent-first positioning (infrastructure reframed as internal) and Product Principles linked from documentation index and vision doc header.
- docs/ARCHITECTURE.md — Terminal screen replaced by Agent Activity Feed; bottom nav is Workspace, Tasks, Settings; workspace tabs drop Terminal.
- docs/ROADMAP.md, backlog/MVP.md, backlog/V1.md — terminal/sandbox UI removed from Phase 1/MVP; Phase 3 sandbox marked internal.
- requirements/FR.md — FR-U001 (3-tab bottom nav), FR-U005 (agent activity feed), Terminal section reframed as internal/agent-invoked.
- specs/TERMINAL.md — reframed as internal agent-invoked component; no user-facing UI.
- ui/Navigation.md, ui/Components.md, ui/Icons.md — no terminal tab; ActivityCard component; terminal icon reused for activity cards.
- docs/DECISION_LOG.md — DL-019 records the decision (amends DL-018).
- docs/adr/ADR-0001-Workspace-First.md — amendment note referencing ADR-0006.
- registry/FEATURES.md — FEAT-002/FEAT-003 marked internal; FEAT-013 added.
- docs/ENVIRONMENT_SETUP.md — terminal research note aligned with ADR-0006.


---

## [0.3.0] — 2026-08-03

### Added

#### Engineering Architecture (docs/)
- DEPENDENCY_GRAPH.md — Module dependency hierarchy, 14-module allowed/forbidden matrix, Hilt binding rule.
- MODULE_BOUNDARIES.md — Per-module responsibilities, public API surfaces, allowed/forbidden dependencies.
- LIFECYCLES.md — Complete lifecycle flows for 7 entities (Workspace, Agent, Tool, Plugin, Provider, Runtime, Background Execution).
- PERFORMANCE_BUDGET.md — 27 measurable performance targets with warning/critical thresholds and CI enforcement.

#### Project Specification
- PROJECT_SPECIFICATION.md → v4.1.0 (frozen), locked architectural rule added.

---

## [0.2.0] — 2026-08-03

### Added

#### Requirements Layer (requirements/)
- FR.md — 95 functional requirements across 10 system areas (FR-W001 through FR-TE005).
- NFR.md — 40 non-functional requirements with measurable targets (NFR-PERF through NFR-PORT).
- CONSTRAINTS.md — 13 design and implementation constraints.
- ASSUMPTIONS.md — 20 project assumptions across 6 categories.
- DEPENDENCIES.md — 26 external dependencies with versions.
- RISKS.md — 12-item risk register with probability, impact, and mitigation.

#### State Machines (state-machines/)
- AgentLifecycle.md — 11-state agent lifecycle with Mermaid diagram.
- TaskLifecycle.md — 10-state task lifecycle with dependency blocking.
- WorkflowLifecycle.md — 10-state workflow lifecycle with DAG sub-states.
- PluginLifecycle.md — 14-state plugin lifecycle from discovery to uninstall.
- ProviderLifecycle.md — 8-state provider lifecycle with auto-degradation.

#### Security (security/)
- ThreatModel.md — STRIDE-based threat model with 25 threats (TM-001 through TM-025).
- PermissionModel.md — Detailed permission model with 14 scopes, hierarchy, and audit trail.
- SandboxPolicy.md — Sandbox security policy with enforcement and violation response.

#### Error Catalog (errors/)
- ERROR_CODES.md — 64 error codes across 9 subsystems (NXR-1xxx through NXR-9xxx).

#### Sequence Diagrams (diagrams/)
- Agent-Execution-Flow.md — Full agent loop sequence diagram.
- Tool-Execution-Flow.md — Permission-gated tool execution flow.
- Plugin-Lifecycle-Flow.md — Plugin install/verify/activate flow.
- Provider-Streaming-Flow.md — SSE streaming with token budget enforcement.
- Memory-Store-Flow.md — Multi-tier memory store and recall flow.

#### Testing Strategy (testing/)
- UnitTests.md — Unit testing strategy (JUnit 5, MockK, 85% target).
- IntegrationTests.md — Module interaction testing strategy.
- E2ETests.md — End-to-end user journey testing.
- PerformanceTests.md — Benchmark strategy with baselines.
- SecurityTests.md — OWASP Mobile Top 10 and penetration test scenarios.
- RegressionTests.md — Regression and migration testing strategy.

#### Capability Matrices (registry/)
- TOOL_MATRIX.md — 36-tool capability matrix (read, write, network, Android, etc.).
- AGENT_MATRIX.md — 15-agent capability matrix (plan, execute, code, browser, etc.).

#### Decision Log (docs/)
- DECISION_LOG.md — 18 engineering decisions (DL-001 through DL-018).

#### Versioning
- VERSIONING.md — Semantic versioning strategy for app, docs, schemas, plugins, providers.

#### Project Specification
- PROJECT_SPECIFICATION.md updated to v4.0.0 with cross-links to all new documents.

---

## [0.1.0] — 2026-08-03

### Added

#### Repository Structure
- 17 top-level directories (.github, docs, architecture, design, specs, roadmap, android, runtime, plugins, tools, agents, memory, sandbox, provider, testing, scripts, assets, examples).
- Workspace-first architectural decision (Workspace is the primary entity, not chat).

#### Documentation (docs/)
- PRODUCT_VISION.md — Product vision, positioning, philosophy, brand identity.
- ARCHITECTURE.md — High-level system architecture, UI layer, workspace-first design.
- SYSTEM_DESIGN.md — Execution flow, agent loop, workspace model, observability.
- ROADMAP.md — 8-phase development roadmap with success metrics.
- CHANGELOG.md — This file.

#### Architecture Deep Dives (architecture/)
- RUNTIME.md — Core runtime: 15 modules, execution flow, event bus, checkpoints.
- AGENT_RUNTIME.md — Agent loop, state management, token budgeting.
- SANDBOX.md — Virtual file system, process isolation, storage layout, resource limits.
- TOOL_SYSTEM.md — Tool interface, 25 categories, registration, execution flow.
- MEMORY_SYSTEM.md — Memory tiers, semantic search, embeddings, vector DB.
- WORKFLOW_ENGINE.md — Workflow types (linear, parallel, branching), DAG execution.
- PLUGIN_SYSTEM.md — Plugin interface, lifecycle, marketplace.
- SECURITY_MODEL.md — Sandboxed execution, permission scopes, API key encryption.
- PROVIDER_SYSTEM.md — AI provider abstraction, 9 providers, request/response models.
- MULTI_AGENT_SYSTEM.md — 15 agent roles, shared context, communication flow.

#### Component Specifications (specs/)
- FILE_SYSTEM.md — Virtual file system operations and storage paths.
- TERMINAL.md — Embedded terminal, supported commands, multi-session.
- GIT.md — Git integration, 13 supported operations.
- BROWSER.md — Browser automation capabilities.
- DATABASE.md — SQLite usage for sandbox and memory.
- AI_PROVIDERS.md — Detailed per-provider specification.
- WORKSPACE.md — Workspace model, hierarchy, operations, configuration.

#### Repository Standards
- README.md — Project overview, features, tech stack, documentation links.
- LICENSE — Apache License 2.0.
- CONTRIBUTING.md — Contribution guidelines.
- CODE_OF_CONDUCT.md — Community code of conduct.
- SECURITY.md — Security policy and vulnerability reporting.
- PROJECT_SPECIFICATION.md — Master index (v2.0.0, rewritten as document index).

[Unreleased]: https://github.com/pavan53732/Nexora/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/pavan53732/Nexora/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/pavan53732/Nexora/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/pavan53732/Nexora/releases/tag/v0.1.0

- Cross-reference polish (from external audit validation — findings verified by reading full files, not grep) — amended existing docs only: diagrams/Agent-Execution-Flow.md now carries a Guard-conditions note referencing AgentLifecycle.md guards (terminal states, start()/retry() guards); docs/ARCHITECTURE.md header now links ADR-0003 + ADR-0006 and the Sandbox Runtime block references docs/SANDBOX_DEPTH.md (FR-S011..S018); sdk/AgentSDK.md, PluginSDK.md, ProviderSDK.md, ToolSDK.md each gained a Testing reference to testing/UnitTests.md + IntegrationTests.md (+E2ETests for agents).
- Gemini + LLM Arena audit fixes — 13 verified findings, amended existing docs only:
  DEPENDENCY_GRAPH.md allowed/forbidden table fully aligned to MODULE_BOUNDARIES.md (ui allows only application+shared; application allows all; services allows runtime+storage+security+shared; runtime now forbids sandbox and allows security; etc.); docs/api/Tool-API.md ToolCategory enum + SKILLS (26th category); registry/SKILLS.md SKL-009 db_* reference removed (tools are sqlite_* only); MODULE_BOUNDARIES.md runtime row public API completed (PermissionManager, Scheduler, Observability, SecurityManager, BackgroundRuntime, ResourceManager, AgentManager); models/Plugin.md permissions → requiredPermissions + added minAppVersion (matches Plugin-API/PLUGIN_SYSTEM); README.md phase table (15 → 16 types) + repo-structure specs count (7 → 11 documents); requirements/FR.md FR-TL008 25+ → 26 categories; docs/api/Plugin-API, Provider-API, Runtime-API, Tool-API dangling ../architecture/ links fixed to ../../architecture/; PRODUCT_VISION.md Core Platform Modules 15+ → 17+; ARCHITECTURE.md runtime diagram marked simplified (17 modules per RUNTIME.md). Rejected: PERFORMANCE_BUDGET "27 vs 29" (the header never contained a count; 27 appears only in historical CHANGELOG — file's 29 target rows verified, no fix needed). audit/ snapshot regenerated to stay byte-identical.
- DeepSeek audit (Part 3) fixes — verified findings, amended existing docs only: docs/api/Agent-API.md AgentType enum was missing ARCHITECT and CUSTOM (only 15 of 16+1 types) — added both with comments; Agent-API.md referenced AgentContext without defining it — added the data class; Agent-API.md link to ../architecture/AGENT_RUNTIME.md was dangling (should be ../../architecture/) — fixed; models/Agent.md AgentType enum now comments that CUSTOM is user-defined, not a built-in type (16 built-ins). Rejected as false/stale: AGENT_MATRIX '15 agent types' (already 16), PLUGINS.md missing PLG-018 (present in table), and all 'wrong link paths' claims for Plugin-API/Provider-API/Tool-API/PluginSDK/ProviderSDK/ToolSDK/AgentSDK (paths resolve correctly in the real repo — DeepSeek audited the flat zip where links appear wrong).
- DeepSeek audit (Part 2) fixes — verified findings, amended existing docs only: added Architect row to MULTI_AGENT_SYSTEM.md Built-in Agent Roles table + clarified CUSTOM enum comment; updated all stale "15 agent" references to 16 (README, PROJECT_SPECIFICATION phase table, backlog/Future, ROADMAP, FR-A005 → "16 agent roles (…architect…)", EXECUTION_LIFECYCLE, AGENT_MATRIX via generator source); PROJECT_SPECIFICATION Scale line "15+ modules, 25+ tool categories" → "17+ modules, 26 tool categories"; ADR-0001 index row now "(amended by ADR-0006)"; DECISION_LOG DL-018 marked ⚠ superseded by DL-019; TERMINAL.md terminal tools now cite TOOL-020..023 + registry link. Rejected as false: AUTONOMY_STABILITY missing from Component Specifications (present), SANDBOX_DEPTH undiscoverable (present in Architecture Deep Dives), ENVIRONMENT_SETUP version mismatch (none).
- DeepSeek audit (Part 1) fixes — verified findings from external audit, amended existing docs only: ADR-0001-Workspace-First.md now carries visible ⚠ superseded-by-ADR-0006 markers on the Terminal tree child, bottom-nav bullet, and workspace-tabs bullet (original ADR text preserved per immutability, override unmistakable); README.md + PRODUCT_VISION.md "25+ tool categories" → "26 categories" (5 spots total); PRODUCT_VISION.md Product Philosophy Design Principles section condensed to a pointer to PRODUCT_PRINCIPLES.md (PP-001..PP-015) to eliminate duplication. DeepSeek's other two claims were checked and rejected: SANDBOX_DEPTH.md IS linked in the master index (Architecture Deep Dives, line 92) and ENVIRONMENT_SETUP.md contains no stray spec-version reference (not found in file).
- Agent orchestration (adopting the ChatGPT-proposed orchestration layer) — amended existing registry/AGENTS.md (+AGT-016 Architect), models/Agent.md + architecture/MULTI_AGENT_SYSTEM.md AgentType enums (+ARCHITECT), AGENT_MATRIX.md regenerated (16 agents), architecture/MULTI_AGENT_SYSTEM.md (Workflow Coordinator framed as **Master Agent** — CEO/project-manager role that never implements; **no-direct-communication rule** for sub-agents; Agent Orchestrator composition table from existing modules), specs/CONTEXT_MANAGEMENT.md EV-6 (+documentation-updated completion gate); requirements/FR.md FR-AG-001..004; testing/UnitTests.md 5 orchestration unit tests; testing/E2ETests.md 5 orchestration journeys (master full delegation, architect-first, no direct calls, docs gate, conflict resolution). No new files.
- Documentation consistency audit — fixed 6 internal contradictions found across the docs: RUNTIME.md module-count claim 15 → 17 (Skill Registry + Evidence & Validation Engine); TOOL_SYSTEM.md category count 25 → 26 (header + catalog note, Skills category added earlier); MULTI_AGENT_SYSTEM.md AgentType enum missing CUSTOM (now matches models/Agent.md); docs/adr/README.md index missing ADR-0006/ADR-0007 (now lists all 7); README.md component-spec list missing Execution Lifecycle link (now 11 specs, matching PROJECT_SPECIFICATION); registry/FEATURES.md FEAT-014 stale "(25 categories, 316 tools)" → "(26 categories, 333 tools)". Verified no duplicate FR/FEAT IDs and no other stale tool counts.

