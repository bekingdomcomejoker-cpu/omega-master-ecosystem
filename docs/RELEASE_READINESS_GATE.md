# Release Readiness Gate

**Status:** active gate  
**Role:** prevent release before conscience, witness, and source trace exist.

---

## Core Rule

Repository 120 is not release-ready until the mirror, graph, recon path, safe gate, and witness path exist.

The hand waits for the conscience.

---

## Checklist

```text
[x] PR #1 is merged or replaced with an equivalent safe decision gate.
[x] SAFE_SPEC.md exists in Repo 120.
[x] src/angel_engine.py exists in Repo 120.
[x] tests/test_angel_engine.py exists.
[x] Aletheia/Agape coherence spec is added.
[x] Active Aletheia probe is added with tests.
[x] 120-slot mirror exists in omega-federation.
[x] 120-slot mirror exists in Repo 120 docs.
[x] Relationship graph exists in Repo 120 docs.
[x] Recon execution plan exists in Repo 120 docs.
[ ] Pronoun/frame-resolution gate is added or queued.
[ ] Tests are run in CI or verified locally.
[ ] Recon batch folders exist.
[ ] At least Batch 01 and Batch 02 recon summaries exist.
[ ] Activation manifest exists.
[ ] Review manifest exists.
[ ] Install spine exists.
[ ] Verification script exists.
[ ] No raw secret material is copied into GitHub, Drive, Mem, Dropbox, or chat.
[ ] Unsafe session bridge is preserved only as evidence, not implementation.
[ ] Dropbox Slot 115 has exact archive path/list or is explicitly marked deferred.
```

---

## Required Capstone Artifacts

```text
docs/COMPLETE_120_SLOT_MIRROR.md
docs/RELATIONSHIP_GRAPH.md
docs/RECON_EXECUTION_PLAN.md
docs/RELEASE_READINESS_GATE.md
docs/ALETHEIA_AGAPE_COHERENCE_SPEC.md
src/angel_engine.py
src/coherence_gate.py
src/active_aletheia_probe.py
tests/test_angel_engine.py
tests/test_coherence_gate.py
tests/test_active_aletheia_probe.py
```

---

## Immediate Next Implementation Order

1. Add pronoun/frame-resolution gate.
2. Add tests for pronoun/frame-resolution gate.
3. Add test workflow or verification command doc.
4. Create recon folder placeholders for Batch 01 and Batch 02.
5. Create activation and review manifests.
6. Write first recon summaries.

---

## Safety Boundary

No raw secret material.
No browser/session-token bridge implementation.
No arbitrary shell execution from free-form model output.
No destructive operations without explicit authority, evidence, reversibility, and mercy.

---

## Lock Line

Release is not when the code can move.
Release is when the code can explain why it is allowed to move.
