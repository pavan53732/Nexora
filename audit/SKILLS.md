# Skill Registry — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See [docs/adr/ADR-0007-Skills-First-Class.md](../docs/adr/ADR-0007-Skills-First-Class.md) for the
> Agent/Skill/Tool model, [models/Skill.md](../models/Skill.md) for the domain model,
> and [specs/EXECUTION_LIFECYCLE.md](../specs/EXECUTION_LIFECYCLE.md) for skill selection.

**Authoritative catalog of every skill.** Stable IDs (`SKL-###`) per [DL-017](../docs/DECISION_LOG.md).
A skill is **expertise** (WHAT), distinct from agents (WHO) and tools (HOW).

## Registry

| ID | Skill | Domain | Core Agent(s) | Primary Tools | Phase | Source |
|----|-------|--------|---------------|---------------|-------|--------|
| SKL-001 | Kotlin Development | Kotlin | Coder | file_*, code_*, terminal_run | 4 | Built-in |
| SKL-002 | Android App Development | Android | Coder | build_gradle, file_*, terminal_run | 4 | Built-in |
| SKL-003 | Jetpack Compose UI | Android | Coder | file_*, code_generate, code_review | 4 | Built-in |
| SKL-004 | Android Debugging | Android | Debugger | terminal_run, debug_*, device_*, file_* | 4 | Built-in |
| SKL-005 | JVM / Java Interop | JVM | Coder | file_*, build_*, terminal_run | 4 | Built-in |
| SKL-006 | Git Workflow | Devops | Git Agent | git_* | 4 | Built-in |
| SKL-007 | Git Conflict Resolution | Devops | Git Agent, Coder | git_diff, git_merge, git_status, file_* | 4 | Built-in |
| SKL-008 | API Design | Web | Coder | file_*, code_review, http_* | 4 | Built-in |
| SKL-009 | SQL / Database Design | Data | Database Agent | sqlite_* | 4 | Built-in |
| SKL-010 | Python Scripting | Data | Coder | terminal_run, pip_install, file_* | 4 | Built-in |
| SKL-011 | Node.js Development | Web | Coder | terminal_run, npm_install, file_* | 4 | Built-in |
| SKL-012 | Web Research | Research | Researcher | browser_*, search_*, http_* | 4 | Built-in |
| SKL-013 | Browser Automation | Web | Browser Agent | browser_* | 4 | Built-in |
| SKL-014 | Test Writing & Execution | Testing | Tester | test_*, file_*, terminal_run | 4 | Built-in |
| SKL-015 | Performance Tuning | JVM | Debugger | obs_metrics, build_*, terminal_run | 5 | Built-in |
| SKL-016 | Security Review | Security | Security Auditor | security_*, code_review, file_* | 5 | Built-in |
| SKL-017 | Documentation Writing | Documentation | Documentation Writer | doc_*, file_* | 4 | Built-in |
| SKL-018 | Data Analysis & Visualization | Data | Researcher | python (via Chaquopy), sqlite_*, search_* | 5 | Built-in |
| SKL-019 | Shell Scripting | Devops | Coder | terminal_*, file_* | 4 | Built-in |
| SKL-020 | Workflow Design | Automation | Workflow Coordinator | workflow_*, agent_delegate | 6 | Built-in |
| SKL-021 | Code Refactoring | Kotlin | Refactoring Agent | code_refactor, code_rename, code_metrics | 4 | Built-in |
| SKL-022 | Prompt Engineering | Research | Researcher | ai_complete, ai_stream | 5 | Built-in |
| SKL-023 | Project Planning | Automation | Planner | task_*, project_*, workflow_* | 6 | Built-in |
| SKL-024 | Deployment & Packaging | Devops | Deployment Agent | build_*, io_export_*, terminal_* | 6 | Built-in |

## Notes

- **Built-in** skills ship with the app; **user-defined** and **learned** skills are
  registered at runtime via the `SkillRegistry` (FR-SK-002/003).
- Skills **map to tools** (one skill uses many tools; many skills share tools) and to
  **agents** (applicable agent types). The executor validates that the selected agent
  actually possesses the selected skill before dispatch.
- Skill acquisition: `skill_list` (TOOL-394), `skill_acquire` (TOOL-395) — see
  [registry/TOOLS.md](./TOOLS.md).
