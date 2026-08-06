# ADR-0004: Sandboxed Execution

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect

## Context

The AI agent in Nexora needs to execute commands, run code, modify files, and manage processes. On Android, there are three approaches:

1. **Direct host execution**: The agent runs commands directly on the Android system. This is a security catastrophe — a misbehaving agent could delete user data, access contacts, or exfiltrate information.

2. **Container/VM**: Run a full Linux container or virtual machine. This provides strong isolation but is extremely heavy on mobile devices (hundreds of MBs of RAM, slow startup).

3. **Application-level sandbox**: Create an isolated execution environment within the app's private storage. The agent can only access files and processes within this sandbox. This is lighter than a VM but provides sufficient isolation for Nexora's use case.

## Decision

Nexora uses an **application-level sandbox**:

- All files live in `/data/data/com.nexora.app/sandbox/workspaces/{id}/`.
- All commands execute in isolated processes within the sandbox.
- Workspaces are isolated from each other.
- Resource quotas (CPU, memory, disk, network) are enforced per workspace.
- The sandbox includes a virtual file system, embedded terminal, and managed runtimes (Python, Node.js).

The Android OS provides the first layer of security (app sandbox). Nexora provides a second layer (workspace isolation within the app).

## Consequences

### Positive
- **Security**: AI cannot access the host system.
- **Performance**: Much lighter than a full VM.
- **Simplicity**: Leverages Android's existing app sandbox.
- **Isolation**: Workspaces cannot interfere with each other.

### Negative
- **Limited to Android capabilities**: Cannot run arbitrary Linux binaries.
- **No root access**: Cannot install system packages.
- **Runtime overhead**: Python and Node.js must be bundled or fetched.

### Mitigation
- Use Termux-compatible libraries for a Linux-like userland.
- Bundle minimal Python (via Chaquopy) and Node.js (via node-android) runtimes.
- Provide package managers (pip, npm) for installing additional packages within the sandbox.
