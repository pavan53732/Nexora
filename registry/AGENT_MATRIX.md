# Nexora Agent Capability Matrix

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [AGENTS.md](./AGENTS.md)
>
Authoritative reference mapping **every agent type** (see [AGENTS.md](./AGENTS.md)) to its permitted capabilities. The orchestrator enforces these constraints at dispatch time. Agents may only invoke tools and actions marked with ✓. Generated from the agent catalog; keep in sync with `registry/AGENTS.md`.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Supported |
| — | Not supported |

## Matrix

| Agent ID | Agent Name | Plan | Execute | Review | Code | Browser | Memory | Terminal | Multi-Agent | Delegate | Background | Streaming | Phase |
|----------|------------|------|---------|--------|------|---------|--------|----------|-------------|----------|------------|-----------|-------|
| AGT-001 | Planner | ✓ | — | ✓ | — | — | ✓ | — | — | ✓ | — | ✓ | 7 |
| AGT-002 | Researcher | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | ✓ | ✓ | 7 |
| AGT-003 | Coder | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | ✓ | ✓ | 7 |
| AGT-004 | Reviewer | — | ✓ | ✓ | ✓ | — | ✓ | — | — | — | — | ✓ | 7 |
| AGT-005 | Tester | — | ✓ | ✓ | ✓ | — | — | ✓ | — | — | ✓ | ✓ | 7 |
| AGT-006 | Debugger | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | ✓ | — | 7 |
| AGT-007 | Documentation Writer | — | ✓ | ✓ | — | — | ✓ | — | — | — | — | ✓ | 7 |
| AGT-008 | Refactoring Agent | ✓ | ✓ | ✓ | ✓ | — | ✓ | — | — | — | — | — | 7 |
| AGT-009 | Deployment Agent | ✓ | ✓ | ✓ | — | — | — | ✓ | — | — | ✓ | ✓ | 7 |
| AGT-010 | Security Auditor | ✓ | ✓ | ✓ | — | — | — | ✓ | — | — | ✓ | — | 7 |
| AGT-011 | Browser Agent | — | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | ✓ | 7 |
| AGT-012 | Database Agent | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | ✓ | 7 |
| AGT-013 | File Manager | — | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | 7 |
| AGT-014 | Git Agent | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | ✓ | — | 7 |
| AGT-015 | Workflow Coordinator | ✓ | — | ✓ | — | — | ✓ | — | ✓ | ✓ | — | ✓ | 7 |

## Capability Definitions

| Capability | Description |
|------------|-------------|
| **Plan** | Create and modify execution plans, break down tasks |
| **Execute** | Directly invoke tools to perform actions on the system |
| **Review** | Inspect results, validate output, self-correct |
| **Code** | Read, write, and execute code (file + terminal tools) |
| **Browser** | Control the headless browser for web interaction |
| **Memory** | Store, retrieve, and manage persistent memory entries |
| **Terminal** | Execute shell commands directly |
| **Multi-Agent** | Spawn and coordinate child agents |
| **Delegate** | Assign subtasks to other agent types |
| **Background** | Run long-lived tasks without blocking the UI thread |
| **Streaming** | Emit incremental results via token or event streams |

## Phase Rollout

- **Phase 7** — All 15 agent types, agent registry, task delegation (see [AGENTS.md](./AGENTS.md)).
- **Phase 8** — Community agent plugins.

## Execution Depth

Agents have a configurable `maxExecutionDepth` (default 10) that limits nested tool calls per turn. Orchestrator agents (AGT-015) enforce depth 3 on delegated children.
