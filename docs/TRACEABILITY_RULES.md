# Traceability Operating Rules — Nexora

## Purpose

This document defines repository operating rules for maintaining requirement-to-contract-to-validation traceability.

## Core Rules

- Every tracked requirement SHOULD have a stable row in `docs/TRACEABILITY.md`.
- Every validation reference SHOULD use a concrete case ID from `testing/cases/`.
- Every case inventory entry SHOULD declare owner, status, evidence path, and review date.
- Lifecycle-sensitive artifacts SHOULD reference the appropriate lifecycle authority when durable lifecycle semantics are material.
- Contract-sensitive changes SHOULD update traceability in the same change or explicitly record a gap.

## Evidence Rule

Evidence paths are defined by `testing/EVIDENCE_CONVENTIONS.md`. Placeholder paths are acceptable for planned coverage, but passed or failed status SHOULD eventually be accompanied by actual evidence artifacts.

## Audit Rule

Cross-document reconciliation audits SHOULD record remaining contradictions or coverage gaps instead of silently omitting them.
