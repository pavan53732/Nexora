# Traceability Coverage Plan — Nexora

## Inventory Baseline

The generated inventory snapshot records the current requirement and test-case identifier populations. It is evidence of enumeration scope, not proof of implementation coverage.

## Operating Status

- Requirement identifiers are enumerated from `requirements/FR.md` and `requirements/NFR.md`.
- Test identifiers are enumerated from `testing/cases/`.
- Existing matrix rows remain curated contract anchors; they do not yet represent complete one-row-per-requirement coverage.

## Next Coverage Waves

1. Add requirement rows for each uncovered FR identifier, preserving the canonical source section and owner.
2. Add requirement rows for each uncovered NFR identifier, preserving quality attribute, measurable target, and validation case.
3. Assign existing case IDs where semantics match; create new case IDs when no validation case is sufficiently specific.
4. Record `Status`, `Owner`, `Evidence`, and `Last Reviewed` for every new mapping.
5. Re-run the inventory snapshot after each coverage wave and record the delta in the audit.

## Guardrail

Do not mark coverage `OK` merely because an architecture or test document exists. `OK` requires an explicit requirement-to-contract-to-case mapping with a defined evidence location.
