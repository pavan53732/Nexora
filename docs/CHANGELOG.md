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
