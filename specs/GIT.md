# Git Integration Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md)

---

## Overview

Full Git support inside the sandbox. Every workspace can have a Git repository. The agent can use Git tools autonomously.

## Supported Operations

| Operation | Tool | Description |
|-----------|------|-------------|
| Initialize | `git_init` | Create a new Git repository. |
| Clone | `git_clone` | Clone a remote repository. |
| Add | `git_add` | Stage files for commit. |
| Commit | `git_commit` | Commit staged changes. |
| Push | `git_push` | Push commits to remote. |
| Pull | `git_pull` | Pull and merge from remote. |
| Branch | `git_branch` | Create, list, delete, switch branches. |
| Merge | `git_merge` | Merge branches. |
| Log | `git_log` | View commit history. |
| Diff | `git_diff` | View file differences. |
| Status | `git_status` | Show working tree status. |
| Stash | `git_stash` | Stash and unstash changes. |
| Remote | `git_remote` | Manage remotes. |

## Phase Mapping

- **Phase 4**: Git tools implementation.
