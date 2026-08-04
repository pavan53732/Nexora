# Skill Registry — Nexora

## Registry

The skill registry is the authoritative inventory of declared skill identities and capability semantics.

Each skill entry SHOULD include or derive the following metadata:

- stable `skillId`
- skill version or revision marker
- domain/capability scope
- prerequisite tools or providers where applicable
- minimum compatible API/SDK or manifest/schema version where relevant
- owning plugin or built-in origin

## Notes

Skills describe capability semantics, not direct execution authority. Execution remains governed by the owning agent, tool, provider, workflow, or plugin contract path.
