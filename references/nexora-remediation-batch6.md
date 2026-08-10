# Nexora Remediation Batch 6 — governance backfill, orphan record, ID-scheme correction (DL-048)

Committed: `HEAD` (main → origin/main). Previous HEAD: `da2b9ca`.

## Context

This batch resumes the schema-aware architectural audit (methodology:
`skills/software-development/markdown-doc-corpus-auditing`). The audit models
the corpus as a typed graph (CANONICAL/SUPPORTING/DERIVED status per
`docs/CANONICAL_SOURCES.md`, ID namespaces FR/NFR/TOOL/TM/DL/ADR) and validates
every cited ID against its authoritative declaration source.

Batches 1–5 (DL-040..044) and the DL-045..047 diagram suite were committed but
**never entered `docs/DECISION_LOG.md`**, leaving a governance-traceability gap
(`docs/TRACEABILITY_RULES.md` Audit Rule + the repository's own convention that
every reconciliation is a DL entry). This batch closes that gap and records the
remaining genuine orphans honestly rather than silently omitting them.

## Findings refined (false positives cleared)

A naive grep pass initially flagged 14 "dangling" IDs. Schema-aware verification
reclassified most as by-design:

- `TOOL-012/013/014` — **false positive**: only occur inside `IT-TOOL-012/013/014`
  (test-case IDs, a separate namespace). No standalone `TOOL-012/013/014` exists.
- `FR-TL-401..406`, `NFR-SEC-021` — **placeholders**, explicitly mapped to real
  ledger IDs in the CANONICAL `docs/FR_NFR_MAPPING.md`. By design.
- `FR-AS-013` — **deliberately absent**, documented as such in
  `docs/research/EMBEDDED_RUNTIME_STRATEGY.md`. By design.

## Genuine findings closed in this batch

### 1. `docs/DECISION_LOG.md` — backfill missing DL entries
- Added `DL-025` (S1 Dynamic Concurrency Cap), `DL-026` (S2 MCP canonical),
  `DL-032` (Embedded runtime strategy + KG phase promotion) — these were cited in
  `docs/CHANGELOG.md` / `specs/TERMINAL.md` but absent from the log.
- Added `DL-041` (Batch 2), `DL-042` (Batch 3), `DL-043` (Batch 4),
  `DL-044` (Batch 5), `DL-045`/`DL-046`/`DL-047` (diagram suite) — the entire
  reconciliation + diagram-suite trail that was committed but never logged.
- Log now spans DL-001..DL-047 continuously (the prior internal gaps at
  DL-025/026/032 are now filled; DL-018/019/034 duplicates noted as superseded
  markers already present, not data defects).

### 2. `docs/TRACEABILITY.md` — honest orphan record (Audit Rule)
- Added an Open Gaps note recording `FR-SESS-001`, `FR-WF-001`, `NFR-COMP-001` as
  matrix rows whose IDs are not yet defined in `requirements/FR.md`/`NFR.md` or the
  authoritative `docs/REQUIREMENT_COVERAGE_LEDGER.md`, with the canonical coverage
  that already exists for each (SessionLifecycle/WorkflowLifecycle/VERSIONING +
  Registry-Standard). These are recorded, not silently dropped, pending an explicit
  decision to define the IDs or re-point the rows.

### 3. `AGENTS.md:40` — ID-scheme correction
- Rule 3 listed `FR-XXX-NNN`, `NFR-XXX-NNN`. The actual corpus uses
  `FR-<PREFIX>-NNN` (e.g. `FR-W001`) / `NFR-<PREFIX>-NNN` (e.g. `NFR-PERF-001`)
  — 93 FR / 57 NFR IDs. Corrected the canonical rule to the real scheme so any
  future automated traceability keys on the correct format.

## Cleanup
- Deleted the leftover `references/nexora-remediation-batch3.md` stub
  (content: `REMOVE-ME`) — a stray reminder file, not a real report.

## Validation run
```
git diff --check                                                                  # CLEAN
grep -n '^||' docs/DECISION_LOG.md docs/TRACEABILITY.md AGENTS.md                 # no doubled pipes
grep -c 'DL-0\(25\|26\|32\|4[1-7]\)' docs/DECISION_LOG.md                        # 10 new rows present
test -f references/nexora-remediation-batch3.md && echo STUB-REMAINS || echo STUB-GONE   # STUB-GONE
grep -n 'FR-<PREFIX>-NNN' AGENTS.md                                              # corrected scheme
```
- `docs/DECISION_LOG.md` DL range now DL-001..DL-047 (continuous).
- Registry totals unchanged: 352 tools / 28 categories (Batch 4's "350" was stale).

## Reuse notes for future batches
- **Namespace disambiguation**: when scanning for `TOOL-NNN`, exclude prefixes like
  `IT-TOOL-NNN` (test-case IDs) — a bare `\bTOOL-\d+\b` matches inside them and
  produces false "dangling tool" findings.
- **Placeholder tolerance**: references inside a CANONICAL placeholder-ledger
  (`FR_NFR_MAPPING.md`) are intentionally unmapped and must not be flagged.
- **Deliberate-absence patterns**: a doc that states "X is deliberately absent /
  undefined" is not a dangling reference.
- **Governance hygiene**: any committed reconciliation batch SHOULD be a DL entry
  in the same pass; the missing DL-041..047 + DL-025/026/032 were a process gap,
  not content defects.
