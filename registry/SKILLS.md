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
