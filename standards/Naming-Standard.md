> **Status: SUPPORTING** for Naming Standard coding standard.
> This document defines conventions for Naming Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Naming Standard — Nexora

## Code

| Element | Format | Example |
|---------|--------|--------|
| Class | PascalCase | `ToolRegistry` |
| Function | camelCase | `executeTool()` |
| Variable | camelCase | `currentWorkspace` |
| Constant | UPPER_SNAKE | `MAX_RETRIES` |
| Enum | PascalCase | `TaskStatus` |
| Enum value | UPPER_SNAKE | `COMPLETED` |
| Package | lowercase | `com.nexora.app.runtime.tools` |
| File | PascalCase.kt | `ToolRegistry.kt` |

## Identifiers

| Type | Format | Example |
|--------|--------|--------|
| Tool ID | `{category}_{action}` | `file_read`, `git_commit` |
| Agent ID | `snake_case` | `workflow_coordinator` |
| Provider ID | `snake_case` | `openai`, `anthropic` |
| Plugin ID | `kebab-case` | `nexora-browser` |
| Feature ID | `{PREFIX}-{NNN}` | `TOOL-001`, `AGT-001` |
| ADR | `ADR-NNNN-Title` | `ADR-0001-Workspace-First` |
| Workspace ID | UUID | `550e8400-e29b-41d4-a716-446655440000` |

## Documentation File Naming

Per-folder conventions for markdown files (keeps the doc repo navigable):

| Folder | Convention | Examples |
|--------|-----------|----------|
| root, docs/, architecture/, specs/, registry/, requirements/, errors/ | UPPER_SNAKE | `RUNTIME.md`, `TOOL_SYSTEM.md`, `FR.md`, `ERROR_CODES.md` |
| models/, security/, state-machines/, testing/, ui/ | PascalCase | `Agent.md`, `ThreatModel.md`, `TaskLifecycle.md`, `UnitTests.md` |
| protocols/, docs/api/, diagrams/ | Hyphen-case | `Tool-Protocol.md`, `Agent-API.md`, `Memory-Store-Flow.md` |
| docs/adr/ | `ADR-NNNN-Title` | `ADR-0007-Skills-First-Class.md` |
| sdk/ | `XSDK.md` | `AgentSDK.md`, `PluginSDK.md` |

Rules:
- One document type per folder; a document's folder implies its role.
- `PROJECT_SPECIFICATION.md` is the master index; every new doc must be added to its index tables.
- Renaming a file requires updating all inbound links (verified by the repo's link check).

## Git

- Branches: `feature/short-description`, `bugfix/short-description`, `phase/N`
- Commits: conventional commits (`feat(scope): description`)
- Tags: `v0.1.0`, `v0.2.0`
