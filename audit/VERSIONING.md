> Back to [PROJECT_SPECIFICATION.md](./PROJECT_SPECIFICATION.md)

# Nexora Versioning Strategy

Nexora uses multiple coordinated versioning schemes — one for the application, one for documentation, one for data schemas, and one for plugin/provider APIs. Each is independent but designed to coexist without ambiguity.

## 1. Semantic Versioning (Application)

The Android application follows **MAJOR.MINOR.PATCH** per [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

| Segment | Meaning | Trigger |
|---------|---------|--------|
| **MAJOR** | Breaking changes | Tool contract change, agent API removal, database schema incompatibility |
| **MINOR** | New features, backward compatible | New agent type, new tool, UI feature, provider addition |
| **PATCH** | Bug fixes | Crash fix, logic correction, performance improvement without API change |

Pre-release suffixes follow the `-betaN` / `-rcN` convention:

| Version | Stage |
|---------|-------|
| `1.0.0-beta1` | Feature-complete, internal testing |
| `1.0.0-rc1` | Release candidate, public beta |
| `1.0.0` | Stable release |
| `1.1.0` | First feature release |
| `1.1.1` | Bug fix release |

## 2. Document Versioning

Specification documents in the repository carry their own version in the document header (currently `v3.0.0` in `PROJECT_SPECIFICATION.md`). Documents use a simplified **MAJOR.MINOR** scheme.

| Segment | Meaning |
|---------|---------|
| **MAJOR** | Structural overhaul, sections reorganized, scope changes |
| **MINOR** | Content updates, new sections added, corrections |

Examples: `v3.0.0` → `v3.1.0` (new section added), `v4.0.0` (complete restructuring). The patch segment is reserved for future use if needed.

## 3. Schema Versioning

All structured data formats carry an integer `schemaVersion` field:

| Schema | Location | Migration |
|---------|----------|-----------|
| Room database | `@Database(version = N)` | AutoMigration + manual fallback |
| Tool parameter definitions | `tool.json` → `schemaVersion` | JSON migration scripts |
| Plugin manifests | `manifest.json` → `schemaVersion` | Validation on load |

Migrations are tracked in the `SchemaMigration` Room entity. Each row records `fromVersion`, `toVersion`, `migrationClass`, `appliedAt`, and `checksum`.

```kotlin
@Entity(tableName = "schema_migrations")
data class SchemaMigration(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val fromVersion: Int,
    val toVersion: Int,
    val migrationClass: String,
    val appliedAt: Long = System.currentTimeMillis(),
    val checksum: String
)
```

## 4. Plugin API Compatibility

The Plugin SDK follows full SemVer. Every plugin declares compatibility bounds:

```json
{
  "minSdkVersion": "1.0.0",
  "maxSdkVersion": "2.0.0",
  "sdkVersion": "1.2.0"
}
```

| SDK Change | Version Impact |
|------------|---------------|
| New optional method / interface | MINOR bump |
| Behavior change in existing API | MINOR bump (if backward compatible) |
| Removed or renamed method / signature change | MAJOR bump |

The runtime validates `minSdkVersion ≤ currentSdkVersion ≤ maxSdkVersion` on plugin load. Plugins outside the range are quarantined with a user-facing incompatibility notice.

## 5. Provider API Versioning

Provider interfaces are treated as **stable contracts**. New capabilities are added via optional interface methods or new provider interfaces — never by modifying existing method signatures. Provider configuration objects carry a `version` field for migration when the config schema evolves.

## 6. Version Format Summary

| Artifact | Format | Example |
|----------|--------|---------|
| App | MAJOR.MINOR.PATCH[-prerelease] | `1.0.0`, `1.1.0-beta2` |
| Document | vMAJOR.MINOR.PATCH | `v3.0.0`, `v3.1.0` |
| Database Schema | Integer | `schemaVersion = 3` |
| Plugin SDK | SemVer string | `sdkVersion = "1.2.0"` |
| Plugin Manifest | SemVer bounds | `minSdk: "1.0.0", maxSdk: "2.0.0"` |
| Provider Config | Integer | `version = 2` |

## 7. Migration Strategy

| Layer | Mechanism |
|-------|-----------|
| **Database** | Room `AutoMigration` for simple column additions; manual `Migration` classes for data transforms. All migrations checksummed. |
| **Config / JSON** | Versioned JSON migration scripts in `assets/migrations/`, applied at startup by `ConfigMigrator`. |
| **Plugin SDK** | Shim layer in the host app provides deprecated-method wrappers when `minSdkVersion` < current MAJOR. Shims log deprecation warnings. |

## 8. Release Channels

| Channel | Audience | Cadence | Source |
|---------|----------|---------|--------|
| **Canary** | Internal team | Per commit | `develop` branch |
| **Beta** | Early adopters | Weekly or per milestone | `beta` branch, Play Store beta track |
| **Stable** | All users | Milestone-driven | `main` branch, Play Store production track |

Canary builds append `-canary.YYYYMMDD` to the version. Beta builds use standard SemVer prerelease tags. Stable builds carry no suffix.
