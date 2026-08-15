# DEC-27 — Concrete Requirement Owner Labels

## Status

**Accepted documentation decision.**

## Context

The requirement coverage ledger used `Platform Infrastructure` as an owner label for maintenance, compatibility, and portability requirements. The repository did not define that phrase as a canonical owner or category. The affected rows already pointed to concrete authorities: `standards/Coding-Standard.md`, `VERSIONING.md`, and `docs/ENVIRONMENT_SETUP.md`.

## Decision

The coverage and regression projections use concrete evidence-backed owner labels:

- `Coding Standards` for requirements mapped to `standards/Coding-Standard.md`.
- `Compatibility & Versioning` for requirements mapped to `VERSIONING.md`.
- `Environment & Portability` for requirements mapped to `docs/ENVIRONMENT_SETUP.md`.
- `Compatibility & Migration` for the manifest/schema backward-compatibility regression case `RT-MIG-001`.

`Platform Infrastructure` is not treated as a canonical Nexora owner category.

## Consequences

`docs/REQUIREMENT_COVERAGE_LEDGER.md` and `testing/cases/RegressionTestCases.md` use the concrete labels above. The requirement identities, primary artifacts, validation IDs, and semantics remain unchanged.

This decision does not create a new subsystem, owner component, lifecycle, API, implementation mechanism, or source code.

## Authority and dependencies

Primary authorities: `standards/Coding-Standard.md`, `VERSIONING.md`, `docs/ENVIRONMENT_SETUP.md`, and `testing/cases/RegressionTestCases.md`.

Projection: `docs/REQUIREMENT_COVERAGE_LEDGER.md`.

This decision does not modify any existing `DEC-*` record.
