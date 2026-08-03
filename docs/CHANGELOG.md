# Changelog — Nexora

All notable changes to the Nexora project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- (nothing yet)

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

[Unreleased]: https://github.com/pavan53732/Nexora/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/pavan53732/Nexora/releases/tag/v0.1.0
