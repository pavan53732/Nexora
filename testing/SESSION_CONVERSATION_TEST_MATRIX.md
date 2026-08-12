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
- Traceability: DEC-20.

### T04 — Session recreation
- Preconditions: terminal `S1`, prior Conversation `C1` exists.
- Action: reopen work through new Session `S2`.
- Expected result: `S2` is a new Session identity.
- Session identity: `S1 != S2`.
- Conversation identity: depends on continuation vs rollback; unchanged if continuation.
- Association result: any later association is new.
- Forbidden result: same-identity reopen.
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
- Traceability: DEC-19.

### T07 — Conversation sequentially associated with different Sessions
- Preconditions: `S1 ↔ C1` no longer active.
- Action: later associate `S2` with `C1`.
- Expected result: allowed continuation/historical multiplicity.
- Session identity: later `S2`.
- Conversation identity: same `C1`.
- Association result: new active association.
- Traceability: DEC-19, DEC-21.

### T08 — Simultaneous Session conflict
- Preconditions: active `S1 ↔ C1`.
- Action: attempt `S1 ↔ C2` simultaneously.
- Expected result: reject.
- Forbidden result: one Session with two active Conversations.
- Traceability: DEC-19.

### T09 — Simultaneous Conversation conflict
- Preconditions: active `S1 ↔ C1`.
- Action: attempt `S2 ↔ C1` simultaneously.
- Expected result: reject.
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
- Traceability: DEC-9, DEC-21.

### T12 — Source preservation
- Preconditions: `C1` and valid checkpoint.
- Action: create branch `C2`.
- Expected result: `C1` remains addressable and unchanged.
- Traceability: DEC-9.

### T13 — Checkpoint lineage preservation
- Preconditions: valid rollback source checkpoint.
- Action: create branch.
- Expected result: branch stores source checkpoint lineage.
- Forbidden result: orphan branch without checkpoint lineage.
- Traceability: DEC-8, DEC-9.

### T14 — Conversation identity preservation during continuation
- Preconditions: ended `S1 ↔ C1`.
- Action: continue via `S2 ↔ C1`.
- Expected result: Conversation identity remains `C1`.
- Traceability: DEC-21.

### T15 — New Conversation identity during rollback
- Preconditions: rollback from `C1`.
- Action: create branch.
- Expected result: new Conversation identity `C2`.
- Traceability: DEC-9.

### T16 — Process death
- Preconditions: active or recoverable Session/Conversation context.
- Action: process death occurs.
- Expected result: no independently selected relationship mutation.
- Forbidden result: automatic Conversation deletion or continuation assumption.
- Traceability: DEC-20, DEC-21.

### T17 — Application restart
- Preconditions: prior Session/Conversation state persisted.
- Action: app restarts.
- Expected result: no independently selected relationship mutation.
- Traceability: DEC-20, DEC-21.

### T18 — Same-Session recovery
- Preconditions: same still-valid Session can be restored.
- Action: recover same Session.
- Expected result: no new Session identity, no cross-Session continuation.
- Traceability: Session lifecycle, DEC-20, DEC-21.

### T19 — New-Session continuation/recovery
- Preconditions: same Session cannot be restored; Conversation remains valid.
- Action: recover via new Session.
- Expected result: new Session identity, same Conversation identity, new active association.
- Traceability: DEC-21.

### T20 — Historical multiplicity
- Preconditions: no concurrent conflict.
- Action: observe sequential Session/Conversation associations over time.
- Expected result: allowed historically; not all-time unique.
- Traceability: DEC-19, DEC-21.

### T21 — Active-cardinality enforcement
- Preconditions: system can evaluate active associations.
- Action: submit conflicting simultaneous association.
- Expected result: reject conflict.
- Traceability: DEC-19.

### T22 — Identity mutation
- Preconditions: existing Session or Conversation.
- Action: attempt same-object identity rewrite.
- Expected result: reject.
- Traceability: DEC-13, Session lifecycle.

### T23 — Terminal Session reuse
- Preconditions: terminal `S1`.
- Action: attempt reopen as `S1`.
- Expected result: reject; require new Session identity.
- Traceability: Session lifecycle, DEC-21.

### T24 — Invalid continuation
- Preconditions: nonexistent, unauthorized, or invalid source Conversation/Session.
- Action: attempt continuation.
- Expected result: reject without semantic mutation.
- Traceability: DEC-21, engineering contract.

### T25 — Invalid rollback
- Preconditions: invalid or unauthorized checkpoint/lineage.
- Action: attempt rollback.
- Expected result: reject; source Conversation preserved; no branch claimed.
- Traceability: DEC-8, DEC-9.
