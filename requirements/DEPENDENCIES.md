> **Status: SUPPORTING** for DEPENDENCIES requirements.
> This document records focused requirements for DEPENDENCIES; canonical subsystem definitions remain in the owning architecture documents.


# External Dependencies — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## Android Platform

| Dependency | Version | Purpose |
-----------|---------|--------|
| Android SDK | API 34 (current min/compile/target baseline; DEC-37) | Target platform APIs |
| Build Tools | 34.0.0 | AAPT2, D8, R8 compilation for the API-34 baseline |
| Platform Tools | Latest | ADB, debugging |

## Language & Build

| Dependency | Version | Purpose |
-----------|---------|--------|
| JDK | 21 | Compilation and tooling |
| Kotlin | 2.0+ | Primary language |
| Gradle | 8.10+ | Build system |
| KSP | 2.0+-1.0.x | Annotation processing (preferred over KAPT) |

## UI

| Dependency | Version | Purpose |
-----------|---------|--------|
| Jetpack Compose | BOM 2024.x | Declarative UI framework |
| Material Design 3 | `androidx.compose.material3` | Design system, components, dynamic color |
| Compose Navigation | `androidx.navigation:navigation-compose` | Screen navigation |
| Coil | 3.x | Image loading (optional, for plugin icons/avatars) |

## Architecture

| Dependency | Version | Purpose |
-----------|---------|--------|
| Hilt | 2.51+ | Dependency injection (Dagger Hilt) |
| Room | 2.6+ | SQLite ORM with coroutines support |
| DataStore | 1.1+ | Preferences and typed key-value storage |
| Kotlin Coroutines | 1.8+ | Asynchronous programming |
| Kotlin Flow | 1.8+ | Reactive data streams |

## Networking

| Dependency | Version | Purpose |
-----------|---------|--------|
| OkHttp | 4.12+ | HTTP client with interceptor support |
| Retrofit | 2.11+ | Type-safe REST client for provider APIs |
| Kotlinx Serialization | 1.6+ | JSON serialization (preferred over Gson/Moshi) |

## Background & Security

| Dependency | Version | Purpose |
-----------|---------|--------|
| WorkManager | 2.9+ | Guaranteed background task scheduling |
| AndroidX Biometric | 1.2+ | Fingerprint/biometric authentication for sensitive actions |
| AndroidX Security Crypto | 1.1+ | EncryptedSharedPreferences and file encryption |

## Testing

| Dependency | Version | Purpose |
-----------|---------|--------|
| JUnit 5 | 5.10+ | Unit test framework |
| Mockito / MockK | 5.x / 1.13+ | Mocking for unit tests |
| Turbine | 1.1+ | Flow testing utilities |
| Compose UI Test | BOM 2024.x | UI component testing |
| Room Testing | 2.6+ | In-memory database for DAO tests |

## Version Management

All dependency versions are centralized in `gradle/libs.versions.toml`. No hardcoded version strings in module-level build files.
