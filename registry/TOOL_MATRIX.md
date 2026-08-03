> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Nexora Tool Capability Matrix

Authoritative reference mapping every registered tool to its supported capabilities. Used by the sandbox controller, permission system, and agent scheduler to determine which tools an agent may invoke.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Supported |
| — | Not supported |

## Matrix

| Tool ID | Tool Name | Category | Read | Write | Network | Android API | Background | Permission Level | Agent-Usable | Sandbox-Required | Streaming | Phase |
|---------|-----------|----------|------|-------|---------|-------------|------------|-----------------|--------------|------------------|-----------|-------|
| `file_read` | File Read | File | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `file_write` | File Write | File | — | ✓ | — | — | — | Low | ✓ | ✓ | — | 1 |
| `file_delete` | File Delete | File | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | 1 |
| `file_list` | File List | File | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `file_search` | File Search | File | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `file_copy` | File Copy | File | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 1 |
| `file_move` | File Move | File | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 1 |
| `shell_execute` | Shell Execute | Terminal | ✓ | ✓ | — | — | — | High | ✓ | ✓ | — | 1 |
| `shell_background` | Shell Background | Terminal | ✓ | ✓ | — | — | ✓ | High | ✓ | ✓ | — | 2 |
| `command_history` | Command History | Terminal | ✓ | — | — | — | — | Low | ✓ | — | — | 2 |
| `git_init` | Git Init | Git | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `git_commit` | Git Commit | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 1 |
| `git_push` | Git Push | Git | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 1 |
| `git_pull` | Git Pull | Git | ✓ | ✓ | ✓ | — | — | Medium | ✓ | — | — | 1 |
| `git_diff` | Git Diff | Git | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `git_log` | Git Log | Git | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `git_branch` | Git Branch | Git | ✓ | ✓ | — | — | — | Medium | ✓ | — | — | 1 |
| `browser_navigate` | Browser Navigate | Browser | ✓ | — | ✓ | ✓ | — | Medium | ✓ | ✓ | — | 2 |
| `browser_screenshot` | Browser Screenshot | Browser | ✓ | — | — | ✓ | — | Medium | ✓ | ✓ | — | 2 |
| `browser_extract` | Browser Extract | Browser | ✓ | — | — | ✓ | — | Medium | ✓ | ✓ | — | 2 |
| `browser_click` | Browser Click | Browser | — | ✓ | — | ✓ | — | Medium | ✓ | ✓ | — | 2 |
| `db_query` | Database Query | Database | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | 2 |
| `db_execute` | Database Execute | Database | — | ✓ | — | — | — | High | ✓ | ✓ | — | 2 |
| `db_schema` | Database Schema | Database | ✓ | — | — | — | — | Low | ✓ | — | — | 2 |
| `http_get` | HTTP GET | Network | ✓ | — | ✓ | — | — | Medium | ✓ | ✓ | ✓ | 1 |
| `http_post` | HTTP POST | Network | — | ✓ | ✓ | — | — | Medium | ✓ | ✓ | ✓ | 1 |
| `http_download` | HTTP Download | Network | ✓ | ✓ | ✓ | — | ✓ | Medium | ✓ | ✓ | ✓ | 2 |
| `memory_store` | Memory Store | Memory | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `memory_search` | Memory Search | Memory | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `memory_delete` | Memory Delete | Memory | — | ✓ | — | — | — | Medium | ✓ | — | — | 1 |
| `ai_complete` | AI Complete | AI | ✓ | — | ✓ | — | — | High | ✓ | — | ✓ | 1 |
| `ai_embed` | AI Embed | AI | ✓ | — | ✓ | — | — | Medium | ✓ | — | — | 2 |
| `ai_analyze_image` | AI Analyze Image | AI | ✓ | — | ✓ | — | — | High | ✓ | — | ✓ | 3 |
| `system_info` | System Info | System | ✓ | — | ✓ | ✓ | — | Low | ✓ | — | — | 1 |
| `workspace_stats` | Workspace Stats | System | ✓ | — | — | — | — | Low | ✓ | — | — | 2 |

## Permission Levels

| Level | Description | Policy |
|-------|-------------|--------|
| Low | Read-only or non-destructive | Auto-approved for trusted agents |
| Medium | Destructive or network-dependent | Requires user confirmation once per session |
| High | System-level or irreversible | Requires explicit approval per invocation |

## Phase Availability

- **Phase 1** — Core file, terminal, git, network, AI, and system tools shipped at launch.
- **Phase 2** — Background execution, browser automation, database access, and embedding.
- **Phase 3** — Multimodal AI, advanced analysis, and specialized integrations.
