> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Regression Tests

## Scope

Regression tests ensure that fixed bugs never reoccur. Every resolved bug from the issue tracker must have a corresponding regression test that would have caught the original defect.

| Regression Area | What Is Guarded |
----------------|-----------------|
| Bug fixes | Each closed issue adds a test that reproduces the original failure condition |
| API compatibility | Public API signatures (Agent API, Tool API, Provider API, Plugin API) remain stable |
| Data migration | Room database schemas upgrade correctly from version N-1 to N |
| Plugin API backward compatibility | Plugins built against SDK 1.x continue to work on runtime 1.y |
| Provider config migration | Provider configurations survive app version upgrades without data loss |

## Framework Stack

| Tool | Purpose |
------|--------|
| JUnit 5 | Test runner |
| Room Migration Test Helper | `MigrationTestHelper` for schema upgrade verification |
| JsonUnit | JSON round-trip comparison for config migration |
| MockK | Mocking for backward-compatibility plugin loading |

## Regression Test Database

| Field | Value |
------|-------|
| Location | `src/test/kotlin/com/nexora/app/regression/` |
| Naming | `Regression_<IssueNumber>Test.kt` |
| Requirement | Every closed bug with label `bug` must have a regression test before merge |
| Linkage | Test class Javadoc references the GitHub issue: `@see https://github.com/nexora/app/issues/NNN` |

## Data Migration Testing

```kotlin
@Test
fun migrateFrom_v2_to_v3() {
    val db = helper.createDatabase(TEST_DB, 2)
    // Insert data in v2 schema
    db.execSQL("INSERT INTO workspaces (id, name) VALUES ('ws1', 'Test')")
    db.close()

    // Run migration
    val migrated = helper.runMigrationsAndValidate(TEST_DB, 3, true)

    // Verify v3 schema + data preserved
    val cursor = migrated.query("SELECT name, settings_json FROM workspaces WHERE id='ws1'")
    assertThat(cursor.moveToFirst()).isTrue()
    assertThat(cursor.getString(cursor.getColumnIndexOrThrow("settings_json"))).isNotNull()
}
```

## Plugin API Backward Compatibility

- **Test harness**: Load a plugin APK compiled against Plugin SDK 1.0 into the current runtime.
- **Verify**: Plugin activates, tools register, and execution completes without `NoSuchMethodError` or `AbstractMethodError`.
- **Matrix**: Test oldest supported SDK version (1.0) against current runtime version.

## Run Schedule

| Trigger | Scope |
---------|--------|
| Every PR | Regression tests for bugs fixed in the PR's target branch |
| Release branch | Full regression suite (all historical bug tests + migration tests) |
| Pre-release | Full suite + manual smoke test of previously-failed scenarios |