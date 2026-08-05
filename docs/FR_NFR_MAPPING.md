# FR / NFR Placeholder-to-Actual Ledger Mapping

> **Status: CANONICAL** — mapping of placeholder IDs (`FR-TL-401`..`406`, `NFR-SEC-021`, etc.) to verified actual requirement IDs from `docs/REQUIREMENT_COVERAGE_LEDGER.md`.
> **Rule source:** `docs/TRACEABILITY_RULES.md` (Evidence Rule, Coverage Rule, Audit Rule).
> **Purpose:** Ensure no placeholder references remain unaligned; every reference points to a concrete, mapped requirement.

---

## Placeholder → Actual Mapping Table

| Placeholder ID | Actual Ledger ID | Category | Owner | Primary Artifact | Validation Case | Evidence Path | Status |
|---|---|---|---|---|---|---|---|
| `FR-TL-401` | `FR-TL001` | Tooling (MCP source) | Tooling | `architecture/TOOL_SYSTEM.md` | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-402` | `FR-TL002` | Tooling (MCP transport) | Tooling | `protocols/Tool-Protocol.md` | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-403` | `FR-TL003` | Tooling (MCP registry) | Tooling | `registry/TOOLS.md` | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-404` | `FR-TL004` | Tooling (MCP lifecycle) | Tooling | `architecture/TOOL_SYSTEM.md` (§Lifecycle) | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-405` | `FR-TL005` | Tooling (MCP security) | Tooling | `security/PermissionModel.md` (§MCP rules) | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `FR-TL-406` | `FR-TL006` | Tooling (MCP phase mapping) | Tooling | `specs/AI_PROVIDERS.md` (§Phase 5) | `IT-TOOL-001` | `evidence/integration/IT-TOOL-001/` | MAPPED |
| `NFR-SEC-021` | `NFR-SEC-001` | Security (deny-by-default) | Security | `security/PermissionModel.md` (§Deny-by-Default) | `SEC-PERM-001` | `evidence/security/SEC-PERM-001/` | MAPPED |

---

## Verification Notes

- **No placeholder patterns remain** in edited docs (`architecture/TOOL_SYSTEM.md`, `protocols/Tool-Protocol.md`, `registry/TOOLS.md`, `registry/TOOL_MATRIX.md`, `specs/BACKGROUND_EXECUTION.md`, `security/PermissionModel.md`, `security/SandboxPolicy.md`, `specs/BROWSER.md`, `specs/AI_PROVIDERS.md`, `docs/DECISION_LOG.md`). Verified with regex search (`FR-[A-Z]{2}-[4-9][0-9]{2}` etc.) — `0` matches.
- All edited documents reference **actual** ledger IDs (`FR-S016`, `FR-AS-009`, `FR-T011`, `FR-W005`, `FR-P011`, `FR-S014`/`015`, `FR-T015`, `FR-EV-002`/`006`, `FR-S028`, `FR-P009`, `NFR-REL-002`/`003`).
- Mapping aligns with `docs/TRACEABILITY_RULES.md` (Evidence Rule, Coverage Rule, Audit Rule) and `docs/REQUIREMENT_COVERAGE_LEDGER.md` (authoritative inventory).

---

## References

- `docs/REQUIREMENT_COVERAGE_LEDGER.md` (authoritative inventory — `FR-TL001`..`015`, `NFR-SEC-001`..`013`).
- `docs/TRACEABILITY_RULES.md` (mapping rules — Evidence, Audit, Coverage).
- `docs/DECISION_LOG.md` (`DL-020` MCP, `DL-021` OEM, `DL-022` Security, `DL-023` Blocked-List, `DL-024` Voice/Camera — all mapped to actual `FR`/`NFR` IDs).
- `docs/CHANGELOG.md` (`v4.5.0` preserved; `G4–G5` entry present — no `v4.6` added per user instruction).

---

*No placeholders remain unmapped. All references point to verified ledger entries.*
