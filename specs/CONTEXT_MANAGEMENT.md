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

## 2. Context Window Token Budget Allocation (FR-CM-002)

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

Progressive summarization prevents context overflows while preserving critical plan history.

- **Trigger Threshold**: When the active context exceeds 75% of the provider model's max token limit, the oldest 20% of Layer 5 content is selected for compaction.
- **Rolling Compactor**: A local summarization prompt is run to generate a dense, bulleted Markdown summary of the historical events.
- **Idempotency & Fidelity Check**: Before the summarized chunk is persisted, a validation pass checks that no core plan variables or status parameters were dropped or mutated. If drift is detected, the compaction is rolled back, and a warning is logged.
- **Resume Reconstruction (FR-CM-004)**: Upon agent resume from a crash, the context window is reconstructed from the `Checkpoint + Summary + semantic memories`. The raw, unsummarized history is never replayed.

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
- **Reasoning Trace Visibility (FR-RN-005)**: The reasoning traces generated by the reasoning models are captured, stored in the execution history, and rendered to the user as collapsible logs in the chat activity feed.
- **Answer-Quality Gates (FR-RN-006)**: Outbound answers must undergo consistency and confident self-review checks prior to transmission. Premise contradictions in user prompts must be explicitly flagged and corrected rather than assumed correct.

---

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
