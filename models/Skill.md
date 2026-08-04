> **Status: DERIVED** for Skill entity shape.
> This document defines the data model for Skill. Canonical lifecycle and behavior are defined in the owning architecture and state-machine documents.
>
> Depends on: the canonical architecture and lifecycle sources for Skill.
> Referenced by: APIs, SDKs, protocols, and tests that consume Skill.


# Domain Model: Skill

> Canonical domain model. See [docs/adr/ADR-0007-Skills-First-Class.md](../docs/adr/ADR-0007-Skills-First-Class.md) and [registry/SKILLS.md](../registry/SKILLS.md).

```kotlin
package com.nexora.app.runtime.skills

/**
 * A first-class expertise unit: WHAT expertise a task needs.
 * Distinct from Agent (WHO performs) and Tool (HOW it is performed) — ADR-0007.
 */
data class Skill(
    val id: String,                    // stable ID, e.g. "SKL-001"
    val name: String,                  // e.g. "Kotlin Development"
    val description: String,           // for AI discovery and planning
    val domain: SkillDomain,           // e.g. ANDROID, WEB, DATA, DEVOPS, SECURITY
    val requiredTools: List<String>,   // tool IDs this skill relies on (TOOL-###)
    val applicableAgents: List<String>,// agent types that can hold this skill (AGT-###)
    val source: SkillSource,           // BUILT_IN, USER_DEFINED, LEARNED
    val prerequisites: List<String> = emptyList(),  // skill IDs required first
    val preferredModelFamilies: List<String> = emptyList(), // e.g. ["coding", "reasoning"]
    val version: String = "1.0.0"
)

enum class SkillDomain {
    ANDROID, KOTLIN, JVM, WEB, DATA, DEVOPS, TESTING, SECURITY,
    DOCUMENTATION, RESEARCH, PRODUCTIVITY, AUTOMATION
}

enum class SkillSource { BUILT_IN, USER_DEFINED, LEARNED }

/**
 * An agent's acquired skills — the agent's capability set.
 */
data class AgentSkillBinding(
    val agentId: String,
    val skillId: String,
    val proficiency: Float = 1.0f,     // 0..1, grows with use (LEARNED source)
    val acquiredAt: Instant,
    val lastUsedAt: Instant?
)

/**
 * Registry of skills and agent–skill bindings. Lives in the runtime module.
 */
interface SkillRegistry {
    suspend fun register(skill: Skill)
    suspend fun get(skillId: String): Skill?
    suspend fun list(domain: SkillDomain? = null): List<Skill>
    suspend fun acquire(agentId: String, skillId: String): AgentSkillBinding
    suspend fun skillsOf(agentId: String): List<AgentSkillBinding>
    suspend fun validate(skill: Skill): SkillValidation  // checks tool refs exist
}
