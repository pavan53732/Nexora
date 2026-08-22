# NEXORA Product Design — Creator-Owned Contract

> **Status: CREATOR-OWNED PRODUCT DESIGN AUTHORITY**
> **Authority:** The creator owns this product design and its selected product decisions.
>
> This document defines **what Nexora is** at the product level.
> It is not an AI-owned canonical architecture document, an ADR, a subsystem specification, or an implementation manifest. The canonical architecture and specifications define **how** this product design is realized.
>
> **Back to:** [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md)
>
> **Status rule:** AI agents MUST read this document before proposing or making product or architectural changes. They MUST follow its selected product decisions, MAY validate implementation against it, and MAY report conflicts or propose amendments separately. AI agents MUST NOT modify, rewrite, delete, weaken, reinterpret, or supersede this document. A conflict with this document MUST stop the change and be reported to the creator for decision.

## 1. Nexora Product Identity

Nexora is an **Android-native AI agent application**. It is a pure Android application, not an operating system, ROM, virtual machine, web product, desktop product, or CLI product. Users interact primarily with agents through a workspace-first, agent-first experience: the user supplies goals, the agent plans and executes work, and meaningful results, progress, approvals, failures, logs, and evidence are surfaced through the established user-facing surfaces. The sandbox, internal terminal, runtimes, and execution engine are internal capabilities rather than the primary interaction surface. [PROJECT_SPECIFICATION.md:7-17,33-41,392-405] [docs/PRODUCT_PRINCIPLES.md:17-25,31-35,98-124,208-220]

The product includes the following selected concepts: workspaces; autonomous agents; cloud AI providers; controlled local execution; a local sandbox; skills; plugins; AI provider settings; background execution and terminal capability; security and permissions; evidence and provenance; and persistent project/workspace context and knowledge. These concepts remain subject to the existing subsystem owners and evidence-state discipline. [docs/PRODUCT_PRINCIPLES.md:29-81,83-147] [docs/CANONICAL_SOURCES.md:20-24,41-45,67-83,91-107]

| Product concept | Product decision | Existing owner | Evidence state |
|---|---|---|---|
| Workspace-first, agent-first interaction | Workspace is primary; agents are the primary interaction model; infrastructure is internal | `PROJECT_SPECIFICATION.md`, `docs/PRODUCT_PRINCIPLES.md`, ADR-0001/0006 | CANONICAL REQUIREMENT; implementation and executed evidence remain separate |
| Cloud AI intelligence | Intelligence, inference, planning, embeddings, and provider-backed generation use eligible cloud/external providers only | `architecture/PROVIDER_SYSTEM.md`, `specs/AI_PROVIDERS.md`, DEC-44 | CANONICAL REQUIREMENT; implementation-unverified in the Phase 0 baseline |
| Local controlled execution | Tools and skills invoke execution through Runtime, PermissionModel, Tool, and Sandbox authorities | `architecture/RUNTIME.md`, `architecture/TOOL_SYSTEM.md`, `security/PermissionModel.md`, `architecture/SANDBOX.md` | CANONICAL REQUIREMENT; implementation-unverified in the Phase 0 baseline |
| Skills and plugins | Skills express reusable expertise; plugins extend registered capabilities; neither becomes a second runtime or authorization authority | ADR-0007, `models/Skill.md`, `architecture/PLUGIN_SYSTEM.md` | CANONICAL REQUIREMENT; implementation-unverified in the Phase 0 baseline |
| Evidence and provenance | Significant claims and execution outcomes are evidence-bounded and retain provenance, authority, freshness, trust, and verification state | `specs/CONTEXT_MANAGEMENT.md`, `testing/EVIDENCE_CONVENTIONS.md` | CANONICAL REQUIREMENT; test definitions exist, executed evidence does not |
| Tool-level bypass and self-grant | Authorized tools may declare bypass flags (bypassSafeguards, allowJailbreakPrompts, selfGrantPermissions) that propagate through existing authorization, sandbox, and provider contracts; DEC-50 | `decisions/DEC-50-tool-bypass-and-self-grant-authorization.md` | CANONICAL REQUIREMENT; implementation-unverified in the Phase 0 baseline |

Nexora remains a Phase 0 documentation baseline. Documentation defines requirements and contracts; it does not prove Kotlin/Java/Gradle implementation, test execution, device behavior, or retained executed evidence. [PROJECT_SPECIFICATION.md:9-17,347-357,376-388] [testing/EVIDENCE_CONVENTIONS.md:42-67]

## 2. Cloud AI Model Architecture

AI intelligence is provided through configurable **cloud/external AI providers**. Nexora MUST NOT depend on one hardcoded provider. The runtime depends on the `AIProvider` abstraction, while provider adapters own provider-specific protocols and capability translation. Local AI models and local inference runtimes are out of scope; localhost, loopback, app-private, and on-device model endpoints are not eligible provider endpoints. [architecture/PROVIDER_SYSTEM.md:15-18,21-63,176-205] [specs/AI_PROVIDERS.md:61-70,141-145] [docs/PRODUCT_PRINCIPLES.md:39-43,177-188]

The product distinguishes the following concepts:

| Concept | Product meaning | Existing architectural boundary |
|---|---|---|
| **AI Provider** | An external/cloud service integration identified by provider type and adapter | `AIProvider`, `ProviderType`, and provider adapters own provider protocol behavior [architecture/PROVIDER_SYSTEM.md:19-42] |
| **AI Model** | A provider-catalog model identified by exact model identity/version and capability metadata | Model catalog and `ProviderRoutePlan` preserve exact model and snapshot identity [architecture/PROVIDER_SYSTEM.md:100-130] |
| **AI Request** | A contextual, permissioned, correlated request sent through an eligible provider route | `CompletionRequest` carries request, correlation, workspace, agent, context, model, tools, policy, and idempotency data [architecture/PROVIDER_SYSTEM.md:66-84] |
| **AI Response** | A provider result normalized into canonical response or typed stream events | `CompletionResponse` and `StreamEnvelope` preserve provider/model/stream/correlation identity [architecture/PROVIDER_SYSTEM.md:88-98,144-163] |
| **AI Capability** | A negotiated model/provider capability, not a universal provider property | `ProviderCapability` and model descriptors govern compatibility [architecture/PROVIDER_SYSTEM.md:44-63,114-142] |
| **AI Configuration** | A named, switchable provider profile containing endpoint, secret reference, model, parameters, and negotiated metadata | `ProviderConfig`, named profiles, `SecureKeyStore`, and per-workspace default profile [architecture/PROVIDER_SYSTEM.md:176-198] [specs/AI_PROVIDERS.md:72-99] |

AI Settings MUST support, at minimum, provider selection, base URL, API key, model name, **Test Connection**, capability refresh/detection where the provider supports it, connection status, validation result, and Save. These are product-level settings behaviors; the implementation technology and exact screen composition remain owned by the UI and provider specifications.

**Test Connection** verifies provider/model connectivity and capability compatibility. It does **not** authorize workspace execution, grant a Tool permission, start a Task, or bypass the Runtime, PermissionModel, Tool, Sandbox, or evidence gates. Provider health checks and model listing already exist in the provider abstraction. [architecture/PROVIDER_SYSTEM.md:21-33,100-130] [security/PermissionModel.md:18-75]

Supported capabilities are conditional, not guaranteed merely because they are named. Where supported by the existing contracts, Nexora may negotiate streaming, reasoning, vision, tool/function calling, embeddings, speech/audio/transcription, image generation through the existing AI Tool category, citations, search, code execution, computer use, and multimodal behavior. Capability support, model limits, adapter representation, stream/resume behavior, and evidence requirements must be detected or declared by the existing provider/model contracts; unsupported capabilities must produce an explicit incompatibility or approved fallback rather than silent downgrade. [architecture/PROVIDER_SYSTEM.md:44-63,100-142] [specs/AI_PROVIDERS.md:101-139] [architecture/TOOL_SYSTEM.md:111-146]

API keys are secrets. They MUST be stored through existing secure provider configuration ownership, never placed in prompts, logs, evidence, telemetry, or generated artifacts, and never exposed to the local model context. AI providers cannot directly access the local filesystem or process environment and cannot bypass PermissionModel, Sandbox, Tool, Runtime, audit, or evidence authority. [architecture/PROVIDER_SYSTEM.md:176-198] [requirements/CONSTRAINTS.md:57-74] [security/SandboxPolicy.md:18-20,101-115] [specs/CONTEXT_MANAGEMENT.md:311-317]

## Context Summarization Policy — CREATOR LOCK

Nexora uses a hybrid context-summarization model.

**Cloud/External AI:** AI-based summarization may be performed through an eligible user-configured cloud/external AI provider using the canonical provider architecture.

**Local deterministic processing:** Nexora may perform deterministic, non-AI context transformations locally when model inference is not required, such as deterministic trimming, windowing, compaction mechanics, metadata reduction, or other explicitly defined non-inference transformations.

**Local AI inference is prohibited.** Nexora must not invoke an on-device/local LLM or other local AI inference engine for context summarization.

Any implementation, agent, skill, plugin, sandbox operation, provider integration, or future architectural proposal that conflicts with this rule is non-compliant unless the creator explicitly changes this document.

## 3. Local Execution Sandbox

The product boundary is:

> **CLOUD AI = intelligence, reasoning, planning, and generation**
>
> **LOCAL SANDBOX = controlled execution**

The model does not directly execute commands. Nexora mediates the path through existing identities and authorities:

```text
AI response or plan
    ↓
Agent / Task / Execution
    ↓
Planner / Runtime / Workflow
    ↓
PermissionModel and policy checks
    ↓
Tool or Skill resolution
    ↓
Tool Executor and local Sandbox
    ↓
Process / File / Terminal operation
    ↓
Result / Artifact / Evidence / Audit
    ↓
Agent observes and continues, repairs, replans, or completes
```

This is a product boundary, not a second execution architecture. The canonical Tool flow already requires validation, complete authorization, parameter validation, sandboxed execution where required, result collection, memory/history persistence, event publication, and return to the AI loop. [architecture/TOOL_SYSTEM.md:173-217] Runtime composition and Sandbox ownership remain authoritative. [architecture/RUNTIME.md:19-37,124-167] [architecture/SANDBOX.md:18-20,148-175]

The local execution product contract includes:

| Area | Product requirement | Existing owner |
|---|---|---|
| Workspace isolation | Each workspace has isolated app-private storage and no cross-workspace path access | `security/SandboxPolicy.md`, `architecture/SANDBOX.md` |
| Filesystem | File operations are mediated by the sandbox VFS and workspace boundary; host paths are denied | `security/SandboxPolicy.md:18-60` |
| Process and command execution | Processes run under sandbox limits, with bounded process count, CPU time, memory, disk, working directory, and cleanup | `security/SandboxPolicy.md:74-105`, `architecture/SANDBOX.md:148-169` |
| Network and egress | Network access is authorized by the effective PermissionModel and workspace mode rather than globally denied. In `AUTOPILOT`, public routable `network:http` and `network:websocket` destinations use the DEC-47 default authorization; `ASSISTED` retains opt-in authorization. Guest egress uses the workspace proxy and fails closed on bypass or unsafe TLS. Loopback, localhost, app-private endpoints, inbound listeners, unauthorized secret-material transmission, and sensitive-domain credential entry or transaction execution remain blocked. | `security/SandboxPolicy.md:62-72`, `security/PermissionModel.md:480-507`, `decisions/DEC-47-open-network-free-browser-unrestricted-guest-packages.md:12-18` |
| Permission | Every side-effecting Tool/action passes the existing scope and approval flow | `security/PermissionModel.md:18-75` |
| Timeout and cancellation | Tool and terminal timeouts are bounded; cancellation propagates through existing execution and terminal contracts | `architecture/TOOL_SYSTEM.md:34-76`, `specs/TERMINAL.md:88-115` |
| Output and result | stdout/stderr, exit status, metadata, artifacts, and truncation are captured under existing Tool/Terminal contracts | `specs/TERMINAL.md:79-86,117-126` |
| Unknown completion | An uncertain non-idempotent side effect remains `UNKNOWN_COMPLETION` until the owning reconciliation contract resolves it | `architecture/TOOL_SYSTEM.md:34-76` |
| Recovery and cleanup | Checkpoints, parent binding, cancellation, process termination, and idempotent cleanup use existing lifecycle authorities | `specs/TERMINAL.md:26-45,97-115`, `specs/BACKGROUND_EXECUTION.md:105-134` |
| Evidence | Execution history, audit, trace, artifacts, claims, and verification preserve identity and provenance | `security/PermissionModel.md:376-440`, `specs/CONTEXT_MANAGEMENT.md:332-353`, `testing/EVIDENCE_CONVENTIONS.md:42-76` |

Nexora MUST NOT create a second execution authority, new sandbox lifecycle, or product-level direct model-to-process pathway.

## 4. Skills

A **Skill** is a reusable expertise or workflow abstraction. It may define inputs, prerequisites, expected outputs, verification, and permitted Tool use; it may orchestrate existing Tools within the existing Agent/Task/Execution/Workflow boundaries. Skills are first-class expertise units: **Agent = who performs**, **Skill = what expertise is needed**, and **Tool = how the work is performed**. [docs/PRODUCT_PRINCIPLES.md:71-81] [models/Skill.md:15-30]

A Skill MUST NOT bypass permissions, directly access unauthorized Android APIs, bypass Sandbox or Tool Manager, become a second Agent Runtime, or become an independent authorization authority. Skill selection and validation remain subordinate to existing Planner, Skill Registry, Tool Registry, PermissionModel, Runtime, Sandbox, and evidence owners. [models/Skill.md:51-60] [architecture/TOOL_SYSTEM.md:223-227]

The product deliberately distinguishes:

| Concept | Role |
|---|---|
| **Agent** | The actor/agent type that performs work |
| **Skill** | The reusable expertise or workflow needed |
| **Task** | The durable unit of requested work |
| **Workflow** | The graph and progression of connected steps |
| **Tool** | The permissioned operation interface used to cause effects or retrieve results |
| **Execution** | The runtime attempt and its state/evidence lineage |

These concepts MUST NOT be collapsed into one identity or lifecycle. Their detailed ownership remains in the existing canonical architecture, models, protocols, registries, and state machines. [docs/CANONICAL_SOURCES.md:20-25,87-104]

## 5. Plugins

A **Plugin** is an extensibility and integration mechanism. Existing plugins may register Tools, Agents, AI Providers, Skills, UI screens, and Memory Backends through the transactional Plugin SDK boundary. Registration is all-or-nothing for the exported capabilities, and activation failure rolls back to the prior committed plugin state. [architecture/PLUGIN_SYSTEM.md:15-36]

Plugins are not automatically trusted with unrestricted filesystem, process, network, secrets, Android permissions, or workspace access. Plugin manifests declare required permission scopes, installation requires user review, and plugin execution remains inside the calling workspace sandbox with the same filesystem, network, and process limits as a Tool. [security/PermissionModel.md:445-460] [security/SandboxPolicy.md:107-124]

Plugin is distinct from Skill. A Plugin is the installable integration/extensibility boundary and may export capabilities; a Skill is an expertise unit that an Agent may acquire or use. A plugin-exported Skill still remains subject to Skill, Tool, Runtime, PermissionModel, Sandbox, lifecycle, and evidence ownership. [architecture/PLUGIN_SYSTEM.md:21-36] [models/Skill.md:15-30] [models/Plugin.md:10-24,60-69]

## 6. AI Settings Page

The intended product behavior is a provider configuration surface reachable from the existing Settings/AI Providers area. The product-level fields are:

| Field or action | Required behavior |
|---|---|
| Provider | Select or identify the configured cloud/external provider profile |
| Base URL | Configure the external provider endpoint, subject to provider/cloud-only validation |
| API Key | Enter or update a secret stored through `SecureKeyStore`; never display or persist it in plaintext |
| Model Name | Select or enter the model identity supported by the provider catalog |
| Test Connection | Verify provider/model connectivity and capability compatibility; no workspace execution authorization |
| Refresh/Detect Capabilities | Refresh the model catalog or capability metadata where supported; do not silently claim unsupported capabilities |
| Connection status | Show the latest connection/validation result with its evidence state and timestamp |
| Save | Persist the profile through existing provider configuration ownership |

This page is a product behavior contract, not a UI implementation decision. It does not select Compose, XML, navigation structure, or package placement. Existing navigation exposes Settings and an AI Providers configuration destination, while terminal and sandbox remain internal with no navigation entry. [ui/Navigation.md:7-18,20-44]

Provider connection status is not execution completion, provider capability metadata is not proof that the capability has been implemented, and a successful Test Connection is not permission to execute a workspace Tool. The UI remains projection-only and cannot grant permissions, transition lifecycle state, claim verification, or create a new authority. [ui/Components.md:9-66] [security/PermissionModel.md:46-75]

## 7. Background Terminal

Nexora includes a background terminal/process capability as an internal agent capability. It is not a user-facing terminal product surface. The conceptual product flow is:

```text
Start process
    ↓
Background execution
    ↓
Process / TerminalSession identity
    ↓
stdout/stderr streaming
    ↓
Status and lifecycle observation
    ↓
Cancel / terminate / timeout / resource enforcement
    ↓
Exit status
    ↓
Artifact / result
    ↓
Audit / trace / evidence / recovery classification
```

The background terminal MUST use the existing `TerminalSession` identity and lifecycle, bind autonomous background work to its parent `Task`, `Execution`, `Workspace`, `Correlation`, and effective deadline, and preserve existing cancellation, timeout, output cap, process termination, checkpoint, cleanup, and unknown-completion rules. It MUST NOT create a competing execution lifecycle. [specs/TERMINAL.md:17-68,79-105,109-126] [specs/BACKGROUND_EXECUTION.md:16-29,105-134,263-285]

The product controls include start, observe, stream, cancel, terminate, timeout, resource limits, process status, exit status, correlation, evidence, recovery, and unknown completion. Android foreground service and WorkManager behavior, notifications, process death, Doze/OEM degradation, checkpointing, and restart remain owned by the canonical background-execution specification. [specs/BACKGROUND_EXECUTION.md:23-37,136-205,206-259]

## 8. Project Knowledge and Context

Nexora maintains persistent workspace/project knowledge that can be selectively supplied to AI. Context MUST be relevant, scoped, provenance-aware, permission-aware, freshness-aware, and trust-aware. Trusted creator/project instructions, canonical requirements and decisions, derived memory, tool results, introspection summaries, and untrusted workspace/external content MUST remain distinguishable. Nexora MUST NOT blindly inject the entire workspace into model context. [specs/CONTEXT_MANAGEMENT.md:22-89,141-202,452-460]

Existing Context Management owns read-time assembly, token budgeting, progressive summarization, trust isolation, freshness, evidence classification, and ClaimRecord binding. Persistent project knowledge is a read-time projection over existing workspace Memory, canonical requirements, locked decisions, constraints, prior verified artifacts, and relevant project configuration; it is not a new Knowledge authority or lifecycle. [docs/CANONICAL_SOURCES.md:22-24,43,69-72] [specs/CONTEXT_MANAGEMENT.md:22-89,319-353,452-460]

Context objects entering a model request retain source identifier, source version or checkpoint, retrieval reason, freshness, authority level, trust classification, evidence class, and conflict status. Significant claims use existing ClaimRecord and claim-to-evidence binding. Stale, contradictory, untrusted, missing-provenance, or insufficiently evidenced content is advisory, blocked, or qualified under the existing Evidence & Validation Engine and cannot authorize Tools or redefine canonical behavior. [specs/CONTEXT_MANAGEMENT.md:78-89,159-202,332-353,452-460]

## 9. Agent Execution Loop

The product-level agent loop is:

```text
Goal
  ↓
Understand
  ↓
Plan
  ↓
Decompose
  ↓
Select Skills and Tools
  ↓
Execute locally through existing authorities
  ↓
Observe
  ↓
Verify
  ↓
Collect evidence
  ↓
Measure progress
  ↓
Continue / Repair / Replan / Complete
```

Completion is evidence-bounded. An agent MUST NOT declare success merely because it generated text, selected a Tool, issued a command, received a provider response, or observed a non-authoritative summary. Existing Agent Runtime, Task, Execution, Workflow, Tool, Permission, Context, ClaimRecord, Reviewer, and Evidence/Validation owners determine whether work is complete and what is shown to the user. [architecture/AGENT_RUNTIME.md:27-35,58-66,140-188,263-280] [architecture/TOOL_SYSTEM.md:173-217] [specs/CONTEXT_MANAGEMENT.md:332-353] [testing/EVIDENCE_CONVENTIONS.md:42-76]

The creator-level product design does not introduce an Execution Kernel, persisted Batch/work-group identity, authoritative Policy Engine, `@platform/*` namespace, cross-platform architecture, local AI authority, production override authority, or duplicate lifecycle/permission/recovery/evidence ownership. The accepted ADR-0010 invariants remain binding. [docs/adr/ADR-0010-Evidence-Bounded-Nexora-Execution-Strengthening-And-Verification.md:419-470]

## 10. Authority and Conflict Protocol

The creator-owned product design answers **what Nexora is**. Canonical architecture, specifications, state machines, models, protocols, APIs, SDKs, registries, requirements, UI documents, and testing documents answer **how the selected product design is realized**. No document may silently reinterpret either layer.

If a canonical document conflicts with this creator-owned design:

> **CONFLICT → STOP → REPORT → CREATOR DECISION**

The conflict MUST identify both documents, the exact line ranges, the competing statements, the affected owner/lifecycle/security/persistence/evidence semantics, and the decision required from the creator. AI agents MUST NOT resolve the conflict by changing this document or silently changing the canonical document.

## 11. Evidence-State Discipline

Every product and implementation statement MUST distinguish:

> **CANONICAL REQUIREMENT ≠ IMPLEMENTED ≠ TEST DEFINED ≠ TESTED ≠ EXECUTED EVIDENCE**

- **CANONICAL REQUIREMENT:** an authoritative product or subsystem contract.
- **IMPLEMENTED:** source implementation exists and is attributable to the owning contract.
- **TEST DEFINED:** a test or fixture specification exists.
- **TESTED:** a specified test was executed and produced a result.
- **EXECUTED EVIDENCE:** the executed result is retained in reproducible form with environment, fixture, identities, result, and artifact location.

The Phase 0 repository currently provides documentation and planned validation artifacts; it does not itself prove implementation or executed runtime/device evidence. [PROJECT_SPECIFICATION.md:9-17,347-357] [testing/EVIDENCE_CONVENTIONS.md:42-76]

## 12. Product Non-Goals

This product design does not introduce or authorize:

- local AI models or local AI inference runtimes;
- a hardcoded single-provider architecture;
- direct model access to host filesystem, Android APIs, process environment, or unrestricted network;
- a second execution kernel, second agent runtime, or second authorization authority;
- persisted Batch/work-group identity or lifecycle;
- authoritative Policy Engine or policy god-object;
- `@platform/*` namespace or a generic cross-platform core;
- Desktop/Web/CLI product expansion;
- user-facing terminal or sandbox infrastructure as the primary interaction surface;
- AI as architecture, permission, lifecycle, security, completion, or evidence authority;
- automatic plugin access to unrestricted filesystem, process, network, secrets, Android permissions, or workspace data;
- completion claims without evidence-bounded validation.

## 13. References and Ownership Map

| Product design area | Primary existing owner | Supporting owners |
|---|---|---|
| Product identity and interaction | `PROJECT_SPECIFICATION.md`, `docs/PRODUCT_PRINCIPLES.md` | `docs/PRODUCT_VISION.md`, ADR-0001, ADR-0006 |
| Cloud AI provider/model/capability/configuration | `architecture/PROVIDER_SYSTEM.md` | `specs/AI_PROVIDERS.md`, provider model/protocol/API/SDK documents |
| Runtime and agent loop | `architecture/RUNTIME.md`, `architecture/AGENT_RUNTIME.md` | `architecture/WORKFLOW_ENGINE.md`, `architecture/MULTI_AGENT_SYSTEM.md` |
| Tool execution | `architecture/TOOL_SYSTEM.md` | Tool protocol/API/SDK/registry, `security/PermissionModel.md` |
| Sandbox and local execution | `architecture/SANDBOX.md`, `security/SandboxPolicy.md` | `specs/TERMINAL.md`, `specs/FULL_ENVIRONMENT.md`, `specs/BACKGROUND_EXECUTION.md` |
| Skills | ADR-0007 and Skill Registry/runtime ownership | `models/Skill.md`, `registry/SKILLS.md` |
| Plugins | `architecture/PLUGIN_SYSTEM.md`, Plugin lifecycle | `models/Plugin.md`, Plugin protocol/API/SDK/registry |
| AI Settings | Provider ownership plus existing Settings/AI Providers UI surface | `ui/Navigation.md`, `ui/Components.md`, `specs/AI_PROVIDERS.md` |
| Permissions and security | `security/PermissionModel.md`, `architecture/SECURITY_MODEL.md` | `security/SandboxPolicy.md`, `security/ThreatModel.md` |
| Context and project knowledge | `specs/CONTEXT_MANAGEMENT.md` | Memory, ClaimRecord, Inference, database, Agent protocol/API |
| Background execution and terminal | `specs/BACKGROUND_EXECUTION.md`, `specs/TERMINAL.md` | Runtime, TerminalSession lifecycle/model, Android UI/notification owners |
| Testing and evidence | `testing/EVIDENCE_CONVENTIONS.md` and existing test-suite/case owners | `docs/TRACEABILITY.md`, requirements, release gates |

This map is a product-to-architecture cross-reference. It does not transfer canonical ownership to this creator document.
