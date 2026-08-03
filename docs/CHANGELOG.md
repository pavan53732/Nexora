# Changelog — Nexora

All notable changes to the Nexora project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- (nothing yet)

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

[Unreleased]: https://github.com/pavan53732/Nexora/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/pavan53732/Nexora/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/pavan53732/Nexora/releases/tag/v0.1.0
