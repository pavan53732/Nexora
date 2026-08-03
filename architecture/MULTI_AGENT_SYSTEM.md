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
| **Workflow Coordinator** | Orchestrates multi-agent task delegation. | 7 |

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
    BROWSER, DATABASE, FILE_MANAGER, GIT, WORKFLOW_COORDINATOR, CUSTOM
}
```

## Shared Context

Agents within a workspace share:

- **Memory** — Access to same memory stores (scoped permissions).
- **Workspace** — Same project files and directories.
- **Tasks** — Shared task queue for delegation and handoff.
- **Execution Context** — Can see each other's recent activity.
- **Artifacts** — Can produce and consume shared artifacts.

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

- The Evidence & Validation Engine (CONTEXT_MANAGEMENT §11 EV-6) triggers the review;
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

## Phase Mapping

- **Phase 7**: All 15 agent types, agent registry, task delegation.
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

### SA-3 — Parallel orchestration (FR-MA-003)

| Rule | Value |
|------|-------|
| Concurrency limit | Max 3 sub-agents per workspace (configurable) |
| Fan-out | Independent subtasks (no dependency edge) run in parallel lanes (FR-EL-007); dependent tasks wait |
| **File conflict** | A sub-agent holds a **write-lock per file**; a second writer waits, or the coordinator assigns a copy and merges at the end |
| Sandbox budgets | Workspace limits split across active sub-agents (FR-S018); each sub-agent isolated |
| Result merging | Coordinator merges outputs + execution histories in dependency order |

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
- **Phase 7**: SA-1..SA-5 with the 15-agent registry, delegation, parallel
  orchestration.
