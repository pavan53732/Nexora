> **Status: SUPPORTING** for Animations focused behavior.
> This document explains focused behavior for Animations. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# UI: Animations — Nexora

## Principles
- Functional, not decorative. Every animation serves a purpose.
- Fast. Most animations should be 150-300ms.
- Respect `reduceMotion` accessibility setting.

## Standard Animations

| Animation | Duration | Easing | Usage |
|-----------|----------|--------|-------|
| Fade in | 150ms | EaseIn | Screen transitions, list items |
| Fade out | 150ms | EaseOut | Screen transitions |
| Slide up | 250ms | EaseInOut | Bottom sheets, dialogs |
| Slide right | 200ms | EaseOut | New list items |
| Scale in | 150ms | EaseOut | Tool call cards appearing |
| Typing cursor | 500ms blink | Linear | Streaming text indicator |
| Progress bar | Indeterminate | Linear | Task execution |

## Streaming Text
AI responses stream token-by-token. The text view appends characters as they arrive. No animation needed — the natural token flow IS the animation.

## Terminal
Terminal output appears instantly (no animation). The terminal should feel responsive and immediate.
