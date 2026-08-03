# Product Vision — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## One-Line Description

> Nexora is an Android application that transforms your phone into a powerful autonomous AI agent workspace, enabling AI agents to think, plan, execute tasks, use tools, manage projects, and automate complex workflows securely within the app.

## Vision Statement

> Nexora is an Android-native autonomous AI agent application that enables intelligent AI agents to plan, reason, use tools, execute multi-step workflows, and collaborate within a secure sandboxed runtime. It goes beyond chat by allowing AI agents to autonomously perform real tasks using files, code, terminals, browsers, APIs, and Android capabilities.

## What Nexora Is

- **An Android application** — A native app you install from an APK or app store.
- **An autonomous AI agent platform** — AI agents that think, plan, and execute on their own.
- **A multi-agent execution environment** — Multiple specialized agents collaborating on tasks.
- **An agent-first AI workspace** — The user interacts with AI agents; infrastructure stays hidden.
- **A sandboxed AI runtime** — Internal secure execution environment isolated from the host system; the agent uses it automatically, the user never touches it.
- **A project workspace** — Manage files, code, and tasks inside the app.
- **A tool execution platform** — 300-500+ tools across 25+ categories, invoked by agents on the user's behalf.
- **A plugin-based AI ecosystem** — Extensible through plugins and community contributions.

## Interaction Model

Nexora mirrors how modern agent assistants behave:

1. The user types a **goal** in chat.
2. The **agent** plans and decides which tools to use.
3. The agent **automatically invokes** the embedded terminal, runtimes (Python, Node), file operations, Git, SQLite, and network tools inside an **isolated sandbox** created on demand.
4. Results stream back into the **conversation** as an activity feed: tool-call cards, output excerpts, file diffs, and log references.
5. The user reviews, approves sensitive operations, and steers the agent — never the infrastructure.

The **sandbox, internal terminal, runtimes, and execution engine are internal
implementation details** (see [ADR-0006](../docs/adr/ADR-0006-Agent-First-Interaction-Model.md)).
They have no primary user-facing screens.

## What Nexora Enables

- **Think** — Reason about goals, decompose problems, and form strategies.
- **Plan** — Create multi-step execution plans with dependencies and ordering.
- **Reason** — Reflect on intermediate results, self-correct, and adapt strategies.
- **Execute** — Run tools, invoke runtimes, modify files, and perform real actions.
- **Use Tools** — Access 300-500+ individual tool functions across 25+ categories.
- **Build Projects** — Create, scaffold, and manage full software projects inside Android.
- **Edit Files** — Read, write, modify, refactor, and version-control files.
- **Run Code** — Execute Python, Node.js, JavaScript, and shell commands in a sandbox.
- **Perform Multi-Step Workflows** — Chain operations into complex, long-running pipelines.
- **Collaborate with Other Agents** — Delegate subtasks, share context, and coordinate.
- **Continue Long-Running Tasks** — Persist state, resume after restart, run in background.
- **Operate Inside a Secure Sandboxed Runtime** — Never touch the host system directly.

The application should feel like having an **autonomous software engineer** running entirely inside your Android phone.

## What Nexora Is Not

- An Android operating system
- A custom ROM
- A Linux distribution
- A virtual machine
- A replacement for Android
- A simple AI chat application
- A wrapper around a web-based AI service
- A prompt-and-response tool
- A static tool collection

## Product Positioning

> **Android AI Agent Platform**

Nexora is consistently positioned as an **Android AI Agent Platform** — an app with a comprehensive AI agent platform inside it, rather than an operating system.

Alternative phrasings:

- Autonomous AI Agent Platform for Android
- The Ultimate AI Agent App for Android

## Brand Identity

| Brand Name | Purpose |
|------------|--------|
| **Nexora Workspace** | Primary project workspace environment |
| **Nexora Sandbox** | Isolated execution environment *(internal — agent-invoked)* |
| **Nexora Runtime** | Core agent execution engine *(internal)* |
| **Nexora Engine** | Planning and reasoning engine *(internal)* |
| **Nexora Memory** | Persistent memory and knowledge system |
| **Nexora Terminal** | Embedded shell terminal *(internal — agent-invoked)* |
| **Nexora Plugins** | Plugin system and marketplace |
| **Nexora Hub** | Plugin marketplace and discovery center |
| **Nexora Agents** | Multi-agent collaboration system |

## Estimated Scale

| Component | Estimated Count |
|-----------|----------------|
| Core Platform Modules | 15+ |
| Tool Categories | 25+ |
| Individual Tool Functions | 300-500 |
| Built-in Agent Types | 10-20 |
| AI Providers | Unlimited |
| Plugins | Unlimited |

## Long-Term Goal

Create the **world's most capable Android AI Agent Platform**, comparable to Cursor, Cline, Claude Code, Roo Code, GitHub Copilot Agent, Gemini CLI, and OpenHands — but designed specifically for Android.

## Product Philosophy

### Autonomous Execution First

Every component must revolve around autonomous execution. The AI agent's ability to act independently is paramount.

### Goal-Oriented Interface

The user gives a **goal**. The AI determines what to do, which tools to use, which files to modify, whether another agent should help, and when execution is complete.

### Agent, Not Chatbot

Every conversation is a potential execution. Every message is a potential task. Every tool call is a real action.

### Agent-First Interface

The user interacts with the **AI agent**, not with the infrastructure. Chat is the command
surface; the terminal, sandbox, and runtimes execute invisibly behind it (ADR-0006).
Infrastructure is an implementation detail — the user sees goals, results, and progress,
never plumbing.

### Design Principles

1. **Plugin-first** — Core is minimal. Everything else is a plugin.
2. **Sandboxed** — AI never touches the host system directly (internal by design).
3. **Extensible** — Add capabilities without modifying core.
4. **Observable** — Every action is logged and traceable (activity feed + execution history).
5. **Offline-capable** — Core features work without network.
6. **Android-native** — Designed for mobile, not a ported desktop app.
7. **Agent-first** — Infrastructure (sandbox, terminal, runtimes, engine) is internal; the agent surfaces results in chat.

### Workspace-First Architecture

The **Workspace** is the primary entity — not the chat screen.

```
Workspace
    ├── Agents
    ├── Tasks
    ├── Files
    ├── Memory
    ├── Terminal   (internal — agent-invoked)
    ├── Plugins
    ├── Logs
    ├── Settings
    └── Chats      (primary interaction surface)
```

## Comparable Products

| Product | Platform | Relevance |
|---------|----------|-----------|
| **Cursor** | Desktop | AI-first code editor. Nexora brings this to Android. |
| **Cline** | VS Code | Autonomous AI coding agent. Nexora is a standalone Android equivalent. |
| **Claude Code** | CLI | Terminal-based AI agent. Nexora adds GUI + mobile. |
| **Roo Code** | VS Code | Multi-model AI agent. Nexora supports multiple providers natively. |
| **GitHub Copilot Agent** | VS Code/GitHub | Integrated AI coding. Nexora is platform-independent. |
| **Gemini CLI** | CLI | Google's CLI agent. Nexora adds GUI, plugins, and mobile. |
| **OpenHands** | Web/Desktop | AI software engineer. Nexora is Android-first. |

### Key Differentiator

Nexora is the **only** platform designed specifically for **Android** as a first-class platform, not a port or wrapper.
