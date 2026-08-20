> **Status: DERIVED** for skill registry inventory. Skills are first-class capabilities per ADR-0007; canonical definitions in [../models/Skill.md](../models/Skill.md).

# Skill Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `skillId` | Stable skill identifier |
| `version` | Skill revision marker |
| `origin` | Built-in or plugin source |
| `domainScope` | Capability/domain scope |
| `prerequisites` | Required tools/providers/skills |
| `minContractVersion` | Minimum compatible contract or manifest/schema version |

## Notes

The Skill registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).

A lesson may be promoted to an existing `LEARNED` Skill only after the existing provenance, evidence, trust, safety, scope, and lifecycle conditions pass and the existing deterministic policy path or user path approves promotion. Policy-approved promotion MUST be recorded through existing Skill Registry, memory, audit, and evidence projections. Acquired or learned Skills remain subject to the existing retirement path. This registry projection creates no new Skill authority, permission, identity, or lifecycle.
