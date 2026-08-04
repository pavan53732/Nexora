
# Context Management Specification — Nexora

> **Status: CANONICAL** for read-time context assembly and projection.
> This document owns how context is built from memory, files, tasks, and history
> at the moment an agent loop iteration begins. It does NOT own memory write (memory writes are owned by MEMORY_SYSTEM.md)
> operations, summarization (summarization is owned by MEMORY_SYSTEM.md), retention (retention policy is owned by MEMORY_SYSTEM.md) policy, or tier promotion (promotion is owned by MEMORY_SYSTEM.md) (see
> [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md)).
>
> Depends on: [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md) (memory source).
> Referenced by: [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md), [../docs/api/Agent-API.md](../docs/api/Agent-API.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

**Context is a pipeline, not a transcript.** Nexora never keeps an unbounded
conversation; it layers context so that what matters is always available and what is
old is compressed — never lost. The golden rule:

> **Compress the conversation, never the state.**

The agent's goal, plan, decisions, and artifacts are **structured state** — persisted
exactly (checkpoints, WAL) and never summarized. Only conversational history is
progressively compressed. This is what lets an agent run for hours or days across
restarts without "losing context".

## 1. The Context Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. STRUCTURED STATE (never compressed)                           │
│    goal · plan · step index · decisions · artifacts ·            │
│    acceptance criteria · validation history                      │
│    ← persisted exactly in checkpoints (FR-CM-001)                │
├──────────────────────────────────────────────────────────────────┤
│ 2. WORKING SET (recent raw context)                              │
│    last N turns · active tool results · current file diffs       │
│    ← bounded by allocation budget (FR-CM-002)                    │
├──────────────────────────────────────────────────────────────────┤
│ 3. PROGRESSIVE SUMMARIES (rolling compression)                   │
│    older turns → rolling summary; summary-of-summaries as        │
│    the task grows (FR-CM-003)                                    │
├──────────────────────────────────────────────────────────────────┤
│ 4. RETRIEVAL LAYER (RAG over persistent stores)                  │
│    semantic memory · knowledge graph · tool/file history ·       │
│    project & long-term memory (FR-CM-004)                        │
└──────────────────────────────────────────────────────────────────┘
```

Layers 2–4 feed the Context Builder; layer 1 is loaded from the checkpoint and is
authoritative. Nothing is ever dropped silently — eviction (retention policy is owned by MEMORY_SYSTEM.md) from layer 2 always lands
in layer 3 or 4 first.

## 2. Token Budget Allocation (FR-CM-002)

`TokenBudget` (AGENT_RUNTIME.md) tracks usage; this spec defines **allocation** — the
priority order and reserved shares of the request window:

| Priority | Layer | Allocation | Policy |
|----------|-------|-----------|--------|
| 1 | Structured state | fixed, always included | Never evicted, never summarized |
| 2 | System prompt + skill/tool definitions | fixed | Included every request |
| 3 | Working set (recent turns + active tool results) | configurable (default 40 %) | Newest-first eviction into summaries |
| 4 | Retrieved memory (layer 4) | configurable (default 20 %) | Relevance-ranked; recall threshold per workspace |
| 5 | Progressive summaries (layer 3) | remainder | Summary-of-summaries when budget pressure persists |
| 6 | Truncation | hard ceiling | Only as a last resort, and only on layer 3 (never 1–2) |

Rules:

- **Reserved for response**: `maxTokensPerRequest - reservedForResponse` (1024 default)
  is the budget for layers 1–5 combined.
- When the allocation cannot fit, **summarization runs before truncation**; truncation
  is a logged, observable event (`context_truncated`), never silent.
- Allocation is visible via `context_stats` (TOOL-396).

## 3. Progressive Summarization (FR-CM-003)

| Aspect | Rule |
|--------|------|
| **Trigger** | Working set exceeds its allocation share (e.g. > 80 % of layer-3 share) |
| **Operation** | Oldest turns are condensed into a rolling summary by the agent (AI-assisted), preserving decisions, facts, and open questions — not prose |
| **Summary-of-summaries** | When the summary itself grows large, prior summaries are condensed again (bounded depth, default 3 levels) |
| **Idempotence** | Summaries are deterministic artifacts stored with the checkpoint; re-summarization only extends, never rewrites history |
| **Fidelity check** | After summarization, the agent verifies the summary still answers: *what is the goal, what was decided, what is next?* |
| **Frequency cap** | Max 1 summarization per N steps (default 5) to avoid churn |

Summaries live in memory (project tier, `memory_store`) tagged `type=summary` so they
are retrievable — summarizing is also a memory operation.

## 4. Resume Reconstruction (FR-CM-004)

After any restart (app kill, device reboot, checkpoint resume):

1. Load **structured state** from the latest checkpoint (authoritative).
2. Load the **rolling summary** for the task (layer 3).
3. Load the **working set** if persisted (partial results, recent tool outputs) —
   otherwise rebuild from tool/file history and memory retrieval.
4. Run **freshness checks** (below) against the actual sandbox/workspace state.

**Never replay raw history** to reconstruct context — replay is only used for
*recovering effects* (idempotency, AUTONOMY_STABILITY §7), not for context.

## 5. Freshness Checks (FR-CM-005)

Before each agent-loop iteration, the Context Builder re-validates referenced state:

| Check | What is re-validated |
|-------|----------------------|
| File state | Files referenced in the plan still exist; content hash unchanged unless the agent changed it |
| Task state | Dependencies and prior step results match the checkpoint |
| Provider state | Active provider profile still healthy (else reroute, see degradation ladder) |
| Sandbox state | Quota, processes, env unchanged since context build |

Stale references are refreshed or flagged to the agent (`context_stale` event) before
the next AI call — the agent never reasons against outdated context.

## 6. Context Tagging & Trust (FR-CM-006)

Every context chunk carries metadata:

| Tag | Example |
|-----|---------|
| Source | `user`, `tool_result`, `file`, `web`, `plugin`, `memory` |
| Timestamp | when the chunk was created |
| Trust level | `trusted` (user/system), `sandbox` (own tool output), `untrusted` (web/downloaded/plugin input) |
| Scope | workspace, session, global |

Untrusted content is **isolated in labeled segments** and injected as data, never as
instructions (extends prompt-injection containment, SANDBOX_DEPTH §3.3 / TM-025). The
agent's system prompt instructs that untrusted segments carry no authority.

## 7. Milestone Memory Curation (FR-CM-007)

The agent **actively curates memory at milestones**, not passively:

- At each step boundary: store structured facts (decisions, results, artifacts) with
  tags — not raw transcripts.
- At task completion: store a **lesson learned** via `memory_lessons` (TOOL-397) —
  feeds closed-loop learning (AUTONOMY_STABILITY §4).
- At session end: promote session memory to project memory (summary + key facts).

This keeps retrieval precise: memory contains curated knowledge, and the pipeline
never depends on raw history for recall.

## 8. Observability (FR-CM-008)

| Signal | Source |
|--------|--------|
| Per-layer token usage | `context_stats` (TOOL-396) |
| Summarization events | `context_summarized` event + execution history |
| Truncation events | `context_truncated` (audit-logged) |
| Stale-context events | `context_stale` |
| Context build latency | PERFORMANCE_BUDGET: context building target 100 ms |

## Phase Mapping

- **Phase 2**: Structured state + working set; TokenBudget allocation; freshness
  checks; resume reconstruction (FR-CM-001/002/004/005).
- **Phase 3**: Progressive summarization (FR-CM-003); context tagging/trust
  (FR-CM-006); milestone curation (FR-CM-007).
- **Phase 4**: Context observability tools (FR-CM-008).
- **Phase 6**: Retrieval-layer depth (memory + knowledge graph integration).

---

## 9. Response Grounding & Attribution (anti-hallucination in chat & coding)

Complements the Git grounding rules (specs/GIT.md GR-1..GR-6) for **all** agent
output — chat answers, code claims, and task reports. The principle is the same:
*every claim is traceable to a tool result or context segment in the same task.*

### RG-1 — Tool-before-claim (FR-GND-001)

A factual claim in any response must come from a **tool call in the same task** —
`memory_recall`, `search_text`, `file_read`, `code_search`, `search_web`,
`git_log` — or from a labeled context segment (system, user, trusted). Claims
resting only on the model's training memory are flagged as unverified, never
presented as fact.

### RG-2 — Citations & sources (FR-GND-002)

Grounded claims carry a **source reference**:

| Claim type | Source format |
|------------|---------------|
| From memory | `[memory:{entryId}]` |
| From file | `[file:{workspaceId}/{path}:{line}]` |
| From web | `[web:{url}]` |
| From tool result | `[tool:{toolId}]` |

If a claim cannot carry a source, it is stated as an opinion or unverified, not fact.

### RG-3 — Uncertainty disclosure (FR-GND-003)

The agent explicitly says **"I don't know"** or marks **low confidence** rather than
guessing. If a question is outside the available context, the agent offers the
retrieval action it *could* take (`memory_recall`, `search_web`) instead of
inventing an answer. Never fabricates files, SHAs, API signatures, or facts.

### RG-4 — Refuse unsupported (FR-GND-004)

Requests that require capabilities the current agent/sandbox cannot provide (missing
tool, missing permission, offline-only data) produce an explicit refusal with the
reason and the path to enable it — never a plausible-sounding made-up execution.

### RG-5 — Code-claim grounding (FR-GND-005)

Before claiming anything about the codebase (a symbol exists, an API is deprecated,
a signature is X, a pattern is used), the agent must verify via the code-intelligence
tools: `code_search` (TOOL-160), `code_symbols` (TOOL-151), `code_references`
(TOOL-153), or `file_read` — then cite the file. Code claims are additionally proven
by the SE pipeline (FR-EL-013: build + tests) before being reported as working.

### RG-6 — Plan-vs-actual honesty (FR-GND-006)

At task completion, the agent's report distinguishes:
**done & verified** (passed gates, sources cited) · **done & unverified** (flagged) ·
**attempted & failed** (with error) · **not attempted** (with reason).
Never reports unverified work as completed (ties to FR-AS-006 verification gates).

### Enforcement & observability

- System prompt enforces RG-1..RG-6 as hard constraints (same layer as untrusted-
  segment rules, §6).
- Unit/E2E tests verify the rules (see testing/UnitTests.md Git Grounding section,
  extended; testing/E2ETests.md grounding journeys).
- Violations are observable: responses without sources for factual claims are
  logged (`grounding_missing_source`), and the trust-growth score (FR-AS-005) is
  decremented.

---

## 10. Reasoning Before Answering (FR-RN-001..006)

Grounding (RG-1..RG-6) prevents *fabrication*; reasoning prevents *superficial*
answers. The agent deliberately thinks **before** answering, in proportion to the
question's complexity and stakes.

### RB-1 — Deliberation gate (FR-RN-001)

For every user message, the agent first classifies how much deliberation is needed
before producing the response:

| Classification | Behavior |
|----------------|----------|
| **Answer now** | Simple, fully grounded request (e.g. "summarize this file") — respond directly, still under RG rules |
| **Reasoning pass** | Complex, uncertain, multi-step, or risky — enter the reasoning pipeline (§10.2) |
| **Clarify first** | Genuinely ambiguous or underspecified — ask a clarifying question instead of guessing (ties to RG-3) |

The gate is a runtime decision (planner/context builder), not just prompt guidance.

### RB-2 — The reasoning pipeline (FR-RN-002)

```
Understand  → restate the question; identify assumptions and ambiguity
Clarify     → ask if genuinely ambiguous (never guess)
Retrieve    → gather evidence FIRST (memory / files / web / code tools)
Reason      → multi-step internal reasoning over the evidence
Draft       → structure the answer (claim → evidence → conclusion)
Verify      → self-check: every claim grounded (RG), contradictions caught
Answer      → with citations + confidence level
```

Reasoning happens *over evidence already in context* (retrieval first — the pipeline
never reasons from memory alone).

### RB-3 — Deliberation effort levels (FR-RN-003)

| Level | Use for | Behavior |
|-------|---------|----------|
| `fast` | simple chat, greetings, confirmations | direct answer, minimal reasoning |
| `balanced` (default) | most tasks | standard reasoning pipeline |
| `thorough` | complex/costly/risky tasks | deeper reasoning, multiple verification passes, optionally reasoning-capable model |

- Level is configurable per workspace, per agent, and per task (FR-RN-003).
- Effort is proportional to stakes — thinking is not uniformly expensive.

### RB-4 — Reasoning-capable models (FR-RN-004)

- `ProviderCapability.REASONING` added to the capability enum (PROVIDER_SYSTEM.md);
  providers that support multi-step reasoning (e.g. OpenAI o-series, Claude
  thinking, Gemini thinking, DeepSeek-R1) declare it.
- Task routing (FR-EL-005) and skill `preferredModelFamilies = ["reasoning"]`
  (models/Skill.md) select reasoning-capable models for `thorough` tasks; `fast`
  tasks use fast models. Provider-agnostic: works through any provider that
  declares the capability.
- A task tagged `reasoning_required` fails fast with a clear message if the active
  profile lacks REASONING (RG-4 refusal path) instead of silently answering
  without deliberation.

### RB-5 — Reasoning visibility (FR-RN-005)

- The reasoning trace is shown in the activity feed as a **collapsible card**
  ("reasoned N steps → expand"): the user sees *why*, progressive disclosure keeps
  the chat clean.
- Reasoning traces are stored in execution history (auditable, FR-M005) and count
  toward token usage (FR-P009) transparently.

### RB-6 — Answer-quality gates & meta-cognition (FR-RN-006)

Before sending, the answer must pass:

| Gate | Check |
|------|-------|
| Grounded | every factual claim has a source (RG-2) |
| Complete | answers the actual question asked (restated in RB-2) |
| Consistent | no self-contradiction; checked against prior statements in the session |
| Confident | confidence level stated for uncertain claims (RG-3) |

If a gate fails → revise, do not send. Additionally, meta-cognition:
- State assumptions explicitly when answering with partial information.
- Flag contradictions in the user's premise rather than silently agreeing.
- For critical outputs, self-consistency: generate 2 reasoning paths, emit the
  most consistent (used only for `thorough`/critical tasks, FR-RN-006).

### Enforcement & observability

- Same enforcement layer as §9: system-prompt hard constraints; `reasoning_effort`
  recorded per response; reasoning traces in execution history.
- Trust-growth score (FR-AS-005) adjusts with reasoning quality (gates passed,
  clarifications used, contradictions flagged).

---

## 11. Evidence & Validation Engine (FR-EV-001..006)

Anti-hallucination is a **runtime policy, not a prompt**. The Evidence & Validation
Engine (`com.nexora.app.runtime.evidence`) is the single module that owns the
mechanics — it sits between the agent loop and the user, and it enforces the RG/RB
rules as code, not as instructions.

```
User → Agent → Planner → Evidence & Validation Engine → Tool Manager → Sandbox/Browser/Files/APIs
                                                              ↓
                                           Verified Evidence → LLM Response → User
```

### EV-1 — Statement classification (FR-EV-001)

Every significant statement in a response is classified **as structured metadata**:

| Class | Meaning | Example |
|-------|---------|---------|
| `VERIFIED` | Confirmed by a tool result / context segment in this task | "Found in workspace file." |
| `DERIVED` | Inferred from evidence (build logs, diffs, tool outputs) | "Inferred from build logs." |
| `ESTIMATED` | Best-effort judgment with stated basis | "Likely caused by dependency mismatch." |
| `UNKNOWN` | Cannot be determined from available information | "Cannot determine from available information." |
| `USER_PROVIDED` | Stated by the user; not independently verified | "Provided by the user." |

Statements ship with a `Statement` record: `(text, classification, source, confidence)`.
Unclassified significant claims are blocked by the engine (FR-EV-001).

### EV-2 — Structured confidence scores (FR-EV-002)

Every major conclusion carries a confidence score as **data** — `HIGH`, `MEDIUM`,
`LOW` — not prose. The score drives autonomy decisions:

| Confidence | Autonomy behavior |
|-----------|-------------------|
| `HIGH` | Proceed automatically (within autonomy mode) |
| `MEDIUM` | Proceed but flag the uncertainty to the user |
| `LOW` | **Ask before proceeding** — request confirmation or gather more evidence first (ties to FR-S016 autonomy modes, FR-AS-003) |

Confidence is computed by the engine from evidence strength + classification, not
stated by the model alone.

### EV-3 — Zero-assumption mode (FR-EV-003)

When required information is missing, the engine forces the agent to: identify the
missing information → explain why it is needed → ask for it or gather it via tools →
continue only when sufficient. The engine rejects outputs that invent missing
details (e.g. "Your project probably uses Hilt." → must instead state it could not
be identified from available files).

### EV-4 — Consolidated guardrails (FR-EV-004)

The engine enforces these rules on every response (no exceptions):

1. Do not fabricate files, classes, or APIs.
2. Do not claim a tool executed unless it actually did (from tool history, FR-M011).
3. Do not report a build as successful without build results.
4. Do not report tests passed without test output.
5. Do not claim code was modified without recording the affected files.
6. Do not invent repository structure.
7. Do not invent package names or dependencies.

Violations are logged (`evidence_guardrail_violation`) and decrement the trust score
(FR-AS-005).

### EV-5 — Fact vs recommendation labeling (FR-EV-005)

Responses distinguish output types: **Verified fact** · **Analysis** · **Recommendation**
· **Speculation** (explicitly labeled as such). Users always know the basis of each
statement.

### EV-6 — Completion validation & reviewer handoff (FR-EV-006)

Before reporting completion, the engine verifies: acceptance criteria met (FR-EL-011),
verification gates passed (FR-AS-006), report status matches plan-vs-actual (RG-6),
and — for documentation-affected work — **documentation updated** (CHANGELOG,
README, ADRs, specs, API docs as applicable; FR-AG-004). For tasks classified **important** (by sensitivity, risk, or cost), the
engine **requires a reviewer agent pass** (AGT-004 Reviewer) before the result
reaches the user — no user-facing completion until the review is done.

### Auditability

Everything the engine does is written to the audit trail: statement classifications,
confidence scores, assumption events, guardrail violations, and reviewer handoffs —
one consistent mechanism for coding, research, and general chat.
