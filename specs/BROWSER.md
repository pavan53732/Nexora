> **Status: SUPPORTING** for BROWSER focused behavior.
> This document explains focused behavior for BROWSER. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# Browser Automation Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## Overview

Browser automation enables agents to interact with web pages: navigate, extract content, fill forms, click elements, and take screenshots.

## Capabilities

| Operation | Description |
|-----------|-------------|
| **Navigate** | Open a URL and wait for page load. |
| **Screenshot** | Capture a screenshot of the current page. |
| **Extract** | Extract page text, links, images, metadata. |
| **Fill Form** | Fill input fields, select dropdowns, check boxes. |
| **Click** | Click buttons, links, and elements. |
| **Scroll** | Scroll the page up/down. |
| **Wait** | Wait for an element or condition. |
| **Execute JS** | Run JavaScript in the page context. |

## Implementation Approach

Use Android's `WebView` in a headless mode for browser automation. No external browser engine required.

## Phase Mapping

- **Later**: Browser automation as a plugin.
