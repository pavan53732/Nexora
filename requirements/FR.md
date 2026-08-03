# Functional Requirements — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## Workspace Management

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-W001 | Create workspace with name, description, and template | Must | 0 |
| FR-W002 | Delete workspace with confirmation and data cleanup | Must | 0 |
| FR-W003 | Rename workspace at any time | Must | 0 |
| FR-W004 | List all workspaces with search and sort | Must | 0 |
| FR-W005 | Configure workspace settings (provider, model, defaults) | Must | 0 |
| FR-W006 | Enforce workspace isolation (no cross-workspace data leaks) | Must | 1 |
| FR-W007 | Import/export workspace as portable archive | Should | 4 |
| FR-W008 | Switch between active workspaces instantly | Must | 0 |
| FR-W009 | Workspace templates (blank, coding, research, automation) | Should | 2 |
| FR-W010 | Display workspace statistics (agents, tasks, usage) | Should | 3 |

## Agent Management

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-A001 | Create agent with name, role, and system prompt | Must | 1 |
| FR-A002 | Configure agent (model, tools, memory, temperature) | Must | 1 |
| FR-A003 | Delete agent with cascade option for history | Must | 1 |
| FR-A004 | List agents in workspace with filters | Must | 1 |
| FR-A005 | Support 15 agent roles (coder, researcher, planner, etc.) | Must | 1 |
| FR-A006 | Define agent permissions per tool and resource | Must | 2 |
| FR-A007 | Chat interface for agent interaction | Must | 1 |
| FR-A008 | Multi-agent coordination via delegation protocol | Must | 5 |
| FR-A009 | Agent-to-agent task delegation with handoff context | Must | 5 |
| FR-A010 | Real-time agent monitoring (status, progress, tokens) | Should | 3 |
| FR-A011 | Checkpoint and resume agent execution | Should | 4 |
| FR-A012 | Cancel running agent with graceful shutdown | Must | 2 |
| FR-A013 | Full agent execution history with replay | Should | 4 |
| FR-A014 | Agent templates for common roles | Should | 2 |
| FR-A015 | Agent resource limits (max tokens, timeout, steps) | Must | 2 |

## Task Management

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-T001 | Create task with description and assign to agent | Must | 2 |
| FR-T002 | Track task status (pending, running, done, failed) | Must | 2 |
| FR-T003 | Set task priority (low, medium, high, critical) | Must | 2 |
| FR-T004 | Define task dependencies (blocked-by, depends-on) | Should | 3 |
| FR-T005 | Delegate task from one agent to another | Must | 5 |
| FR-T006 | Display task timeline with start/end/duration | Should | 3 |
| FR-T007 | Retry failed task with configurable attempts | Must | 2 |
| FR-T008 | Cancel pending or running task | Must | 2 |
| FR-T009 | Bulk task operations (cancel, retry, reassign) | Should | 4 |
| FR-T010 | Task output and artifact storage | Must | 2 |
| FR-T011 | Scheduled execution — one-off delayed and recurring tasks with constraints (network, unmetered, charging), backed by WorkManager; dedupe of duplicate scheduled jobs | Must | 2 |
| FR-T012 | Priority queue ordering — queued tasks run in priority order (critical > high > medium > low); higher-priority tasks jump the queue | Must | 2 |
| FR-T013 | Global background control — user can pause and resume all background execution with one action | Should | 3 |

## Tool System

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-TL001 | Register tools via declarative interface | Must | 1 |
| FR-TL002 | Execute tools within sandbox with timeout | Must | 1 |
| FR-TL003 | Discover available tools by category and agent | Must | 1 |
| FR-TL004 | Enforce tool permissions per agent role | Must | 2 |
| FR-TL005 | Configurable tool execution timeout | Must | 1 |
| FR-TL006 | Cache tool results with TTL | Should | 4 |
| FR-TL007 | Chain tool outputs as inputs to next tool | Must | 1 |
| FR-TL008 | Support 25+ tool categories (file, web, code, etc.) | Must | 3 |
| FR-TL009 | Plugin-provided tools with dynamic registration | Must | 6 |
| FR-TL010 | Tool versioning with backward compatibility | Should | 6 |
| FR-TL011 | Tool health check and status reporting | Should | 4 |
| FR-TL012 | Per-tool configuration (params, defaults) | Must | 1 |
| FR-TL013 | Search tools by name, category, capability | Should | 3 |
| FR-TL014 | Mark tools as favorites for quick access | Should | 3 |
| FR-TL015 | Tool execution logging and audit trail | Must | 2 |

## AI Provider System

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-P001 | Register providers (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, LM Studio, GGUF, Custom) | Must | 0 |
| FR-P002 | Switch active provider per workspace | Must | 0 |
| FR-P003 | Provider health check and connectivity test | Must | 1 |
| FR-P004 | Streaming responses with real-time UI update | Must | 1 |
| FR-P005 | Embedding generation for memory and search | Must | 4 |
| FR-P006 | Model selection from provider catalog | Must | 1 |
| FR-P007 | Provider configuration (API key, endpoint, params) | Must | 0 |
| FR-P008 | Automatic fallback on provider failure | Should | 3 |
| FR-P009 | Per-session token usage tracking | Must | 2 |
| FR-P010 | Side-by-side provider comparison | Should | 7 |
| FR-P011 | Provider profiles — named, switchable configurations (API key, endpoint, model, streaming, params); create, edit, duplicate, delete, switch independently | Must | 1 |
| FR-P012 | Per-workspace default provider profile — workspace settings bind a profile; agents route through the active profile | Must | 1 |
| FR-P013 | Provider isolation — provider credentials, configurations, and request data are isolated per provider; no cross-provider access or data flow; provider code cannot read other providers' keys or configs | Must | 5 |

## Memory System

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-M001 | Session memory — auto-capture conversation context | Must | 2 |
| FR-M002 | Project memory — workspace-scoped knowledge | Must | 3 |
| FR-M003 | Long-term memory — persistent across sessions | Should | 4 |
| FR-M004 | Knowledge graph — entity relationships | Should | 5 |
| FR-M005 | Execution history — full agent step log | Must | 2 |
| FR-M006 | Semantic memory search via embeddings | Should | 4 |
| FR-M007 | Memory pruning based on relevance and age | Should | 5 |
| FR-M008 | Export memory data (JSON, markdown) | Should | 7 |
| FR-M009 | Memory scope control (session, workspace, global) | Must | 3 |
| FR-M010 | Persistent memory across app restarts | Must | 2 |
| FR-M011 | Tool history — every tool invocation recorded (tool, params, result, duration, permission decision, workspace, agent); queryable per workspace/task/tool | Must | 2 |
| FR-M012 | File history — version history of files modified by agents (snapshot/diff per write, revert to any version, quota-aware retention) | Must | 3 |
| FR-M013 | User preferences — learned and explicit preferences (coding style, default model, tool choices, patterns); persisted in DataStore, scoped global + per workspace | Should | 4 |
| FR-M014 | Knowledge graph — extract entities, relationships, and facts from conversations, tool results, and files; store and dedupe (merge by entity identity) | Should | 5 |
| FR-M015 | Knowledge graph query — query by entity, list relationships, traverse paths, and surface graph results in semantic recall | Should | 5 |

## Sandbox

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-S001 | Virtual file system isolated per workspace | Must | 1 |
| FR-S002 | Process execution within sandbox constraints | Must | 1 |
| FR-S003 | Resource limits (CPU, memory, disk, network) | Must | 1 |
| FR-S004 | Workspace-to-workspace filesystem isolation | Must | 1 |
| FR-S005 | Network restrictions (allow/deny lists) | Should | 3 |
| FR-S006 | Scoped environment variables per workspace | Should | 3 |
| FR-S007 | Automatic sandbox cleanup on workspace delete | Must | 1 |
| FR-S008 | Manual sandbox reset to clean state | Should | 4 |
| FR-S009 | Sandbox resource usage statistics | Should | 4 |
| FR-S010 | Sandbox templates with preconfigured environments | Should | 5 |
| FR-S011 | Sandbox telemetry — agent can query its own sandbox state (processes, disk, env, quotas, network rules) via tools | Must | 3 |
| FR-S012 | Sandbox lifecycle autonomy — agents create ephemeral sandboxes, reset to clean state, and apply sandbox templates | Must | 3 |
| FR-S013 | Workspace snapshots & rollback — full-workspace snapshot and atomic restore to any snapshot | Should | 4 |
| FR-S014 | Network egress policy — deny-by-default, per-workspace domain allowlists, per-task time windows, all egress logged through an in-app proxy | Must | 3 |
| FR-S015 | Quarantine & content scanning — network-downloaded files quarantined and scanned; promotion requires permission | Must | 3 |
| FR-S016 | Autonomy modes & adaptive approval — manual / assisted / autopilot; risk-scored permission decisions with full audit | Should | 4 |
| FR-S017 | Per-workspace encryption at rest — workspace storage encrypted with Keystore-backed keys | Should | 4 |
| FR-S018 | Per-agent sandbox isolation — delegated sub-agents run in separate sandbox instances | Should | 5 |

## Plugin System

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-PL001 | Install plugin from file or marketplace | Must | 6 |
| FR-PL002 | Uninstall plugin with cleanup | Must | 6 |
| FR-PL003 | Plugin lifecycle management (init, start, stop) | Must | 6 |
| FR-PL004 | Plugin permission declaration and enforcement | Must | 6 |
| FR-PL005 | Plugin-specific configuration UI | Should | 7 |
| FR-PL006 | Plugin update with migration support | Should | 7 |
| FR-PL007 | Plugin marketplace browsing and search | Should | 8 |
| FR-PL008 | Plugin dependency resolution | Should | 7 |
| FR-PL009 | Plugin isolation (separate classloader) | Must | 6 |
| FR-PL010 | Plugin discovery and metadata inspection | Should | 7 |

## UI/UX

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-U001 | Bottom navigation (Workspace, Tasks, Settings) — no infrastructure tabs | Must | 0 |
| FR-U002 | Workspace dashboard with agent and task overview | Must | 0 |
| FR-U003 | Task list with status, priority, and assignment | Must | 2 |
| FR-U004 | Agent chat with streaming response display | Must | 1 |
| FR-U005 | Agent activity feed — tool calls, terminal output, and file changes surfaced in chat (replaces the user-facing terminal panel) | Must | 3 |
| FR-U006 | File explorer for sandbox contents | Must | 3 |
| FR-U007 | Settings screen (providers, appearance, security) | Must | 0 |
| FR-U008 | Dynamic theme (light, dark, system) | Must | 0 |
| FR-U009 | In-app notification system | Should | 3 |
| FR-U010 | Global search across workspaces, agents, tasks | Should | 4 |
| FR-U011 | Chat is the single primary interaction surface — goal entry, streaming responses, tool-call cards, permission prompts, and results all live in the conversation | Must | 1 |

## Terminal (Internal)

> The terminal is an **internal component** (ADR-0006): it is invoked by agents, never
> opened by the user. There is no user-facing terminal screen or tab; output is surfaced
> in the chat activity feed and execution logs.

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-TE001 | Execute shell commands within sandbox, agent-invoked | Must | 3 |
| FR-TE002 | Stream command output into the agent activity feed in real time | Must | 3 |
| FR-TE003 | Command history per terminal session (internal, agent-managed) | Must | 3 |
| FR-TE004 | Tab completion for commands and paths | Should | 4 |
| FR-TE005 | Multiple concurrent terminal sessions (internal) | Should | 5 |

## Execution Lifecycle

> Full lifecycle defined in [specs/EXECUTION_LIFECYCLE.md](../specs/EXECUTION_LIFECYCLE.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-EL-001 | Goal & outcome analysis — derive objective, expected outcome, and acceptance criteria from the user's goal before execution | Must | 2 |
| FR-EL-002 | Automatic task & subtask decomposition with dependencies | Must | 2 |
| FR-EL-003 | Automatic agent selection — assign the best-suited specialized agent per task | Must | 7 |
| FR-EL-004 | Automatic skill selection — determine required skills per task via the SkillRegistry | Must | 4 |
| FR-EL-005 | Per-task provider/model selection — choose the best-suited provider profile and model per task | Should | 5 |
| FR-EL-006 | Dependency & runtime resolution — plugins, packages, runtimes, and env templates resolved and validated before execution | Must | 2 |
| FR-EL-007 | Execution ordering & parallelism — determine sequential vs parallel execution from the dependency graph | Must | 2 |
| FR-EL-008 | Per-step validation criteria — every step declares pass/fail criteria; results validated before proceeding | Must | 2 |
| FR-EL-009 | Error detection & recovery — automatic retries (bounded, backoff), fallbacks, and checkpoints per failure class | Must | 2 |
| FR-EL-010 | Reflection & self-review after execution | Must | 2 |
| FR-EL-011 | End-to-end verification — acceptance criteria re-checked; objective confirmed achieved before completion | Must | 2 |
| FR-EL-012 | Completion reporting — logs, report, execution history, memory storage, and follow-up/improvement identification | Must | 2 |
| FR-EL-013 | Software-engineering pipeline — build, static analysis, unit/integration/E2E tests, perf & security checks, bounded auto-fix loop, final validation for coding tasks | Must | 4 |

## Skills

> Skills are a first-class concept (WHO=agent, WHAT=skill, HOW=tool) — see [ADR-0007](../docs/adr/ADR-0007-Skills-First-Class.md) and [registry/SKILLS.md](../registry/SKILLS.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-SK-001 | Skill registry — first-class skill catalog (id, name, description, domain, required tools, applicable agents); stable IDs | Must | 4 |
| FR-SK-002 | Skill acquisition — agents acquire skills (built-in assignment, user-defined, or learned from experience); persisted per agent | Must | 4 |
| FR-SK-003 | Skill–tool mapping — skills reference tools; many skills may share the same tools; tool refs validated at registration | Must | 4 |
| FR-SK-004 | Skill-aware planning — the planner selects skills per task and resolves them to agents and tools; executor validates agent possession before dispatch | Must | 4 |
| FR-SK-005 | Skill discovery & management — list, inspect, and acquire skills via tools (`skill_list`, `skill_acquire`) | Should | 4 |

## Web Search & Extraction

> Tools: `search_web` (TOOL-171), `browser_extract` (TOOL-247) and the browser toolset (TOOL-2xx) — see [registry/TOOLS.md](../registry/TOOLS.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-WS-001 | Web search — search the web via a configured search provider; return ranked results (title, URL, snippet) | Must | 4 |
| FR-WS-002 | Web page extraction — extract text, structured content, and metadata from a page | Must | 4 |
| FR-WS-003 | Extraction modes — plain text, markdown, structured (JSON), and screenshot modes | Should | 4 |
| FR-WS-004 | Search provider configuration — configurable search backend (default or user-defined endpoint), per-workspace selection | Should | 4 |
| FR-WS-005 | Content safety — extracted/downloaded web content enters the sandbox quarantine (FR-S015) before promotion; untrusted content is labeled in agent context (prompt-injection containment) | Must | 4 |
