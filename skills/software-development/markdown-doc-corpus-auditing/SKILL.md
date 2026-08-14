---
name: markdown-doc-corpus-auditing
description: "Use when auditing a large markdown doc corpus (docs/, specs/, architecture/, etc.) for collisions, drift, and stale references. Detect read-cache masking and force real file bytes before trusting any report."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
 hermes:
 tags: [documentation, auditing, evidence-based, markdown, traceability, cache-bypass]
 related_skills: [hermes-agent-skill-authoring, spec-corpus-governance, full-corpus-doc-review]
---

# Markdown Doc-Corpus Auditing

## Overview

When a repository is a large, heavily cross-referenced markdown documentation corpus
(docs/, specs/, architecture/, registry/, models/, etc.), most edits must be checked
against the *actual* on-disk bytes of many files, not cached or truncated views. This
skill encodes the workflow for running a complete, verifiable audit pass: full-file
reads, cross-reference validation, collision detection, and truth-recovery when a
read tool silently returns a stale "unchanged" stub instead of real content.

It exists because the single most common silent failure in doc corpora is not a
missing file — it is a *present-but-hidden* file whose real content the agent never
sees, leading to false "collision" reports or missed collisions.

## When to Use

- The user demands a "complete evidence-based report" with "verbatim line-level
 evidence for every claim" and forbids grep/search as a substitute for comprehension.
- The repo is documentation-heavy with 100+ md files across many directories
 (docs/, architecture/, specs/, requirements/, registry/, models/, etc.).
- You must verify cross-document references (e.g. ADR-0006, docs/api/*, TOOL-### IDs)
 resolve to real files and real sections.
- You are reconciling a commit that deleted/restructured documents (e.g. 0f77772)
 and must confirm which references are now dangling.

### Don't use for

- Codebases with code as the primary artifact (use `codebase-inspection` +
 `requesting-code-review` instead).
- Single-document review (plain `read_file` suffices).
- Repositories where the user has not demanded full-line-by-line evidence.

## Core Workflow (numbered, with completion criteria)

1. **Take inventory, not content.** Use `search_files(target='files')` to enumerate
 every file in scope; do NOT use `search_files(target='content')` as a substitute
 for reading. Completion: an explicit list of every md file with its path, in
 hand before any collision claim is written.

2. **Read each file in full via `read_file`.** No skipping lines. Completion: every
 file's full text has produced a tool result with real content (≥ 1 line, not a
 cache-stub). If any read returns ~300 chars or a `status: unchanged` stub, flag
 it immediately (see Pitfall P1).

3. **Suspect the read cache on small/stable files.** Several docs in a large corpus
 are small and get edited once then frozen; `read_file` dedup may serve a cached
 stub with no content. Completion test for these: the file's reported char count
 matches its actual disk size. If read_file reports ~294-310 chars for a file
 you know is larger, treat it as cache-stubbed (see Pitfall P1).

4. **Force real bytes via `execute_code` with Python `open()`.** For any file
 suspected of cache masking, bypass the read cache:
 ```python
 with open("absolute/path/to/file.md") as f:
 text = f.read()
 print(len(text), "chars")
 print(text[:3000])
 ```
 Completion: the printed char count and content come from disk directly, not from
 the read_file cache. Use this as the source of truth for any collision claim.
 See `references/cache-masking-detection-recipe.md`.

5. **Build the claim list from real bytes only.** Every collision/dead-reference
 assertion must cite `file:line` from content you have actually seen (cache-bypassed
 where needed). Completion: a draft report where no claim is unverifiable from the
 content in step 4.

6. **Validate cross-references against `git show origin/main:<path>`.** For "does
 file X exist on the remote?" questions, do not rely on your local working tree
 alone — query the remote ref directly so the user can trust the answer. Completion:
 at least one remote-verification command proving the file's presence (or absence)
 on origin/main.

7. **Commit/restore in the same pass as the report.** If the audit produces
 restorations or edits, the commit + push must go hand-in-hand; a report that
 points at missing files is only half-done until the repo state matches the report.
 Completion: `git push origin main` confirmed and the remote HEAD commit hash
 verified.

## Collision Classes to Look For (reference table)

| Class | What it is | Primary check |
|---|---|---|
| A. Direct contradictions | Two live docs state opposing facts | Full read both files |
| B. Stale cross-references | Doc points at an ID/section that no longer exists | grep IDs against target file's real content |
| C. Dangling file refs | Doc links a file that was deleted | `git ls-files` + `git log --diff-filter=D` |
| D. Metric mismatches | Same number, two different values (target vs budget) | Cross-check NFR.md vs ROADMAP.md vs BUDGET |
| E. Semantic drift / tensions | Not a contradiction, but a surface added without updating the constraint | Read the relevant security/threat doc after the spec change |
| F. Format defects | Table corruption (doubled pipes `\|\|`), truncation | Scan restored/created files for `l.startswith('||')` |

## Pitfall P1 — The read_file "unchanged" stub

- **Symptom:** `read_file` returns a 300-char-ish stub with text like
 `status: unchanged` or a misleading summary, with no actual file content.
- **Root cause:** internal read cache dedups re-reads of unchanged files; for
 small files it collapses to a stub.
- **Fix:** re-read the exact current bytes via `execute_code` + `open()`. Do not
 call `read_file` a third time — it will serve the same stub.
- **Trigger files in a doc corpus:** any small, stable file edited once then frozen
 (PRODUCT_VISION.md, GLOSSARY.md, ROADMAP.md, SYSTEM_DESIGN.md, TRACEABILITY_RULES.md,
 DEPENDENCY_GRAPH.md, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md).

## Pitfall P2 — "Stale" numbers in historical docs are not always collisions

- A document pinned to a commit date (e.g., `docs/DECISION_LOG.md` or `docs/CHANGELOG.md` pinned to a specific commit) intentionally carries time-capsule numbers. A
 mismatch between its tool count and current registry is *by design*, not a defect.
 Always check for a "pinned to commit" declaration before reporting a "stale number"
 collision.

## Pitfall P3 — Cache-masking hides real corruption

- When a tool corrupts a file (e.g. doubled pipes `||` on markdown tables from the
 patch tool), and that same file is then served from cache, the corruption never
 appears. Force `open()` reads on any file you patched, especially table-heavy docs.

## Verification Checklist

- [ ] Inventory step: every md file path enumerated before claims written
- [ ] Every cited `file:line` is verifiable from content in hand
- [ ] Every "missing file" claim is confirmed via `git ls-remote`/`git show origin/main`
- [ ] Every "stale number" claim is checked against a pinning declaration
- [ ] At least one `execute_code` `open()` read performed to bypass cache (see P1)
- [ ] If the audit changed files, a push + remote HEAD verification completed
- [ ] Final tree: `git status` clean relative to origin/main

## One-Shot Recipes

### Recipe 1: Recover files deleted in a specific commit, then verify

```
git restore --source=<commit>^ -- <path1> <path2> ...
git add -A && git commit -m "docs(recovery): restore files deleted in <commit>"
git push origin main
git show origin/main:docs/adr/ADR-0006-Agent-First-Interaction-Model.md | head -1 # verify
```
Completion: remote `git show` prints the file's real first line, proving it landed.

### Recipe 2: Audit the audit directory

When a prior audit dropped stale reports, verify nothing else references them:
```python
# scan whole tree for any reference to the basename of each deleted file
import os
for tgt in ["audit_2_report.md", ...]:
 for root,_,files in os.walk("."):
 for fn in files:
 t = open(os.path.join(root,fn), errors="ignore").read()
 if tgt.lower() in t.lower(): print("REF:", os.path.join(root,fn))
```
Completion: zero REF lines (or explicit notes on what should be updated).

