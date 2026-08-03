# Changelog — Nexora

All notable changes to the Nexora project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
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
- Response grounding & attribution (anti-hallucination in chat & coding) — amended existing specs/CONTEXT_MANAGEMENT.md with §9 RG-1..RG-6 (tool-before-claim, citations & sources, uncertainty disclosure, refuse-unsupported, code-claim grounding via code-intelligence tools, plan-vs-actual honesty) + enforcement/observability (grounding_missing_source log, trust-score decrement); requirements/FR.md FR-GND-001..006; architecture/AGENT_RUNTIME.md grounded-responses + code-claim verification capabilities; testing/UnitTests.md 5 grounding unit tests; testing/E2ETests.md 5 grounding journeys (non-existent API, cited fact, out-of-context, unsupported capability, plan-vs-actual mismatch). No new files.
- Git grounding rules (anti-hallucination) — amended existing specs/GIT.md with GR-1..GR-6 (structured results + repo snapshot, read-before-write gate, path grounding, SHA grounding, verify-after-write, repo content as untrusted data); requirements/FR.md FR-GT-001..006; testing/UnitTests.md 6 grounding unit tests; testing/E2ETests.md 5 hallucination journeys (non-existent file, fabricated SHA, dirty-tree merge, malicious README, stale repo). No new files.
- Context management spec — new specs/CONTEXT_MANAGEMENT.md: context-as-pipeline (structured state never compressed · working set · progressive summaries · retrieval layer); token budget allocation (priority order, truncation only after summarization); progressive summarization (thresholds, summary-of-summaries, fidelity check); resume reconstruction (checkpoint + summary + retrieval, never raw replay); freshness checks; context tagging & trust (untrusted isolation); milestone memory curation; observability. FR-CM-001..008; NFR-REL-011 (context resume fidelity); FEAT-031; tools TOOL-396 context_stats (OBS), TOOL-397 memory_lessons (MEM) — catalog now 333 tools; linked from PROJECT_SPECIFICATION v4.5.0 and README.
- Autonomy & stability spec — new specs/AUTONOMY_STABILITY.md Part A (plan repair with bounded repair cycles, agent heartbeat & watchdog with checkpoint restart, budget escalation never silent-stop, closed-loop learning via memory_lessons, trust growth adjusting autonomy modes, verification gates as hard gates) and Part B (idempotency & exactly-once recovery with replay log, degradation ladder provider→local→offline→read-only, timeout discipline, fault-injection testing). FR-AS-001..009; NFR-REL-012 (exactly-once recovery), NFR-REL-013 (degradation continuity); FEAT-032/033; E2E resilience journeys added (kill on non-idempotent call, network loss, provider storm, disk-full, double restart, summarization churn).
- Skills as first-class capability (ADR-0007) + complete execution lifecycle — new ADR-0007 (Agent=WHO, Skill=WHAT, Tool=HOW; skill registry; agents acquire skills); models/Skill.md (Skill, AgentSkillBinding, SkillRegistry); registry/SKILLS.md (24 built-in skills, SKL-001..024); specs/EXECUTION_LIFECYCLE.md (24-stage generic lifecycle + software-engineering pipeline with pass gates and bounded auto-fix loop); requirements FR-EL-001..013 (goal analysis, task decomposition, agent/skill/tool/model/plugin selection, ordering & parallelism, validation criteria, error recovery, reflection, E2E verification, completion reporting, SE pipeline) and FR-SK-001..005 (skill registry, acquisition, tool mapping, skill-aware planning, discovery); AGENT_RUNTIME.md capabilities (agent/skill selection, validation criteria, objective verification, follow-up); RUNTIME.md Skill Registry module (16 modules); MODULE_BOUNDARIES runtime row (Skill, SkillRegistry); new tool category Skills (SKL, TOOL-394 skill_list, TOOL-395 skill_acquire) — catalog now 331 tools / 26 categories; FEAT-027..029; linked from PROJECT_SPECIFICATION.md (v4.4.0), README.md, PRODUCT_PRINCIPLES.md PP-006, AGENTS.md; TOOL_SYSTEM.md 26th category row.

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
