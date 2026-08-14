> **Status: SUPPORTING** for GIT focused behavior.
> This document explains focused behavior for GIT. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


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
| Fetch | `git_fetch` | Download objects and refs from another repository. |
| Remote | `git_remote` | Manage set of tracked repositories. |
| Tag | `git_tag` | Create, list, delete or verify a tag object signed with GPG. |
| Reset | `git_reset` | Reset current HEAD to the specified state. |
| Revert | `git_revert` | Revert some existing commits. |
| Clean | `git_clean` | Remove untracked files from the working tree. |
| Blame | `git_blame` | Show what revision and author last modified each line of a file. |

## Grounding Rules (anti-hallucination)

Git is where agents hallucinate visibly — invented paths, fake SHAs, imagined repo
state, claimed-but-never-made commits. These rules make every claim about the
repository traceable to a real tool result **within the same task**. They compose the
existing mechanisms: structured `ToolResult` (Tool-API), path canonicalization
(SandboxPolicy §2), freshness checks (CONTEXT_MANAGEMENT §5), context trust tagging
(CONTEXT_MANAGEMENT §6), and verification gates (EXECUTION_LIFECYCLE §3, FR-AS-006).

### GR-1 — Structured results with repo snapshot (FR-GT-001)

- Every git tool returns **structured canonical data** in `ToolResult.Success.output`
  (JSON): files, SHAs, diffs, exit code — never free-form prose the model can misread.
- Every git `ToolResult` **attaches a fresh repo snapshot**: current branch, `HEAD`
  SHA, dirty/staged state, remotes. The agent reasons over the snapshot, never over
  memory or assumptions.

### GR-2 — Read-before-write gate (FR-GT-002)

- No mutating git operation (`git_add`, `git_commit`, `git_push`, `git_pull`,
  `git_merge`, `git_branch -d`, `git_reset`, `git_revert`, `git_clean`,
  `git_stash`) may execute **unless the agent performed a read pass in the same
  task**: `git_status` → `git_diff` → `git_log` → `git_branch` (as applicable).
- The read pass is enforced by the git tool wrapper (returns `ToolResult.Error` with `NXR-2003` and sets `ToolInvocation` status to `PENDING_AUTHORIZATION` if skipped) — not just prompt guidance.

### GR-3 — Path grounding (FR-GT-003)

- Every file path referenced in a plan or tool call must pass a real
  `file_exists` / `file_info` check before any mutation. A path that does not exist
  is **discovered** (`file_search`, `find`) — never assumed.
- `SandboxFileSystem` canonicalization remains the backstop; a Git-tool path escape is a Tool sandbox-policy violation and returns `NXR-2009`.

### GR-4 — SHA grounding (FR-GT-004)

- Branch/tag/commit references are resolved to **real SHAs** via `git_log` /
  `git_branch` / `git_remote` before being used as arguments. Fuzzy or fabricated
  references are rejected by the tool (`NXR-2003`).
- Verification always compares **SHAs, not descriptions**.

### GR-5 — Verify-after-write (FR-GT-005)

- After `git_commit`: `git_log -1` confirms the SHA; working tree clean.
- After `git_push`: local `HEAD` equals remote ref SHA (`git_log origin/<branch>`).
- After `git_merge` / `git_revert` / `git_reset`: read pass re-run; resulting tree
  matches the declared intent.
- Destructive previews (`git_reset --hard`, `git_clean`, force-push) require
  `PENDING_AUTHORIZATION` (the `ToolInvocation` is held for human approval) with a dry-run plan.

### GR-6 — Repo content is data, not instructions (FR-GT-006)

- Files inside a repository — especially from clones the agent did not author
  (README, `.github/`, commit messages, issues) — are **untrusted context segments**
  (CONTEXT_MANAGEMENT §6): labeled, isolated, injected as data with **zero
  authority**. The agent reports instructions found in files; it never follows them.
- Plan-vs-actual: at task end the final `git_diff` must match what the agent declared
  in its plan; deviations are reported explicitly, never papered over (ties to
  FR-EL-011 / FR-AS-006 gates).

## Phase Mapping

- **Phase 4**: Git tools implementation (13 tools + grounding rules GR-1..GR-6).
