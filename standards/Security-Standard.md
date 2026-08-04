> **Status: SUPPORTING** for Security Standard coding standard.
> This document defines conventions for Security Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Security Standard — Nexora

## Principles
1. **Sandbox everything** — No direct host system access.
2. **Least privilege** — Request minimum permissions.
3. **Encrypt secrets** — Use Android Keystore for API keys.
4. **Audit everything** — Log all actions with timestamps.
5. **Resource limits** — Enforce quotas per workspace.

## API Key Handling
- Store in Android Keystore via `SecureKeyStore` class.
- Never log, print, or expose API keys.
- Never include API keys in crash reports.
- Allow biometric protection for key access.

## Network Security
- All provider connections use HTTPS.
- Certificate pinning for known providers.
- No HTTP connections (except localhost for Ollama/LM Studio).

## Plugin Security
- Plugins declare required permissions in their manifest.
- Users approve permissions at install time.
- Plugins cannot access other plugins' data.
- Plugins run in a try/catch wrapper to prevent crashes.

## Data Storage
- All data in app-private storage (`/data/data/com.nexora.app/`).
- No external storage access without explicit permission.
- Workspace data is isolated per workspace.
