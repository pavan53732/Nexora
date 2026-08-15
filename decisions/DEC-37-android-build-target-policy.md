# DEC-37 — Android Build Target and Compatibility Policy

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Android SDK, compile SDK, target SDK, and build-tool policy for the Nexora application.

## Problem

The documentation contains two incompatible build targets. The requirements and environment contract select API 34 for minimum, compile, and target behavior, while the Full Environment W^X section states `targetSdk=36`. The documented environment currently verifies API 34 and Build Tools 34.0.0, not API 36.

## Decision

Nexora uses Android API 34 as the minimum SDK, compile SDK, and target SDK for the current source implementation baseline. Build Tools 34.0.0 and JDK 21 remain the baseline toolchain requirements. The current application is a pure Android application; this decision does not alter that classification.

The `targetSdk=36` statement in the Full Environment specification is not applicable to the current baseline. It must be treated as a future compatibility note only if a later architecture decision explicitly selects a newer target and updates the complete toolchain and release contract.

## Constraints and consequences

The Android scaffold MUST compile against API 34 and declare target SDK 34. Documentation and implementation MUST NOT rely on API-36-only behavior. Android 15/API 35 runtime behavior remains a compatibility concern for devices running newer Android versions and is handled by the existing foreground-service, WorkManager, checkpoint, and handoff contracts; it does not change the target SDK baseline.

Any future target upgrade requires an explicit decision, updated SDK/build-tools verification, compatibility review, performance review, manifest review, and planned device evidence before source configuration changes.

## Invariants

This decision does not create a new lifecycle state, permission scope, provider, sandbox mechanism, or deployment architecture. It preserves Android-native implementation, min API 34, Kotlin, Gradle, Compose, Room, DataStore, Hilt, and WorkManager requirements already selected elsewhere.

## Required projections

Requirements/CONSTRAINTS.md, requirements/DEPENDENCIES.md, specs/FULL_ENVIRONMENT.md, docs/ENVIRONMENT_SETUP.md, docs/PERFORMANCE_BUDGET.md, and source-start traceability MUST use API 34 as the current baseline. The incompatible targetSdk=36 claim MUST be removed or explicitly qualified as future-only.
