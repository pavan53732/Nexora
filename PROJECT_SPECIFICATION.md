# PROJECT SPECIFICATION — NEXORA

---

| Field | Value |
|------|-------|
| **Project Name** | Nexora |
| **Package** | `com.nexora.app` |
| **Application target** | Android (native, Kotlin/Java + Gradle) |
| **Tagline** | Autonomous AI Agent App for Android |
| **Alt Taglines** | Think. Plan. Execute. / Your Personal AI Agent. / One App. Unlimited AI Agents. / Autonomous AI for Android. / From Prompt to Execution. / AI That Gets Work Done. |
| **Positioning** | **Pure Android application** |
| **Spec Version** | 4.6.0 |
| **Status** | Phase 0 — Foundation Complete |
| **Created** | 2026-08-03 |
| **Last Updated** | 2026-08-06 (v4.6 — typed inference streaming, bounded reasoning, ContextSnapshot) |
| **Document Owner** | Lead Architect (Super Z) |

---

## What is This Document?

This is the **master index** for the Nexora project. All detailed content lives in focused documents linked below. This file is the single entry point to navigate the entire specification.

> **Rule**: Update the relevant document BEFORE implementing significant changes. The specification and implementation must never diverge.

---

## Canonical Documentation

The authoritative ownership map is [docs/CANONICAL_SOURCES.md](docs/CANONICAL_SOURCES.md). Shared runtime terminology is defined in [docs/GLOSSARY.md](docs/GLOSSARY.md). High-level overview documents are non-normative summaries.

## Quick Reference

- **One-line**: Nexora is an Android application that transforms your phone into a powerful autonomous AI agent workspace.
- **Positioning**: Pure Android application (not an OS, ROM, or VM).
- **Architecture**: Workspace-first (Workspace > Chat).
- **Interaction**: Agent-first — users chat with agents; the sandbox, internal terminal, runtimes, and execution engine are internal implementation details (ADR-0006).
- **Principles**: 15 codified product principles (PP-001–015) — autonomous agents, provider-agnostic, tool-based execution, persistent memory, agent-driven execution, plugins, background execution, multi-agent orchestration, dashboards, sandboxing, observability, and more.
- **Scale**: 17+ modules, 28 tool categories, 300-500 tools, 10-20 agents.
- **Phases**: 8 development phases (Foundation through Plugin Marketplace).

---

## Document Index

### Product & Vision

| Document | Path |
|----------|------|
| **Product Vision** | [docs/PRODUCT_VISION.md](docs/PRODUCT_VISION.md) |
| **Product Principles** | [docs/PRODUCT_PRINCIPLES.md](docs/PRODUCT_PRINCIPLES.md) |
| **Creator-Owned Product Design** | [NEXORA_PRODUCT_DESIGN_BY_CREATER.md](NEXORA_PRODUCT_DESIGN_BY_CREATER.md) — creator-owned product authority for what Nexora is; not an ADR or subsystem specification |
| **Architecture** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **System Design** | [docs/SYSTEM_DESIGN.md](docs/SYSTEM_DESIGN.md) |
| **Roadmap** | [docs/ROADMAP.md](docs/ROADMAP.md) |
| **Changelog** | [docs/CHANGELOG.md](docs/CHANGELOG.md) |

### Architecture Decision Records (ADRs)

| ADR | Title | Path |
|-----|-------|------|
| ADR-0001 | Workspace-First Architecture (amended by ADR-0006) | [docs/adr/ADR-0001-Workspace-First.md](docs/adr/ADR-0001-Workspace-First.md) |
| ADR-0002 | Plugin-First Design | [docs/adr/ADR-0002-Plugin-System.md](docs/adr/ADR-0002-Plugin-System.md) |
| ADR-0003 | Autonomous Agent Runtime Loop | [docs/adr/ADR-0003-Agent-Runtime.md](docs/adr/ADR-0003-Agent-Runtime.md) |
| ADR-0004 | Sandboxed Execution | [docs/adr/ADR-0004-Sandbox.md](docs/adr/ADR-0004-Sandbox.md) |
| ADR-0005 | Provider Abstraction Layer | [docs/adr/ADR-0005-Provider-Abstraction.md](docs/adr/ADR-0005-Provider-Abstraction.md) |
| ADR-0006 | Agent-First Interaction Model (Infrastructure Is Internal) | [docs/adr/ADR-0006-Agent-First-Interaction-Model.md](docs/adr/ADR-0006-Agent-First-Interaction-Model.md) |
| ADR-0007 | Skills as a First-Class Capability | [docs/adr/ADR-0007-Skills-First-Class.md](docs/adr/ADR-0007-Skills-First-Class.md) |
| ADR-0008 | Typed Inference Streaming and Structured Reasoning Artifacts | [docs/adr/ADR-0008-Typed-Inference-Streaming.md](docs/adr/ADR-0008-Typed-Inference-Streaming.md) |

### API Documentation

| Document | Path |
|----------|------|
| **Tool API** | [docs/api/Tool-API.md](docs/api/Tool-API.md) |
| **Plugin API** | [docs/api/Plugin-API.md](docs/api/Plugin-API.md) |
| **Agent API** | [docs/api/Agent-API.md](docs/api/Agent-API.md) |
| **Provider API** | [docs/api/Provider-API.md](docs/api/Provider-API.md) |
| **Runtime API** | [docs/api/Runtime-API.md](docs/api/Runtime-API.md) |

### SDK Documentation

| Document | Path |
|----------|------|
| **Tool SDK** | [sdk/ToolSDK.md](sdk/ToolSDK.md) |
| **Plugin SDK** | [sdk/PluginSDK.md](sdk/PluginSDK.md) |
| **Provider SDK** | [sdk/ProviderSDK.md](sdk/ProviderSDK.md) |
| **Agent SDK** | [sdk/AgentSDK.md](sdk/AgentSDK.md) |

### Architecture Deep Dives

| Document | Path |
|----------|------|
| **Core Runtime** | [architecture/RUNTIME.md](architecture/RUNTIME.md) |
| **Agent Runtime** | [architecture/AGENT_RUNTIME.md](architecture/AGENT_RUNTIME.md) |
| **Sandbox** | [architecture/SANDBOX.md](architecture/SANDBOX.md) |
| **Sandbox Depth & Autonomy Roadmap** | [docs/SANDBOX_DEPTH.md](docs/SANDBOX_DEPTH.md) |
| **Tool System** | [architecture/TOOL_SYSTEM.md](architecture/TOOL_SYSTEM.md) |
| **Memory System** | [architecture/MEMORY_SYSTEM.md](architecture/MEMORY_SYSTEM.md) |
| **Workflow Engine** | [architecture/WORKFLOW_ENGINE.md](architecture/WORKFLOW_ENGINE.md) |
| **Plugin System** | [architecture/PLUGIN_SYSTEM.md](architecture/PLUGIN_SYSTEM.md) |
| **Security Model** | [architecture/SECURITY_MODEL.md](architecture/SECURITY_MODEL.md) |
| **Provider System** | [architecture/PROVIDER_SYSTEM.md](architecture/PROVIDER_SYSTEM.md) |
| **Multi-Agent System** | [architecture/MULTI_AGENT_SYSTEM.md](architecture/MULTI_AGENT_SYSTEM.md) |

### Component Specifications

| Document | Path |
|----------|------|
| **File System** | [specs/FILE_SYSTEM.md](specs/FILE_SYSTEM.md) |
| **Terminal** | [specs/TERMINAL.md](specs/TERMINAL.md) |
| **Git** | [specs/GIT.md](specs/GIT.md) |
| **Browser** | [specs/BROWSER.md](specs/BROWSER.md) |
| **Database** | [specs/DATABASE.md](specs/DATABASE.md) |
| **AI Providers** | [specs/AI_PROVIDERS.md](specs/AI_PROVIDERS.md) |
| **Workspace** | [specs/WORKSPACE.md](specs/WORKSPACE.md) |
| **Background Execution** | [specs/BACKGROUND_EXECUTION.md](specs/BACKGROUND_EXECUTION.md) |
| **Execution Lifecycle** | [specs/EXECUTION_LIFECYCLE.md](specs/EXECUTION_LIFECYCLE.md) |
| **Context Management** | [specs/CONTEXT_MANAGEMENT.md](specs/CONTEXT_MANAGEMENT.md) |
| **Autonomy & Stability** | [specs/AUTONOMY_STABILITY.md](specs/AUTONOMY_STABILITY.md) |
| **Pipes (Multi-Instance)** | [specs/PIPES.md](specs/PIPES.md) |

### Domain Models

| Model | Path |
|-------|------|
| **Workspace** | [models/Workspace.md](models/Workspace.md) |
| **Agent** | [models/Agent.md](models/Agent.md) |
| **Task** | [models/Task.md](models/Task.md) |
| **Execution** | [models/Execution.md](models/Execution.md) |
| **Memory** | [models/Memory.md](models/Memory.md) |
| **Tool** | [models/Tool.md](models/Tool.md) |
| **Plugin** | [models/Plugin.md](models/Plugin.md) |
| **Provider** | [models/Provider.md](models/Provider.md) |
| **Workflow** | [models/Workflow.md](models/Workflow.md) |
| **Session** | [models/Session.md](models/Session.md) |
| **TerminalSession** | [models/TerminalSession.md](models/TerminalSession.md) |
| **Skill** | [models/Skill.md](models/Skill.md) |
| **Permission** | [models/Permission.md](models/Permission.md) |
| **Instance & Pipe** | [models/Instance.md](models/Instance.md) |
| **Inference Pipeline Artifacts** | [models/Inference.md](models/Inference.md) |

### Protocols

| Protocol | Path |
|----------|------|
| **Agent Protocol** | [protocols/Agent-Protocol.md](protocols/Agent-Protocol.md) |
| **Tool Protocol** | [protocols/Tool-Protocol.md](protocols/Tool-Protocol.md) |
| **Execution Protocol** | [protocols/Execution-Protocol.md](protocols/Execution-Protocol.md) |
| **Plugin Protocol** | [protocols/Plugin-Protocol.md](protocols/Plugin-Protocol.md) |
| **Memory Protocol** | [protocols/Memory-Protocol.md](protocols/Memory-Protocol.md) |
| **Provider Protocol** | [protocols/Provider-Protocol.md](protocols/Provider-Protocol.md) |

### Development Standards

| Standard | Path |
|----------|------|
| **Coding Standard** | [standards/Coding-Standard.md](standards/Coding-Standard.md) |
| **Documentation Standard** | [standards/Documentation-Standard.md](standards/Documentation-Standard.md) |
| **Testing Standard** | [standards/Testing-Standard.md](standards/Testing-Standard.md) |
| **Logging Standard** | [standards/Logging-Standard.md](standards/Logging-Standard.md) |
| **Security Standard** | [standards/Security-Standard.md](standards/Security-Standard.md) |
| **Performance Standard** | [standards/Performance-Standard.md](standards/Performance-Standard.md) |
| **Naming Standard** | [standards/Naming-Standard.md](standards/Naming-Standard.md) |

### UI Specifications

| Spec | Path |
|-----|------|
| **Navigation** | [ui/Navigation.md](ui/Navigation.md) |
| **Theme** | [ui/Theme.md](ui/Theme.md) |
| **Components** | [ui/Components.md](ui/Components.md) |
| **Typography** | [ui/Typography.md](ui/Typography.md) |
| **Spacing** | [ui/Spacing.md](ui/Spacing.md) |
| **Icons** | [ui/Icons.md](ui/Icons.md) |
| **Animations** | [ui/Animations.md](ui/Animations.md) |

### Requirements

| Document | Path |
|----------|------|
| **Functional Requirements** | [requirements/FR.md](requirements/FR.md) |
| **Non-Functional Requirements** | [requirements/NFR.md](requirements/NFR.md) |
| **Constraints** | [requirements/CONSTRAINTS.md](requirements/CONSTRAINTS.md) |
| **Assumptions** | [requirements/ASSUMPTIONS.md](requirements/ASSUMPTIONS.md) |
| **Dependencies** | [requirements/DEPENDENCIES.md](requirements/DEPENDENCIES.md) |
| **Risks** | [requirements/RISKS.md](requirements/RISKS.md) |

### Decision Log

| Document | Path |
|----------|------|
| **Engineering Decision Log** | [docs/DECISION_LOG.md](docs/DECISION_LOG.md) |

### Dependency Graph & Module Boundaries

| Document | Path |
|----------|------|
| **Dependency Graph** | [docs/DEPENDENCY_GRAPH.md](docs/DEPENDENCY_GRAPH.md) |
| **Module Boundaries** | [docs/MODULE_BOUNDARIES.md](docs/MODULE_BOUNDARIES.md) |

### Lifecycles

| Document | Path |
|----------|------|
| **Entity Lifecycles** | [docs/LIFECYCLES.md](docs/LIFECYCLES.md) |

### Performance Budget

| Document | Path |
|----------|------|
| **Performance Budget** | [docs/PERFORMANCE_BUDGET.md](docs/PERFORMANCE_BUDGET.md) |

### State Machines

| Lifecycle | Path |
|-----------|------|
| **Agent Lifecycle** | [state-machines/AgentLifecycle.md](state-machines/AgentLifecycle.md) |
| **Task Lifecycle** | [state-machines/TaskLifecycle.md](state-machines/TaskLifecycle.md) |
| **Workflow Lifecycle** | [state-machines/WorkflowLifecycle.md](state-machines/WorkflowLifecycle.md) |
| **Plugin Lifecycle** | [state-machines/PluginLifecycle.md](state-machines/PluginLifecycle.md) |
| **Provider Lifecycle** | [state-machines/ProviderLifecycle.md](state-machines/ProviderLifecycle.md) |
| **Provider Stream Lifecycle** | [state-machines/ProviderStreamLifecycle.md](state-machines/ProviderStreamLifecycle.md) |
| **Instance & Pipe Lifecycle** | [state-machines/InstanceLifecycle.md](state-machines/InstanceLifecycle.md) |

### Sequence Diagrams

| Flow | Path |
|------|------|
| **Agent Execution Flow** | [diagrams/Agent-Execution-Flow.md](diagrams/Agent-Execution-Flow.md) |
| **Tool Execution Flow** | [diagrams/Tool-Execution-Flow.md](diagrams/Tool-Execution-Flow.md) |
| **Plugin Lifecycle Flow** | [diagrams/Plugin-Lifecycle-Flow.md](diagrams/Plugin-Lifecycle-Flow.md) |
| **Provider Streaming Flow** | [diagrams/Provider-Streaming-Flow.md](diagrams/Provider-Streaming-Flow.md) |
| **Memory Store Flow** | [diagrams/Memory-Store-Flow.md](diagrams/Memory-Store-Flow.md) |

### Security

| Document | Path |
|----------|------|
| **Threat Model** | [security/ThreatModel.md](security/ThreatModel.md) |
| **Permission Model** | [security/PermissionModel.md](security/PermissionModel.md) |
| **Sandbox Policy** | [security/SandboxPolicy.md](security/SandboxPolicy.md) |

### Error Catalog

| Document | Path |
|----------|------|
| **Error Codes** | [errors/ERROR_CODES.md](errors/ERROR_CODES.md) |

### Testing Strategy

| Strategy | Path |
|----------|------|
| **Unit Tests** | [testing/UnitTests.md](testing/UnitTests.md) |
| **Integration Tests** | [testing/IntegrationTests.md](testing/IntegrationTests.md) |
| **E2E Tests** | [testing/E2ETests.md](testing/E2ETests.md) |
| **Performance Tests** | [testing/PerformanceTests.md](testing/PerformanceTests.md) |
| **Security Tests** | [testing/SecurityTests.md](testing/SecurityTests.md) |
| **Regression Tests** | [testing/RegressionTests.md](testing/RegressionTests.md) |

### Backlog

| Version | Path |
|---------|------|
| **MVP (Phase 1)** | [backlog/MVP.md](backlog/MVP.md) |
| **V1 (Phases 1-3)** | [backlog/V1.md](backlog/V1.md) |
| **V2 (Phases 4-6)** | [backlog/V2.md](backlog/V2.md) |
| **Future (Phases 7+)** | [backlog/Future.md](backlog/Future.md) |

### Feature Registry (Stable IDs)

| Registry | Path |
|---------|------|
| **Features** | [registry/FEATURES.md](registry/FEATURES.md) |
| **Tools** | [registry/TOOLS.md](registry/TOOLS.md) |
| **Agents** | [registry/AGENTS.md](registry/AGENTS.md) |
| **Plugins** | [registry/PLUGINS.md](registry/PLUGINS.md) |
| **Providers** | [registry/PROVIDERS.md](registry/PROVIDERS.md) |
| **Tool Capability Matrix** | [registry/TOOL_MATRIX.md](registry/TOOL_MATRIX.md) |
| **Agent Capability Matrix** | [registry/AGENT_MATRIX.md](registry/AGENT_MATRIX.md) |
| **Skills** | [registry/SKILLS.md](registry/SKILLS.md) |

### Versioning

| Document | Path |
|----------|------|
| **Versioning Strategy** | [VERSIONING.md](VERSIONING.md) |

---

## Repository Structure

```
Nexora/
├── .github/                # GitHub Actions, issue templates
├── docs/                   # Product documentation
│   ├── PRODUCT_VISION.md
│   ├── ARCHITECTURE.md
│   ├── SYSTEM_DESIGN.md
│   ├── ROADMAP.md
│   ├── CHANGELOG.md
│   ├── DECISION_LOG.md    # Engineering decision log (DL-001+)
│   ├── DEPENDENCY_GRAPH.md # Module dependency graph + forbidden deps
│   ├── MODULE_BOUNDARIES.md # Per-module API surface and dep rules
│   ├── LIFECYCLES.md        # Entity lifecycle flows (7 entities)
│   ├── PERFORMANCE_BUDGET.md # 27 measurable performance targets
│   ├── adr/               # Architecture Decision Records (5 ADRs)
│   │   ├── ADR-0001-Workspace-First.md
│   │   ├── ADR-0002-Plugin-System.md
│   │   ├── ADR-0003-Agent-Runtime.md
│   │   ├── ADR-0004-Sandbox.md
│   │   └── ADR-0005-Provider-Abstraction.md
│   └── api/               # API documentation (5 APIs)
│       ├── Tool-API.md
│       ├── Plugin-API.md
│       ├── Agent-API.md
│       ├── Provider-API.md
│       └── Runtime-API.md
├── requirements/           # Requirements layer (FR, NFR, constraints, risks)
│   ├── FR.md
│   ├── NFR.md
│   ├── CONSTRAINTS.md
│   ├── ASSUMPTIONS.md
│   ├── DEPENDENCIES.md
│   └── RISKS.md
├── architecture/           # Architecture deep dives (10 docs)
├── specs/                  # Component specifications (7 docs)
├── models/                 # Canonical domain models (12 docs)
├── protocols/              # Communication contracts (6 docs)
├── sdk/                    # SDK documentation (4 docs)
├── standards/              # Development standards (7 docs)
├── ui/                     # UI specifications (7 docs)
├── state-machines/         # State machine definitions (5 lifecycles)
├── diagrams/               # Sequence diagrams (Mermaid, 5 flows)
├── security/               # Security deep dives (threat model, permissions, sandbox)
├── errors/                 # Error catalog (NXR-1xxx through NXR-9xxx)
├── testing/                # Testing strategy (6 test types)
├── backlog/                # Versioned backlog (MVP, V1, V2, Future)
├── registry/               # Feature registry with stable IDs + matrices
│   ├── FEATURES.md
│   ├── TOOLS.md
│   ├── AGENTS.md
│   ├── PLUGINS.md
│   ├── PROVIDERS.md
│   ├── TOOL_MATRIX.md
│   └── AGENT_MATRIX.md
├── android/                # Planned implementation module (Phase 1; not present in the current documentation-only snapshot)
├── runtime/                # Planned implementation module (Phase 2; not present in the current documentation-only snapshot)
├── sandbox/                # Planned implementation module (Phase 3; not present in the current documentation-only snapshot)
├── tools/                  # Planned implementation module (Phase 4; not present in the current documentation-only snapshot)
├── providers/              # Planned implementation module (Phase 5; not present in the current documentation-only snapshot)
├── memory/                 # Planned implementation module (Phase 6; not present in the current documentation-only snapshot)
├── agents/                 # Planned implementation module (Phase 7; not present in the current documentation-only snapshot)
├── plugins/                # Planned implementation module (Phase 8; not present in the current documentation-only snapshot)
├── workflows/              # Planned workflow definitions and templates (not present in the current documentation-only snapshot)
├── storage/                # Planned database and persistence layer (not present in the current documentation-only snapshot)
├── services/               # Planned Android services (foreground, scheduled; not present in the current documentation-only snapshot)
├── shared/                 # Shared utilities and extensions
├── testing/                # Test suites
├── scripts/                # Build and utility scripts
├── assets/                 # Static assets (icons, fonts, etc.)
├── examples/               # Example plugins, agents, workflows
├── design/                 # UI/UX design assets and mockups
├── roadmap/                # Roadmap planning documents
├── PROJECT_SPECIFICATION.md # This file (master index)
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── .gitignore
```

---

## Development Phases

| Phase | Name | Goal | Key Deliverables |
|-------|------|------|-----------------|
| **0** | Foundation | Repo structure, documentation, registries | This repository’s documentation-first snapshot: requirements, architecture, models, protocols, standards, state machines, diagrams, security, testing, registries, dependency graph, module boundaries, lifecycles, and performance budget. The live file inventory is determined by the repository tree rather than a fixed count in this roadmap row. |
| **1** | Android Foundation | Bootable app, no AI yet | Agent-first chat UI, navigation, theme, settings, workspace manager, interfaces |
| **2** | Core Runtime | Agent execution loop | Planner, executor, tool manager, event bus, checkpoints |
| **3** | Sandbox | Isolated execution | Virtual FS, terminal, process manager, Python/Node |
| **4** | Tools | Tool interface + foundational tools | 50+ tools across 8 categories |
| **5** | Cloud AI Providers | Provider abstraction + active cloud/external providers | Cloud/external provider adapters, streaming, health checks, profile switching; no local AI providers |
| **6** | Memory | Persistent memory system | Session, project, long-term, semantic search |
| **7** | Autonomous Agents | Built-in agent types | 16 agents, multi-agent coordination |
| **8** | Plugin Marketplace | Everything is a plugin | Plugin SDK, Nexora Hub, community plugins |

---

## Locked Architectural Rule

> **Everything is a service behind an interface. UI never talks directly to implementations.**
>
> `UI → Service Interface → Runtime → Implementation`
>
> This applies to: ToolManager, ProviderManager, MemoryManager, PluginManager, WorkspaceManager, Sandbox, Scheduler, Logging, Security, AgentRuntime.

> **Locked Interaction Rule — Agent-first: infrastructure is internal (ADR-0006).**
>
> Users interact with AI agents through chat. The sandbox, internal terminal, runtimes,
> and execution engine are internal implementation details, triggered automatically by
> agents in an isolated environment. They have no primary user-facing screens; results
> surface in the conversation as an agent activity feed (tool calls, output, file changes).

---

*Documentation baseline v4.6.0. Updates are contract-driven; implementation must align with the linked canonical specifications and migration/versioning rules.*
