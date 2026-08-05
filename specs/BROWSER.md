> **Status: CANONICAL** for browser automation and extraction behavior.
> This document owns the headless WebView bridge architecture, command protocol, and scraping policies.
> It does NOT own core sandbox containment (see [../security/SandboxPolicy.md](../security/SandboxPolicy.md))
> or network egress proxies (see [../specs/BACKGROUND_EXECUTION.md](BACKGROUND_EXECUTION.md)).
>
> Depends on: [../security/SandboxPolicy.md](../security/SandboxPolicy.md), [../architecture/SANDBOX.md](../architecture/SANDBOX.md).
> Referenced by: [../registry/TOOLS.md](../registry/TOOLS.md), [../docs/SANDBOX_DEPTH.md](../docs/SANDBOX_DEPTH.md).

# Browser Automation Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md) · [../security/SandboxPolicy.md](../security/SandboxPolicy.md)

---

## 1. Overview

Nexora provides standard headless web browsing and extraction capabilities for autonomous agents. Because the sandboxed guest environment (proot Debian-slim) operates under strict Android seccomp constraints (W^X / JITless) and storage limits, **running a local headless Chromium or Puppeteer binary inside the guest is completely unsupported**. Such binaries fail to JIT, consume excessive space, and violate platform security boundaries.

Instead, Nexora implements the **Headless WebView Bridge Protocol**. This protocol redirects browser automation commands from the sandboxed guest to a native Android `WebView` instance hosted securely within the JVM main application process.

---

## 2. Headless WebView Bridge Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   Nexora Android App (JVM)             │
│                                                        │
│  Headless WebView (Host) <─── ToolManager (Intercept)  │
│          │                           ▲                 │
│     (Loads URL)                      │                 │
│          │                     executeTool()           │
│          ▼                           │                 │
│   [Secure Network]                   │                 │
│          │                           │                 │
│  ┌───────┼───────────────────────────┼──────────────┐  │
│  │       ▼                           │              │  │
│  │  proot Linux Guest (Debian)       │              │  │
│  │                                   │              │  │
│  │   Agent Loop ───────── [Tool] ────┘              │  │
│  │   (Python/Node)       (browser_navigate)         │  │
│  │                                                  │  │
│  │   /workspace/downloads/ ◄────────────────────────│  │
│  │   (Shared storage path for downloads/scrapes)    │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Protocol Operations

Browser automation is exposed to the agent loop via specialized tools (`TOOL-2xx` series). These tools bypass proot subprocess spawns and run directly on the host JVM WebView:

| Operation | Tool ID | Description | Parameters | Host JVM Action |
|---|---|---|---|---|
| `browser_navigate` | `TOOL-201` | Loads a URL in the headless WebView and waits for `DOM_CONTENT_LOADED` | `url`, `timeoutMs` | Invokes `WebView.loadUrl()`; injects standard User-Agent |
| `browser_screenshot`| `TOOL-202` | Captures a high-resolution PNG of the active page | `outputFilename` | Draws the WebView canvas onto an Android Bitmap; saves to workspace `/files/` |
| `browser_extract` | `TOOL-203` | Extracts text, links, headings, or metadata | `selector`, `mode` | Executes host-side JavaScript to parse DOM; returns JSON structure |
| `browser_click` | `TOOL-204` | Performs a click event on an element matching a CSS selector | `selector` | Dispatches simulated touch events to WebView coordinates |
| `browser_fill` | `TOOL-205` | Injects text into an input field or form element | `selector`, `value`| Focuses element and programmatically changes the value attribute |
| `browser_execute` | `TOOL-206` | Runs raw JavaScript inside the page context and returns serializable output | `script` | Invokes `WebView.evaluateJavascript()` with callback |

---

## 4. Bridge Data Contracts (Kotlin)

### Browser Navigation Request

```kotlin
data class BrowserNavigationRequest(
    val url: String,
    val timeoutMs: Long = 30_000,
    val blockImages: Boolean = true,
    val blockThirdPartyCookies: Boolean = true
)
```

### Browser Extraction Response

```kotlin
data class BrowserExtractionResponse(
    val title: String,
    val currentUrl: String,
    val htmlContent: String?,
    val textContent: String?,
    val links: List<WebLink>,
    val metadata: Map<String, String>
)

data class WebLink(val text: String, val url: String)
```

---

## 5. Security & Confinement Rules

To prevent prompt-injection attacks, data exfiltration, or sandbox escapes through web content, the bridge enforces the following security boundaries:

- **Isolated Network Egress**: All network traffic generated by the headless `WebView` flows through the same OkHttp egress proxy as the sandbox. This enforces per-workspace Allowed Domains and logs every request (`FR-S014`).
- **Data vs. Instruction Wrapping**: Text extracted from pages is tagged as untrusted, labeled with source context, and treated strictly as passive data inside the Context Builder (`FR-S015` / `FR-WS-005`), preventing malicious pages from hijacking the agent loop.
- **No Java-Interface Injections**: The WebView instance MUST NOT expose any Java interfaces (`addJavascriptInterface`) to the web page. All data extraction is unidirectional via `evaluateJavascript` string evaluation.
- **No Localhost Access**: Headless WebView requests attempting to connect to localhost, loopback addresses (`127.0.0.1`), or app-private database endpoints are immediately blocked.
- **Image/Resource Blocking**: To minimize token costs, bandwidth, and battery drain, WebView settings default to blocking image loading, custom fonts, and third-party tracking scripts.

---

## 6. Phase Mapping

- **Phase 3 (Core Telemetry)**: Headless WebView class integration; core navigation and text extraction tools (`browser_navigate`, `browser_extract`).
- **Phase 4 (Autonomy)**: Screenshot capture (`browser_screenshot`) writing to VFS; form-fill and click simulation; content quarantine wrapping.
- **Phase 5 (Advanced Templates)**: Playwright-compatible Python/Node wrapper scripts inside the guest that proxy commands to the host JVM port dynamically.
