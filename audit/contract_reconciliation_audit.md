# Contract Reconciliation Audit — Nexora

## Scope

This audit reviews consistency across architecture, models, state machines, protocols, APIs, SDKs, registries, traceability, and testing documents after the API/SDK contract hardening work.

## Confirmed alignments

- API specs now define stronger ownership boundaries between Agent, Tool, Provider, Plugin, and Runtime.
- API and SDK docs consistently reference correlation IDs, idempotency keys, resume tokens, pagination cursors, durable version semantics, cancellation, and canonical error envelopes.
- Protocol docs now mirror explicit lifecycle, deduplication, and terminal-outcome rules for Agent, Tool, Provider, Plugin, and Execution flows.
- Task and Execution models were strengthened to separate durable lifecycle status from transient execution phase.
- Traceability was restored from concern-only coverage to a requirement-level matrix for the core contract path.

## Remaining contradictions or gaps

### 1. Requirement coverage is still incomplete

The repository requirements set is far broader than the restored matrix. Many requirement IDs in `requirements/FR.md` and `requirements/NFR.md` still lack explicit rows, so traceability remains partial.

### 2. State-machine-to-model alignment is not complete across all entities

Task/Execution alignment was improved, but other models such as Workspace, Session, Workflow, Memory, and TerminalSession still need explicit lifecycle alignment checks against their operational documents.

### 3. Testing docs do not uniformly assert envelope semantics

The testing documents mention canonical contract evidence, but most do not yet explicitly enumerate checks for `correlationId`, `idempotencyKey`, `resumeToken`, pagination cursor semantics, or event deduplication behavior.

### 4. Registries remain mostly descriptive

The registries define inventory and capability matrices, but they do not consistently capture contract-version or compatibility metadata implied by the hardened SDK/API documents.

### 5. Memory contract path remains lighter than the other subsystems

Memory protocols and models are comparatively less explicit about the same envelope and lifecycle rigor now applied to Agent/Tool/Provider/Plugin/Runtime paths.

## Recommended follow-up work

1. Extend requirement-level traceability to all requirement IDs in `requirements/FR.md` and key `NFR.md` entries.
2. Audit remaining models against state machines or authoritative lifecycle sources.
3. Add explicit canonical envelope assertions to unit, integration, regression, and E2E testing docs.
4. Add compatibility/version metadata expectations to registries where relevant.
5. Harmonize the memory path with the same cross-layer contract precision used elsewhere.
