> **Status: SUPPORTING** for FR requirements.
> This document records focused requirements for FR; canonical subsystem definitions remain in the owning architecture documents.


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
| FR-A005 | Support 16 agent roles (coder, researcher, planner, architect, etc.) | Must | 1 |
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

## Session and Workflow Lifecycle

> Session semantics are governed by `state-machines/SessionLifecycle.md` and the Session–Conversation contracts. Workflow semantics are governed by `architecture/WORKFLOW_ENGINE.md` and `state-machines/WorkflowLifecycle.md`.

| ID | Requirement | Priority | Phase |
|---|---|---|---|
| FR-SESS-001 | Maintain the canonical Session context lifecycle while preserving Session identity, terminal behavior, and distinct Session–Conversation continuation semantics | Must | 1 |
| FR-WF-001 | Orchestrate workflow graph progression through the canonical workflow lifecycle, including dependency ordering, step execution, completion, failure, cancellation, and recovery outcomes | Must | 2 |

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
| FR-TL008 | Support 26 tool categories (file, web, code, skills, etc.) | Must | 3 |
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
| FR-P001 | Register cloud/external providers (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Custom external endpoint) | Must | 0 |
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
| FR-P014 | Typed inference stream — closed event envelope with request/stream/correlation/provider/model identity and monotonic sequence | Must | 5 |
| FR-P015 | Stream integrity — gap/duplicate detection and exactly one committed terminal event; socket close is never success | Must | 5 |
| FR-P016 | Bounded backpressure and cancellation propagation across Agent, Router, adapter, EventBus, and UI | Must | 5 |
| FR-P017 | Stream resume/reconnect — native cursor or explicit restart-with-lineage; partial output remains marked | Must | 5 |
| FR-P018 | Capability/latency/privacy-aware ProviderRoutePlan with persisted selection reason; provider cost metadata MAY inform non-blocking preference or tie-breaking but MUST NOT block an otherwise eligible route | Should | 5 |
| FR-P019 | Mid-stream failover creates a new stream with lineage; cross-provider output is never silently spliced | Must | 5 |

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

| FR-S019 | Full Environment per workspace using bundled Debian-slim rootfs | Must | 3 |
| FR-S020 | Bundled Debian-slim rootfs in APK assets with integrity verification (SHA-256 + signature) | Must | 3 |
| FR-S021 | proot-based userland execution inside sandbox without root privileges | Must | 3 |
| FR-S022 | glibc-compatible runtime for pip/npm binary wheels | Must | 3 |
| FR-S023 | Per-workspace rootfs overlay — writable layer on read-only base | Must | 3 |
| FR-S024 | Rootfs cache management (LRU eviction, size quotas, reset to clean) | Should | 4 |
| FR-S025 | Environment template marketplace (pre-configured rootfs recipes: data science, web dev, mobile) | Should | 5 |
| FR-S026 | Cross-architecture rootfs support (ARM64 primary, x86_64 emulator via QEMU user-mode) | Should | 5 |
| FR-S027 | Rootfs health check and automatic corruption repair | Should | 5 |
| FR-S028 | Offline package cache — apt packages cached per workspace for offline reinstall | Could | 4 |

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


## Context Management

> Pipeline defined in [specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-CM-001 | Structured state is never compressed — goal, plan, decisions, and acceptance criteria persist exactly in checkpoints | Must | 2 |
| FR-CM-002 | Token budget allocation — priority-ordered allocation across context layers (state, system, working set, retrieval, summaries); truncation only after summarization and only on the summary layer | Must | 2 |
| FR-CM-003 | Progressive summarization — rolling summary triggered by budget thresholds, summary-of-summaries, idempotent summary artifacts, fidelity check after each summarization | Must | 3 |
| FR-CM-004 | Resume reconstruction — context rebuilt from checkpoint + summary + retrieval; raw history is never replayed for context | Must | 2 |
| FR-CM-005 | Freshness checks — referenced file/task/provider/sandbox state re-validated before each agent-loop iteration; stale context flagged | Must | 2 |
| FR-CM-006 | Context tagging & trust — every chunk labeled (source, timestamp, trust level, scope); untrusted content isolated in labeled segments | Must | 3 |
| FR-CM-007 | Milestone memory curation — agent stores structured facts and lessons at step boundaries and task completion, not raw transcripts | Must | 3 |
| FR-CM-008 | Context observability — per-layer token usage, summarization/truncation/stale events visible via context_stats and execution history | Should | 4 |
| FR-CM-009 | Project introspection — pre-flight pass reads API schemas, database schemas, configuration files, build definitions, UI layouts, domain models, and infrastructure files before the Planner creates an ExecutionPlan; populates a lightweight ProjectContext in working memory (Layer 3); Knowledge Graph queried after introspection; all summaries carry EV classification (DERIVED/ESTIMATED) | Must | 2 |
| FR-CM-010 | Versioned ContextSnapshot — immutable model/tokenizer budget, included/excluded segments, hashes, and output/reasoning reservations per provider request | Must | 2 |
| FR-CM-011 | Retrieval scoring — relevance, trust, freshness, source diversity, and near-duplicate suppression determine memory inclusion | Must | 4 |
| FR-CM-012 | Context compaction lineage — every summary/compaction records parent artifact, fidelity result, and reproducible segment references | Must | 3 |

## Autonomy & Stability

> Defined in [specs/AUTONOMY_STABILITY.md](../specs/AUTONOMY_STABILITY.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-AS-001 | Plan repair — on step failure: diagnose, then retry / repair / re-plan / re-delegate / escalate (bounded, max 3 cycles); repair decisions recorded in history | Must | 4 |
| FR-AS-002 | Agent heartbeat & watchdog — heartbeat per loop iteration; hang detection with checkpoint restart (bounded) and escalation | Must | 2 |
| FR-AS-003 | Technical-boundary escalation — context/token, step, wall-clock, provider-call, Tool-call, repair, verifier, device, or resource safety exhaustion pauses, summarizes, retries, reconciles, escalates, or marks incomplete according to the owning contract; cost/usage notifications are informational only and cost alone MUST NOT pause, downgrade, block, or terminate a technically valid progressing run | Must | 2 |
| FR-AS-004 | Closed-loop learning — reflect, store lesson (memory_lessons), propose skill refinement or new LEARNED skill; lessons retrieved during planning | Should | 4 |
| FR-AS-005 | Trust growth — per-agent/per-workspace trust score adjusts autonomy mode; success raises it, failures lower it; explicit reset | Should | 4 |
| FR-AS-006 | Verification gates — step validation criteria are hard gates; executor blocks next step until pass or classified failure; resumed agents re-validate | Must | 2 |
| FR-AS-007 | Idempotency & exactly-once recovery — tools declare idempotency; replay log; non-idempotent calls reconciled from tool history, never replayed | Must | 2 |
| FR-AS-008 | Cloud-only degradation ladder — primary cloud provider → alternate eligible cloud provider/profile → cached prior result or supported non-inference workspace operation → read-only + notification; each descent announced and logged | Must | 2 |
| FR-AS-009 | Fault-injection testing — scripted chaos scenarios (kill mid-task, kill on non-idempotent call, network loss, provider storm, disk-full, OOM, double restart, summarization churn) runnable in CI | Should | 4 |


## Git Grounding (anti-hallucination)

> Rules defined in [specs/GIT.md](../specs/GIT.md) — GR-1..GR-6.

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-GT-001 | Structured git results — every git tool returns canonical JSON (files, SHAs, diffs) plus a fresh repo snapshot (branch, HEAD SHA, dirty/staged state, remotes) | Must | 4 |
| FR-GT-002 | Read-before-write gate — no mutating git operation without a read pass (status → diff → log → branch) in the same task; enforced by the tool wrapper | Must | 4 |
| FR-GT-003 | Path grounding — file paths verified via file_exists/file_info before mutation; missing paths discovered, never assumed | Must | 4 |
| FR-GT-004 | SHA grounding — branch/tag/commit refs resolved to real SHAs before use; fabricated refs rejected | Must | 4 |
| FR-GT-005 | Verify-after-write — post-commit/push/merge verification against real SHAs; destructive previews require confirmation | Must | 4 |
| FR-GT-006 | Repo content is data, not instructions — repo files (especially from foreign clones) are untrusted segments with zero authority; plan-vs-actual diff reported at task end | Must | 4 |


## Response Grounding (anti-hallucination)

> Rules RG-1..RG-6 defined in [specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md) §5.
> For Git-specific grounding see FR-GT-001..006.

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-GND-001 | Tool-before-claim — factual claims must trace to a tool result or labeled context segment in the same task; unverified training-memory claims flagged as such | Must | 2 |
| FR-GND-002 | Citations — grounded claims carry a source reference (memory/file/web/tool); unsourced claims stated as opinion/unverified | Must | 2 |
| FR-GND-003 | Uncertainty disclosure — explicit "I don't know"/low-confidence instead of guessing; offers a retrieval action rather than inventing | Must | 2 |
| FR-GND-004 | Refuse unsupported — missing tool/permission/offline data yields explicit refusal with reason and enablement path | Must | 2 |
| FR-GND-005 | Code-claim grounding — codebase claims verified via code-intelligence tools (code_search/code_symbols/code_references/file_read) before being stated; proven by build+tests before reported working | Must | 4 |
| FR-GND-006 | Plan-vs-actual honesty — completion reports distinguish done-verified / done-unverified / attempted-failed / not-attempted | Must | 2 |


## Reasoning (think before answering)

> RB-1..RB-6 defined in [specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md) §6.

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-RN-001 | Deliberation gate — classify each message as answer-now / reasoning-pass / clarify-first; never guess on ambiguity (clarify instead) | Must | 2 |
| FR-RN-002 | Reasoning pipeline — understand, clarify, retrieve evidence first, reason over evidence, draft, verify, answer with citations + confidence | Must | 2 |
| FR-RN-003 | Deliberation effort levels — six-level reasoning effort scale (OFF / LOW / MEDIUM / HIGH / X_HIGH / MAX), configurable per workspace, agent, and task; effort proportional to stakes (see CONTEXT_MANAGEMENT §6 Reasoning Effort Scale) | Must | 2 |
| FR-RN-004 | Reasoning-capable models — REASONING provider capability; per-task routing to reasoning models for thorough tasks; fail-fast if unavailable at X_HIGH/MAX; graceful degradation to model maximum at HIGH and below | Should | 5 |
| FR-RN-005 | Reasoning visibility — collapsible redacted ReasoningSummary in activity feed/history with approach, evidence, decisions, uncertainty, verification, and token usage; raw private chain-of-thought excluded | Must | 2 |
| FR-RN-006 | Answer-quality gates — grounded, complete, consistent, confident before sending; assumptions stated; premise contradictions flagged; self-consistency for critical outputs | Must | 2 |
| FR-RN-007 | Reasoning disable (OFF) — user can disable reasoning entirely per scope (task/agent/workspace/global); OFF bypasses the deliberation gate to the FAST path, omits reasoning parameters from provider requests, and never selects REASONING models; grounding/evidence gates (RG/EV) remain active under OFF | Must | 2 |
| FR-RN-008 | Reasoning settings surface — Settings → Model Config → Reasoning: level selector (OFF first), effective-level indicator showing the governing layer (task → agent → workspace → global → default MEDIUM), per-agent/per-workspace overrides; changes apply to new messages immediately; no chat-embedded toggle (ADR-0006) | Must | 2 |
| FR-RN-009 | Executable ReasoningPolicy — bound provider/tool calls, reasoning tokens, repair cycles, verifier passes, wall time, and non-overridable device/resource safety ceilings per effort level; usage and cost remain observable metadata and are not execution gates | Must | 2 |
| FR-RN-010 | Bounded critic/verifier pipeline — independent critic for high-stakes effort, disagreement-driven repair, then clarification/escalation at the applicable technical safety or liveness limit; financial cost or internal credit status MUST NOT be the stop condition | Must | 4 |
| FR-RN-011 | Structured ReasoningSummary — persist redacted approach/evidence/decisions/uncertainty/verification, never require raw private chain-of-thought | Must | 2 |
| FR-RN-012 | Evidence-calibrated confidence — confidence derives from evidence coverage, source quality, contradiction checks, and verifier results rather than model self-report | Must | 2 |


## Evidence & Validation Engine

> EV-1..EV-6 defined in [specs/CONTEXT_MANAGEMENT.md](../specs/CONTEXT_MANAGEMENT.md) §7.

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-EV-001 | Statement classification — every significant statement carries structured metadata: VERIFIED / DERIVED / ESTIMATED / UNKNOWN / USER_PROVIDED; unclassified significant claims blocked | Must | 2 |
| FR-EV-002 | Structured confidence — HIGH/MEDIUM/LOW as data; LOW → ask before proceeding (ties to autonomy modes) | Must | 2 |
| FR-EV-003 | Zero-assumption mode — missing information is identified, explained, and gathered/asked for; outputs inventing missing details rejected | Must | 2 |
| FR-EV-004 | Consolidated guardrails — engine enforces the 7 anti-fabrication rules on every response; violations logged and trust-decrementing | Must | 2 |
| FR-EV-005 | Fact vs recommendation labeling — responses distinguish verified fact / analysis / recommendation / speculation | Should | 2 |
| FR-EV-006 | Completion validation & reviewer handoff — acceptance criteria, gates, and plan-vs-actual verified before completion; important tasks require a Reviewer agent pass before user-facing completion | Must | 4 |


## Multi-Agent Sub-Tasks

> SA-1..SA-5 defined in [architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-MA-001 | Sub-agent autonomous completion — delegated subtasks run end-to-end by the sub-agent (spawn → execute → verify → report); interruptions limited to approval gates, budget escalation, and heartbeat failure | Must | 7 |
| FR-MA-002 | Complete handoff — delegation includes goal, acceptance criteria, constraints, available evidence, required skills/tools, and report format; ambiguity resolved via one EV-gated question, never guessing | Must | 7 |
| FR-MA-003 | Parallel orchestration — dependency-aware fan-out with a per-workspace concurrency limit; per-file write locks (second writer waits or coordinator merges a copy); sandbox budgets split across sub-agents; results merged in dependency order | Must | 7 |
| FR-MA-004 | Inherited policies — sub-agents explicitly operate under zero-assumption, grounding (RG), reasoning (RB), verification gates, guardrails, and the Evidence & Validation Engine | Must | 7 |
| FR-MA-005 | Sub-agent reporting — plan-vs-actual report with verification evidence; important subtasks require the Reviewer pass before merging | Must | 7 |


## Agent Orchestration

> Master Agent / orchestrator defined in [architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-AG-001 | Master Agent role — the coordinator (AGT-015) owns goal decomposition, sub-agent spawning, assignment, progress tracking, result merging, conflict resolution, and completion decisions; it never performs implementation itself | Must | 7 |
| FR-AG-002 | No direct sub-agent communication — all inter-agent communication flows through the orchestration layer (EventBus + coordinator + shared memory); agents publish results, never call other agents | Must | 7 |
| FR-AG-003 | Agent Orchestrator composition — orchestration is an explicit concern composed from AgentManager + Executor + WorkflowEngine + EventBus + Evidence & Validation Engine | Must | 7 |
| FR-AG-004 | Documentation completion gate — documentation-affected work requires docs updated (CHANGELOG, README, ADRs, specs, API docs as applicable) before completion is reported | Must | 4 |


## Multi-Instance Pipes

> Pipe transport, pairing, discovery, and cross-instance delegation defined in [specs/PIPES.md](../specs/PIPES.md).

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-MI-001 | Instance discovery — zero-configuration discovery of peer Nexora instances on the same machine (rendezvous directory) and LAN (mDNS/DNS-SD `_nexorapipe._tcp`); no manual address entry | Must | 7 |
| FR-MI-002 | Pipe transport — TLS 1.3 mutual-auth channels between instances (loopback same-machine, mTLS LAN); length-prefixed JSON envelopes with `correlationId`, `pipeId`, `workspaceId`, `version`; closed payload type set (DelegateTask/Accept/Reject/Progress/Result/Heartbeat/Revoke/Close) | Must | 7 |
| FR-MI-003 | Same-machine main/sub orchestration — multiple local instances coordinate through pipes with automatic coordinator/sub-instance assignment (single coordinator role per FR-AG-001 preserved) | Must | 7 |
| FR-MI-004 | Instance pairing & identity — per-install Ed25519 `pipeKey` (private key in SecureKeyStore), user-confirmed fingerprint pairing (QR or 6-word code), per-workspace pairing scope, one-tap revocation | Must | 7 |
| FR-MI-005 | Cross-instance delegation — a coordinator delegates SA-1..SA-5 subtasks to a remote instance over a pipe; remote admission control (Manual/Assisted/Autopilot per pipe, FR-S016); remote sub-agent runs in its own sandbox (FR-S018) with its own provider profiles (FR-P011); results merge in dependency order | Must | 7 |
| FR-MI-006 | Pipe heartbeats & auto-reconnect — 30 s heartbeats; 3 missed = Degraded, 5 missed = Disconnected; bounded reconnect (3 attempts, exponential backoff, NFR-REL-003); mid-task disconnect blocks the subtask and escalates per FR-AS-003, resuming from checkpoint on reconnect | Must | 7 |
| FR-MI-007 | Pipe broadcast routing — coordinator broadcasts typed messages to all connected pipes of a workspace; recipients treat broadcasts as data, not instructions (FR-CM-006); rate-limited (1/s, burst 5); `DENY`-by-default scope | Should | 7 |
| FR-MI-008 | Pipe security gates — pairing, connect, and broadcast pass PermissionManager checks with `instance:*` scopes (pair/connect `ASK`, broadcast `DENY` defaults); forged or malformed payloads rejected pre-parse, audited CRITICAL, 3 violations auto-revoke | Must | 7 |
| FR-MI-009 | Pipe failure handling — discovery absence is graceful (not an error); pairing mismatch aborts with audit; version incompatibility blocks handshake with a clear user notice; revoked pipes close immediately with graceful remote cancellation | Must | 7 |
| FR-MI-010 | Pipes settings surface — Settings → Pipes: paired instance list, pair/revoke, acceptance mode per pipe, discovery toggle; pipe activity surfaces in the chat activity feed with a pipe badge (FR-U005); no pipes tab or slash-command surface (FR-U011) | Must | 7 |


## Conversation Checkpoint and Branching

| ID | Requirement | Priority | Phase |
|---|---|---|---|
| FR-CB001 | Create an immutable conversation checkpoint at the selected post-turn or explicit user trigger | Should | Covered by the Session–Conversation engineering contract, persistence/schema boundary, and implementation handoff; concrete storage selection remains downstream |
| FR-CB002 | Preserve checkpoint identity, conversation boundary, integrity, and lineage references | Should | Covered by the Session–Conversation engineering contract, persistence/schema boundary, and implementation handoff; concrete storage selection remains downstream |
| FR-CB003 | Create a non-destructive conversation branch from an eligible checkpoint without altering the source conversation | Should | Covered by the Session–Conversation engineering contract, persistence/schema boundary, and implementation handoff; concrete storage selection remains downstream |
| FR-CB004 | Reject unauthorized, stale, expired, invalid, or conflicting checkpoint operations without mutating the source | Should | Covered by the Session–Conversation engineering contract, persistence/schema boundary, and implementation handoff; concrete storage selection remains downstream |
| FR-CB005 | Make repeated submission of the same operation identity safe without duplicate branch creation | Should | Covered by the Session–Conversation engineering contract, persistence/schema boundary, and implementation handoff; concrete storage selection remains downstream |
| FR-CB006 | Do not imply reversal of task, execution, context, memory, file, workspace, provider, Git, or external side-effect state | Must | Covered by the Session–Conversation engineering contract, persistence/schema boundary, and implementation handoff; concrete storage selection remains downstream |

## Skill Lifecycle Boundary

| ID | Requirement | Priority | Phase |
|---|---|---|---|
| FR-SK001 | Register, validate, discover, acquire, bind, revoke, and retire skills through the canonical Skill Registry lifecycle | Must | Existing Skill Registry/runtime phase |
| FR-SK002 | Allow Agent Runtime skill selection without requiring per-task manual user selection | Must | Existing Agent Runtime phase |
| FR-SK003 | Apply canonical tool, permission, sandbox, approval, and audit policy to skill use | Must | Existing security/runtime phase |
