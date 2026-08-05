> **Status: DERIVED** for FEATURES registry.
> This document describes the registry surface for FEATURES. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for FEATURES.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Feature Registry — Nexora

> Stable identifiers for all features. Used across documentation, implementation, testing, and issue tracking.

## Prefix Convention

| Prefix | Domain |
|--------|--------|
| `FEAT-` | General features |
| `TOOL-` | Tools |
| `AGT-` | Agents |
| `PLG-` | Plugins |
| `PROV-` | Providers |
| `MEM-` | Memory features |
| `UI-` | UI features |
| `SEC-` | Security features |
| `PERF-` | Performance features |

## General Features

| ID | Feature | Phase | Status |
|----|---------|-------|--------|
| FEAT-001 | Workspace Management | 1 | Planned |
| FEAT-002 | Virtual File System (internal — ADR-0006) | 3 | Planned |
| FEAT-003 | Embedded Terminal (internal — agent-invoked, ADR-0006) | 3 | Planned |
| FEAT-004 | Agent Loop | 2 | Planned |
| FEAT-005 | Event Bus | 2 | Planned |
| FEAT-006 | Checkpoint System | 2 | Planned |
| FEAT-007 | Background Execution | 2 | Planned |
| FEAT-008 | Permission Manager | 2 | Planned |
| FEAT-009 | Streaming Responses | 5 | Planned |
| FEAT-010 | Dark/Light Theme | 1 | Planned |
| FEAT-011 | Material You | 1 | Planned |
| FEAT-012 | Multi-Workspace | 1 | Planned |
| FEAT-013 | Agent-First Chat Interaction (goal entry, streaming, activity feed — primary surface) | 1 | Planned |
| FEAT-014 | Full Tool Catalog (27 categories, 343 registered tools with stable IDs) | 4 | Planned |
| FEAT-015 | Scheduled Jobs (one-off delayed + recurring with constraints, WorkManager) | 2 | Planned |
| FEAT-016 | Rich Background Notifications (running, progress %, completed, failed, approval) | 2 | Planned |
| FEAT-017 | Knowledge Graph (entity extraction, relationships, traversal, semantic search) | 5 | Planned |
| FEAT-018 | Tool & File History (tool invocation records, file versioning with revert) | 2 | Planned |
| FEAT-019 | User Preferences (learned + explicit, global and per-workspace) | 4 | Planned |
| FEAT-020 | Sandbox Telemetry & Self-Monitoring (agents observe their own environment) | 3 | Planned |
| FEAT-021 | Workspace Snapshots & Rollback (full-workspace time travel) | 4 | Planned |
| FEAT-022 | Adaptive Autonomy Modes (manual / assisted / autopilot, risk-scored approvals) | 4 | Planned |
| FEAT-023 | Network Egress Policy & DLP (deny-by-default, allowlists, outbound inspection) | 3 | Planned |
| FEAT-024 | Quarantine & Content Scanning (network downloads gated before promotion) | 3 | Planned |
| FEAT-025 | Per-Agent Sandbox Isolation (sub-agents in separate sandbox instances) | 5 | Planned |
| FEAT-026 | Sandbox Templates (pre-baked environment profiles) | 3 | Planned |
| FEAT-027 | Skills as First-Class Capability (skill registry, agent–skill bindings, skill acquisition) | 4 | Planned |
| FEAT-028 | Complete Execution Lifecycle (objective → planning → selection → validation → verification → report → follow-up) | 2 | Planned |
| FEAT-029 | Software Engineering Pipeline (build, static analysis, tests, perf/security, auto-fix, final validation) | 4 | Planned |
| FEAT-030 | Web Search & Extraction (configurable search provider, extraction modes, quarantine-gated content) | 4 | Planned |
| FEAT-031 | Context Pipeline (structured state, token allocation, progressive summarization, resume reconstruction, freshness, tagging) | 2 | Planned |
| FEAT-032 | Autonomy Hardening (plan repair, heartbeat/watchdog, budget escalation, closed-loop learning, trust growth, verification gates) | 2 | Planned |
| FEAT-033 | Stability Hardening (idempotent exactly-once recovery, degradation ladder, fault-injection suite) | 2 | Planned |
| FEAT-034 | Multi-Instance Pipes (zero-config same-machine + LAN discovery, pairing, cross-instance delegation, broadcast routing — specs/PIPES.md) | 7 | Planned |
