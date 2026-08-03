# Security Policy — Nexora

---

## Reporting a Vulnerability

If you discover a security vulnerability in Nexora, please report it responsibly.

### How to Report

1. **Preferred**: Open a GitHub Issue with the `security` label. Do not include exploit details publicly.
2. **Sensitive**: If the vulnerability is critical and should not be disclosed publicly, contact the maintainer directly.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Android version and device tested on

### What We Commit To

- Acknowledge receipt within 48 hours
- Assess the severity and impact
- Develop and release a fix in a timely manner
- Credit the reporter (unless anonymity is requested)
- Follow coordinated disclosure (no public disclosure until a fix is available)

## Security Architecture

Nexora is designed with security as a core principle:

- **Sandboxed execution** — AI agents never access the host system directly.
- **Workspace isolation** — Each workspace is isolated from others.
- **Permission system** — Every tool requires explicit permission.
- **Encrypted storage** — API keys stored via Android Keystore.
- **Audit logging** — Every action is logged.

See [architecture/SECURITY_MODEL.md](architecture/SECURITY_MODEL.md) for the full security architecture.
