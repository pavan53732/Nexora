# Product Principles — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> Related: [PRODUCT_VISION.md](./PRODUCT_VISION.md) · [docs/ARCHITECTURE.md](./ARCHITECTURE.md) · [docs/adr/README.md](./adr/README.md)

---

## 1. Purpose

This document codifies the **invariant product principles** of Nexora. Every product
decision — UI, roadmap, marketing, and implementation — must align with these
principles. If a proposed feature contradicts a principle, the feature is wrong, not
the principle.

**Stable IDs:** `PP-001` … `PP-015` (referenced in docs, backlog, and issue tracking).

## 2. Positioning Statement

> **Nexora is an Android-native application for autonomous AI agents.**
> You talk to agents — they get real work done.
> Think. Plan. Execute.

Users interact with **agents**, never with infrastructure. The sandbox, terminal,
runtimes, and execution engine are internal implementation details that agents
trigger automatically (ADR-0006).

---

## 3. Core Principles

### PP-001 — Autonomous Agents, Not a Chatbot

Nexora is an **agent-driven Android application**, not a chat application. Every conversation is a
potential execution; every message is a potential task. The user gives a **goal**; the
agent plans, uses tools, iterates, and completes the goal autonomously.

- Sources: [ADR-0003](../docs/adr/ADR-0003-Agent-Runtime.md) · [ADR-0006](../docs/adr/ADR-0006-Agent-First-Interaction-Model.md) · [PRODUCT_VISION.md](./PRODUCT_VISION.md) · [FR-A001–015](../requirements/FR.md)

### PP-002 — Provider-Agnostic

Nexora is provider-agnostic. A single abstraction supports **OpenAI-compatible APIs,
Anthropic, Gemini, OpenRouter, local models (Ollama, LM Studio, GGUF), and custom
endpoints**. The runtime never depends on a specific provider; users bring their own
keys and models, and can switch per workspace.

- Sources: [ADR-0005](../docs/adr/ADR-0005-Provider-Abstraction.md) · [specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) · [PROV-001–009](../registry/PROVIDERS.md)

### PP-003 — Tool-Based Execution

Agents accomplish tasks by **using tools**, not only generating text. Every capability
is a tool behind a uniform, permissioned, audited interface. Text is the interface;
tools are how work gets done.

- Sources: [TOOL_SYSTEM](../architecture/TOOL_SYSTEM.md) · [TOOL-001–133](../registry/TOOLS.md) · [FR-TL001–015](../requirements/FR.md)

### PP-004 — Persistent Memory Across Sessions

Nexora remembers. Session, project, and long-term memory tiers persist across
sessions and restarts, with semantic search and execution history. Agents build on
previous work instead of starting from zero.

- Sources: [MEMORY_SYSTEM](../architecture/MEMORY_SYSTEM.md) · [FR-M001–010](../requirements/FR.md)

### PP-005 — Agent-Driven Execution (built-in terminal/shell, internal)

Nexora includes a Linux-like shell and embedded runtimes (Python, Node) inside an
isolated sandbox. The **agent** invokes them automatically for command execution,
scripts, Git, and SQLite. Per ADR-0006 this is an **internal capability**: users see
results (activity feed, logs), never a shell prompt. *"Built-in terminal" is a
capability, not a user-facing feature.*

- Sources: [ADR-0006](../docs/adr/ADR-0006-Agent-First-Interaction-Model.md) · [specs/TERMINAL.md](../specs/TERMINAL.md) · [SANDBOX](../architecture/SANDBOX.md)

### PP-006 — Plugin/Skill System

Everything is a plugin: tools, providers, agents, and skills. Capabilities extend
without modifying the core, via a stable, versioned plugin API and (later) a
marketplace.

**Skills are first-class** (ADR-0007): Agent = WHO performs the work · Skill = WHAT
expertise is needed · Tool = HOW it is performed. The planner selects skills per task
and resolves them to agents and tools; agents acquire skills over time.

- Sources: [ADR-0002](../docs/adr/ADR-0002-Plugin-System.md) · [ADR-0007](../docs/adr/ADR-0007-Skills-First-Class.md) · [PLUGIN_SYSTEM](../architecture/PLUGIN_SYSTEM.md) · [registry/SKILLS.md](../registry/SKILLS.md) · [FR-PL001–010](../requirements/FR.md) · [FR-SK001–005](../requirements/FR.md)

### PP-007 — Background Execution

Long-running tasks keep running when the app is minimized or the device restarts.
Foreground services, WorkManager scheduling, and checkpointing guarantee that an
agent's work survives interruption and resumes with full state fidelity.

- Sources: [LIFECYCLES §7](../docs/LIFECYCLES.md) · [docs/api/Runtime-API.md](./api/Runtime-API.md) · DL-010

### PP-008 — Multi-Agent Orchestration

Specialized agents collaborate: delegation with handoff context, shared workspace and
memory, and coordinated workflows. One goal can be executed by a team of agents.

- Sources: [MULTI_AGENT_SYSTEM](../architecture/MULTI_AGENT_SYSTEM.md) · [FR-A008/009](../requirements/FR.md)

### PP-009 — Dashboard & Session Management

The workspace is the primary entity (ADR-0001). Dashboards give an overview of
agents, tasks, files, and memory per workspace; sessions persist and resume. The user
manages *projects and conversations* — never plumbing.

In the ordinary agent-first interaction, the user expresses goals and provides required
input, responds to clarification requests, approves or denies permission-gated actions,
cancels work, configures supported settings, and inspects meaningful execution evidence.
The runtime performs planning, orchestration, capability selection, background progression,
checkpointing, retry, and recovery on behalf of the goal. This boundary does not prohibit
additional administrative, configuration, observability, or future interaction surfaces
where separately established by an authoritative document.

This principle preserves the distinction between user-facing outcomes and controls and
primarily internal execution machinery. Internal infrastructure is not the primary
interaction surface, while meaningful activity, progress, results, approvals, errors,
completion information, logs, audit information, and established cost or token
information remain observable through their authoritative user-facing surfaces.

This principle does not define the detailed semantics or ownership of execution
checkpoints, context snapshots, conversation checkpoints, file versions, workspace
snapshots, memory artifacts, skills, workflows, tools, or commands. Those distinctions
remain governed by their canonical architecture, specification, model, registry, and
decision documents.

- Sources: [ADR-0001](../docs/adr/ADR-0001-Workspace-First.md) · [FR-W001–010](../requirements/FR.md) · [FR-U001–011](../requirements/FR.md) · [ADR-0006](../docs/adr/ADR-0006-Agent-First-Interaction-Model.md) · [ADR-0009](../docs/adr/ADR-0009-Adaptive-Autonomy-And-Persistence.md) · [BACKGROUND_EXECUTION](../specs/BACKGROUND_EXECUTION.md) · [AGENT_RUNTIME](../architecture/AGENT_RUNTIME.md) · [TOOL_SYSTEM](../architecture/TOOL_SYSTEM.md) · [WORKFLOW_ENGINE](../architecture/WORKFLOW_ENGINE.md)

---

## 4. Supporting Principles

### PP-010 — Sandboxed, Permissioned Execution

AI never touches the host system directly. Every workspace gets an isolated sandbox;
every sensitive operation passes a permission gate. Least privilege by default.

- Sources: [ADR-0004](../docs/adr/ADR-0004-Sandbox.md) · [SANDBOX](../architecture/SANDBOX.md) · [FR-S001–010](../requirements/FR.md)

### PP-011 — Checkpoint & Resume

Agent state is persisted continuously; any interruption (crash, kill, restart) resumes
with **100% state fidelity**. Autonomy you can rely on.

- Sources: [NFR-REL-001/002](../requirements/NFR.md) · [AGENT_RUNTIME](../architecture/AGENT_RUNTIME.md)

### PP-012 — Observable by Default

Every action is logged and traceable: agent activity feed, tool-call cards, execution
history, and audit trail. Users trust agents they can audit.

- Sources: [FR-U005](../requirements/FR.md) · [SYSTEM_DESIGN → Observability](./SYSTEM_DESIGN.md) · [FR-TL015](../requirements/FR.md)

### PP-013 — Token & Cost Control

Token budgets per request/session with transparent usage tracking. On a phone with
paid APIs, cost awareness is a user-facing feature, not plumbing.

- Sources: [AGENT_RUNTIME → TokenBudget](../architecture/AGENT_RUNTIME.md) · [FR-P009](../requirements/FR.md)

### PP-014 — Offline-Capable

Core features work without network. Local providers (Ollama, LM Studio, GGUF) keep
agents useful offline; workspace data is always available locally.

- Sources: [NFR-REL-006](../requirements/NFR.md) · [CONSTRAINTS → AI Providers](../requirements/CONSTRAINTS.md)

### PP-015 — First-Run Onboarding

The agent-first model requires a 3-step guided setup: **provider → workspace →
first goal**. The app explains itself in minutes, then gets out of the way.

- Sources: [NFR-USE-004](../requirements/NFR.md) · [MVP backlog](../backlog/MVP.md)

---

## 5. Guardrails — What Nexora Is Not

| Guardrail | Detail |
|-----------|--------|
| Not a chatbot | A chat UI exists, but execution is the product (PP-001) |
| Not a terminal app | The shell is internal (PP-005); no user-facing terminal screen or tab |
| Not an OS / ROM / VM | An app on Android (ADR-0001, README) |
| Not a wrapper around a web AI service | Native, local-first, plugin-based (PP-002, PP-006, PP-014) |
| Not a static tool collection | Tools exist to serve agents (PP-003) |
| Not an infrastructure UI | Sandbox, runtimes, and engine have no primary screens (ADR-0006) |

**Marketing guardrail:** sell *"agents that get work done"*, never *"a terminal in
your pocket."*

---

## 6. Principle → Documentation Map

| Principle | ADR | Architecture | Spec | Requirements |
|-----------|-----|--------------|------|--------------|
| PP-001 Autonomous agents | ADR-0003, ADR-0006 | AGENT_RUNTIME, RUNTIME | — | FR-A001–015 |
| PP-002 Provider-agnostic | ADR-0005, ADR-0008 | PROVIDER_SYSTEM, ProviderStreamLifecycle | AI_PROVIDERS, Provider-Protocol | FR-P001–019 |
| PP-003 Tool-based execution | — | TOOL_SYSTEM | — | FR-TL001–015 |
| PP-004 Persistent memory | — | MEMORY_SYSTEM | DATABASE | FR-M001–010 |
| PP-005 Agent-driven execution | ADR-0006 | SANDBOX | TERMINAL, GIT, FILE_SYSTEM | FR-TE001–005, FR-S001–010 |
| PP-006 Plugin/skill system | ADR-0002 | PLUGIN_SYSTEM | — | FR-PL001–010 |
| PP-007 Background execution | — | RUNTIME | — | NFR-REL-001/002 |
| PP-008 Multi-agent orchestration | — | MULTI_AGENT_SYSTEM | — | FR-A008/009 |
| PP-009 Dashboard & sessions | ADR-0001 | ARCHITECTURE | WORKSPACE | FR-W001–010, FR-U001–011 |
| PP-010 Sandboxed execution | ADR-0004 | SANDBOX | — | FR-S001–010, NFR-SEC-001 |
| PP-011 Checkpoint & resume | — | AGENT_RUNTIME | — | NFR-REL-001/002 |
| PP-012 Observable by default | — | SYSTEM_DESIGN | — | FR-U005, FR-TL015 |
| PP-013 Token & cost control | — | AGENT_RUNTIME | AI_PROVIDERS | FR-P009 |
| PP-014 Offline-capable | — | — | — | NFR-REL-006 |
| PP-015 First-run onboarding | — | — | — | NFR-USE-004 |

---

## 7. How to Use This Document

1. **New features** must map to at least one principle; the mapping is recorded in the
   [Feature Registry](../registry/FEATURES.md).
2. **A feature contradicting a principle** is a design error — resolve the conflict
   with a new ADR before implementation.
3. **UI decisions** must serve the agent-first surface (chat + activity feed +
   dashboards); infrastructure views only in developer mode.
4. **Marketing and docs** must follow the guardrails in §5.
