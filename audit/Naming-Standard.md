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

## Git

- Branches: `feature/short-description`, `bugfix/short-description`, `phase/N`
- Commits: conventional commits (`feat(scope): description`)
- Tags: `v0.1.0`, `v0.2.0`
