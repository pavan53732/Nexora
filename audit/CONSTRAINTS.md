# Design and Implementation Constraints — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## Platform

| Constraint | Detail |
|-----------|--------|
| Target platform | Android native only — no cross-platform frameworks (no Flutter, React Native, KMP UI) |
| Rationale | Full access to Android APIs, optimal performance, native sandbox capabilities |

## Language

| Constraint | Detail |
|-----------|--------|
| Primary language | Kotlin (100% new code) |
| Secondary language | Java only where required by third-party libraries or Android internals |
| Style | Idiomatic Kotlin — sealed classes, coroutines, extension functions, value classes |

## Build System

| Constraint | Detail |
|-----------|--------|
| Build tool | Gradle with Kotlin DSL (`build.gradle.kts`) |
| Wrapper | Gradle wrapper checked into VCS — no version skew across environments |
| Version catalog | Dependencies managed via `libs.versions.toml` |

## Minimum SDK

| Constraint | Detail |
|-----------|--------|
| Min API level | 34 (Android 14) |
| Target API level | 34 |
| Compile API level | 34 |
| Rationale | Predictable behavior, modern APIs (photo picker, predictive back, granular permissions) |

## Architecture

| Constraint | Detail |
|-----------|--------|
| Server-side components | **None.** All logic runs on-device or via API calls to external AI providers |
| Root access | **Not required.** App must function on stock, unrooted devices |
| Inter-module communication | **Event bus only.** No direct dependencies between feature modules |
| Persistent data location | **App private storage only.** No external storage writes without explicit user action |

## Size

| Constraint | Detail |
|-----------|--------|
| APK size target | < 50MB base (without plugins or downloaded models) |
| Rationale | Fast downloads, low storage impact, Play Store compliance |

## Security

| Constraint | Detail |
|-----------|--------|
| Tool execution | Must run within sandbox boundaries — no direct filesystem access outside designated paths |
| Filesystem access | No direct access outside the app's sandbox and user-granted directories |
| API keys | Never stored in plaintext; never committed to VCS; never logged |

## AI Providers

| Constraint | Detail |
|-----------|--------|
| Provider model | External API calls only — providers are not bundled with the app |
| Supported providers | OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, LM Studio, GGUF, Custom endpoint |
| Local models | Ollama, LM Studio, GGUF run as separate on-device processes, not embedded |

## Plugin API

| Constraint | Detail |
|-----------|--------|
| API stability | Plugin API must remain backward-compatible across minor version bumps (x.y.z where y changes) |
| Breaking changes | Only permitted in major version increments with documented migration guide |

## Data

| Constraint | Detail |
|-----------|--------|
| Storage | All persistent data resides in app's private storage (`getFilesDir()`, Room DB, DataStore) |
| No cloud sync | No built-in cloud sync — users may export/import data manually |
