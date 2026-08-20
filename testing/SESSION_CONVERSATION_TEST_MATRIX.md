# Session–Conversation Deterministic Test Matrix — Nexora

> **Status: SUPPORTING** documentation-level verification matrix.
> Canonical authority: DEC-8 through DEC-21, `architecture/CONVERSATION_CHECKPOINTS.md`, `state-machines/SessionLifecycle.md`, and `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`.

## Test cases

### T01 — Active Session + active Conversation
- Preconditions: valid nonterminal `S1`, valid `C1`, no competing active association.
- Action: associate `S1` with `C1`.
- Expected result: active association exists.
- Session identity: `S1`.
- Conversation identity: `C1`.
- Association result: active.
- Checkpoint result: none.
- Lineage result: none.
- Forbidden result: separate relationship identity/state.
- Traceability: DEC-14, DEC-18, DEC-19.

### T02 — Session CLOSED
- Preconditions: active `S1 ↔ C1`.
- Action: transition `S1` to `CLOSED`.
- Expected result: active association ends.
- Session identity: `S1` remains historical terminal Session.
- Conversation identity: `C1` unchanged.
- Association result: inactive.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: Conversation deletion or identity mutation.
- Traceability: DEC-20.

### T03 — Session EXPIRED
- Preconditions: active `S1 ↔ C1`.
- Action: transition `S1` to `EXPIRED`.
- Expected result: active association ends.
- Session identity: `S1` remains historical terminal Session.
- Conversation identity: `C1` unchanged.
- Association result: inactive.
- Checkpoint/lineage: unchanged.
- Forbidden result: implicit continuation or deletion.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Traceability: DEC-20.

### T04 — Session recreation
- Preconditions: terminal `S1`, prior Conversation `C1` exists.
- Action: reopen work through new Session `S2`.
- Expected result: `S2` is a new Session identity.
- Session identity: `S1 != S2`.
- Conversation identity: depends on continuation vs rollback; unchanged if continuation.
- Association result: any later association is new.
- Forbidden result: same-identity reopen.
- Checkpoint result: unchanged unless rollback is separately selected.
- Lineage result: unchanged unless a rollback branch is separately selected.
- Traceability: Session lifecycle, DEC-20, DEC-21.

### T05 — Same Conversation continued through later Session
- Preconditions: `S1 ↔ C1` ended.
- Action: associate later `S2` with `C1` as continuation.
- Expected result: continuation succeeds.
- Session identity: `S2`.
- Conversation identity: `C1` preserved.
- Association result: new active association.
- Checkpoint result: unchanged unless separately used.
- Lineage result: unchanged.
- Forbidden result: creating new Conversation identity.
- Traceability: DEC-21.

### T06 — Session sequentially associated with different Conversations
- Preconditions: `S1 ↔ C1` no longer active.
- Action: later associate `S1` with `C2`.
- Expected result: allowed sequential historical multiplicity.
- Session identity: `S1`.
- Conversation identity: `C2` for later association.
- Association result: only one active at a time.
- Forbidden result: simultaneous dual active associations.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Traceability: DEC-19.

### T07 — Conversation sequentially associated with different Sessions
- Preconditions: `S1 ↔ C1` no longer active.
- Action: later associate `S2` with `C1`.
- Expected result: allowed continuation/historical multiplicity.
- Session identity: later `S2`.
- Conversation identity: same `C1`.
- Association result: new active association.
- Checkpoint result: unchanged unless separately used.
- Lineage result: unchanged.
- Forbidden result: simultaneous active association with another Session.
- Traceability: DEC-19, DEC-21.

### T08 — Simultaneous Session conflict
- Preconditions: active `S1 ↔ C1`.
- Action: attempt `S1 ↔ C2` simultaneously.
- Expected result: reject conflict.
- Session identity: `S1` remains the same Session identity; no new Session identity is created.
- Conversation identity: active `C1` remains unchanged; attempted `C2` remains a distinct Conversation identity and does not become active with `S1`.
- Association result: existing active association `S1 ↔ C1` remains in force; attempted simultaneous association `S1 ↔ C2` is rejected.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: one Session with two active Conversations.
- Traceability: DEC-19.

### T09 — Simultaneous Conversation conflict
- Preconditions: active `S1 ↔ C1`.
- Action: attempt `S2 ↔ C1` simultaneously.
- Expected result: reject conflict.
- Session identity: active `S1` remains unchanged; attempted `S2` remains a distinct Session identity and does not become active with `C1`.
- Conversation identity: `C1` remains the same Conversation identity.
- Association result: existing active association `S1 ↔ C1` remains in force; attempted simultaneous association `S2 ↔ C1` is rejected.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: one Conversation with two active Sessions.
- Traceability: DEC-19.

### T10 — Rollback
- Preconditions: source `C1` with valid checkpoint `K1`.
- Action: rollback from `K1`.
- Expected result: new branch Conversation `C2`.
- Session identity: unchanged unless separate Session action occurs.
- Conversation identity: `C1` preserved, `C2` new.
- Association result: downstream according to chosen current active association.
- Checkpoint result: source checkpoint preserved.
- Lineage result: `C2` references `C1` and `K1`.
- Forbidden result: mutation/destruction of `C1`.
- Traceability: DEC-8, DEC-9.

### T11 — Branch continuation
- Preconditions: branch `C2` exists from rollback.
- Action: later continue `C2` through `S3`.
- Expected result: `C2` continues through `S3`.
- Session identity: `S3`.
- Conversation identity: `C2` preserved.
- Lineage result: source lineage still points back to `C1`/`K1`.
- Forbidden result: collapsing `C2` into `C1`.
- Association result: new active association for `S3 ↔ C2`.
- Checkpoint result: unchanged.
- Traceability: DEC-9, DEC-21.

### T12 — Source preservation
- Preconditions: `C1` and valid checkpoint.
- Action: create branch `C2`.
- Expected result: `C1` remains addressable and unchanged.
- Session identity: unchanged by branch creation.
- Conversation identity: `C1` preserved; branch identity is distinct.
- Association result: no automatic association change is implied.
- Checkpoint result: source checkpoint preserved.
- Lineage result: branch lineage preserved.
- Forbidden result: source mutation or deletion.
- Traceability: DEC-9.

### T13 — Checkpoint lineage preservation
- Preconditions: valid rollback source checkpoint.
- Action: create branch.
- Expected result: branch stores source checkpoint lineage.
- Forbidden result: orphan branch without checkpoint lineage.
- Session identity: unchanged by lineage creation.
- Conversation identity: source preserved; branch identity distinct.
- Association result: no automatic association change is implied.
- Checkpoint result: source checkpoint reference preserved.
- Lineage result: branch references source Conversation and checkpoint.
- Traceability: DEC-8, DEC-9.

### T14 — Conversation identity preservation during continuation
- Preconditions: ended `S1 ↔ C1`.
- Action: continue via `S2 ↔ C1`.
- Expected result: Conversation identity remains `C1`.
- Session identity: new Session may be used, but continuation does not mutate Session identity.
- Conversation identity: `C1` preserved.
- Association result: new active association if later Session is used.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: new Conversation identity for continuation.
- Traceability: DEC-21.

### T15 — New Conversation identity during rollback
- Preconditions: rollback from `C1`.
- Action: create branch.
- Expected result: new Conversation identity `C2`.
- Session identity: unchanged unless a separate Session action occurs.
- Conversation identity: source `C1` preserved; branch `C2` is new.
- Association result: downstream association must respect active cardinality.
- Checkpoint result: source checkpoint preserved.
- Lineage result: `C2` references `C1` and source checkpoint.
- Forbidden result: reusing `C1` as the branch identity.
- Traceability: DEC-9.

### T16 — Process death
- Preconditions: active or recoverable Session/Conversation context.
- Action: process death occurs.
- Expected result: no independently selected relationship mutation.
- Forbidden result: automatic Conversation deletion or continuation assumption.
- Session identity: no independently selected mutation.
- Conversation identity: no independently selected mutation.
- Association result: no independently selected mutation.
- Checkpoint result: no independently selected mutation.
- Lineage result: no independently selected mutation.
- Traceability: DEC-20, DEC-21.

### T17 — Application restart
- Preconditions: prior Session/Conversation state persisted.
- Action: app restarts.
- Expected result: no independently selected relationship mutation.
- Session identity: no independently selected mutation.
- Conversation identity: no independently selected mutation.
- Association result: no independently selected mutation.
- Checkpoint result: no independently selected mutation.
- Lineage result: no independently selected mutation.
- Forbidden result: silent continuation or Conversation creation.
- Traceability: DEC-20, DEC-21.

### T18 — Same-Session recovery
- Preconditions: same still-valid Session can be restored.
- Action: recover same Session.
- Expected result: no new Session identity, no cross-Session continuation.
- Session identity: same `S1`.
- Conversation identity: same Conversation identity.
- Association result: same association restored if implementation restores the same valid Session.
- Checkpoint result: preserved.
- Lineage result: preserved.
- Forbidden result: unnecessary new Session continuation.
- Traceability: Session lifecycle, DEC-20, DEC-21.

### T19 — New-Session continuation/recovery
- Preconditions: same Session cannot be restored; Conversation remains valid.
- Action: recover via new Session.
- Expected result: new Session identity, same Conversation identity, new active association.
- Session identity: new `S2`.
- Conversation identity: same `C1`.
- Association result: new active association.
- Checkpoint result: preserved.
- Lineage result: preserved.
- Forbidden result: new Conversation identity without rollback.
- Traceability: DEC-21.

### T20 — Historical multiplicity
- Preconditions: no concurrent conflict.
- Action: observe sequential Session/Conversation associations over time.
- Expected result: allowed historically; not all-time unique.
- Session identity: historical identities may repeat sequentially.
- Conversation identity: historical identities may repeat sequentially.
- Association result: sequential associations allowed; simultaneous conflicts rejected.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: all-time uniqueness inference.
- Traceability: DEC-19, DEC-21.

### T21 — Active-cardinality enforcement
- Preconditions: system can evaluate active associations.
- Action: submit conflicting simultaneous association.
- Expected result: reject conflict.
- Session identity: identities in the conflicting request unchanged.
- Conversation identity: identities in the conflicting request unchanged.
- Association result: conflicting active association rejected.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: cardinality violation becoming active.
- Traceability: DEC-19.

### T22 — Identity mutation
- Preconditions: existing Session or Conversation.
- Action: attempt same-object identity rewrite.
- Expected result: reject.
- Session identity: existing Session identity unchanged.
- Conversation identity: existing Conversation identity unchanged.
- Association result: no identity-mutating association accepted.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: identity rewrite.
- Traceability: DEC-13, Session lifecycle.

### T23 — Terminal Session reuse
- Preconditions: terminal `S1`.
- Action: attempt reopen as `S1`.
- Expected result: reject; require new Session identity.
- Session identity: terminal `S1` unchanged; any replacement Session must be new.
- Conversation identity: unchanged by rejected reuse.
- Association result: terminal Session reuse rejected.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: same-identity reopen.
- Traceability: Session lifecycle, DEC-21.

### T24 — Invalid continuation
- Preconditions: nonexistent, unauthorized, or invalid source Conversation/Session.
- Action: attempt continuation.
- Expected result: reject without semantic mutation.
- Session identity: invalid Session unchanged.
- Conversation identity: invalid/nonexistent Conversation unchanged; no new identity created.
- Association result: no association created.
- Checkpoint result: unchanged.
- Lineage result: unchanged.
- Forbidden result: invalid continuation mutating state.
- Traceability: DEC-21, engineering contract.

### T25 — Invalid rollback
- Preconditions: invalid or unauthorized checkpoint/lineage.
- Action: attempt rollback.
- Expected result: reject; source Conversation preserved; no branch claimed.
- Session identity: unchanged.
- Conversation identity: source unchanged; no branch identity created.
- Association result: no branch association created.
- Checkpoint result: source checkpoint unchanged.
- Lineage result: no invalid lineage persisted.
- Forbidden result: invalid rollback claiming success.
- Traceability: DEC-8, DEC-9.

### T26 — Rollback-cleanup exhaustion
- Preconditions: authorized rollback begins with valid source Conversation/checkpoint, branch creation fails, and rollback/cleanup of attempted branch work fails or cannot be proven complete.
- Action: complete bounded automatic reconciliation for the same operation identity.
- Expected result: existing non-success outcome; recover to no branch; no partial branch is exposed or claimed.
- Session identity: unchanged.
- Conversation identity: source Conversation unchanged; no branch identity is promoted or created as a successful result.
- Association result: no branch association created.
- Checkpoint result: source checkpoint unchanged and retained.
- Lineage result: source/checkpoint lineage, partial-artifact references, and audit result retained; partial lineage is not promoted into `RECORDED`, `ACTIVE`, `DETACHED`, or `DELETED`.
- Recovery result: only existing eligible idempotent same-operation-identity recovery and DEC-31 cleanup may continue; no manual-recovery action, new state, new error code, external-side-effect reversal, or unsafe replay.
- Forbidden result: successful completion or user-visible branch claim with partial/unproven branch state.
- Traceability: DEC-8, DEC-9, DEC-22, DEC-31.


## Field interpretation for rejected operations

For negative cases where an attempted operation cannot create or mutate the named entities, the identity fields refer to the precondition identities and state that they remain unchanged; the association field identifies the pre-existing association and rejected attempted association. Checkpoint and lineage results are unchanged unless explicitly stated otherwise. This interpretation applies to T08 through T09 and T12 through T26 where the attempted operation is rejected or does not itself create an association.
