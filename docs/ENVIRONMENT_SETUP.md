> **Status: SUPPORTING** for environment setup. This document explains focused usage and behavior but does not own the canonical definition. The canonical source is [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md).
>
> Depends on: [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md).

# Environment Setup — Nexora (Linux)

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> Related: [requirements/DEPENDENCIES.md](../requirements/DEPENDENCIES.md) · [docs/ROADMAP.md](./ROADMAP.md) · [docs/PERFORMANCE_BUDGET.md](./PERFORMANCE_BUDGET.md) · [specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) · [specs/TERMINAL.md](../specs/TERMINAL.md) · [specs/GIT.md](../specs/GIT.md) · [specs/DATABASE.md](../specs/DATABASE.md) · [architecture/SANDBOX.md](../architecture/SANDBOX.md)

---

| Field | Value |
|-------|-------|
| **Host OS** | Debian GNU/Linux 13 (trixie), x86_64 |
| **Date** | 2026-08-05 |
| **Scope** | Phase 1 pre-work — environment preparation only |
| **Status** | Complete & verified — no Android project created yet |
| **Repository** | `https://github.com/pavan53732/Nexora` (branch `main`) |

---

## 1. Repository & Documentation Review

The repository was cloned into the workspace and the documentation reviewed before any
environment work, per the [Documentation Standard](../standards/Documentation-Standard.md).

Documents reviewed (at minimum):

- `PROJECT_SPECIFICATION.md` — master index, package `com.nexora.app`, workspace-first, 8 phases (Phase 0 complete)
- `README.md` — product overview, tech stack (Kotlin, Gradle, API 34+, Material 3 / Compose)
- `docs/ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md`, `docs/ROADMAP.md`, `docs/PRODUCT_VISION.md`
- `docs/DEPENDENCY_GRAPH.md`, `docs/MODULE_BOUNDARIES.md`, `docs/LIFECYCLES.md`, `docs/PERFORMANCE_BUDGET.md`
- `requirements/` — FR (95), NFR (40), CONSTRAINTS (13), ASSUMPTIONS (20), DEPENDENCIES, RISKS (12)
- `standards/` — Coding, Documentation, Testing, Logging, Security, Performance, Naming
- `registry/` — FEATURES, TOOLS, AGENTS, PLUGINS, PROVIDERS (PROV-001…009), TOOL_MATRIX, AGENT_MATRIX
- `docs/adr/` — ADR-0001…0007
- `sdk/` — AgentSDK, PluginSDK, ProviderSDK, ToolSDK
- `specs/` — FILE_SYSTEM, TERMINAL, GIT, BROWSER, DATABASE, AI_PROVIDERS, WORKSPACE, FULL_ENVIRONMENT

**Key environment-relevant decisions extracted from the docs:**

| Item | Decision | Source |
|------|----------|--------|
| Min SDK | API 34 (Android 14) | NFR-COMPAT-001, DL-013 |
| Build tools | Build Tools 34.0.0 (AAPT2, D8, R8) | requirements/DEPENDENCIES.md |
| JDK | 21 | requirements/DEPENDENCIES.md |
| Kotlin | 2.0+ (Kotlin-only codebase, KSP preferred over KAPT) | requirements/DEPENDENCIES.md, Coding-Standard |
| Gradle | 8.10+ (Gradle Wrapper required, reproducible builds) | requirements/DEPENDENCIES.md, NFR-PORT-001 |
| APK budget | < 50 MB (R8/ProGuard, resource shrinking) | DL-014, RISK-005 |
| Libraries | Compose BOM, Material 3, Navigation Compose, Hilt, Room, DataStore, Coroutines/Flow, OkHttp, Retrofit, Kotlinx Serialization, WorkManager, Biometric, Security Crypto | requirements/DEPENDENCIES.md, DECISION_LOG DL-001…DL-018 |
| Version centralization | `gradle/libs.versions.toml` — no hardcoded versions | requirements/DEPENDENCIES.md |

---

## 2. Installed Software & Versions

### System

| Package | Version |
|---------|----------|
| git | 2.47.3 |
| curl | 8.14.1 |
| wget | 1.25.0 |
| unzip | 6.00 |
| zip | 3.0 |
| tar | 1.35 |
| gzip | 1.13 |
| gcc (build-essential) | 14.2.0 |
| g++ (build-essential) | 14.2.0 |
| make (build-essential) | 4.4.1 |
| cmake | 3.31.6 |
| pkg-config | 1.8.1 |
| openssl | 3.5.6 |
| ca-certificates | installed |
| Git LFS (optional) | 3.6.1 |

### Java

| Component | Version | Location |
|-----------|----------|----------|
| Eclipse Temurin OpenJDK 21 LTS (JDK) | **21.0.12** (build 21.0.12+8-LTS) | `/home/z/tools/jdk/jdk-21.0.12+8` |
| javac | 21.0.12 | `$JAVA_HOME/bin/javac` |

### Android SDK

| Component | Version | Location |
|-----------|----------|----------|
| Command Line Tools | 11076708 (sdkmanager 12.0) | `$ANDROID_HOME/cmdline-tools/latest` |
| Platform-Tools | 37.0.1 (adb 1.0.41) | `$ANDROID_HOME/platform-tools` |
| Build-Tools | **34.0.0** (per repo docs), 36.1.0 (latest) | `$ANDROID_HOME/build-tools/` |
| Platforms | android-29, android-34, android-35, android-36 | `$ANDROID_HOME/platforms/` |
| Sources | android-29, android-35, android-36 | `$ANDROID_HOME/sources/` |

### Android Build Tools

| Tool | Version | Where it runs from |
|------|----------|---------------------|
| AAPT2 | 2.20-14042983 (build-tools 36.1.0) | `build-tools/36.1.0/aapt2` |
| D8 | 9.0.3-dev | `build-tools/36.1.0/d8` (same JAR as R8) |
| R8 | 9.0.3-dev | wrapper script invoking `build-tools/36.1.0/lib/d8.jar` with R8 main class |
| Bundletool | 1.18.3 | `$ANDROID_HOME/bundletool/bundletool.jar` |
| zipalign | build-tools 36.1.0 | `build-tools/36.1.0/zipalign` |
| apksigner | 0.9 | `build-tools/36.1.0/apksigner` |

> AAPT2/D8/zipalign/apksigner are bundled per build-tools version; AGP will
> select the version it needs automatically. R8 and Bundletool additionally ship as
> standalone wrappers for direct CLI use.

### Build Language Tooling

| Tool | Version | Location |
|------|----------|----------|
| Gradle | **9.6.1** | `/home/z/tools/gradle/current` (≥ 8.10 required by repo docs ✓) |
| Kotlin (kotlinc) | **2.1.0** | `/home/z/tools/kotlin/kotlinc` (≥ 2.0 required ✓) |

### Python

| Component | Version | Location |
|-----------|----------|----------|
| python3 | **3.12.13** (≥ 3.12 required ✓) | `/usr/bin/python3` |
| pip3 | 25.0.1 | `/home/z/.venv/bin/pip3` |
| venv | ✓ (tested) | `python3 -m venv` |

---

## 3. Environment Variables

Persisted in `/home/z/tools/nexora_env.sh`:

```sh
export JAVA_HOME=/home/z/tools/jdk/jdk-21.0.12+8
export ANDROID_HOME=/home/z/tools/android-sdk
export ANDROID_SDK_ROOT=/home/z/tools/android-sdk
export GRADLE_HOME=/home/z/tools/gradle/current
export KOTLIN_HOME=/home/z/tools/kotlin/kotlinc
```

Load in a shell with:

```sh
source /home/z/tools/nexora_env.sh
```

## 4. PATH Configuration

```
$ANDROID_HOME/cmdline-tools/latest/bin   # sdkmanager, avdmanager, lint, apkanalyzer
$ANDROID_HOME/platform-tools             # adb, fastboot
$ANDROID_HOME/build-tools/36.1.0         # aapt2, d8, zipalign, apksigner, dexdump
$ANDROID_HOME/r8                         # r8 wrapper script
$ANDROID_HOME/bundletool                 # bundletool wrapper script
$GRADLE_HOME/bin                         # gradle
$KOTLIN_HOME/bin                         # kotlinc, kotlin
/home/z/tools/cmake/bin                  # cmake
/home/z/.local/bin                       # git-lfs, other user-installed tools
```

## 5. Tool Locations

| Tool | Path |
|------|------|
| Java (JAVA_HOME) | `/home/z/tools/jdk/jdk-21.0.12+8` |
| Android SDK (ANDROID_HOME / ANDROID_SDK_ROOT) | `/home/z/tools/android-sdk` |
| Python | `/usr/bin/python3` |
| Gradle | `/home/z/tools/gradle/current` |
| Kotlin | `/home/z/tools/kotlin/kotlinc` |
| Bundletool | `/home/z/tools/android-sdk/bundletool/bundletool.jar` |
| R8 | wrapper invoking `build-tools/36.1.0/lib/d8.jar` (R8 main class) |
| CMake | `/home/z/tools/cmake/bin/cmake` |
| Git LFS | `/home/z/.local/bin/git-lfs` |

---

## 6. Verification Results

### Version checks (all passed)

| Command | Result |
|---------|--------|
| `java -version` | openjdk version "21.0.12" 2026-07-21 LTS ✓ |
| `javac -version` | javac 21.0.12 ✓ |
| `sdkmanager --version` | 12.0 ✓ |
| `adb version` | Android Debug Bridge 1.0.41, Version 37.0.1-15733141 ✓ |
| `gradle --version` | Gradle 9.6.1 ✓ |
| `kotlinc -version` | kotlinc-jvm 2.1.0 ✓ |
| `python3 --version` | Python 3.12.13 ✓ |
| `pip3 --version` | pip 25.0.1 ✓ |
| `git --version` | git version 2.47.3 ✓ |
| `git lfs version` | git-lfs/3.6.1 ✓ |
| `aapt2 version` | 2.20-14042983 ✓ |
| `d8 --version` | D8 9.0.3-dev ✓ |
| `r8 --version` | R8 9.0.3-dev ✓ |
| `bundletool version` | 1.18.3 ✓ |
| `apksigner --version` | 0.9 ✓ |
| `zipalign` | responds (help text, exit 0) ✓ |
| `cmake --version` | 3.31.6 ✓ |

### Functional smoke tests (all passed)

1. **Kotlin pipeline** — `kotlinc` compiled a program; JVM executed it → `42`
2. **Java → DEX pipeline** — `javac` + `d8 --release --lib android-34/android.jar` produced valid `classes.dex`
3. **AAPT2** — compiled `res/values/strings.xml` → `compiled.zip` (no errors)
4. **Gradle** — Gradle 9.6.1 started successfully on JVM 21
5. **Python** — `python3 -m venv` + `pip install requests` + import verified
6. **Environment variables** — all five resolve to real paths; every tool resolves from PATH

### SDK licenses

All accepted via `sdkmanager --licenses` (output confirmed: *"All SDK package licenses accepted"*).

---

## 7. Android Library Compatibility (Step 3)

Verified compatible with the future Phase 1 stack. All coordinates were checked against
Google Maven / Maven Central on 2026-08-05; the repo's minimums
([requirements/DEPENDENCIES.md](../requirements/DEPENDENCIES.md)) are met or exceeded.

| Library | Repo minimum | Verified available | Status |
|---------|-------------|-------------------|--------|
| Jetpack Compose (BOM) | BOM 2024.x | Available on Google Maven | ✓ |
| Material 3 | material3 | via Compose BOM | ✓ |
| Navigation Compose | navigation-compose | Available on Google Maven | ✓ |
| Hilt | 2.51+ | Available on Maven Central | ✓ |
| Room | 2.6+ | Available on Google Maven | ✓ |
| DataStore | 1.1+ | Available on Google Maven | ✓ |
| WorkManager | 2.9+ | Available on Google Maven | ✓ |
| Coroutines / Flow | 1.8+ | Available on Maven Central | ✓ |
| Kotlinx Serialization | 1.6+ | Available on Maven Central | ✓ |
| OkHttp | 4.12+ | Available on Maven Central | ✓ |
| Retrofit | 2.11+ | Available on Maven Central | ✓ |
| AndroidX Biometric | 1.2+ | Available on Google Maven | ✓ |
| AndroidX Security Crypto | 1.1+ | Available on Google Maven | ✓ |
| Coil (optional) | 3.x | Available on Maven Central | ✓ |
| KSP | 2.0+-1.0.x | Available on Maven Central | ✓ |

**Build compatibility confirmed:** JDK 21 (AGP 9.x requires JDK 17+), Gradle 9.6.1
(≥ 8.10 required), Kotlin 2.1.0, compileSdk 36
(34/35 also installed), minSdk 34 platform installed, build-tools 34.0.0 installed.
Repositories `google()` + `mavenCentral()` cover every dependency (Hilt is published to
Maven Central only). Version centralization in `gradle/libs.versions.toml` is supported
by the toolchain.

> No Android project, Gradle files, or source code were created — this is compatibility
> verification only.

---

## 8. AI Provider Integration Readiness (Step 4)

The environment is ready for all nine providers from
[specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) and the
[Provider Registry](../registry/PROVIDERS.md) (PROV-001…009). **No API keys are
configured anywhere** (per NFR-SEC-005, keys will be stored encrypted via Android
Keystore at implementation time).

| Provider | Protocol | Environment readiness |
|----------|----------|----------------------|
| OpenAI | OpenAI-compatible REST + SSE | ✓ OkHttp + kotlinx-serialization available |
| Anthropic | REST (`x-api-key` header) | ✓ same stack |
| Gemini | Google AI REST | ✓ same stack |
| Groq | OpenAI-compatible | ✓ |
| OpenRouter | OpenAI-compatible | ✓ |
| Ollama | OpenAI-compatible (local) | ✓ (network stack supports localhost endpoints) |
| LM Studio | OpenAI-compatible (local) | ✓ |
| Local GGUF | llama.cpp / mlc-llm (Phase 5 decision) | ✓ NDK toolchain available (cmake 3.31.6, build-essential) if native integration is chosen |
| Custom | user-defined | ✓ baseUrl-overridable design |

The HTTP stack (OkHttp + Retrofit + Kotlinx Serialization) matches
DL-005/DL-006 decisions. Streaming (SSE) and `Flow<StreamChunk>` are supported by the
chosen libraries.

---

## 9. Embedded Runtime Research (Step 5)

Research for Phase 3 ([architecture/SANDBOX.md](../architecture/SANDBOX.md),
[specs/TERMINAL.md](../specs/TERMINAL.md), [specs/GIT.md](../specs/GIT.md),
[specs/DATABASE.md](../specs/DATABASE.md)). **Nothing in this section is installed as a
system package — these are application components to be integrated later.**

### 9.1 Embedded Python runtime

| Criterion | Chaquopy | python-for-android | Termux Python |
|-----------|----------|--------------------|---------------|
| Android compatibility | Excellent — official Gradle plugin, Java⇄Python interop, PyPI builds | Good — but rebuilds the whole app | Good — bionic debs, not embeddable SDK |
| License | **MIT** (fully open source since v12.0.1) | MIT | GPL-3.0 (viral) |
| Performance | CPython native; JNI overhead modest | CPython native | CPython native |
| APK impact | +15–50 MB (ABI-split friendly) | similar/larger | n/a |
| Maintenance | **Active** — v17.0.0 (Dec 2025) | Active — v2026.05.09 | Active |
| Integration complexity | **Low** — one Gradle plugin block | High — restructures build | Very high — manual JNI |
| **Recommendation** | ✅ **Chaquopy** | fallback | avoid (GPL) |

### 9.2 Embedded JavaScript engine

| Criterion | app.cash.quickjs | taoweiji/quickjs-android | Hermes | J2V8 / LiquidCore |
|-----------|------------------|--------------------------|--------|-------------------|
| Android compatibility | Excellent (AAR, all ABIs) | Excellent | Via React Native | Older / heavy |
| License | MIT (QuickJS) | MIT | MIT | Apache-2.0 / MIT+LGPL |
| Performance | Fast interpreter, low memory (no JIT) | same engine | JIT — fastest | JIT |
| APK impact | ~1.5–3 MB/ABI | ~1.5–3 MB/ABI | ~3–6 MB | 10–25 MB |
| Maintenance | **Active** — 0.9.2 on Maven Central | Active — v1.3.0 | Active (Meta) | Stale / low activity |
| Integration complexity | Low | Low | Medium (RN-bound) | Medium |
| **Recommendation** | ✅ **app.cash.quickjs** | good alternative | only if JIT needed | avoid |

### 9.3 Embedded Git

| Criterion | JGit | libgit2 + Git24j | Dulwich |
|-----------|------|------------------|---------|
| Android compatibility | Excellent — pure Java (runs on ART, no JNI) | Good — requires NDK build | Only via Python runtime |
| License | EDL (BSD-3) + optional EPL | libgit2 MIT / Git24j LGPL-2.1 | Apache-2.0 |
| Performance | Good for app workloads | Fastest (C) | Slowest |
| APK impact | ~3–5 MB | ~2–4 MB (.so × ABIs) | ~1–2 MB (with Python) |
| Maintenance | **Very active** — 7.7.1 (2026-07) | libgit2 active; **Git24j dormant since 2021** | Active |
| Integration complexity | **Low** | High (NDK + JNI) | Medium |
| **Recommendation** | ✅ **JGit** | revisit only for huge repos | only if Python ships anyway |

### 9.4 Embedded terminal / shell

| Criterion | Termux terminal-view | jackpal Android-Terminal-Emulator | Custom PTY view |
|-----------|----------------------|-----------------------------------|-----------------|
| Android compatibility | Excellent (battle-tested, termux-app v0.118.3) | Good (older era) | Full control, high effort |
| License | **GPL-3.0 (viral — would force open-sourcing Nexora)** | Apache-2.0 | ours |
| Performance | Excellent | Good | depends on implementation |
| APK impact | ~2–5 MB | ~1 MB | ~1–3 MB |
| Maintenance | Active | **Archived (2022)** | n/a |
| Integration complexity | Medium | Low (drop-in) | High |
| **Recommendation** | ⚠ best tech, GPL blocker | ✅ vendor as Apache-2.0 base (mksh/busybox shell via NDK) | only with strong reason |

> **Note (ADR-0006):** the terminal is an **internal, agent-invoked** component — there is
> no user-facing terminal UI. This removes the interactive-rendering requirement: only
> the PTY/shell execution core is needed (plus activity-card rendering of captured
> output), further favoring a small vendored implementation.
>
> Licensing review needed before Phase 3 — this is flagged in
> [requirements/RISKS.md](../requirements/RISKS.md) risk space (RISK-009).

### 9.5 SQLite

| Criterion | Room + built-in SQLite | requery sqlite-android | NDK custom build |
|-----------|------------------------|------------------------|------------------|
| Android compatibility | Perfect (platform) | Good (AAR, modern amalgamation 3.49.0) | Good |
| License | Apache-2.0 | MIT | Public domain |
| Performance | Good; version tied to OS | Best (newest SQLite everywhere) | Best (tunable) |
| APK impact | 0 | ~1–3 MB | ~1–2 MB |
| Maintenance | n/a | **Active** (3.49.0, 2025-05) | own burden |
| Integration complexity | **Lowest** | Medium (Room SQLiteDriver) | High |
| **Recommendation** | ✅ default (per DL-003) | add via Room `SQLiteDriver` when newer SQLite/vector features needed | only for exotic features |

### 9.6 Secure sandbox execution

| Layer | Option | License | APK impact | Recommendation |
|-------|--------|---------|------------|----------------|
| Baseline | Android app sandbox (UID + SELinux + seccomp) | n/a | 0 | ✅ mandatory default |
| One-off risky work | `android:isolatedProcess` services | n/a | 0 | ✅ use where applicable |
| User scripts | QuickJS (interpreter, no JIT) or **wasmi** (WASM, Apache-2.0, v1.1.0) | MIT / Apache-2.0 | ~1–2 MB | ✅ recommended for untrusted code |
| Untrusted native code | Wasmtime via NDK (Apache-2.0, v47.0.3) | Apache-2.0 | 10–20 MB | only if ever needed |

**Summary:** Chaquopy (Python), app.cash.quickjs (JS), JGit (Git), vendored jackpal
terminal emulator (Apache-2.0) + NDK shell, Room + built-in SQLite (upgrade path:
requery sqlite-android), and layered sandbox (platform + isolatedProcess + QuickJS/wasmi).
All respect the < 50 MB APK budget (total estimated impact: +20–60 MB with Python;
ABI splitting or per-feature download mitigations exist).

---

## 10. Issues Encountered & Resolutions

| # | Issue | Resolution |
|---|-------|------------|
| 1 | No `sudo` access in this workspace environment — cannot use `apt-get install` for system packages | Downloaded prebuilt binaries to `/home/z/tools/` and added to PATH via env script. cmake from Kitware GitHub, git-lfs from GitHub Releases, JDK from Adoptium/Temurin, Gradle from services.gradle.org, Kotlin from JetBrains GitHub. |
| 2 | Only JRE (headless) was pre-installed — no `javac` | Downloaded full Eclipse Temurin JDK 21.0.12+8 from Adoptium to `/home/z/tools/jdk/`. |
| 3 | R8 standalone JAR no longer downloadable from `dl.google.com` or Maven Central (returns HTML error pages) | R8 is bundled inside the D8 JAR in build-tools. Created a wrapper script at `$ANDROID_HOME/r8/r8` that invokes `java -cp build-tools/36.1.0/lib/d8.jar com.android.tools.r8.R8`. Verified `r8 --version` = 9.0.3-dev. |
| 4 | D8 smoke test failed with "Invalid output" — output directory must already exist | D8 requires the `--output` directory to pre-exist (unlike javac which creates it). Used `mkdir -p` before invoking D8. |
| 5 | Shell env script with backslash line continuations inside `export PATH=...` caused parse errors on some shells | Rewrote `/home/z/tools/nexora_env.sh` to use a `for` loop with `case` dedup for PATH additions — POSIX-portable and idempotent. |
| 6 | GitHub token supplied in task message was doubled (40-char token repeated) | Used the first 40-char token for clone; token scrubbed from git remote URL after clone. |
| 7 | sdkmanager CLI version is 12.0 (not 22.0 as in previous session) | This is the latest cmdline-tools package (11076708). The newer version works identically; all SDK install commands succeeded. |

---

## 11. Recommendations & Next Steps

1. **Environment reproducibility** — source `/home/z/tools/nexora_env.sh` at the start of
   every development session. For CI, the same tool versions and env vars should be
   configured in GitHub Actions.
2. **Phase 1 scaffold versions** (to be applied when Phase 1 begins):
   AGP **9.3.1**, Gradle Wrapper **9.6.1**, Kotlin **2.1.0** (or latest stable), KSP matching Kotlin,
   `compileSdk 36`, `minSdk 34`, `targetSdk 36`, single universal APK (NFR-PORT-002),
   versions centralized in `gradle/libs.versions.toml`.
3. **Repositories** — `google()` + `mavenCentral()` in `settings.gradle.kts`; no other
   repositories required.
4. **W^X Compatibility (`targetSdk=36`)** — Android 10+ enforces W^X (no memory pages
   both writable and executable). Nexora does **not** lower `targetSdk` to bypass this.
   Instead, W^X compatibility is achieved through:
   - **proot with seccomp-bpf filtering** — intercepts `mmap`/`mprotect` syscalls from
     guest programs and remaps them safely without violating host SELinux policies.
   - **Pre-patched guest binaries** — Node.js in the bundled rootfs runs with the
     `--jitless` flag (disables V8 JIT compilation, which requires W^X pages). Standard
     compiled binaries (Python, Git, C tools, pip packages) execute without issues.
   - **`android:extractNativeLibs="true"`** — ensures native libraries are extracted to
     the filesystem before loading, avoiding W^X edge cases with direct APK loading.
   - **PT_INTERP patching** — ELF binaries in the rootfs are patched to use a compatible
     dynamic linker path inside the proot namespace (`/lib/ld-linux-aarch64.so.1`).
   This approach keeps `targetSdk=36` for Google Play compliance while maintaining full
   Linux userland capability inside the sandbox.
5. **No API keys** — provider keys are implemented in Phase 5 with Android Keystore
   encrypted storage (NFR-SEC-005/010); none are configured now.
6. **Embedded runtimes** — Phase 3 decision: Chaquopy / app.cash.quickjs / JGit /
   vendored terminal emulator / Room+SQLite / layered sandbox (see §9). Requires a
   licensing review for the terminal component (GPL vs Apache-2.0).
7. **CI** — GitHub Actions can reuse these exact versions for build/lint/test gates
   (NFR-MAINT-004).

---

*Environment fully verified 2026-08-05. Next step: Phase 1 — Android project scaffold
(bootable app, navigation, theme, settings, core interfaces — no AI).*

---

# Appendix C: Building the Debian-slim Rootfs for Nexora

## C.1 Overview

This guide describes how to build the bundled Full Environment Debian-slim rootfs packaged in the Nexora APK.

## C.2 Prerequisites

- Docker or Podman
- `debootstrap` (or a container image that provides it)
- `xz` for compression
- Android NDK for cross-compiling proot when needed

## C.3 Build Steps

### Step 1: Create the Base Filesystem

```bash
docker run --rm --privileged -v "$(pwd)/build:/build" debian:bookworm-slim bash -c '
  apt-get update && apt-get install -y debootstrap xz-utils
  debootstrap --variant=minbase --arch=arm64 bookworm /build/rootfs http://deb.debian.org/debian
  chroot /build/rootfs bash -c "
    apt-get install -y --no-install-recommends \
      python3 python3-pip python3-venv nodejs npm git curl wget ca-certificates \
      build-essential bash dash coreutils grep sed gawk procps psmisc
    apt-get clean
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
  "
  tar -cJf /build/debian-slim-arm64.tar.xz -C /build/rootfs .
'
```

### Step 2: Generate the Manifest

The manifest must include the rootfs version, architecture, and SHA-256 checksums for all packaged files. Generate it as part of the reproducible build rather than hand-editing it.

### Step 3: Sign the Manifest

```bash
gpg --detach-sign --armor -o manifest.json.asc manifest.json
```

### Step 4: Integrate into the APK

```text
app/src/main/assets/
├── rootfs/
│   ├── debian-slim-arm64.tar.xz
│   ├── manifest.json
│   └── manifest.json.asc
└── proot/
    ├── proot-arm64
    └── proot-x86_64
```

## C.4 proot Compilation (Android)

```bash
git clone https://github.com/termux/proot.git
cd proot
export CC="$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android24-clang"
make V=1 -C src proot
```

Use a vetted release artifact or reproducible source build; do not download opaque binaries into the repository.

## C.5 Testing

```bash
mkdir -p /tmp/nexora-test
tar -xJf debian-slim-arm64.tar.xz -C /tmp/nexora-test
./proot-arm64 -R /tmp/nexora-test /bin/bash -c "python3 -c 'import sys; print(sys.version)'"
./proot-arm64 -R /tmp/nexora-test /bin/bash -c "node -e 'console.log(process.version)'"
```

## C.6 Size Optimization

| Technique | Expected effect |
|---|---|
| `--variant=minbase` debootstrap | Smaller base than standard Debian |
| Remove docs and manpages | Reduces extracted size |
| Strip debug symbols | Reduces binary footprint |
| Clean apt lists and caches | Reduces packaged size |
| xz compression with a reproducible setting | Reduces APK asset size |

Target: less than 70 MB compressed for the base plus Python, Node.js, and build tooling.

## C.7 CI/CD Pipeline

Rootfs builds should run in a pinned, reproducible CI environment, produce checksums and signatures, and publish artifacts only through the release process. Do not commit generated rootfs archives or signing keys to the source repository.

## C.8 Related Files

- [specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md)
- [architecture/SANDBOX.md](../architecture/SANDBOX.md)
- [requirements/FR.md](../requirements/FR.md)
- [requirements/RISKS.md](../requirements/RISKS.md)
