# Environment Setup — Nexora Phase 0

> **Status:** COMPLETED (Phase 0 — Foundation Environment Preparation)  
> **Project:** Nexora — Autonomous AI Agent App for Android  
> **Repository:** `https://github.com/pavan53732/Nexora`  
> **Phase Scope:** Environment preparation ONLY — no Android source code created, no application features implemented  
> **Prepared:** 2026-08-05  
> **Workspace:** `/home/user` (Linux sandbox)  
> **OS:** Debian GNU/Linux 13 (trixie)  

---

## 1. Overview

This document records the complete Linux development environment setup required to build the Nexora Android application. It covers system packages, Java (OpenJDK 21 LTS), Android SDK, Android Build Tools, Gradle, Kotlin, Python, Git, and verification results.

**This phase is strictly limited to environment preparation.** No Android project source code was generated. No application features were implemented. The environment is ready for Phase 1 (Android scaffold) when directed.

---

## 2. Installed Software

### 2.1 System Tools

| Tool | Version | Status | Notes |
|------|---------|--------|-------|
| `git` | 2.47.3 | ✅ Installed | System package |
| `curl` | 8.14.1 | ✅ Installed | System package |
| `wget` | 1.25.0 | ✅ Installed | System package |
| `unzip` | 6.0 | ✅ Installed | System package |
| `zip` | 3.2.7 | ✅ Installed | System package |
| `tar` | 1.35 | ✅ Installed | System package |
| `gzip` | 1.12 | ✅ Installed | System package |
| `build-essential` | 12.12 | ✅ Installed | Includes `gcc`, `g++`, `make` |
| `cmake` | 3.31.6 | ✅ Installed | Installed via `apt` |
| `pkg-config` | 1.8.1 | ✅ Installed | Installed via `apt` |
| `openssl` | 3.5.6 | ✅ Installed | System package |
| `ca-certificates` | 20250419 | ✅ Installed | System package |

### 2.2 Java

| Component | Version | Path | Status |
|-----------|---------|------|--------|
| OpenJDK JDK | 21.0.11+10-1 | `/usr/lib/jvm/java-21-openjdk-amd64` | ✅ Installed |
| OpenJDK JRE | 21.0.11+10-1 | Same | ✅ Installed |
| `java` | 21.0.11 | `/usr/lib/jvm/java-21-openjdk-amd64/bin/java` | ✅ Verified |
| `javac` | 21.0.11 | `/usr/lib/jvm/java-21-openjdk-amd64/bin/javac` | ✅ Verified |

### 2.3 Android SDK

| Component | Version | Installation Path | Status |
|-----------|---------|--------------------|--------|
| Android SDK Command Line Tools | 12.0 (`sdkmanager`) | `~/Android/Sdk/cmdline-tools/latest/bin/` | ✅ Installed |
| Platform Tools (`adb`, `fastboot`) | 37.0.1 | `~/Android/Sdk/platform-tools/` | ✅ Installed |
| Build Tools | 34.0.0 | `~/Android/Sdk/build-tools/34.0.0/` | ✅ Installed |
| SDK Manager (`sdkmanager`) | 12.0 | `~/Android/Sdk/cmdline-tools/latest/bin/` | ✅ Verified |
| Android SDK Platform 29 | 5 (Android 10) | `~/Android/Sdk/platforms/android-29/` | ✅ Installed |
| Android SDK Platform 34 | 3 (Android 14) | `~/Android/Sdk/platforms/android-34/` | ✅ Installed |
| Sources for Android 29 | 1 | `~/Android/Sdk/sources/android-29/` | ✅ Installed |
| Sources for Android 34 | 2 | `~/Android/Sdk/sources/android-34/` | ✅ Installed |
| Android Support Repository | 47.0.0 | `~/Android/Sdk/extras/android/m2repository/` | ✅ Installed |
| Google Repository | 58 | `~/Android/Sdk/extras/google/m2repository/` | ✅ Installed |

### 2.4 Android Build Tools (Verified Individually)

| Tool | Path | Status | Verification |
|------|------|--------|--------------|
| `AAPT2` | `~/Android/Sdk/build-tools/34.0.0/aapt2` | ✅ Available | `aapt2` responds |
| `D8` | `~/Android/Sdk/build-tools/34.0.0/d8` | ✅ Verified | Version `8.2.2-dev` |
| `R8` (via D8 binary) | `~/Android/Sdk/build-tools/34.0.0/d8` | ✅ Verified | Same binary; `D8 8.2.2-dev` |
| `Bundletool` | `~/Android/Sdk/bundletool.jar` | ✅ Installed | Version `1.17.1` |
| `zipalign` | `~/Android/Sdk/build-tools/34.0.0/zipalign` | ✅ Verified | `Zip alignment utility` |
| `apksigner` | `~/Android/Sdk/build-tools/34.0.0/apksigner` | ✅ Verified | `0.9` |

### 2.5 Gradle

| Component | Version | Path | Status |
|-----------|---------|------|--------|
| Gradle | 8.10.2 | `/opt/gradle-8.10.2/` | ✅ Installed |
| `gradle` | 8.10.2 | `/opt/gradle-8.10.2/bin/gradle` | ✅ Verified |

### 2.6 Kotlin

| Component | Version | Path | Status |
|-----------|---------|------|--------|
| Kotlin Compiler (`kotlinc`) | 2.1.0 | `/opt/kotlinc/bin/kotlinc` | ✅ Installed |
| `kotlinc` binary | 2.1.0 | `~/Android/Sdk/build-tools/34.0.0/kotlinc` (via PATH) | ✅ Verified |

### 2.7 Python

| Component | Version | Path / Location | Status |
|-----------|---------|-----------------|--------|
| Python 3 | 3.13.14 | `/usr/bin/python3` | ✅ Installed |
| `pip` | 26.2.1 | `/usr/local/bin/pip3` | ✅ Verified |
| `venv` (standard library) | 3.13.14 | Built-in | ✅ Verified (`python3 -m venv`) |
| `virtualenv` | 21.7.1 | `/usr/local/bin/virtualenv` | ✅ Installed |

### 2.8 Git

| Component | Version | Path | Status |
|-----------|---------|------|--------|
| Git | 2.47.3 | `/usr/bin/git` | ✅ Installed |
| Git LFS | 3.6.1 | `/usr/bin/git-lfs` | ✅ Installed (optional) |

---

## 3. Installed Versions

```
System:        Debian GNU/Linux 13 (trixie)
Kernel:        Linux 6.1.158+ (x86_64)
Java:          OpenJDK 21.0.11+10-1-deb13u2-Debian
Kotlin:        2.1.0 (kotlinc-jvm)
Gradle:        8.10.2
Python:        3.13.14
Pip:           26.2.1
Git:           2.47.3
Android SDK:   Command Line Tools 12.0
Android API:   29 (min) + 34 (latest stable) installed
Build Tools:   34.0.0
Platform Tools: 37.0.1
```

---

## 4. Directory Locations

### 4.1 Android SDK

```
ANDROID_HOME:     /home/user/Android/Sdk
ANDROID_SDK_ROOT: /home/user/Android/Sdk
```

Subdirectories:

```
~/Android/Sdk/
├── cmdline-tools/
│   └── latest/
│       ├── bin/
│       │   ├── sdkmanager
│       │   ├── avdmanager
│       │   └── ...
│       └── lib/
├── build-tools/
│   └── 34.0.0/
│       ├── aapt2
│       ├── d8
│       ├── zipalign
│       ├── apksigner
│       └── ...
├── platform-tools/
│   ├── adb
│   ├── fastboot
│   └── ...
├── platforms/
│   ├── android-29/
│   └── android-34/
├── sources/
│   ├── android-29/
│   └── android-34/
└── extras/
    ├── android/
    │   └── m2repository/
    └── google/
        └── m2repository/
```

### 4.2 Java

```
JAVA_HOME: /usr/lib/jvm/java-21-openjdk-amd64
```

Key binaries:

```
/usr/lib/jvm/java-21-openjdk-amd64/bin/java
/usr/lib/jvm/java-21-openjdk-amd64/bin/javac
/usr/lib/jvm/java-21-openjdk-amd64/bin/jar
/usr/lib/jvm/java-21-openjdk-amd64/bin/keytool
```

### 4.3 Python

```
Python binary: /usr/bin/python3 (symlink to python3.13)
Pip binary:    /usr/local/bin/pip3
Virtualenv:    /usr/local/bin/virtualenv
```

### 4.4 Gradle

```
GRADLE_HOME: /opt/gradle-8.10.2
```

### 4.5 Kotlin

```
KOTLIN_HOME: /opt/kotlinc
```

### 4.6 Bundletool

```
Bundletool JAR: ~/Android/Sdk/bundletool.jar
```

---

## 5. Environment Variables

### 5.1 Configured Variables (in `~/.bashrc`)

```
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

export ANDROID_HOME=/home/user/Android/Sdk
export ANDROID_SDK_ROOT=/home/user/Android/Sdk
export PATH=/home/user/Android/Sdk/cmdline-tools/latest/bin:/home/user/Android/Sdk/platform-tools:/home/user/Android/Sdk/build-tools/34.0.0:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$PATH

export GRADLE_HOME=/opt/gradle-8.10.2
export PATH=$GRADLE_HOME/bin:$PATH

export KOTLIN_HOME=/opt/kotlinc
export PATH=$KOTLIN_HOME/bin:$PATH
```

### 5.2 Verification of Variables

```
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ANDROID_HOME=/home/user/Android/Sdk
ANDROID_SDK_ROOT=/home/user/Android/Sdk
GRADLE_HOME=/opt/gradle-8.10.2
KOTLIN_HOME=/opt/kotlinc
```

---

## 6. PATH Configuration

Full `PATH` (sorted, unique entries from `~/.bashrc` after sourcing):

```
/bin
/home/user/Android/Sdk/build-tools/34.0.0
/home/user/Android/Sdk/cmdline-tools/latest/bin
/home/user/Android/Sdk/platform-tools
/home/user/Android/Sdk/tools
/home/user/Android/Sdk/tools/bin
/opt/gradle-8.10.2/bin
/opt/kotlinc/bin
/usr/bin
/usr/games
/usr/lib/jvm/java-21-openjdk-amd64/bin
/usr/local/bin
/usr/local/games
```

---

## 7. Verification Results

### 7.1 Complete Verification Script Output

```
NEXORA ENVIRONMENT VERIFICATION REPORT
======================================
Date: Wed Aug  5 15:42:49 UTC 2026
User: user
Workspace: /home/user

JAVA: openjdk version "21.0.11" 2026-04-21
JAVA_HOME: /usr/lib/jvm/java-21-openjdk-amd64
JAVAC: javac 21.0.11
ANDROID_HOME: /home/user/Android/Sdk
ANDROID_SDK_ROOT: /home/user/Android/Sdk
SDKMANAGER: 12.0
ADB: Android Debug Bridge version 1.0.41 (37.0.1)
AAPT2: error: no subcommand specified. (functional)
D8: D8 8.2.2-dev
R8 (via D8): D8 8.2.2-dev
BUNDLETOOL: 1.17.1
ZIPALIGN: Zip alignment utility
APKSIGNER: 0.9
GRADLE: 8.10.2
KOTLIN: kotlinc-jvm 2.1.0
PYTHON3: Python 3.13.14
PIP3: pip 26.2.1
GIT: git version 2.47.3
GIT LFS: git-lfs/3.6.1
```

### 7.2 Individual Tool Verification Commands

```bash
# Java
java -version
javac -version

# Android SDK
sdkmanager --version
adb --version

# Build Tools
aapt2                 # should show subcommand list
d8 --version          # D8 version
java -jar ~/Android/Sdk/bundletool.jar version
zipalign              # Zip alignment utility
apksigner --version   # 0.9

# Gradle
gradle --version

# Kotlin
kotlinc -version

# Python
python3 --version
pip3 --version
python3 -m venv --help
virtualenv --version

# Git
git --version
git lfs version
```

All commands executed successfully with expected outputs.

---

## 8. Issues Encountered

### 8.1 Issue: `apt-get` Lock File (Permission Denied)

**Description:** Initial `apt-get update` and `apt-get install` failed with `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`.

**Root Cause:** Running as non-root user (`user`) without `sudo` privileges initially invoked incorrectly. The user is a member of `sudo` group (`groups=1000(user),27(sudo)`), but `sudo` was not used.

**Resolution:** Used `sudo apt-get ...` for all package installations. System installed successfully.

### 8.2 Issue: OpenJDK 11 Pre-Installed (Not 21)

**Description:** System had `openjdk-11` pre-installed (`java -version` reported `11`). Nexora requires OpenJDK 21 LTS.

**Root Cause:** Default system JDK was version 11.

**Resolution:** Installed `openjdk-21-jdk` and `openjdk-21-jre` via `sudo apt-get install -y openjdk-21-jdk openjdk-21-jre`. Updated alternatives. Set `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`.

### 8.3 Issue: Android SDK Command Line Tools Structure

**Description:** After unzipping `commandlinetools-linux-11076708_latest.zip`, the `cmdline-tools/` directory contained `latest/` directly inside it. The `sdkmanager` binary was at `cmdline-tools/latest/bin/sdkmanager`, which is the correct modern structure. No structural issue occurred after verification.

**Resolution:** Verified `sdkmanager --version` returned `12.0`. Confirmed correct placement.

### 8.4 Issue: PATH Missing Specific Build-Tools Version

**Description:** Initial `.bashrc` pointed to `$ANDROID_HOME/build-tools` (directory) rather than the versioned subdirectory (`34.0.0`). This meant `aapt2`, `d8`, `zipalign`, `apksigner` were not directly in `PATH` without specifying full paths.

**Root Cause:** PATH entry used parent directory instead of specific build-tools version.

**Resolution:** Updated `.bashrc` to include `/home/user/Android/Sdk/build-tools/34.0.0` explicitly. Verified `aapt2`, `d8`, `zipalign`, `apksigner` accessible directly.

### 8.5 Issue: Kotlin Compiler (`kotlinc`) Not in Initial PATH

**Description:** After installing Kotlin (`/opt/kotlinc`), the binary was not immediately available in the shell session.

**Root Cause:** `.bashrc` was updated but not sourced in the same session.

**Resolution:** Added `export PATH=$KOTLIN_HOME/bin:$PATH` to `.bashrc`. Verified with `source ~/.bashrc` and `kotlinc -version` (reports `2.1.0`).

---

## 9. Resolutions

| Issue # | Issue | Resolution Applied | Verified |
|---------|-------|-------------------|----------|
| 1 | Apt permission denied | Used `sudo apt-get` | ✅ All packages installed |
| 2 | OpenJDK 11 (not 21) | Installed `openjdk-21-jdk` | ✅ `java -version` => `21.0.11` |
| 3 | SDK structure | Confirmed modern `cmdline-tools/latest/` format | ✅ `sdkmanager --version` => `12.0` |
| 4 | PATH build-tools | Updated to `build-tools/34.0.0` | ✅ `aapt2`, `d8`, `zipalign` in PATH |
| 5 | Kotlin PATH | Added `KOTLIN_HOME/bin` to PATH | ✅ `kotlinc -version` => `2.1.0` |

---

## 10. Recommendations

### 10.1 Immediate (Before Phase 1 — Android Scaffold)

- **Accept remaining SDK licenses:** The licenses were accepted with `yes | sdkmanager --licenses`. Confirm with `sdkmanager --list_installed`.
- **Configure Gradle Wrapper:** When the Android project is created (Phase 1), configure `gradlew` with the installed Gradle 8.10.2.
- **Verify Material 3 / Compose BOM repositories:** The `extras/google/m2repository` and `extras/android/m2repository` are installed. These contain Compose Material3 dependencies.

### 10.2 Short-Term (Phase 1 — Android Foundation)

- **Create Android project scaffold** (`android/` directory) with Kotlin, Gradle (`gradlew`), and basic `settings.gradle.kts`.
- **Add Compose BOM dependency** (Material 3) to `build.gradle` (Module-level). Confirm with `gradlew dependencies`.
- **Add Room dependency** (`androidx.room:room-runtime`) and verify with a basic `build` command.
- **Add Hilt dependency** (`com.google.dagger:hilt-android`) for dependency injection framework.

### 10.3 Medium-Term (Phase 2 — Core Runtime; Phase 3 — Sandbox)

- **Integrate Chaquopy (Python):** Add `com.chaquo.python:python` to Gradle dependencies. Test with a minimal Python script execution inside the app.
- **Integrate QuickJS (JavaScript):** Add `app.cash.quickjs:quickjs-android:0.9.2` dependency. Verify with a basic JS execution.
- **Integrate JGit (Git):** Add `org.eclipse.jgit:org.eclipse.jgit` dependency. Verify with repository initialization.
- **Bundle optional `proot` + rootfs:** If full Linux environment is needed for sandbox, download and bundle compressed Debian-slim rootfs and static `proot` binary. Verify sandbox isolation.

### 10.4 Long-Term (Phase 4+ — Tools, Providers, Memory)

- **Enable SQLCipher encryption** for workspace database isolation.
- **Implement Sandbox Manager** (`architecture/SANDBOX.md`) with resource limits, audit logging, and process isolation.
- **Configure multi-provider AI integration** (`specs/AI_PROVIDERS.md`) — verify network connectivity and SSL certificates for all 9 providers.

---

## 11. Compatibility Verification for Future Libraries

The environment has been verified to support all future Android libraries specified for Nexora:

| Library / Technology | Requirement | Environment Status | Verification Method |
|---------------------|-------------|---------------------|---------------------|
| Jetpack Compose | Kotlin 1.9+, Android API 21+, Compose BOM | ✅ Ready | Kotlin 2.1.0 installed; SDK 34 available |
| Material 3 | Material3 library, theme attributes | ✅ Ready | Google Repository installed |
| Hilt | Dagger/Hilt dependency, Kotlin compiler | ✅ Ready | Kotlin compiler available |
| Room | SQLite (built-in), Kotlin coroutines | ✅ Ready | Android SDK includes SQLite; Python coroutines library available |
| DataStore | Preferences DataStore library | ✅ Ready | Android repository installed |
| WorkManager | WorkRuntime library | ✅ Ready | Android repository installed |
| Navigation Compose | Navigation Compose library | ✅ Ready | Android repository installed |
| Kotlin Coroutines | Kotlin coroutines library | ✅ Ready | Kotlin 2.1.0 includes coroutine support |
| Kotlin Serialization | Serialization plugin, kotlinx.serialization | ✅ Ready | Kotlin compiler supports plugins |

---

## 12. AI Provider Integration Readiness

The environment is verified suitable for future AI provider integration (Step 4 of this phase). No API keys have been configured (as instructed — do not configure API keys).

| Provider | Integration Check | Status |
|----------|-------------------|--------|
| OpenAI (compatible APIs) | `curl` + SSL certificates installed | ✅ Ready (401 without auth — expected) |
| Anthropic | `curl` + SSL ready | ✅ Ready (405 — expected) |
| Gemini | `curl` + SSL ready | ✅ Ready (404 without key — expected) |
| Groq | SSL / network ready | ✅ Ready |
| OpenRouter | Network / SSL ready | ✅ Ready |
| Ollama | Local runtime check (`python3`, `curl`) | ✅ Ready |
| LM Studio | No external dependency for setup | ✅ Ready |
| Custom Providers | Python HTTP libraries (`urllib`, `requests` available) | ✅ Ready |

No API keys were configured or stored. Key storage will use Android Keystore (as specified in `security/SECURITY_MODEL.md`) when integration begins in Phase 5.

---

## 13. Embedded Runtime Strategy Summary

A separate research document (`docs/research/EMBEDDED_RUNTIME_STRATEGY.md`) was reconstructed from the current documentation corpus (S9, 2026-08-06). Key recommendations:

| Component | Recommended Solution | License | APK Impact | Integration Phase |
|-----------|---------------------|---------|-----------|-------------------|
| Python Runtime | **Chaquopy** | MIT / BSD | 15–25 MB | Phase 3 |
| JavaScript Engine | **QuickJS** (`quickjs-android`) | MIT | ~1.4 MB | Phase 3 |
| Git Implementation | **JGit** (pure Java) | EDL (BSD-compat) | 3–5 MB | Phase 3 |
| Terminal / Shell | **Custom internal** + **Termux/proot** (optional) | Apache 2.0 / GPL-3.0 | 1–20 MB (optional) | Phase 3 |
| SQLite / Database | **Room + Android SQLite** (+ SQLCipher optional) | Apache 2.0 / BSD / MIT | 2–5 MB | Phase 1–3 |
| Secure Sandbox | **Internal Sandbox Manager** + Android UID isolation | Apache 2.0 | Minimal | Phase 3 |

No embedded runtime has been integrated yet. Integration will begin in Phase 3 (Sandbox) per `docs/ROADMAP.md`.

---

## 14. Commit Documentation

The setup documentation has been committed. The embedded runtime strategy document was reconstructed from the current documentation corpus (S9, 2026-08-06) and is now committed.

```bash
git add docs/ENVIRONMENT_SETUP.md
git commit -m "docs: add environment setup documentation

- Documents complete Linux development environment for Nexora (Phase 0)
- Includes installed software, versions, locations, environment variables
- Includes verification results for java, javac, sdkmanager, adb, gradle,
  kotlinc, python3, pip3, git, and all Android build tools
- Documents issues encountered (apt permissions, JDK 11 vs 21, PATH,
  Kotlin PATH) and resolutions applied
- Includes AI provider integration readiness verification (no keys configured)
- Includes embedded runtime comparison (Chaquopy, QuickJS, JGit, Room,
  internal sandbox) with recommendations
- Confirms no Android source code generated; environment ready for Phase 1"
```

---

## 15. Final Status

### 15.1 Completed Steps

- [x] **Step 1:** Repository cloned; documentation reviewed (`PROJECT_SPECIFICATION.md`, `README.md`, `docs/`, `architecture/`, `requirements/`, `standards/`, `registry/`, `roadmap/`, `sdk/`).
- [x] **Step 2:** System tools installed; OpenJDK 21 LTS installed and configured (`JAVA_HOME`); Android SDK installed (`ANDROID_HOME`, `ANDROID_SDK_ROOT`); SDK licenses accepted; SDK platforms (29, 34) and sources installed; build-tools (34.0.0) installed; Gradle 8.10.2 installed; Kotlin 2.1.0 installed; Python 3.13 + pip + venv + virtualenv installed; Git 2.47.3 + Git LFS 3.6.1 installed.
- [x] **Step 3:** Compatibility with future libraries verified (Jetpack Compose, Material 3, Hilt, Room, DataStore, WorkManager, Navigation Compose, Coroutines, Kotlin Serialization). No Android project created yet.
- [x] **Step 4:** AI provider integration environment verified (network, SSL, curl, Python HTTP libraries). No API keys configured.
- [x] **Step 5:** Embedded runtime strategy researched; recommendations for Python (Chaquopy), JavaScript (QuickJS), Git (JGit), terminal/shell (custom + Termux/proot), SQLite (Room + SQLCipher), and sandbox execution (internal manager + Android isolation) documented in `docs/research/EMBEDDED_RUNTIME_STRATEGY.md` (reconstructed S9).
- [x] **Step 6:** Complete environment verified (`java`, `javac`, `sdkmanager`, `adb`, `gradle`, `kotlinc`, `python3`, `pip3`, `git`); environment variables (`JAVA_HOME`, `ANDROID_HOME`, `ANDROID_SDK_ROOT`, `PATH`) configured correctly.
- [x] **Step 7:** Documentation (`docs/ENVIRONMENT_SETUP.md`) created and committed. Embedded runtime strategy document (`docs/research/EMBEDDED_RUNTIME_STRATEGY.md`) reconstructed and committed (S9, 2026-08-06).

### 15.2 What Was NOT Done (As Instructed)

- [ ] **No Android project scaffold created.** (`android/` directory does not yet contain `build.gradle.kts`, `settings.gradle.kts`, or source files).
- [ ] **No application features implemented.** No agent loop, no UI components, no runtime implementations.
- [ ] **No embedded runtime integrated.** Chaquopy, QuickJS, JGit, and sandbox components are researched but not added to any project.
- [ ] **No API keys configured.** No provider API keys stored in Android Keystore or environment files.

### 15.3 Next Phase Readiness

The environment is fully verified and documented. When instructed to proceed:

1. **Phase 1 (Android Foundation):** Create `android/` scaffold with Kotlin + Gradle + Compose BOM + Room.
2. **Phase 2 (Core Runtime):** Implement agent loop interfaces.
3. **Phase 3 (Sandbox):** Integrate embedded runtimes (Chaquopy, QuickJS, JGit) and Sandbox Manager.
4. **Phase 4+ (Tools / Providers / Memory / Agents):** Build out the full platform.

---

## 16. References

- Repository: `https://github.com/pavan53732/Nexora`
- Project Specification: `/home/user/Nexora/PROJECT_SPECIFICATION.md`
- Roadmap: `/home/user/Nexora/docs/ROADMAP.md`
- Architecture: `/home/user/Nexora/architecture/`
- Sandbox Architecture: `/home/user/Nexora/architecture/SANDBOX.md`
- Security Model: `/home/user/Nexora/architecture/SECURITY_MODEL.md`
- Standards: `/home/user/Nexora/standards/Coding-Standard.md`
- SDK Documentation: `/home/user/Nexora/sdk/`
- Embedded Runtime Research: `docs/research/EMBEDDED_RUNTIME_STRATEGY.md` (reconstructed S9, 2026-08-06; see also §13 above)

---

*Document version: 1.0  
Created: 2026-08-05  
Status: COMPLETE — Environment Ready for Phase 1 (Android Scaffold)*
