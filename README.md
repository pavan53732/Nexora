# Nexora

> **Autonomous AI Agent App for Android**
> Think. Plan. Execute.

---

## What is Nexora?

Nexora is a **pure Android application** — an Android application that transforms your phone into a powerful autonomous AI agent workspace. AI agents think, plan, execute tasks, use tools, manage projects, and automate complex workflows securely within the app.

It goes beyond chat. AI agents autonomously perform real tasks using files, code, terminals, browsers, APIs, and Android capabilities.

### What Nexora Is

- An **Android application** — install from APK or app store.
- An **autonomous AI application** — AI agents that think, plan, and execute.
- A **multi-agent execution environment** — specialized agents collaborating.
- An **agent-first AI workspace** — you talk to agents; they do the work for you.
- A **project workspace** — manage files, code, and tasks inside the app.
- A **tool execution application** — 300-500+ tools across 28 categories, invoked by agents.
- A **plugin-based AI application** — extensible through community plugins.

### What Nexora Is Not

- An Android operating system
- A custom ROM, Linux distribution, or virtual machine
- A replacement for Android
- A simple AI chat application
- A terminal emulator or developer shell — the embedded terminal is an internal agent tool
- An infrastructure UI — the sandbox, runtimes, and execution engine are hidden behind the agent

---

## Architecture

Nexora uses a **workspace-first** architecture. The workspace is the primary entity — not the chat screen.

```
Workspace
    ├── Agents
    ├── Tasks
    ├── Files
    ├── Memory
    ├── Terminal (internal — agent-invoked; output in Logs/activity feed)
    ├── Plugins
    ├── Logs
    ├── Settings
    └── Chats
```

Chats are one artifact within a workspace. This scales much better as the application grows.

---

## Key Features

- **Autonomous Agents** — 16 built-in agent types (Planner, Coder, Researcher, Reviewer, etc.)
- **Skills** — first-class expertise units (Kotlin Development, Android Debugging, Git Conflict Resolution, API Design…) that agents acquire and apply via tools (Agent = who, Skill = what, Tool = how)
- **Agent-First Chat** — you give the agent a goal; everything else happens automatically.
- **Agent-Driven Execution** — agents automatically use the terminal, runtimes (Python/Node), Git, and SQLite inside an isolated sandbox — no infrastructure UI.
- **Sandboxed Execution** — AI never touches the host system directly (internal by design).
- **Tool System** — 28 tool categories, 300-500 individual tools, all agent-invoked and plugin-based.
- **Multi-Provider AI** — Cloud/external OpenAI-compatible APIs, Anthropic, Gemini, Groq, OpenRouter, and Custom external endpoints.
- **Typed inference streaming** — sequenced events, bounded backpressure, cancellation, resume lineage, committed Tool-call assembly, and exactly-one terminal behavior.
- **Bounded deep reasoning** — executable ReasoningPolicy, critic/verifier gates, evidence-calibrated confidence, redacted ReasoningSummary, and reproducible ContextSnapshot.
- **Memory System** — Session, project, and long-term memory with semantic search.
- **Plugin Marketplace** — Everything (tools, providers, agents) is installable as a plugin.
- **Multi-Agent Collaboration** — Agents share memory, workspace, and tasks.

---

## Development Phases

| Phase | Name | Status |
|-------|------|--------|
| 0 | Foundation (repo structure, docs) | Current |
| 1 | Android Foundation (app scaffold, no AI) | Upcoming |
| 2 | Core Runtime (agent loop) | Upcoming |
| 3 | Sandbox (VFS, terminal, runtimes) | Upcoming |
| 4 | Tools (generic interface + tools) | Upcoming |
| 5 | Cloud AI Providers | Upcoming |
| 6 | Memory (persistent memory) | Upcoming |
| 7 | Autonomous Agents (16 types) | Upcoming |
| 8 | Plugin Marketplace | Upcoming |

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full roadmap.

---

## Repository Structure

```
Nexora/
├── .github/          # GitHub Actions, issue templates
├── docs/             # Product documentation
├── architecture/     # Architecture deep dives (10 documents)
├── specs/            # Component specifications (11 documents)
├── docs/             # Current documentation corpus
├── architecture/     # Canonical architecture documents
├── decisions/        # Architecture decisions
├── models/           # Domain model projections
├── specs/            # Engineering-facing specifications
├── state-machines/   # Canonical lifecycle/state machines
├── testing/          # Test specifications and cases
├── scripts/          # Utility/documentation scripts
└── planned implementation modules/  # Android/runtime/tool/provider/etc. modules are planned by roadmap phases and are not yet present in this Phase 0 repository snapshot
```

---

## Documentation

- [Project Specification (Master Index)](PROJECT_SPECIFICATION.md)
- [Product Vision](docs/PRODUCT_VISION.md)
- [Product Principles](docs/PRODUCT_PRINCIPLES.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [System Design](docs/SYSTEM_DESIGN.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)

### Architecture Deep Dives

- [Core Runtime](architecture/RUNTIME.md)
- [Agent Runtime](architecture/AGENT_RUNTIME.md)
- [Sandbox](architecture/SANDBOX.md)
- [Tool System](architecture/TOOL_SYSTEM.md)
- [Memory System](architecture/MEMORY_SYSTEM.md)
- [Workflow Engine](architecture/WORKFLOW_ENGINE.md)
- [Plugin System](architecture/PLUGIN_SYSTEM.md)
- [Security Model](architecture/SECURITY_MODEL.md)
- [Provider System](architecture/PROVIDER_SYSTEM.md)
- [Provider Stream Lifecycle](state-machines/ProviderStreamLifecycle.md)
- [Typed Inference Streaming ADR](docs/adr/ADR-0008-Typed-Inference-Streaming.md)
- [Inference Pipeline Models](models/Inference.md)
- [Multi-Agent System](architecture/MULTI_AGENT_SYSTEM.md)

### Component Specifications

- [File System](specs/FILE_SYSTEM.md)
- [Terminal](specs/TERMINAL.md)
- [Git](specs/GIT.md)
- [Browser](specs/BROWSER.md)
- [Database](specs/DATABASE.md)
- [AI Providers](specs/AI_PROVIDERS.md)
- [Workspace](specs/WORKSPACE.md)
- [Background Execution](specs/BACKGROUND_EXECUTION.md)
- [Execution Lifecycle](specs/EXECUTION_LIFECYCLE.md)
- [Context Management](specs/CONTEXT_MANAGEMENT.md)
- [Autonomy & Stability](specs/AUTONOMY_STABILITY.md)
- [Pipes (Multi-Instance Collaboration)](specs/PIPES.md)

---

## Tech Stack

- **Language**: Kotlin / Java
- **Build**: Gradle
- **Platform**: Android (API 34+)
- **UI**: Material Design 3 / Material You (Jetpack Compose)
- **Architecture**: Clean Architecture, Plugin-first

---

## License

This project is licensed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.
