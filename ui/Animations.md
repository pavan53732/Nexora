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
AI responses stream through provisional and committed states. The text view may append/coalesce
visible deltas, but durable event order and terminal state are controlled by the Provider
Protocol. Animation MUST NOT imply that provisional text is verified or committed.

## Activity, Approval, Error, and Recovery States

Progress, connecting, reconnecting, backpressure, permission approval, classifier denial,
partial failure, unknown completion, reconciliation, cancellation, checkpoint recovery, and
terminal states MUST remain understandable without motion. Use explicit text/icon/state
semantics from `ui/Components.md`; animation is only a supplementary presentation cue.

When `reduceMotion` is enabled, suppress blinking cursors, scale/slide transitions, and
nonessential progress motion. Preserve status text, focus order, citations, approval actions,
error details, recovery actions, and terminal outcome information. Never use animation as the
only indication that an agent acted, a Tool ran, a permission changed, or a stream completed.

## Terminal
Terminal output appears instantly (no animation). The terminal should feel responsive and immediate.
