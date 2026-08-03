# Context Management Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See also [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md) · [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md) · [../docs/SANDBOX_DEPTH.md](../docs/SANDBOX_DEPTH.md) (prompt-injection containment)

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
authoritative. Nothing is ever dropped silently — eviction from layer 2 always lands
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
