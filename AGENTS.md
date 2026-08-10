# AGENTS.md — Nexora Repository Rules

> Every AI agent (Hermes, Codex, Claude Code, OpenCode, etc.) operating in this
> repository must follow these rules. Override any model-level defaults that
> conflict.

## Rule 1 — Read files in full (line-by-line, not grep)

This repository is documentation-heavy. Every Markdown file is a specification
artifact with cross-references, canonical ownership declarations, and precise
requirement IDs. Skimming, grep-matching keywords, or reading only a few lines
will miss critical context.

- Use `read_file` (or equivalent) to read every line of every file relevant to
  the task.
- Never use grep/search as a substitute for full-file comprehension.
- After reading: the agent must be able to state what each file owns, what
  status it claims, and what other files it references.
- If a file was read earlier in the session and `read_file` returns a cached
  "unchanged" stub, re-verify current bytes via a direct filesystem read
  (e.g., `execute_code` with `open()`) before acting on stale context.

## Rule 2 — Evidence-based work (zero assumptions)

Every claim must be backed by the actual file contents, cited as `path:line`.

- Do not assume a symbol exists — find its definition.
- Do not assume a cross-reference resolves — verify it.
- Do not assume a library is available — check the project manifest.
- Do not assume tool counts, phase numbers, or requirement IDs — read the
  current file. Stale numbers from prior sessions or outdated research
  documents are not authoritative.

## Rule 3 — Match existing conventions

- Status headers: `CANONICAL`, `SUPPORTING`, `DERIVED` — do not change a
  file's status without justification.
- Table format: consistent column counts, no doubled-pipe (`||`) defects
  (a known patch-tool artifact — scan for it after every edit).
- IDs: `FR-<PREFIX>-NNN` (e.g. `FR-W001`), `NFR-<PREFIX>-NNN` (e.g. `NFR-PERF-001`), `TOOL-NNN`, `TM-NNN`, `DL-NNN`,
  `ADR-NNNN` — use the existing naming scheme. Verify IDs exist before
  citing them.
- Links: repository-relative (`../architecture/RUNTIME.md`). From
  `docs/` subdirectories, use `../../` to reach the repo root.

## Rule 4 — Minimal edits, no drive-by changes

- Touch only what the task needs. No reformatting, no renames, no
  "while I'm here" cleanups unless the task explicitly asks.
- When a file change spans many locations, use `patch` in replace mode
  with unique surrounding context.
- If a patch fails twice, rewrite the enclosing section with `write_file`
  instead of attempting a third patch.
- After every patch on a table, scan for doubled pipes (`||`).

## Rule 5 — Respect canonical ownership

- [`docs/CANONICAL_SOURCES.md`](docs/CANONICAL_SOURCES.md) defines which
  document owns each concept. Do not fix a derived document by
  contradicting its canonical source.
- When two files conflict, the canonical source wins. Record the conflict
  if the derived document needs updating.

## Rule 6 — Historical records are not stale

- `CHANGELOG.md` and `DECISION_LOG.md` entries are historical snapshots.
  Do not rewrite them just to remove old numbers or outdated counts.
- Historical sections in `FR_NFR_MAPPING.md` (e.g., S4 mapping) describe
  what was mapped at that time — do not "fix" them to current values.
- The research document (`docs/research/NEXORA_VS_ZCODE_CAPABILITY_GAP.md`)
  is pinned to a specific commit and has a historical-snapshot banner.
  Its metrics are intentionally frozen.

## Rule 7 — Verify after editing

After any edit:
- `git diff --check` — no whitespace errors
- Scan for doubled pipes (`||` at line starts) in every touched table
- Verify all cited IDs (FR, NFR, TOOL, TM, DL, ADR) exist in their
  source files
- Verify all relative links resolve from the file's directory

## Rule 8 — Commit with detailed messages

Commit messages must describe:
- What was changed (file:line range)
- Why it was changed (the contradiction or gap)
- What was verified (the validation commands run)
- What was intentionally preserved (historical references left untouched)
