# Traceability Operating Rules — Nexora

## Purpose

This document defines repository operating rules for maintaining requirement-to-contract-to-validation traceability.

## Core Rules

- Every requirement in `requirements/FR.md` and `requirements/NFR.md` MUST appear in `docs/REQUIREMENT_COVERAGE_LEDGER.md`.
- Every tracked requirement SHOULD have a stable row in `docs/TRACEABILITY.md` once its owner and implementation surfaces are known.
- Every validation reference SHOULD use a concrete case ID from `testing/cases/`.
- Every case inventory entry SHOULD declare owner, status, evidence path, and review date.
- Lifecycle-sensitive artifacts SHOULD reference the appropriate lifecycle authority when durable lifecycle semantics are material.
- Contract-sensitive changes SHOULD update traceability in the same change or explicitly record a gap.

## Evidence Rule

Evidence paths are defined by `testing/EVIDENCE_CONVENTIONS.md`. Placeholder paths are acceptable for planned coverage, but passed or failed status SHOULD eventually be accompanied by actual evidence artifacts.

## Audit Rule

Cross-document reconciliation audits SHOULD record remaining contradictions or coverage gaps instead of silently omitting them.

## Coverage Rule

The coverage ledger is the authoritative completeness checkpoint. A requirement is not considered covered merely because a related architecture document exists; coverage requires an identified owner, primary artifact, validation case, and evidence path or an explicit evidence exception.
