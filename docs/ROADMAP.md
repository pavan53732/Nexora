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

- Typed sequenced inference events and exactly-one terminal contract (FR-P014/015)
- Bounded backpressure, cancellation, reconnect, and stream lineage (FR-P016/017/019)
- Capability/latency/privacy-aware ProviderRoutePlan with non-blocking provider-cost metadata or preference (FR-P018, DEC-25)
- ProviderStreamLifecycle and adapter conformance suite
- ReasoningPolicy, verifier/critic, redacted ReasoningSummary (FR-RN-009..012)
- Reproducible model-aware ContextSnapshot (FR-CM-010..012)

> The runtime must NEVER depend on a specific provider implementation.

## Phase 6 — Memory

**Goal:** Persistent memory system.

Session, Project, Long-Term memory. Semantic search. Execution history.

## Phase 7 — Autonomous Agents

**Goal:** 16 built-in agent types.

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
| Cold start | Target under 2 seconds; warning threshold 3 seconds |
| Memory (idle) | Idle RSS under 512 MB (canonical target per NFR-PERF-005) |
| First-task time | Under 2 minutes |
| Crash rate | Under 0.1% |


> **S2 — MCP Canonical Status:** MCP adapter contract (`architecture/TOOL_SYSTEM.md` §MCP Client + `protocols/Tool-Protocol.md` §MCP Invocation) is now marked canonical in `docs/CANONICAL_SOURCES.md`. Implementation remains `Phase 5` (`specs/AI_PROVIDERS.md`); registry (`TOOL-397`..`402`) and capability matrix (`TOOL_MATRIX.md`) already synchronized (`G4` commit `8e1e937`). No phase timing change required.


## Capability placement decisions

- Conversation checkpoint and non-destructive conversation branching are runtime/session capabilities dependent on conversation persistence and authorization; no implementation phase is claimed until the conversation/session persistence plan assigns one.
- Execution checkpointing remains Phase 2. Workspace snapshot/rollback remains its existing sandbox phase. These are not conversation rollback.
- Skill lifecycle completion follows the existing Skill Registry/runtime phases; this documentation decision does not claim implementation.
- No first-class Command artifact or command phase is established by DEC-12.
- JavaScript-scripted workflows: planned later and out of the current scope; no current-phase requirement, architecture, API, or implementation commitment is created.
- Dedicated `/workflows` monitoring panel: planned later and out of the current scope; no current-phase user-facing infrastructure-panel commitment is created.
