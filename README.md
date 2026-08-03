# Nexora

> **Autonomous AI Agent App for Android**
> Think. Plan. Execute.

---

## What is Nexora?

Nexora is an **Android AI Agent Platform** — an Android application that transforms your phone into a powerful autonomous AI agent workspace. AI agents think, plan, execute tasks, use tools, manage projects, and automate complex workflows securely within the app.

It goes beyond chat. AI agents autonomously perform real tasks using files, code, terminals, browsers, APIs, and Android capabilities.

### What Nexora Is

- An **Android application** — install from APK or app store.
- An **autonomous AI agent platform** — AI agents that think, plan, and execute.
- A **multi-agent execution environment** — specialized agents collaborating.
- An **agent-first AI workspace** — you talk to agents; they do the work for you.
- A **project workspace** — manage files, code, and tasks inside the app.
- A **tool execution platform** — 300-500+ tools across 25+ categories, invoked by agents.
- A **plugin-based AI ecosystem** — extensible through community plugins.

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
    ├── Terminal
    ├── Plugins
    ├── Logs
    ├── Settings
    └── Chats
```

Chats are one artifact within a workspace. This scales much better as the platform grows.

---

## Key Features

- **Autonomous Agents** — 15 built-in agent types (Planner, Coder, Researcher, Reviewer, etc.)
- **Agent-First Chat** — you give the agent a goal; everything else happens automatically.
- **Agent-Driven Execution** — agents automatically use the terminal, runtimes (Python/Node), Git, and SQLite inside an isolated sandbox — no infrastructure UI.
- **Sandboxed Execution** — AI never touches the host system directly (internal by design).
- **Tool System** — 25+ tool categories, 300-500 individual tools, all agent-invoked and plugin-based.
- **Multi-Provider AI** — OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, LM Studio, GGUF, Custom.
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
| 5 | AI Providers (9 providers) | Upcoming |
| 6 | Memory (persistent memory) | Upcoming |
| 7 | Autonomous Agents (15 types) | Upcoming |
| 8 | Plugin Marketplace | Upcoming |

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full roadmap.

---

## Repository Structure

```
Nexora/
├── .github/          # GitHub Actions, issue templates
├── docs/             # Product documentation
├── architecture/     # Architecture deep dives (10 documents)
├── specs/            # Component specifications (7 documents)
├── android/          # Android application source
├── runtime/          # Core runtime implementation
├── plugins/          # Plugin implementations
├── tools/            # Tool implementations
├── agents/           # Agent implementations
├── memory/           # Memory system
├── sandbox/          # Sandbox implementation
├── provider/         # AI provider implementations
├── testing/          # Test suites
├── scripts/          # Build and utility scripts
├── assets/           # Static assets
├── examples/         # Example plugins, agents, workflows
├── design/           # UI/UX design assets
└── roadmap/          # Roadmap planning
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
- [Multi-Agent System](architecture/MULTI_AGENT_SYSTEM.md)

### Component Specifications

- [File System](specs/FILE_SYSTEM.md)
- [Terminal](specs/TERMINAL.md)
- [Git](specs/GIT.md)
- [Browser](specs/BROWSER.md)
- [Database](specs/DATABASE.md)
- [AI Providers](specs/AI_PROVIDERS.md)
- [Workspace](specs/WORKSPACE.md)

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
