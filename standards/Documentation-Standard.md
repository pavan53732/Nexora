> **Status: SUPPORTING** for Documentation Standard coding standard.
> This document defines conventions for Documentation Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Documentation Standard — Nexora

## Rule
> Update the relevant document BEFORE implementing significant changes.

## Document Types

| Type | Location | Updated When |
|------|----------|-------------|
| Spec changes | `docs/`, `architecture/`, `specs/` | Before any code change |
| New model | `models/` | Before implementing the model |
| New protocol | `protocols/` | Before implementing the protocol |
| ADR | `docs/adr/` | When a major decision is made |
| Feature | `registry/` | When a feature is planned |
| API change | `docs/api/`, `sdk/` | Before implementing the change |

## Decision-record decider vocabulary

Decision records MAY identify the accountable decision participants as `Creator`, `Product Owner`, `Architecture Owner`, or another explicitly named project authority. These are provenance labels for who selected or authorized a decision; they do not create a new subsystem authority, lifecycle, permission, implementation, or evidence owner. `Creator` refers to the creator-owned product authority defined in `NEXORA_PRODUCT_DESIGN_BY_CREATER.md`; that document remains protected from AI modification.

## Format
- Markdown for all documentation
- Include a back-link to `PROJECT_SPECIFICATION.md` at the top
- Include code examples in Kotlin
- Include diagrams in ASCII art
- Cross-link related documents

## Implementation-Ready Contract Rule

Documentation is the design boundary for the future Android application. Significant behavior MUST be specified before source implementation begins; implementation MUST NOT infer missing semantics from a convenient component, a related identifier, or the absence of a documented prohibition.

Each normative contract SHOULD make its evidence and boundaries explicit:

- identify the canonical owner and distinguish canonical, supporting, derived, decision, explanatory, proposal, and historical text;
- define the relevant identity, inputs, outputs, preconditions, postconditions, lifecycle/state effects, ownership, authorization, persistence, recovery, cancellation, timeout, retry, concurrency, resource, privacy, audit, and observable-outcome rules;
- preserve distinctions between independent entities, states, identifiers, responsibilities, and lifecycle phases unless a canonical source explicitly relates them;
- project canonical behavior consistently into models, protocols, APIs, SDKs, registries, UI, requirements, and planned validation without creating a second authority;
- classify unsupported or non-derivable behavior as `UNKNOWN`, `OPEN/DEFERRED`, `PROPOSAL`, or `OWNER DECISION REQUIRED` rather than promoting inference into normative behavior; and
- link every requirement to its canonical owner, primary contract, derived implementation surfaces, concrete planned validation case, and evidence path or documented evidence exception under [../docs/TRACEABILITY_RULES.md](../docs/TRACEABILITY_RULES.md).

A documentation change that materially affects a lifecycle, protocol, API, security rule, persistence contract, requirement, registry identity, or recovery behavior MUST update the affected projections and traceability in the same change or record an explicit gap. Planned validation is not executed evidence, and documentation MUST NOT claim implementation, runtime, device, or test completion before the corresponding evidence exists.
