> **Status: CANONICAL** for multi-agent coordination and delegation.
> This document owns agent-to-agent task delegation, parallel sub-agent spawning,
> result merging, and inter-agent communication protocols. It does NOT own the
> internal single-agent loop (see [AGENT_RUNTIME.md](AGENT_RUNTIME.md)) or workflow
> graph progression (see [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md)).
>
> Depends on: [AGENT_RUNTIME.md](AGENT_RUNTIME.md) (single-agent loop), [RUNTIME.md](RUNTIME.md) (service composition).
> Referenced by: [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md), [registry/AGENTS.md](../registry/AGENTS.md).

# Multi-Agent System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [AGENT_RUNTIME.md](AGENT_RUNTIME.md) | [WORKFLOW_ENGINE.md](WORKFLOW_ENGINE.md)

---

## Overview

Nexora supports multiple collaborating agents within a workspace. Each agent has a specialized role. Agents share memory, workspace, tasks, and execution context.

## Built-in Agent Roles

| Agent | Role | Phase |
|-------|------|-------|
| **Planner** | Decomposes goals into structured execution plans. | 7 |
| **Researcher** | Gathers information, searches, reads documentation. | 7 |
| **Coder** | Writes, modifies, and refactors code. | 7 |
| **Reviewer** | Reviews code changes for correctness and quality. | 7 |
| **Tester** | Writes and executes tests. | 7 |
| **Debugger** | Diagnoses and fixes bugs and errors. | 7 |
| **Documentation Writer** | Generates docs, comments, READMEs. | 7 |
| **Refactoring Agent** | Restructures code for maintainability. | 7 |
| **Deployment Agent** | Handles build, packaging, deployment. | 7 |
| **Security Auditor** | Scans for vulnerabilities. | 7 |
| **Browser Agent** | Automates browser interactions. | 7 |
| **Database Agent** | Manages database operations. | 7 |
| **File Manager** | Handles file operations and organization. | 7 |
| **Git Agent** | Manages version control workflows. | 7 |
| **Workflow Coordinator (Master Agent)** | The CEO/project-manager role: understands the goal, breaks it into tasks, spawns sub-agents, assigns work, tracks progress, merges results, resolves conflicts, and decides when work is complete. **Never performs implementation itself** (matrix: Execute = —). | 7 |
| **Architect** | Designs system architecture, validates module boundaries, reviews dependencies, designs APIs and database schemas, reviews scalability. | 7 |

## Agent Interface

```kotlin
interface Agent {
    val id: String
    val type: AgentType
    val name: String
    val description: String
    val capabilities: List<String>
    val defaultTools: List<String>

    suspend fun execute(task: AgentTask, context: AgentContext): AgentResult
}

enum class AgentType {
    PLANNER, RESEARCHER, CODER, REVIEWER, TESTER, DEBUGGER,
    DOCUMENTATION_WRITER, REFACTORING, DEPLOYMENT, SECURITY_AUDITOR,
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR, ARCHITECT, CUSTOM  // COORDINATOR = Master Agent (never implements); CUSTOM = user-defined agents
}
```

## Shared Context

Agents within a workspace share:

- **Memory** — Access to same memory stores (scoped permissions).
- **Workspace** — Same project files and directories (read access to the shared base; writes go through the file-sharing model below).
- **Tasks** — Shared task queue for delegation and handoff.
- **Execution Context** — Can see each other's recent activity.
- **Artifacts** — Can produce and consume shared artifacts.

## File Sharing & Isolation Model (resolves sandbox/sandbox-depth wording)

FR-S018 grants each sub-agent an **isolated sandbox** for *process, network, quota, and
permission* boundaries — it does NOT mean the sub-agent cannot see the workspace files.
The consistent model is a **shared read-only base + private writable overlay + merge**:

- **Shared base snapshot**: at delegation time the coordinator exposes a read-only view of
  the current committed workspace (files, `tasks/` checkpoints, `env/`). All sub-agents
  read the same base; no sub-agent can mutate another's in-flight state.
- **Private overlay**: each sub-agent writes into its own copy-on-write overlay. Its
  `run_background`/terminal work and generated files land in the overlay, not directly in
  the coordinator's tree, so a compromised or failing sub-agent cannot corrupt siblings.
- **Shared-file writes**: when a subtask must modify a shared file, it takes a **per-file
  write-lock** (SA-3). A second writer waits, or the coordinator assigns a copy and merges
  at the end. This is the only path that mutates the shared base.
- **Result promotion**: completed outputs are promoted from the overlay to the shared
  workspace as **artifacts** (SA-5), never via raw cross-sandbox file access. Promotion is
  permissioned (the `artifact:read` scope planned in SANDBOX_DEPTH §3.2).
- **Merge ownership**: the coordinator merges outputs + execution histories in dependency
  order (SA-3); conflicts surface as review findings, not silent overwrites.

This reconciles "same project files" (read base) with "separate sandbox instances" (process
+ overlay isolation) and "promoted via artifacts" (merge path). SANDBOX_DEPTH §3.2's
"files... not shared with the coordinator" is corrected to "files are not *directly*
shared — they are read from the base snapshot and promoted as artifacts."

## Communication Flow

```
Workflow Coordinator
    |
    v
Delegates to Planner Agent -> Produces execution plan
    |
    v
Delegates to Coder Agent -> Implements code
    |
    v
Delegates to Tester Agent -> Writes and runs tests
    |
    v
Delegates to Reviewer Agent -> Reviews changes

## Mandatory Review Rule (FR-EV-006)

For tasks classified **important** (sensitivity, risk, or cost), the runtime
**requires a Reviewer agent pass** before the result reaches the user:

```
Coder Agent → Tester Agent → Reviewer Agent → User
```

- The Evidence & Validation Engine (CONTEXT_MANAGEMENT §7 EV-6) triggers the review;
  no user-facing completion until the reviewer approves.
- The reviewer checks against the task's declared validation criteria (FR-EL-008);
  findings return to the originating agent as a bounded fix loop (FR-AS-001).
    |
    v
Results aggregated -> Workflow Coordinator combines results
    |
    v
Report to user
```

## Controlled Execution-Capability Requests

The orchestrator MUST preserve the derived capability matrix as the ordinary dispatch boundary. A parent or specialized agent cannot grant itself Terminal, Background, Delegate, or any other unlisted capability. When a delegated plan requires execution outside the current agent's declared capabilities, the orchestrator MUST prefer delegation to an eligible agent. A temporary task-scoped escalation is permitted only through the existing permission, approval,
sandbox, resource, deadline, and audit gates.

An escalation request is bound to one `workspaceId`, `taskId`, execution lineage, requesting `agentId`, capability, purpose, affected operation class or canonical Tool IDs, required scopes, effective deadline, maximum concurrency/resource limits, cancellation rule, and revocation condition. It is not a new agent type, permanent capability, Tool identity, permission scope, or lifecycle state. It expires on task completion, cancellation, deadline exhaustion, explicit revocation, or terminal failure, whichever occurs first. It cannot be transferred to another task or silently reused by another agent.

A delegated worker receives only the capability and context required for its assigned acceptance criteria. The parent retains plan/delegation responsibility; the worker retains its own Tool, permission, sandbox, execution, and lifecycle responsibilities. The parent MUST NOT treat a delegation request, temporary grant, or worker plan as evidence that the operation succeeded. Results require the existing Tool, evidence, acceptance, and completion gates.

Terminal escalation continues to require `sandbox:execute` and applicable workspace read/write scopes. Background escalation continues to require checkpointing, cancellation propagation, progress reporting, resource limits, Android lifecycle handling, notification policy, and degraded-mode behavior. No escalation bypasses host isolation, network/device permissions, applicable canonical denial or classification outcome, sensitive-app blocking, unknown-completion reconciliation, or failure-ledger strategy mutation.

Every escalation request and delegation decision MUST be recorded in the existing correlated trace and permission/audit projections with requester, target worker when delegated, purpose, scope, decision, approval transaction, grant lifetime, use, result, expiry/revocation, and final disposition. User-visible status MUST distinguish requested, delegated, approved, denied, active, expired, revoked, cancelled, and completed outcomes. If an active grant expires or is revoked, descendant cancellation and checkpoint behavior follow existing runtime rules; no new durable Task or Execution state is introduced.

### Delegation depth bound

Delegation depth is measured from the root task/delegating agent lineage. A delegation request increments the lineage depth for its child. The maximum permitted depth is **4**; a request that would exceed depth 4 is denied before child creation and is recorded through the existing correlated error and audit path. This is a bound on delegation topology, not a new agent, Task, Execution, or lifecycle state.

## Agent Registry

```kotlin
class AgentRegistry {
    private val agentTypes = mutableMapOf<AgentType, Agent>()

    fun register(agent: Agent)
    fun create(type: AgentType, workspaceId: String): AgentInstance
    fun listAvailable(): List<AgentType>
    fun getInstance(agentId: String): AgentInstance?
}
```

## Communication Rule (FR-AG-002)

**Sub-agents never communicate directly with each other.** All inter-agent
communication flows through the orchestration layer (EventBus + coordinator +
shared memory). An agent may never call another agent; it publishes results and the
coordinator routes them. This centralizes coordination, prevents coupling, and
simplifies conflict resolution and audit.

## Multi-Agent Coordinator

The coordinator role is composed from existing runtime modules (Agent Manager +
Executor + Workflow Engine + EventBus + SA-1..SA-5 contract) — an explicit
coordination concern, not a new standalone module (FR-AG-003):

| Responsibility | Owned by |
|----------------|----------|
| Spawning specialized sub-agents | AgentManager |
| Scheduling parallel work + dependencies | Executor + WorkflowEngine (FR-EL-007) |
| Coordinating shared memory | MemoryManager + EventBus |
| Tracking progress | Observability (TaskProgress) |
| Collecting/merging outputs, detecting conflicts | Coordinator agent (SA-3) |
| Dispatching validation/testing | Evidence & Validation Engine (EV-6) |
| Deciding goal achievement | Master Agent + EVE completion policy |

## Phase Mapping

- **Phase 7**: All 16 agent types, agent registry, task delegation, Master Agent role.
- **Phase 8**: Community agent plugins.

---

## Sub-Agent Autonomous Completion (SA-1..SA-5)

A delegated subtask runs **end-to-end by the sub-agent** — without mid-task check-ins,
without assumptions, verified, then reported. The coordinator delegates once and
collects the result; it does not micro-manage.

### SA-1 — Autonomous completion contract (FR-MA-001)

Once delegated, a sub-agent owns the subtask to completion:

```
Delegate → Spawn (own sandbox, FR-S018) → Execute (own plan) →
Verify (EV gates, FR-EL-008/011) → Report (plan-vs-actual, RG-6) → Coordinator merges
```

Interruptions are **limited to**:
- High-risk approval gate (PermissionManager `ASK`, FR-S016) — one prompt, then resume
- Budget exhaustion (FR-AS-003) — escalate with state, never silent stop
- Heartbeat failure (FR-AS-002) — checkpoint restart, then escalate

No mid-task check-ins for status; progress flows via the activity feed.

### SA-2 — Complete handoff rule (FR-MA-002)

Every delegation carries the **complete handoff context** (FR-A009) so the sub-agent
never needs to interrupt for missing basics:

| Element | Required |
|---------|----------|
| Goal + expected outcome | ✓ |
| Acceptance criteria (FR-EL-008) | ✓ |
| Constraints (permissions, budgets, scope) | ✓ |
| Available evidence (memory, files, prior results) | ✓ |
| Required skills + tools (FR-EL-004/006) | ✓ |
| Report-back format | ✓ |

If genuinely ambiguous, the sub-agent asks **once** via the Evidence & Validation
Engine (EV), then continues — it never guesses (FR-EV-003).

### SA-3 — Parallel coordination (FR-MA-003)

Dynamic, resource-budgeted concurrency cap (S1):

```
max_parallel_agents = min(
    memory_budget / per_agent_memory_estimate,
    cpu_cores,
    configurable_max
)
```

- **Default:** 3 sub-agents per workspace.
- **High-end devices (8+ CPU cores, 8GB+ memory):** cap rises to 8–16.
- The cap is enforced by the `ResourceManager` (see `RUNTIME.md`) using per-workspace `sandbox_limits.concurrency` (see `models/Workspace.md`).
- If the cap is reached, additional delegation requests are queued (not rejected) and started when an active sub-agent completes.

| Rule | Value |
|------|-------|
| Concurrency limit | Dynamic `min(memory_budget/per_agent_est, cpu_cores, configurable_max)`; default 3; high-end 8–16 |
| Fan-out | Independent subtasks (no dependency edge) run in parallel lanes (`FR-EL-007`); dependent tasks wait |
| **File conflict** | A sub-agent holds a **write-lock per file**; a second writer waits, or the coordinator assigns a copy and merges at the end |
| Sandbox budgets | Workspace limits split across active sub-agents (`FR-S018`); each sub-agent isolated |
| Result merging | Coordinator merges outputs + execution histories in dependency order |
| **Deadlock detection** | A waits-for graph over file write-locks + pending delegation futures is monitored by the coordinator; cycles abort the youngest child and report to the Master Agent (FR-MA-005) |
| **Delegation timeout** | Every delegation carries an explicit deadline; on expiry the coordinator aborts the child, logs `NXR-3011`, and resumes the parent (FR-MA-003) |

#### Adaptive Delegation Effort

The concurrency cap is a safety/resource ceiling, not an instruction to use the maximum number of agents. Before fan-out, the coordinator MUST classify the requested work using the existing task goal, acceptance criteria, dependency graph, evidence requirements, available tools, workspace resource limits, and expected breadth/depth. It SHOULD select the smallest delegation set that can cover independent work and SHOULD increase parallelism only when additional lanes are expected to add distinct evidence or artifacts.

The coordinator MUST prevent duplicate delegation by recording each child objective, scope boundary, source/tool focus, and expected artifact. A new child with overlapping scope requires an explicit re-plan reason. The coordinator MUST stop spawning when the acceptance criteria are satisfied, the evidence target is met, the remaining work is dependency-bound, or the expected information gain is lower than the remaining resource and time cost.

Effort allocation MUST remain non-financial and technical. It may use token, call, time, CPU, memory, battery, concurrency, and provider/resource ceilings, but it MUST NOT introduce internal credit or financial-cost gating contrary to DEC-25. Cost metadata remains observational.

#### Asynchronous Results and Artifact Handoff

Independent children MAY complete out of order. The coordinator MUST accept partial results, preserve each result’s child execution identity and provenance, and continue eligible independent work without waiting for an unrelated slow child. A child result is not complete merely because text was returned: it MUST identify plan-versus-actual status, acceptance-criteria effects, evidence references, artifact references, unresolved questions, failures, and recommended next action.

Large outputs SHOULD be persisted as permissioned artifacts and returned by stable references. The coordinator MUST NOT repeatedly copy large child outputs through conversation context when an artifact reference preserves the source, version, permissions, and integrity. Artifact promotion and merge remain governed by the existing workspace/file-lock and workflow authorities.

The coordinator MUST expose coordination telemetry sufficient to explain child count, fan-out reason, dependency edges, queue time, active time, tool calls, duplicate-scope suppression, partial-result arrivals, artifact references, cancellation, timeout, merge conflict, and final end-state. Telemetry is observability data; it MUST NOT silently redefine Task, Execution, Agent, or Artifact lifecycle states.

#### Deadlock Watchdog Algorithm (ADR-0009, Decision #6)

The `CoordinatorAgent` runs a periodic watchdog coroutine (default interval: 5 s) that
maintains a **waits-for graph** `W`:

- **Nodes** are active sub-agents in the workspace queue.
- **Edges** `A → B` exist when `A` is blocked waiting on:
  - a file write-lock currently held by `B` (from the per-file `ReentrantReadWriteLock`
    in `ResourceManager`, RUNTIME.md §Resource Manager), or
  - a delegation `Future` that `B` has not resolved (e.g. `B` is awaiting its own
    provider stream or a downstream tool commit).
- A **cycle** in `W` means a deadlock: every agent in the cycle is waiting on another
  member and none can progress.

On cycle detection:

1. Identify the **youngest** agent in the cycle (lowest `startedAt`).
2. Abort that agent's execution coroutine, cancel its in-flight tool/stream calls,
   and release its held write-locks.
3. Commit an `execution_checkpoint` (BackgroundExecution §3) so its partial work is
   recoverable.
4. Log `NXR-3011` (Agent coordination failed) to the audit trail with the cycle path
   and the aborted agent's `correlationId`.
5. Promote the **parent** task (the one that delegated to the cycle) out of the
   resource deadlock by re-planning its subtask assignment (FR-AS-001 Plan Repair,
   option **c. Re-plan**) — the parent never waits on the aborted child.

The graph is recomputed from authoritative lock-ownership state in `ResourceManager`
and the delegation futures table in `ExecutionState` (models/Execution.md). Lock
state is the single source of truth; stale edges from cancelled agents are pruned on
each sweep.

#### Delegation Timeout Enforcement

Each delegation records a `deadlineAt` timestamp derived from the task's configured
`timeout` (Toolbox §Timeout Discipline, FR-TL002) plus jitter (ADR-0009 Decision #8).
If the deadline passes before the delegate reports `COMPLETED` or `FAILED`:

- The coordinator aborts the child (same cleanup path as deadlock).
- Emits `NXR-3011` with `cause: "delegation_timeout_exceeded"`.
- Resumes the parent from its last checkpoint with the delegated subtask marked
  `not-attempted` (FR-AS-005 reporting semantics).

### SA-4 — Inherited rules (FR-MA-004)

Sub-agents operate under the same anti-hallucination + reasoning policies as primary
agents — explicitly, not by implication: zero-assumption mode (FR-EV-003), grounding
(RG-1..6), reasoning (RB-1..6), verification gates (FR-AS-006), guardrails
(FR-EV-004), and the Evidence & Validation Engine on every response.

### SA-5 — Sub-agent reporting (FR-MA-005)

The completion report follows RG-6 plan-vs-actual: done-verified / done-unverified /
failed / not-attempted, with verification evidence attached. Important subtasks go
through the Reviewer pass (FR-EV-006) before merging.

## Phase Mapping (sub-agents)

- **Phase 5**: Per-agent sandbox isolation (FR-S018) — the substrate for SA-1.
- **Phase 7**: SA-1..SA-5 with the 16-agent registry, delegation, parallel
  orchestration.

---

## Cross-Instance Extension (Pipes)

Multi-instance collaboration — delegating SA-1..SA-5 subtasks to **remote Nexora
instances** (same machine or LAN) over authenticated pipes — is specified in
[../specs/PIPES.md](../specs/PIPES.md) (canonical). The coordinator role, the
no-direct-communication rule (FR-AG-002), the concurrency cap (SA-3), and all
inherited policies (SA-4) apply unchanged across a pipe boundary: a remote sub-agent
is a first-class `Task` whose executor happens to run in another instance's sandbox
(FR-S018) with that instance's own provider profiles (FR-P011). Instance/pipe states
are owned by [../state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md);
models in [../models/Instance.md](../models/Instance.md); requirements FR-MI-001..010.


## Delegation Boundaries and Performance Controls

This upgrade strengthens multi-agent performance semantics.

### Delegation criteria

Subagent delegation is justified only when it provides a clear benefit such as:

- independent parallelizable work;
- distinct expertise requirements;
- isolated verification;
- bounded evidence collection that does not duplicate active work.

Delegation MUST NOT occur merely because multi-agent capability exists.

### Fan-out controls

The orchestrator MUST prevent:

- redundant subagents collecting the same evidence;
- duplicate context construction for identical objectives;
- uncontrolled fan-out from recursive delegation;
- delegation loops between planner/specialist agents.

### Subagent output aggregation

Aggregating subagent outputs MUST include:

- source subagent identity;
- task scope;
- evidence/provenance references;
- conflict indicators;
- unresolved items;
- verification status.

### Conflict Resolution and Abstention

The coordinator MUST resolve conflicting outputs in this order: canonical authority; fresh, verified evidence; independent verifier agreement; then explicit user direction. Majority vote, provider confidence, or output frequency MUST NOT override canonical authority or verified contradictory evidence.

If the conflict remains unresolved after bounded verification, the coordinator MUST preserve both positions with provenance, mark the result uncertain or incomplete, and escalate or request clarification. It MUST NOT silently merge incompatible claims into a confident result. The selected or escalated disposition and the rejected alternatives are recorded in the merged execution history.
