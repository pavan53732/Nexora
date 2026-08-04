> **Status: SUPPORTING** for Spacing focused behavior.
> This document explains focused behavior for Spacing. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# UI: Spacing — Nexora

## Grid
Base unit: 4dp. All spacing is a multiple of 4dp.

| Token | Value | Usage |
|-------|-------|-------|
| `spacing_xxs` | 2dp | Inline icon gaps |
| `spacing_xs` | 4dp | Between related items |
| `spacing_sm` | 8dp | Card padding, list item padding |
| `spacing_md` | 12dp | Section spacing |
| `spacing_lg` | 16dp | Standard margin |
| `spacing_xl` | 24dp | Section dividers |
| `spacing_xxl` | 32dp | Screen section spacing |
| `spacing_xxxl` | 48dp | Major screen divisions |

## Cards
- Card corner radius: 12dp
- Card elevation: 2dp (dark), 1dp (light)
- Card padding: 16dp

## Touch Targets
- Minimum: 48dp x 48dp
- Recommended: 56dp x 48dp for primary actions
