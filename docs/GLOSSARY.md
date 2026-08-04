# Runtime Glossary — Nexora

> **Status: CANONICAL** for cross-document runtime terminology.
> Canonical subsystem documents own behavior; this glossary owns shared term meaning.

| Term | Meaning | Canonical owner |
|---|---|---|
| Core Runtime | System-wide composition of services and coordination boundaries. | `architecture/RUNTIME.md` |
| Agent Runtime | The per-agent reflect, plan, context, provider, tool, evaluate, and checkpoint loop. | `architecture/AGENT_RUNTIME.md` |
| Multi-Agent Coordinator | Delegation, parallel sub-agent spawning, result merging, and inter-agent communication. | `architecture/MULTI_AGENT_SYSTEM.md` |
| Workflow Engine | Workflow graph definition, sequencing, branching, looping, and recovery. | `architecture/WORKFLOW_ENGINE.md` |
| Planner | Produces task decomposition, dependencies, assignments, provider choices, and validation criteria. | `architecture/RUNTIME.md`, `specs/EXECUTION_LIFECYCLE.md` |
| Executor | Executes planned task steps and manages execution state; it does not own workflow graph progression. | `architecture/RUNTIME.md` |
| Tool Manager | Discovers, validates, authorizes, routes, and executes tool calls through the sandbox boundary. | `architecture/TOOL_SYSTEM.md` |
| Tool Registry | Catalog of tool identities and metadata. | `registry/TOOLS.md` |
| Agent Registry | Catalog of agent identities and metadata. | `registry/AGENTS.md` |
| Background Runtime | Runtime coordination for long-running work while the app is backgrounded. | `specs/BACKGROUND_EXECUTION.md` |
| `AgentExecutionService` | Android foreground-service host used to keep eligible agent execution alive in the background. | `specs/BACKGROUND_EXECUTION.md` |
| Full Environment | The single supported bundled Debian-slim guest rootfs with glibc and `apt`, extracted from APK assets and run through proot. | `specs/FULL_ENVIRONMENT.md` |
| Supporting document | A focused explanation that cannot redefine canonical behavior. | `docs/CANONICAL_SOURCES.md` |
| Derived document | A projection of canonical identity, shape, capability, or integration data. | `docs/CANONICAL_SOURCES.md` |
