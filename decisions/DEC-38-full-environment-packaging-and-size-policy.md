# DEC-38 — Full Environment Packaging and Release-Size Policy

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Delivery packaging and size measurement for the bundled Full Environment.

## Problem

The documentation contains a base APK target below 50 MB and critical thresholds of 50 MB/60 MB, while the Full Environment specification requires a 50–70 MB compressed Debian rootfs bundled with the application and the performance document estimates approximately 75 MB for the base app with the Full Environment.

## Decision

The Full Environment remains bundled as an architecture-specific APK/AAB asset because it is the selected execution environment for autonomous agent work. Release-size gates apply to the architecture-specific compressed AAB/APK delivery artifact received by a user, not to an aggregate artifact containing every ABI rootfs.

The architecture-specific delivery target is 80 MB download size. The approximately 95 MB multi-ABI aggregate package is not the user delivery measurement and is not a release gate. The prior `<50 MB base APK` and `60 MB all-bundled-resources` limits are superseded for builds that include the Full Environment; they remain applicable only to a minimal foundation variant that excludes the Full Environment assets.

## Packaging constraints

The Android App Bundle MUST deliver only the matching rootfs and proot assets for the device ABI. The build MUST keep the base application and Full Environment asset measurements separate and MUST report both the architecture-specific delivery size and the aggregate build size. The rootfs remains app-private at runtime, is integrity-verified, and uses the existing read-only base plus per-workspace writable overlay model.

A release fails when the architecture-specific delivered artifact exceeds 80 MB unless an explicitly recorded release exception includes the measured size, cause, mitigation, and owner approval. The minimal foundation variant remains subject to the existing 50 MB base and 60 MB all-resource gates when it is built without the Full Environment.

## Invariants

This decision does not change sandbox containment, rootfs integrity verification, app-private storage, provider routing, permissions, or the Full Environment’s Phase-3 implementation mapping. It does not authorize external downloads as a replacement for the bundled baseline.

## Required projections

requirements/CONSTRAINTS.md, docs/PERFORMANCE_BUDGET.md, specs/FULL_ENVIRONMENT.md, docs/ENVIRONMENT_SETUP.md, docs/ROADMAP.md, and release-test documentation MUST distinguish minimal-foundation limits from architecture-specific Full Environment delivery limits.
