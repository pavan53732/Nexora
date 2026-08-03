> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Nexora Agent Capability Matrix

Authoritative reference mapping each agent type to its permitted capabilities. The orchestrator enforces these constraints at dispatch time. Agents may only invoke tools and actions marked with ✓.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Supported |
| — | Not supported |

## Matrix

| Agent ID | Agent Name | Plan | Execute | Review | Code | Browser | Memory | Terminal | Multi-Agent | Delegate | Background | Streaming | Phase |
|----------|------------|------|---------|--------|------|---------|--------|----------|-------------|----------|------------|-----------|-------|
| AGT-001 | General Assistant | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 1 |
| AGT-002 | Code Developer | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | ✓ | ✓ | 1 |
| AGT-003 | Research Analyst | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | ✓ | ✓ | 1 |
| AGT-004 | Data Analyst | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | ✓ | ✓ | 2 |
| AGT-005 | Creative Writer | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | ✓ | 1 |
| AGT-006 | Debug Expert | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | ✓ | — | 1 |
| AGT-007 | DevOps Engineer | ✓ | ✓ | ✓ | ✓ | — | — | ✓ | — | — | ✓ | ✓ | 2 |
| AGT-008 | QA Tester | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | — | — | — | ✓ | 2 |
| AGT-009 | Security Auditor | ✓ | ✓ | ✓ | — | ✓ | — | ✓ | — | — | ✓ | — | 2 |
| AGT-010 | Technical Writer | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | ✓ | 1 |
| AGT-011 | Project Manager | ✓ | — | ✓ | — | — | ✓ | — | — | ✓ | — | ✓ | 2 |
| AGT-012 | System Administrator | ✓ | ✓ | ✓ | — | — | — | ✓ | — | — | ✓ | — | 2 |
| AGT-013 | Workflow Orchestrator | ✓ | — | ✓ | — | — | ✓ | — | ✓ | ✓ | — | ✓ | 2 |
| AGT-014 | Learning Assistant | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | ✓ | 3 |
| AGT-015 | Personal Assistant | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 3 |

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

- **Phase 1** — General-purpose agents for code, research, writing, and debugging.
- **Phase 2** — Specialized agents for operations, QA, security, project management, and orchestration.
- **Phase 3** — Learning and full-capability personal assistants with unrestricted tool access.

## Execution Depth

Agents have a configurable `maxExecutionDepth` (default 10) that limits nested tool calls per turn. AGT-015 (Personal Assistant) defaults to depth 5 for safety. Orchestrator agents (AGT-011, AGT-013) enforce depth 3 on delegated children.
