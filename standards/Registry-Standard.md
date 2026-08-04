# Registry Standard — Nexora

## Rule

All registries SHOULD expose a consistent compatibility metadata shape wherever applicable, even when the registry is primarily descriptive.

## Required Compatibility Fields

Where a registry entry represents an executable or compatibility-sensitive capability, it SHOULD include or derive:

- stable identifier
- version or revision marker
- origin (`built-in` or plugin/provider source)
- compatibility range or minimum compatible contract version
- dependent capability references where applicable
- declared execution-relevant flags, such as streaming, cancellation, sandbox, delegation, or resume support when relevant

## Notes

Registries remain inventory documents, but they SHOULD not drift from the API/SDK compatibility model. Shared compatibility semantics help traceability, regression review, and plugin/provider/tool onboarding.
