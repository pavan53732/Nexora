# Environment Tiers Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md) | [../docs/ENVIRONMENT_SETUP.md](../docs/ENVIRONMENT_SETUP.md)

---

## 1. Overview

Nexora's sandbox provides three environment tiers, each offering increasing capability and fidelity to a standard Linux userland. The **Full Environment (Tier 2)** is the default and primary target — a complete Debian-slim rootfs bundled in the APK, providing glibc compatibility, `apt` package management, and full binary wheel support for pip/npm.

| Tier | Name | Size | C Library | Package Manager | Bundled | Default |
|------|------|------|-----------|---------------|---------|---------|
| 0 | Embedded Shell | ~2 MB | N/A | N/A | Yes | No |
| 1 | Micro Environment | ~5 MB | musl | `apk` (Alpine) | Optional | No |
| 2 | **Full Environment** | **~50–70 MB** | **glibc** | **`apt` (Debian)** | **Yes** | **Yes** |

## 2. Tier 0 — Embedded Shell

### 2.1 Purpose

Zero-latency command execution for simple file operations. No Linux userland — pure Kotlin/Java implementations of common shell commands.

### 2.2 Available Commands

- Navigation: `ls`, `cd`, `pwd`, `tree`
- File ops: `cat`, `head`, `tail`, `touch`, `mkdir`, `rm`, `cp`, `mv`, `chmod`
- Search: `grep`, `find` (basic)
- Archive: `zip`, `unzip`, `tar` (limited formats)
- Environment: `export`, `env`, `echo`, `which`
- Git: `git` (pure Java implementation via JGit)

### 2.3 Limitations

- No native binary execution
- No `apt`, `pip`, `npm` (package managers unavailable)
- No compilation toolchain
- Python/Node runtimes not available

### 2.4 When Used

- Workspace initialization before Tier 2 extraction
- Fallback when Tier 2 is corrupted or reset
- Ultra-low-memory mode on devices with < 3GB RAM

## 3. Tier 1 — Micro Environment (Alpine/musl)

### 3.1 Purpose

Optional lightweight Linux userland for size-constrained deployments where APK bloat must be minimized.

### 3.2 Specifications

- **Base**: Alpine Linux rootfs (minirootfs)
- **Size**: ~5 MB compressed, ~15 MB extracted
- **C library**: musl libc
- **Package manager**: `apk`
- **Shell**: BusyBox ash

### 3.3 Limitations (Critical)

| Issue | Impact | Mitigation |
|-------|--------|------------|
| musl/glibc incompatibility | pip/npm binary wheels often fail to install or run | Source compilation required; slower; needs build tools in sandbox |
| Limited package repository | Many packages unavailable in Alpine repos | Tier 1 explicitly marked as limited; agent warned |
| BusyBox GPL-2.0 | License risk if bundled in APK | Bundled as separate asset with license attribution; not linked into app code |
| Agent training mismatch | Agents trained on `apt`/`dpkg`; `apk` is niche | Auto-detect and inject `apk` cheat-sheet into agent context |

### 3.4 When Used

- User explicitly selects "Minimal Install" during onboarding
- Device storage critically low (< 500 MB free)
- Enterprise policy mandates minimal APK footprint

### 3.5 Bundling Model

Tier 1 is **optional** — included as a secondary asset in the APK but not extracted by default. User choice during first launch determines which tier is activated.

## 4. Tier 2 — Full Environment (Debian-slim/glibc) ⭐ DEFAULT

### 4.1 Purpose

Complete Linux userland enabling true agent autonomy: arbitrary package installation, binary execution, compilation, and full compatibility with the Python/Node ecosystem.

### 4.2 Specifications

- **Base**: Debian 12 (Bookworm) slim variant
- **Size**: ~50–70 MB compressed (xz), ~180–220 MB extracted
- **C library**: glibc 2.36+
- **Package manager**: `apt` (Advanced Package Tool)
- **Shell**: `bash` (default), `dash` (minimal)
- **Pre-installed**: `python3`, `python3-pip`, `nodejs`, `npm`, `git`, `curl`, `wget`, `ca-certificates`, `build-essential` (meta)

### 4.3 Bundling Architecture

```text
APK assets/
├── rootfs/
│   ├── debian-slim-arm64.tar.xz
│   ├── debian-slim-x86_64.tar.xz
│   └── manifest.json
├── proot/
│   ├── proot-arm64
│   └── proot-x86_64
└── licenses/
    └── debian-slim-LICENSE
```

### 4.4 Extraction Lifecycle

| Phase | Action | Storage Location |
|-------|--------|----------------|
| **First Launch** | Detect architecture → select correct tar.xz → stream-extract to app-private storage | `/data/data/com.nexora.app/rootfs/` |
| **Verification** | SHA-256 checksum of extracted tree vs manifest; re-extract on mismatch | — |
| **Mount** | proot binds `/` to extracted rootfs, workspace files into `/workspace` | Runtime only |
| **Execution** | All shell commands run inside proot namespace | — |
| **Cache** | Extracted rootfs persists across app restarts | App-private storage |
| **Reset** | User can "Reset Environment" — wipe rootfs, re-extract from APK assets | — |
| **Update** | New APK version contains updated rootfs; diff-extract only changed files | — |

### 4.5 proot Execution Model

```text
Android Kernel (unmodified)
└── Nexora App Process (UID: app_123)
    └── proot (static binary, no root required)
        └── Debian-slim rootfs
            ├── /usr/bin/python3  → workspace Python scripts
            ├── /usr/bin/apt      → package installation
            ├── /usr/bin/node     → Node.js runtime
            └── /workspace        → bind-mount to VFS (read-write)
```

**Key properties:**

- **No root required**: proot uses `ptrace` for syscall interception and path rewriting
- **No kernel modules**: Pure userspace; works on supported Android versions
- **Bind mounts**: Workspace VFS exposed as `/workspace` inside rootfs
- **Network**: Inherits Android network namespace; egress proxy still applies (FR-S014)

### 4.6 glibc Binary Wheel Compatibility

| Ecosystem | Tier 2 Support | Tier 1 (Alpine) Status |
|---|---|---|
| **PyPI (pip)** | ✅ Binary wheels install directly (`manylinux` tags match glibc) | ❌ Often fails; requires `--no-binary` or compilation |
| **npm** | ✅ Native modules compile against glibc; prebuilt binaries work | ⚠️ Mixed; some packages assume glibc |
| **Cargo (Rust)** | ✅ Standard target `aarch64-unknown-linux-gnu` | ⚠️ Needs `musl` target or cross-compile |
| **Go** | ✅ Standard Linux builds work | ✅ Static binaries work; cgo may fail |
| **Conda** | ✅ Miniforge works (Linux ARM64) | ❌ Not supported on musl |

### 4.7 Workspace Integration

Each workspace mounts the **same read-only rootfs** with a **private writable overlay** for per-workspace state:

```text
/data/data/com.nexora.app/
├── rootfs/
├── workspaces/
│   └── {workspace-id}/
│       ├── files/
│       ├── rootfs-overlay/
│       │   ├── tmp/
│       │   ├── var/cache/apt/
│       │   ├── usr/local/
│       │   └── home/agent/
│       └── env/
```

**Overlay mechanism**: proot's root and bind options create a union view. Writes go to the overlay; reads fall through to the shared base. This keeps the base rootfs pristine while allowing per-workspace customization.

### 4.8 Package Installation Flow

```text
Agent: apt install ffmpeg jq
↓
Sandbox: proot apt update && proot apt install -y ffmpeg jq
↓
Overlay: Packages installed to workspace overlay
↓
VFS: Changes reflected in workspace files
↓
Persistence: Overlay preserved across sessions and app restarts
```

**Quota enforcement**: apt downloads and installed packages count toward workspace disk quota. Apt cache is auto-pruned after install where safe.

### 4.9 Python Environment

```bash
python3 --version
pip3 --version
python3 -m venv /workspace/.venv
source /workspace/.venv/bin/activate
pip install numpy pandas requests
```

### 4.10 Node Environment

```bash
node --version
npm --version
cd /workspace
npm init -y
npm install express lodash
```

## 5. Environment Selection & Auto-Promotion

### 5.1 User Selection (Onboarding)

```text
Welcome to Nexora
├── [Recommended] Full Environment (~70 MB)
│   └── Debian Linux with apt, pip, npm — maximum capability
├── [Minimal] Micro Environment (~5 MB)
│   └── Alpine Linux with apk — limited packages, smaller size
└── [Advanced] Embedded Shell Only (~2 MB)
    └── Basic commands, no package manager — expert use
```

Default selection: Full Environment (Tier 2).

### 5.2 Auto-Promotion (Agent-Driven)

| Trigger | Action | User Notification |
|---|---|---|
| Agent runs `apt` in Tier 0/1 | Prompt user to enable Full Environment | One-tap enable; extraction begins |
| `pip install` fails with a manylinux compatibility error in Tier 1 | Suggest Tier 2 with explanation | Non-blocking |
| `npm install` requires native compilation in Tier 1 | Detect missing headers; suggest Tier 2 | Contextual hint in activity feed |

### 5.3 Runtime Tier Switching

```kotlin
enum class EnvironmentTier { EMBEDDED, MICRO, FULL }

class WorkspaceSandbox {
    var currentTier: EnvironmentTier = EnvironmentTier.FULL
}
```

## 6. Performance Characteristics

| Metric | Tier 0 | Tier 1 | Tier 2 |
|---|---:|---:|---:|
| Cold start | < 50 ms | 2–5 s | 3–8 s |
| Warm start | < 50 ms | < 100 ms | < 200 ms |
| Memory overhead | 5 MB | 20 MB | 80 MB |
| Disk footprint (per workspace) | 10 MB | 25 MB | 50 MB + overlay |
| Package install speed | N/A | Slow | Fast |
| `pip install numpy` | N/A | 3–5 minutes | 10–20 seconds |

## 7. Security Model

### 7.1 Rootfs Integrity

- SHA-256 checksums for every file in `manifest.json`
- Signature verification with Nexora release key
- Re-extraction triggered on checksum mismatch
- Base rootfs is read-only; only overlay is writable

### 7.2 proot Isolation

- proot runs as app UID with no privilege escalation
- ptrace scope is limited to child processes
- Android seccomp-bpf still applies
- Network egress is filtered by the in-app proxy (FR-S014)

### 7.3 GPL Compliance (Bundled Model)

Since Tier 2 and Tier 1 contain GPL components bundled in the APK:

| Requirement | Implementation |
|---|---|
| Source code offer | `licenses/` directory contains license/source-offer information |
| License attribution | In-app Open Source Licenses screen lists all components |
| No linking | Rootfs is a data asset, not linked into app code |
| Modification rights | Users can extract and modify the rootfs; modifications void support |

Legal review is required before Google Play submission.

## 8. Phase Mapping

| Phase | Deliverable |
|---|---|
| Phase 1 | Tier 0 interface contracts and basic command implementations |
| Phase 2 | Tier 2 rootfs build pipeline and proot integration design |
| Phase 3 | Tier 2 extraction, verification, proot execution, apt/pip/npm integration |
| Phase 4 | Tier 1 optional Alpine environment and onboarding selection UI |
| Phase 5 | Environment templates |
| Phase 6 | Cross-architecture support |
| Phase 8 | Template marketplace |

## 9. Related Specifications

- [architecture/SANDBOX.md](../architecture/SANDBOX.md)
- [specs/TERMINAL.md](TERMINAL.md)
- [docs/ENVIRONMENT_SETUP.md](../docs/ENVIRONMENT_SETUP.md)
- [requirements/FR.md](../requirements/FR.md)
- [requirements/RISKS.md](../requirements/RISKS.md)
- [security/SandboxPolicy.md](../security/SandboxPolicy.md)
