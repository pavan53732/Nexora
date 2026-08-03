# Development Roadmap — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Phase 0 — Foundation (CURRENT)

**Goal:** Repository structure, documentation, architectural foundations.

- [x] Repository structure with 17 top-level directories
- [x] PROJECT_SPECIFICATION.md as master index
- [x] Focused documentation split (docs/, architecture/, specs/)
- [x] Repository standard files (README, LICENSE, CONTRIBUTING, etc.)
- [x] Workspace-first architecture decision

## Phase 1 — Android Foundation

**Goal:** Bootable app with navigation, theme, settings, core interfaces. No AI yet.

- Android project scaffold (Kotlin, Gradle, Material 3)
- Navigation framework (workspace-first, no infrastructure tabs)
- Agent-first chat UI (goal entry, streaming responses, activity feed)
- Theme system (dark mode first, Material You)
- Settings screen
- Workspace Manager (create, switch, archive, delete)
- File Manager (browse virtual file system)
- Plugin Framework interfaces
- Runtime interfaces (planner, executor, tool manager contracts)
- Tool interfaces (generic Tool contract)
- AI Provider interfaces (provider abstraction)

## Phase 2 — Core Runtime

**Goal:** Agent runtime loop.

```
Planner → Executor → Tool Manager → Sandbox → Result
```

- Planner, Executor, Context Builder
- Event Bus (pub/sub)
- Token Budget Manager
- Agent Loop (reflect, plan, execute, repeat)
- Checkpoint system

## Phase 3 — Sandbox

**Goal:** Sandboxed execution environment *(internal — agent-invoked only, ADR-0006; no user-facing sandbox/terminal UI)*.

- Virtual file system
- Embedded terminal (Linux-like shell, internal)
- Process Manager
- Runtime Manager (Python, Node.js)
- Log capture
- Resource limits
- Sandbox depth Tier 1 (see [SANDBOX_DEPTH.md](SANDBOX_DEPTH.md)): telemetry (FR-S011), lifecycle autonomy + templates (FR-S012), egress policy + DLP (FR-S014), quarantine & scanning (FR-S015)

## Phase 4 — Tools

**Goal:** Generic tool interface + foundational tools.

```kotlin
interface Tool {
    id: String
    name: String
    description: String
    permissions: String[]
    execute(params): ToolResult
}
```

Priority: File System, Terminal, Search, Workspace, Git, Network, Memory, Package Manager.

## Phase 5 — AI Providers

**Goal:** Provider abstraction + 9 providers.

OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, LM Studio, GGUF, Custom.

> The runtime must NEVER depend on a specific provider implementation.

## Phase 6 — Memory

**Goal:** Persistent memory system.

Session, Project, Long-Term memory. Semantic search. Execution history.

## Phase 7 — Autonomous Agents

**Goal:** 15 built-in agent types.

Planner, Coder, Researcher, Browser, Reviewer, Tester, Debugger, Documentation Writer, and more.

## Phase 8 — Plugin Marketplace

**Goal:** Everything is a plugin.

Plugin SDK, Nexora Hub, tools/providers/agents as plugins.

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Tool count | 300-500 |
| Agent types | 10-20 |
| APK size | Under 50 MB |
| Cold start | Under 3 seconds |
| Memory (idle) | Under 256 MB |
| First-task time | Under 2 minutes |
| Crash rate | Under 0.1% |
