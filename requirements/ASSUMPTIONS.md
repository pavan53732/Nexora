# Project Assumptions — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

## Device

| Assumption | Detail |
|-----------|--------|
| RAM | Device has >= 4GB RAM available to the app |
| Processor | ARM64 (AArch64) architecture — no 32-bit support required |
| Storage | >= 1GB free storage for app data, sandboxes, and local models |
| Android version | Android 14 (API 34) or later with Material Design 3 / Material You support |
| Google Play Services | Available on device (reserved for future Firebase integration) |

## Network

| Assumption | Detail |
|-----------|--------|
| Connectivity | Active internet connection required for cloud-based AI provider calls |
| Offline | App remains functional in read-only mode when offline; agent execution requires network |
| Latency | Network latency to providers is acceptable for streaming responses (< 2s first token) |

## User

| Assumption | Detail |
|-----------|--------|
| API keys | User has API keys for at least one configured AI provider |
| Single user | One user per device — no multi-user, multi-tenant, or profile switching |
| Permissions | User grants runtime permissions (storage, notifications) when prompted |
| Technical level | User understands basic AI agent concepts; onboarding covers the rest |

## AI Providers

| Assumption | Detail |
|-----------|--------|
| External services | AI providers (OpenAI, Anthropic, etc.) are third-party SaaS with their own SLAs |
| Local models | Ollama, LM Studio, and GGUF run as separate on-device processes managed by the user |
| API stability | Provider APIs follow their published specs; breaking changes are infrequent |

## Plugins

| Assumption | Detail |
|-----------|--------|
| Distribution | Plugins are distributed via Nexora Hub (future) or sideloaded as signed packages |
| Trust model | Users accept plugin permissions before installation; no pre-vetting by Nexora |
| Isolation | Plugins run in isolated classloaders and cannot crash the host app |

## Development

| Assumption | Detail |
|-----------|--------|
| Build environment | Developers use Android Studio Hedgehog or later with JDK 21 |
| Version control | Git with conventional commits; PR-based workflow |
| CI/CD | GitHub Actions available for automated builds and tests |