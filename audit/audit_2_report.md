# Audit 2 Report — Deep Semantic Consistency Audit

## Scope and Method

This pass audits the repository at commit `af9a699` on `main`. All 134 tracked Markdown documents were read completely again. The audit then compared meaning across canonical architecture, state machines, models, protocols, APIs, SDKs, registries, errors, security, requirements, testing, diagrams, and the Full Environment documentation.

The review does not treat token presence as semantic proof. Extracted tables, identifiers, and references were used only to locate and organize concepts already read in context. Findings are reported only where the documents collectively leave a contradiction, undefined mapping, or unverifiable implementation obligation.

## Repository Integrity

The repository contains 134 Markdown documents and approximately 12,509 Markdown lines. The normalized Markdown graph has 649 internal edges and zero broken relative links. The documentation is structurally connected, but several connected layers do not share explicit semantic contracts.

The central audit question was: can an implementer, without inventing policy, derive one deterministic state model, error model, security model, execution protocol, persistence model, and test evidence chain from the repository?

## Critical Finding 1 — The Evidence System Cannot Prove Completion

The requirement documents contain 274 distinct requirement-like identifiers. The traceability matrix contains 12 identifiers, leaving 262 requirements unrepresented. Testing documents contain only 10 identifiers, leaving 264 requirements without explicit test linkage. The threat model contains 28 threat identifiers, but security tests contain no `TM-*` references.

This means the repository cannot prove the complete chain `requirement/threat → canonical behavior → implementation → executable test → observed result`. A test inventory or scenario description is not sufficient evidence without an identifier, expected result, failure behavior, contract owner, and implementation target.

**Required action:** create a complete evidence matrix for every FR, NFR, TM, and TOOL identifier, with canonical source, lifecycle/model/protocol/API links, implementation owner, test case, expected result, failure condition, artifact location, and status.

## Critical Finding 2 — Error Semantics Stop at the Catalog Boundary

`errors/ERROR_CODES.md` defines 78 canonical `NXR-*` codes. Protocol, API, and SDK documents do not reference the canonical codes. Testing references only two codes and security documents reference six. The catalog provides recovery descriptions, but public contracts do not carry a stable mapping for error identity, retryability, idempotency, lifecycle effect, audit sensitivity, or cleanup.

This creates semantic drift even if every layer uses the word “error.” An API caller cannot derive whether a failure is retryable; a protocol consumer cannot know the wire representation; an SDK cannot know which exception maps to which code; and a background service cannot know whether to restore a checkpoint, cancel, or retry.

**Required action:** define a canonical error envelope and map every public operation and protocol failure to one or more `NXR-*` codes and recovery rules. Test those mappings.

## Critical Finding 3 — Agent Lifecycle, Model Status, and Runtime Phase Are Three Different Vocabularies

The canonical Agent lifecycle contains `Created`, `Configured`, `Ready`, `Running`, `Paused`, `WaitingApproval`, `Reflecting`, `Completing`, `Completed`, `Failed`, and `Cancelled`. The Agent model contains `IDLE`, `THINKING`, `EXECUTING`, `WAITING`, `ERROR`, and `CANCELLED`. The runtime architecture also describes loop activities such as planning, reflection, tool execution, and completion.

The documents never establish whether the model enum is a persisted projection, whether runtime activities are phases, or how a status such as `WAITING` distinguishes approval from dependency blocking or provider waiting. Several canonical states have no model representation.

**Impact:** persistence, UI, event consumers, API responses, approval gates, cancellation, and checkpoint restore can disagree.

**Required action:** define separate lifecycle state and runtime phase types with a complete mapping, or make the model exactly derive from the canonical lifecycle.

## Critical Finding 4 — Contract Layers Do Not Directly Declare Lifecycle Authority

The audited models, protocols, APIs, SDKs, and registries generally describe their domain without directly linking to the canonical lifecycle document. This affects Agent, Plugin, Provider, Task, Workflow, ToolCall, and related sessions/workspaces.

Indirect references through architecture or a source index do not provide enough local authority for a contract consumer. A status field, protocol event, API response, and SDK callback must state whether it is a lifecycle state, a phase, an event, or a projection.

**Required action:** add direct lifecycle authority and compatibility sections to every lifecycle-bearing contract document.

## High Finding 5 — Lifecycle Tables Do Not Define Transition Semantics

The five lifecycle documents provide state descriptions but their state tables do not consistently define guards, effects, emitted events, persistence points, invalid transitions, rollback behavior, or idempotency. The documents discuss transitions in prose, but the implementer still must infer parts of the transition contract.

**Impact:** valid/invalid transition behavior, retries, cancellation, approval, crash recovery, and duplicate events can differ between implementations.

**Required action:** expand each lifecycle machine with explicit transition rows containing source, event, guard, target, side effects, emitted events, persistence, rollback, idempotency, and invalid-transition behavior.

## High Finding 6 — Provider State Has No Stable Persistence/API Projection

Provider lifecycle defines `Registered`, `Configuring`, `Configured`, `Testing`, `Healthy`, `Degraded`, `Unhealthy`, `Disabled`, and `Removed`, but the Provider model does not define a lifecycle status field or a normative projection. The architecture mentions registry and in-memory health state without resolving persistence authority, cache invalidation, API serialization, or routing eligibility.

**Required action:** define the provider-state source of truth and its persistence, cache, event, API, and router mappings.

## High Finding 7 — Plugin Transient States Are Not Durable or Recoverable by Contract

Plugin lifecycle defines download, verification, install, activation, deactivation, uninstall, and failure states. The model exposes only `INSTALLED`, `ACTIVE`, `DISABLED`, and `ERROR`. No complete mapping says which states survive process death, how progress is restored, or how `Inactive` differs from `Disabled`.

**Required action:** define durable/transient state boundaries and model/event/API/registry projections, including interrupted-operation recovery.

## High Finding 8 — Task Lifecycle and Execution Phase Semantics Are Unresolved

Task lifecycle defines formal states such as `Queued`, `Running`, `Blocked`, `WaitingApproval`, `RetryPending`, and `Completed`. Execution protocol and execution lifecycle documents introduce planning/execution phases and protocol states such as `PLANNING` and `EXECUTING`.

The repository does not define whether phases are persisted, how they map to TaskStatus, which events are ordered, or how cancellation, approval, retry, checkpointing, and background recovery interact with them.

**Required action:** define TaskStatus, ExecutionPhase, TaskEvent, checkpoint, and recovery compatibility in one normative matrix.

## High Finding 9 — ToolCall Approval and Failure Semantics Are Split Across Documents

Tool model status, tool architecture approval predicates, tool protocol timeout/error behavior, error catalog codes, and security policy each describe a portion of ToolCall behavior. No single mapping connects approval decision, permission result, execution, timeout, cancellation, partial output, error code, audit event, retry, and final status.

**Required action:** define a complete ToolCall contract and test every state/error/security transition.

## High Finding 10 — Public Operations Do Not Have Wire-Contract Matrices

Provider architecture/API/SDK share methods such as completion, streaming, embedding, model listing, and health checks, but protocols do not provide explicit operation-to-message mappings. Agent, Tool, Plugin, and Runtime chains show the same pattern: operations exist at some layers while protocol messages, error envelopes, lifecycle effects, permissions, timeouts, cancellation, and idempotency are not connected in one matrix.

**Required action:** add an operation matrix for every public API and SDK operation containing request model, response model, protocol message, events, errors, lifecycle effects, security requirements, and tests.

## High Finding 11 — Threat Controls Are Not Semantically Verified

The security ownership split is reasonable, but the threat model’s 28 threats are not linked to security test cases. Permission and sandbox documents also do not carry threat identifiers that identify which threats each control mitigates.

**Required action:** map each threat to protected asset, attacker capability, precondition, control, enforcement point, expected denial/containment, audit event, cleanup, test, and residual risk.

## High Finding 12 — Full Environment Is Internally Coherent but Operationally Under-Evidenced

The Full Environment documents consistently specify one APK-bundled Debian-slim rootfs with glibc, apt, proot, on-demand extraction, Python, Node/npm, binary wheels, and overlays. The semantic gap is not the environment description; it is the absence of complete evidence for asset integrity, architecture selection, extraction rollback, proot startup, apt operations, Python wheel loading, npm native modules, overlay isolation, cache cleanup, and restart recovery.

**Required action:** link every environment invariant to a requirement, implementation owner, operational test, failure case, and rollback/recovery behavior.

## High Finding 13 — Supporting Documents Often Refer to an Unnamed Owner

Multiple derived and supporting documents state that behavior is defined by an “owning architecture document” without naming the document. This pattern appears in protocols, registries, models, UI support documents, and standards. It makes semantic conflict resolution dependent on external inference.

**Required action:** replace generic ownership language with explicit canonical source, supporting sources, derived boundaries, and conflict-resolution rules. Keep the source map as an index, not as a substitute for local authority.

## Medium Finding 14 — Task Metadata Contains Duplicate Authority Declarations

`models/Task.md` contains duplicate derived declarations. The Task status relationship to its lifecycle is substantively aligned, but document metadata ownership is ambiguous.

**Required action:** keep one authority block and move enum consistency into an explicit constraint section.

## Semantic Implementation Risk

The most dangerous remaining implementation decisions are not isolated missing fields. They are boundary decisions: what is persisted versus transient, which state is authoritative after a crash, which event is emitted first, which error code controls recovery, whether approval is a state or decision, how registry caches invalidate, how provider health becomes routing truth, how plugin installation resumes, and how Full Environment extraction rolls back.

The current documents provide enough intent for a skilled team to make those decisions, but not enough normative detail to guarantee that two independent implementations would behave identically.

## Required Remediation Sequence

1. Define canonical semantic types: lifecycle state, execution phase, event, error, decision, result, and projection.
2. Expand lifecycle machines into complete transition contracts.
3. Connect every public operation to request/response/event/error/security/test matrices.
4. Define durable versus transient state for Agent, Task, Plugin, Provider, Workflow, ToolCall, Session, Workspace, and background execution.
5. Build complete requirement and threat evidence traceability.
6. Assign explicit ownership to all derived/supporting documents.
7. Add Full Environment operational and failure-recovery evidence.
8. Re-read all changed documents and repeat the semantic audit.

## Final Assessment

The repository is structurally connected and architecturally coherent at a high level, but it is not semantically deterministic or evidence-complete. The primary blockers are the disconnected evidence system, orphaned error catalog, divergent lifecycle/model/phase vocabularies, incomplete transition semantics, absent operation-to-wire matrices, and unverified threat controls.

This report records the maximum-depth semantic audit of the current repository state. No source documents were modified during the audit itself.
