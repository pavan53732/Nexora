# DEC-28 — ROADMAP Terminology Normalization

## Status

**Accepted documentation decision.**

## Context

The ROADMAP used “Navigation framework” and “Plugin Framework interfaces” without defining either phrase as a canonical framework or implementation technology. The repository does define workspace-first navigation behavior in `ui/Navigation.md` and plugin interfaces, capability registration, and SDK contracts in `architecture/PLUGIN_SYSTEM.md` and `sdk/PluginSDK.md`.

## Decision

The ROADMAP uses the following evidence-backed terminology:

- `Workspace-first navigation (bottom navigation, workspace tabs, side drawer, and deep links)` for the Phase 1 navigation item.
- `Plugin interface, capability registration, and SDK contracts` for the Phase 1 plugin item.

These terms describe documented behavior and interfaces without selecting a navigation library, Android component, plugin runtime technology, package structure, or deployment mechanism.

## Consequences

`docs/ROADMAP.md` is aligned with `ui/Navigation.md`, `architecture/PLUGIN_SYSTEM.md`, and `sdk/PluginSDK.md`. The roadmap phase and planned status are unchanged.

The decision does not create new requirements, lifecycle states, APIs, SDK methods, framework dependencies, or implementation evidence.

## Authority and dependencies

Navigation behavior: `ui/Navigation.md` and `docs/adr/ADR-0006-Agent-First-Interaction-Model.md`.

Plugin architecture and capability registration: `architecture/PLUGIN_SYSTEM.md`, `sdk/PluginSDK.md`, `models/Plugin.md`, and `registry/PLUGINS.md`.

Projection: `docs/ROADMAP.md`.

This decision does not modify any existing `DEC-*` record.
