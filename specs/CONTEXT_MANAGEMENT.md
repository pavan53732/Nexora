> **Status: CANONICAL** for Read-time context assembly, Grounding (RG), Reasoning (RB), and the Evidence & Validation Engine (EV).
> This document owns how the context window is budgeted, progressively summarized, tagged, and isolated. 
> It also owns anti-hallucination citations, the deliberation pre-pass gate, and output statement classification.
>
> Depends on: [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md), [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md).
> Referenced by: [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md), [../specs/EXECUTION_LIFECYCLE.md](EXECUTION_LIFECYCLE.md).

# Context Management Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md) · [../specs/EXECUTION_LIFECYCLE.md](EXECUTION_LIFECYCLE.md)

---

## 1. Overview

Autonomous agents rely heavily on their active context window. If the context window is unstructured, lacks provenance, or overflows, agents suffer from prompt-injection exploits, drift, and severe hallucinations. 

This specification defines Nexora's complete read-time context assembly pipeline: **Token Budgeting**, **Progressive Summarization**, **Context Tagging and Trust Isolation**, **Response Grounding (RG)**, **Reasoning Pipelines (RB)**, and the **Evidence & Validation Engine (EV)**.

---

## 2. Deterministic Context Assembly Layer

This upgrade formalizes a **Deterministic Context Assembly Layer (CAL)**. CAL is the canonical read-time process that constructs model input from higher-authority persisted sources without turning compaction artifacts into the sole source of truth.

### Authority distinction

CAL MUST distinguish between:

1. canonical conversation history;
2. working context;
3. retrieved context;
4. summarized context;
5. compressed context;
6. evidence;
7. decisions;
8. requirements;
9. constraints;
10. memory;
11. tool results;
12. execution state.

Summaries and compressed context are **derived context views**. They MUST NOT become the only recoverable representation of a conversation when canonical conversation history exists.

### Required context categories

For each model invocation, CAL assembles from explicit categories:

- current user request;
- active task;
- immutable conversation facts;
- relevant prior messages;
- active requirements;
- active constraints;
- locked decisions;
- relevant evidence;
- relevant memories;
- relevant tool results;
- current execution state;
- required output contract.

### Token budgeting and truncation

Token pressure is handled as an **assembly problem**, not as destructive deletion of canonical history.

CAL MUST define:

- selection rules;
- priority ordering by authority and recency;
- per-category token budgets;
- truncation rules for low-authority duplicate material;
- compaction rules for derived views;
- reconstruction rules back to canonical sources;
- provenance for every included context object;
- invalidation and freshness rules;
- conflict surfacing when high-authority sources disagree.

### Provenance requirement

Each context object included in model input SHOULD carry enough metadata to answer: **what source caused this context to enter the model input?**

Minimum provenance fields:

- source category;
- source identifier;
- source version or checkpoint;
- retrieval reason;
- freshness timestamp or sequence;
- authority level.


## 2.1 Context Window Token Budget Allocation (FR-CM-002)

To avoid context overflow (`NXR-1006`) and maximize recall accuracy, the context window is assembled as five distinct, priority-ordered layers. Truncation is restricted strictly to Layer 5.

```text
┌────────────────────────────────────────────────────────┐
│ Layer 1: System Prompt & Hard Constraints              │  (100% uncompressible)
├────────────────────────────────────────────────────────┤
│ Layer 2: Current Goal, Plan, & Step Status             │  (100% uncompressible)
├────────────────────────────────────────────────────────┤
│ Layer 3: Active Working Set (Latest Tool Outputs, etc) │  (uncompressible)
├────────────────────────────────────────────────────────┤
│ Layer 4: Semantic Memory Retrieval (Recall Segment)    │  (configurable limit)
├────────────────────────────────────────────────────────┤
│ Layer 5: Progressive Rolling Summary (Older step log)  │  (progressive truncation)
└────────────────────────────────────────────────────────┘
```

### Allocation Rules

- **Layer 1 (System Prompt)**: Holds core safety instructions, STRIDE threat mitigations, and the tool registry. Always injected verbatim.
- **Layer 2 (State Checkpoint)**: Holds the current structured execution plan, step list, and checkpoint variables. Never compressed (`FR-CM-001`).
- **Layer 3 (Active Working Set)**: Holds file buffers, active directory lists, and the immediate preceding step output. 
- **Layer 4 (Retrieval Segment)**: Filled with workspace semantic memory entries (`FR-M002`) relevant to the current step, capped at 20% of the active context window.
- **Layer 5 (Rolling Summary)**: Holds the summarized history of older conversation and execution logs. If the sum of all layers exceeds 75% of the model's total token context, Layer 5 is compressed using progressive summarization.

---

## 3. Progressive Summarization Pipeline (FR-CM-003)

**Hierarchical Context Compaction & Semantic Memory Distillation** prevents context overflows while preserving critical plan history.

- **Trigger Threshold**: When the active context exceeds 75% of the provider model's max token limit, the oldest 20% of Layer 5 content is selected for compaction.
- **Rolling Compactor**: A local summarization prompt is run to generate a dense, bulleted Markdown summary of the historical events. Older tool outputs and intermediary reasoning steps are automatically distilled into persistent SQLite `memory_lessons` (`TOOL-409`) and knowledge graph entities.
- **Idempotency & Fidelity Check**: Before the summarized chunk is persisted, a validation pass checks that no core plan variables or status parameters were dropped or mutated. If drift is detected, the compaction is rolled back, and a warning is logged.
- **Resume Reconstruction (FR-CM-004)**: Upon agent resume from a crash, the context window is reconstructed from the `Checkpoint + Summary + semantic memories`. The raw, unsummarized history is never replayed.

### Long-Horizon Task and Artifact Projection

Long-running work MUST be reconstructable without relying on the model’s conversational recall alone. CAL therefore maintains a derived long-horizon projection over the existing `Task`, `Workflow`, `Execution`, `ContextSnapshot`, execution-checkpoint, `Memory`, `ClaimRecord`, and artifact records. This projection is not a new lifecycle, identity, or ownership authority; it is a resumable view assembled from the owning artifacts.

For each active long-running task, the projection MUST preserve the current goal, phase/step status, acceptance-criteria status, active constraints, locked decisions, open clarification questions, evidence gaps, delegated-child summaries, artifact references, latest verified outputs, unresolved failures, next eligible action, and the source checkpoint or execution identity from which each item was derived. Large outputs SHOULD remain as permissioned artifact references rather than being copied repeatedly through coordinator or conversation context.

Compaction MUST preserve this projection before compressing older conversational or execution detail. A reconstructed context MUST be able to identify what was completed, what was only proposed, what evidence is still missing, which delegated work is active or failed, which artifacts are authoritative, and what action is safe to perform next. If reconstruction cannot establish those facts, the runtime MUST pause for clarification or recovery rather than infer continuity.

When a clean sub-agent context is created for an independent delegated task, the handoff MUST carry the relevant projection subset, evidence references, constraints, acceptance criteria, and artifact destinations. The sub-agent MUST return structured results and artifact references; the coordinator MUST not treat an unreferenced free-form summary as equivalent to persisted evidence.

---

## 4. Context Tagging, Metadata, & Trust Isolation (FR-CM-006)

All inputs injected into the context window are structured with explicit XML tags carrying metadata. This provides strict provenance tracking and prompt-injection containment.

### Labeled Context Segment

```xml
<context_segment source="file_read" path="src/app.kt" trust="TRUSTED" occurred_at="2026-08-05T14:00:00Z">
// File contents here
</context_segment>

<context_segment source="web_scrape" url="https://example.com" trust="UNTRUSTED" occurred_at="2026-08-05T14:15:00Z">
<untrusted_content>
// Raw scraped web text here
</untrusted_content>
</context_segment>
```

### Isolation Constraints

- **`<untrusted_content>` Gating**: Any content retrieved from external sources (web scrapes, downloads, third-party plugin repositories) MUST be enclosed within the `<untrusted_content>` block.
- **Instruction Stripping**: The system prompt instructs the provider model to treat text inside `<untrusted_content>` strictly as passive data. The model is forbidden from executing commands or following directives found inside untrusted blocks.
- **Freshness Validation (FR-CM-005)**: Before any loop iteration, the `ContextBuilder` re-validates that all referenced files, workspace parameters, and provider statuses have not drifted. Stale segments are marked `EXPIRED` and re-fetched.
- **Tool and introspection result boundary**: Browser/search results, Tool outputs, imported database records or schemas, Git/Terminal content, plugin-repository content, and ProjectContext/introspection summaries are context data, not instructions or canonical authority. Before inclusion in a `ContextSnapshot`, each result MUST retain source, trust, freshness, authority, and evidence classification metadata. Instruction-like text inside a result MUST remain passive untrusted content and MUST NOT authorize a Tool, change a permission, alter a lifecycle/requirement/decision, or bypass verification. A result with missing provenance, stale freshness, unresolved contradiction, or insufficient evidence remains non-authoritative and is blocked or qualified by the existing Evidence & Validation Engine.

## Stale Evidence Precedence

When evidence conflicts due to staleness, the following rules apply:

### Authority Preservation

1. **Canonical-source authority is preserved.** Freshness and verification status are metadata used for retrieval and conflict handling; they do NOT override canonical-source authority. Canonical requirements, decisions, and specifications cannot be displaced merely because another artifact is newer.
2. **Locked DEC-* decisions remain authoritative** according to repository authority rules (`docs/CANONICAL_SOURCES.md`). A stale canonical source remains authoritative until the repository's canonical authority is explicitly superseded.
3. **Derived context, retrieved content, tool results, memory, summaries, and other contextual artifacts cannot silently redefine canonical behavior.**

### Conflict Handling Among Contextual Artifacts

Where canonical authority is not directly at stake, the following precedence applies among contextual artifacts:

1. **Canonical conversation facts** (immutable message history) override all derived context.
2. **Fresh tool results** override stale tool results from the same tool.
3. **Fresh memory entries** override stale memory entries of the same kind.
4. **Fresh summaries** override stale summaries of the same source.
5. **Verified evidence** overrides unverified or contradicted evidence.

### Definitions

- **Authority**: The right to define normative behavior, owned by canonical documents (`docs/CANONICAL_SOURCES.md`).
- **Provenance**: The origin and lineage of evidence (e.g., tool result, memory entry, summary).
- **Freshness**: A retrieval classification indicating whether evidence has been recently validated or re-fetched.
- **Verification status**: Whether evidence has been validated against its source or through independent checks.
- **Conflict status**: Whether evidence contradicts other evidence or canonical authority.

### Conflict Resolution

Staleness is determined by:

- explicit freshness timestamps or sequence numbers;
- invalidation events from the source subsystem;
- detection of contradictory newer evidence.

Stale evidence that cannot be refreshed enters a conflict state and MUST NOT silently override fresh evidence. Conflicting evidence MUST preserve provenance and authority rather than being resolved by freshness alone. The runtime escalates unresolved conflicts when they affect task completion criteria or canonical authority.


---

## 5. Response Grounding (RG) citation Rules (FR-GND-001..FR-GND-006)

To prevent hallucinations, agents must ground every factual assertion in verified tool outputs or secure memory segments.

- **Tool-before-Claim (FR-GND-001)**: Every factual claim made in chat (e.g. "Line 12 has an error") MUST correspond to a verified tool output (e.g. `file_read` or `lint_run`) within the active task history. General training memory cannot be cited as fact.
- **Structured Citations (FR-GND-002)**: Grounded claims MUST attach an explicit citation marker pointing to the originating tool execution or memory record (e.g. `[file_read:src/app.kt:12]`). Unsourced assertions are flagged as opinion or unverified.
- **Uncertainty Disclosure (FR-GND-003)**: If a supporting tool result or memory segment is absent, the agent MUST explicitly declare uncertainty (e.g., "I don't know") and offer an explanatory retrieval tool call rather than guessing.
- **Plan-vs-Actual Honesty (FR-GND-006)**: The final completion report MUST strictly differentiate between:
  - `DONE-VERIFIED` (Implemented and verified by tests/build exit code 0)
  - `DONE-UNVERIFIED` (Implemented but untested)
  - `ATTEMPTED-FAILED` (Attempted but failed validation checks)
  - `NOT-ATTEMPTED` (Dropped from plan due to constraints)

---

## 6. Deliberation Gate & Reasoning Pipeline (FR-RN-001..FR-RN-006)

All inbound user messages are passed through an initial, fast **Deliberation Gate** to determine the necessary reasoning depth before initiating plan execution:

```
Inbound User Message
         │
         ▼
 Deliberation Gate (Classification Pass)
         │
         ├─── FAST ───────► Answer Immediately (no tools, e.g. "Hi")
         │
         ├─── BALANCED ───► Plan → Execute Tool Loop → Verify → Answer
         │
         └─── THOROUGH ───► Route to REASONING Model → Complete Plan Repair → Reviewer Pass
```

### Effort Levels & Routing

- **FAST (no-tool pass)**: Used for simple clarifications, greetings, or basic read requests.
- **BALANCED (standard loop)**: Executes the normal plan → act → observe cycle using standard cost-efficient models.
- **THOROUGH (reasoning-capable loop)**: Reserved for high-stakes, multi-agent, coding, or security tasks. The `ProviderRouter` automatically routes these tasks to REASONING-capable models (`FR-RN-004`).
- **Reasoning Artifact Visibility (FR-RN-005)**: Nexora stores and renders a redacted `ReasoningSummary` containing approach, evidence, decisions, uncertainty, and verification results. Raw private model chain-of-thought is neither required nor persisted.
- **Answer-Quality Gates (FR-RN-006)**: Outbound answers must undergo consistency and confident self-review checks prior to transmission. Premise contradictions in user prompts must be explicitly flagged and corrected rather than assumed correct.

### Reasoning Effort Scale (FR-RN-007, FR-RN-008)

The deliberation effort control is a 6-level scale, user-selectable and model-mapped.
`OFF` disables reasoning entirely; the remaining levels raise the reasoning budget and
routing preference for REASONING-capable models (`ProviderCapability.REASONING`).

| Level | Gate behavior | Provider routing | Reasoning artifact |
|-------|---------------|------------------|-----------------|
| `OFF` | Reasoning disabled — deliberation gate bypassed; messages take the FAST path unconditionally; REASONING models never selected | Standard models only; `reasoning_effort`/`thinking` parameters omitted from requests (not merely zeroed) | None produced |
| `LOW` | FAST for simple; BALANCED otherwise | Standard models; reasoning parameters set to provider minimum where supported | Stored, collapsed by default |
| `MEDIUM` | FAST / BALANCED classification (default) | Standard models; moderate reasoning budget | Stored, collapsed |
| `HIGH` | BALANCED default; THOROUGH on elevated stakes | Prefers REASONING-capable models when available (falls back per FR-RN-004 fail-fast rule) | Stored, expanded on completion |
| `X_HIGH` | THOROUGH default | REASONING model required; fail-fast if none configured | Stored, expanded |
| `MAX` | THOROUGH + bounded extended self-consistency (RB-6 on every outbound answer) | REASONING model required; maximum configured reasoning budget | Redacted summary stored and expanded; private chain-of-thought not retained |

**Default:** `MEDIUM` for new workspaces/agents (preserves the pre-scale BALANCED behavior).

**Override hierarchy** (first non-null wins, mirroring the PermissionModel layering):

```
task override → agent override → workspace override → global settings → DEFAULT (MEDIUM)
```

- A task-level override applies for that task only; an agent-level override pins the level for everything that agent runs; workspace and global levels are the standing defaults.
- `OFF` at any layer is absolute for that scope: even a THOROUGH-classified message executes without reasoning passes (the Evidence & Validation Engine's grounding and verification gates — RG/EV rules — remain fully active; `OFF` removes deliberation depth, never evidence discipline).
- Provider compatibility: if the active model lacks `REASONING` capability, levels above `MEDIUM` degrade gracefully to the model's maximum and a notice is logged (FR-RN-004 fail-fast applies only at `X_HIGH`/`MAX`, where the user explicitly demanded a reasoning model).
- Token accounting: higher levels consume more reasoning tokens; usage is tracked per level (FR-P009) and surfaced in the activity feed trace header.

**User surface (FR-RN-008):** Settings → Model Config → Reasoning exposes the level selector (with `OFF` first), the effective-level indicator showing which layer currently governs, and per-agent/per-workspace override entries. Level changes apply to new messages immediately; running tasks keep their start-of-task level. Per ADR-0006 there is no slash-command or chat-embedded toggle — the selector lives in Settings.

---

## 6.1 Executable ReasoningPolicy (FR-RN-009, FR-RN-010)

The effective effort level resolves to a bounded policy persisted at task start:

| Level | Provider calls | Repair cycles | Verifier passes | Independent critic |
|---|---:|---:|---:|---|
| `OFF` | 1 | 0 | Evidence gate only | No |
| `LOW` | 1 | 1 | 0–1 | No |
| `MEDIUM` | 1–2 | 2 | 1 | Optional |
| `HIGH` | 2–3 | 3 | 1 | Critical claims |
| `X_HIGH` | 3–4 | 3 | 2 | Required |
| `MAX` | Configured bounded maximum | 3 | 2–3 | Diverse-model critic |

`ReasoningPolicy` caps reasoning tokens, Tool calls, wall-clock time, repair/verifier
cycles, provider calls, and applicable device/resource safety ceilings. Usage and
provider-cost metadata MAY be recorded and displayed, but no internal credit or
financial-cost threshold blocks, pauses, downgrades, or terminates a technically valid
progressing execution. Technical exhaustion follows FR-AS-003 and never silently
expands the policy.

#### Non-overridable Policy Ceilings

The runtime MUST apply non-overridable safety ceilings for provider calls, reasoning tokens, Tool calls, repair cycles, verifier passes, wall-clock time, and device/resource class. Task, agent, workspace, and global settings MAY reduce an effective ceiling but MUST NOT increase it. Invalid or over-ceiling policies are rejected before execution and the effective policy is recorded in the immutable `ContextSnapshot`.

Critic disagreement triggers bounded repair, then clarification/escalation.
Confidence is derived from evidence coverage, verifier results, contradiction checks,
and source quality—not provider self-confidence alone (FR-RN-012). For long-running projects, the runtime MUST enforce an adversarial validation gate before committing mutating side-effects (e.g., file writes, Git commits, database migrations).

### Cross-document execution-mode mapping

The Context Management deliberation labels are routing classifications, not a second lifecycle or execution-mode owner. `FAST` maps to Agent Runtime `FAST`; `BALANCED` maps to Agent Runtime `NORMAL`; and `THOROUGH` selects Agent Runtime `DEEP` when additional reasoning is required and the existing verification gate selects `VERIFY` when independent validation is required. Agent Runtime `RECOVER` is entered only through the existing failure, checkpoint, fallback, or context-reconstruction path and is not a user-facing deliberation label. The six Context Management effort levels (`OFF`, `LOW`, `MEDIUM`, `HIGH`, `X_HIGH`, `MAX`) select bounded `ReasoningPolicy` values and provider routing; they do not create additional lifecycle states. NFR-CI-006 and `architecture/AGENT_RUNTIME.md` remain authoritative for minimum-sufficient mode selection, while Context Management owns effort-level and context-assembly projections.

## 6.2 ReasoningSummary Privacy (FR-RN-011)

The durable artifact records approach, evidence references, decisions, high-level
alternatives, uncertainty, verification, usage, and redaction status. It MUST exclude
credentials, hidden system prompts, raw untrusted content, and unrestricted private
chain-of-thought. Provider-native private reasoning stays transient unless a provider
returns an explicitly user-shareable summary.

## 6.3 ContextSnapshot Compiler (FR-CM-010..012)

Every provider request references an immutable `ContextSnapshot` containing model and
tokenizer identity, token limits, output/reasoning reservations, included/excluded
segments, token counts, relevance/diversity scores, trust/freshness, evidence class,
content hashes, and compaction lineage.

Allocation is model-aware: hard constraints and structured state remain exact; Tool
schemas, active working set, retrieval, summary, multimodal input, expected output, and
reasoning reserve compete within the actual model/tokenizer budget. Retrieval deduplicates
near-identical memories and preserves source diversity. Every exclusion has a reason.
Snapshots are reproducible from durable segment IDs and hashes.

## 7. Evidence & Validation Engine (EV) (FR-EV-001..FR-EV-006)

The Evidence & Validation Engine assigns a structured confidence and verification classification to all significant assertions crossing the API and boundary layers.

### Statement Classifications (FR-EV-001)

- **`VERIFIED`**: Claim is backed by executable proof (e.g. "Build succeeds with exit code 0" backed by `build_compile` output).
- **`DERIVED`**: Claim is logically derived from verified facts (e.g. "Modifying class X will affect class Y" backed by `code_dependencies` output).
- **`ESTIMATED`**: Claim is based on heuristics, historical trends, or non-deterministic variables (e.g. "Task will take 5 seconds" based on latency logs).
- **`UNKNOWN`**: Claim has no supporting data. Assertions of category `UNKNOWN` are blocked from crossing the user boundary.

### Operational Enforcement

- **Structured Confidence (FR-EV-002)**: Claims carry confidence scores (`HIGH` / `MEDIUM` / `LOW`). Any score of `LOW` automatically triggers an `ASK` approval prompt or a clarification gate.
- **Zero-Assumption Mode (FR-EV-003)**: The engine blocks the agent from filling in missing specifications with assumed values. If the goal lacks clarity, the engine halts the loop, states the ambiguity, and prompts the user for instructions.
- **Completion Validation (FR-EV-006)**: Before a task is marked completed, the `Reviewer` agent evaluates the evidence log against the task's initial validation criteria. If important, a manual or separate `Reviewer` pass is a hard gate before the user-facing completion notification is unlocked.

### Claim-to-Evidence Binding

Every significant user-facing factual claim MUST have a claim record containing a stable claim identifier, evidence references, evidence class, source authority, freshness status, contradiction status, verifier result, confidence classification, and user-facing disposition. A general evidence list or provider self-confidence is not sufficient to establish claim support. The derived `ClaimRecord` projection is defined in `../models/Inference.md`, persisted as the standalone `claim_record` artifact in `../specs/DATABASE_SCHEMA.md`, and carried or referenced by terminal Agent protocol/API events; validation is planned through `UT-EV-007` and `E2E-REL-009`.

Claims classified `UNKNOWN`, contradicted, or below the applicable confidence gate MUST NOT be presented as verified fact. They MUST be clarified, explicitly labeled as uncertain analysis, or withheld. Claim records preserve provenance without persisting unrestricted private chain-of-thought.

---

## 8. Project Introspection (Pre-Flight Pass) (FR-CM-009)

Before the Planner creates an ExecutionPlan, the runtime runs a **pre-flight
introspection pass** over the workspace. The `ProjectIntrospector` is an
enhancement of the Context Builder — not a separate pipeline stage — that reads
the project's structure and populates a lightweight `ProjectContext` in working
memory. This gives the Planner richer initial context without changing the
existing agent-first loop.

### Introspection Flow

```
User Goal (from Chat inside Workspace)
    │
    ▼
ProjectIntrospector ──reads──> API schemas, DB schemas, configs,
                               build files, UI layouts, domain models,
                               infrastructure files
    │
    ▼
ProjectContext populated in working memory (Layer 3 — Active Working Set)
    │
    ▼
Knowledge Graph query ──retrieves──> relevant past entities, relationships,
                                      and facts (FR-M014/M015, Phase 4)
    │
    ▼
Planner (now has richer context) ──creates──> ExecutionPlan
    │
    ▼
  [existing agent loop continues — Coordinator → Coder → Tester → Reviewer]
```

### ProjectContext Shape

```kotlin
data class ProjectContext(
    val workspaceId: String,
    val apiSchemas: List<ApiSchemaSummary>,       // OpenAPI, GraphQL, gRPC
    val databaseSchemas: List<DbSchemaSummary>,   // table/column/index info
    val configFiles: List<ConfigFileSummary>,     // YAML, JSON, TOML, .env
    val buildFiles: List<BuildFileSummary>,       // Gradle, Make, CMake
    val uiLayouts: List<UiLayoutSummary>,         // Compose, XML layouts
    val domainModels: List<DomainModelSummary>,   // entity classes, interfaces
    val infrastructureFiles: List<InfraFileSummary>, // Docker, CI/CD, deploy configs
    val populatedAt: Instant
)
```

Each summary type carries the file path, parsed structure, and a confidence
score — `DERIVED` (structured format, machine-parsed) or `ESTIMATED`
(heuristic interpretation). The Evidence & Validation Engine (§7) applies
the same classification rules.

### Introspection Tools (Category 28 — Project Introspection)

Seven tools invoke the readers. Each tool is a standard `Tool` implementation
executing in the sandbox with `sandbox:read` permission:

| ID | Tool | Reads | Phase |
|----|------|-------|-------|
| TOOL-410 | `introspect_api` | OpenAPI, Swagger, GraphQL schemas, gRPC protos | 4 |
| TOOL-411 | `introspect_database` | SQL schema files, migration files, Room entities | 4 |
| TOOL-412 | `introspect_config` | YAML, JSON, TOML, .env, .properties files | 4 |
| TOOL-413 | `introspect_build` | build.gradle.kts, pom.xml, Makefile, CMakeLists.txt | 4 |
| TOOL-414 | `introspect_ui` | Compose @Composable, XML layout files, theme definitions | 4 |
| TOOL-415 | `introspect_domain` | Kotlin/Java data classes, interfaces, enums, sealed classes | 4 |
| TOOL-416 | `introspect_infrastructure` | Dockerfile, docker-compose.yml, CI configs, deploy scripts | 4 |

All seven tools return structured JSON with `filePath`, `parsedStructure`,
`confidence` (DERIVED/ESTIMATED), and `warnings`. They run in parallel during
introspection — no ordering dependency between readers.

### Phase Mapping

- **Phase 2**: ProjectIntrospector interface defined (FR-CM-009).
- **Phase 4**: All 7 introspection tools implemented; Knowledge Graph retrieval
  integrated; ProjectContext populated before planning.

### Design Rules

1. **Not a separate pipeline stage.** The ProjectIntrospector is part of the
   Context Builder — it enriches Layer 3 (Active Working Set) before the
   Planner runs. It does not alter the agent-first loop or the Coordinator role.
2. **Read-only.** Introspection tools require only `sandbox:read`. No file
   mutations, no tool chaining, no provider calls during introspection.
3. **Best-effort.** If a workspace has no API schemas, that reader returns an
   empty list — introspection never blocks. Missing readers are not errors.
4. **Evidence-tagged.** Every summary carries the EV classification (DERIVED
   or ESTIMATED); the Planner treats ESTIMATED fields as advisory, not
   authoritative.
5. **KG query after introspection.** The Knowledge Graph is queried AFTER the
   ProjectContext is populated, so entity extraction can reference the fresh
   file paths and schema names.


## Context Drift Protection

CAL MUST explicitly protect against:

- lost requirements;
- lost constraints;
- stale summaries;
- stale memories;
- contradictory memories;
- outdated decisions;
- stale tool results;
- cross-conversation contamination;
- cross-agent contamination;
- subagent context loss;
- agent handoff drift;
- branch contamination.

If conflicts are detected, CAL MUST surface an explicit conflict state rather than silently choosing one source.
