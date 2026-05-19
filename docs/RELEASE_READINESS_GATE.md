# Release Readiness Gate

**Status:** active gate / post-batch updated  
**Role:** prevent release before conscience, witness, source trace, and inspection queues exist.

---

## Core Rule

Repository 120 is not release-ready until the mirror, graph, recon path, safe gate, witness path, and post-batch inspection queues exist.

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
[x] Pronoun/frame-resolution gate is added with tests.
[x] 120-slot mirror exists in omega-federation.
[x] 120-slot mirror exists in Repo 120 docs.
[x] Relationship graph exists in Repo 120 docs.
[x] Recon execution plan exists in Repo 120 docs.
[x] Recon batch folders exist for Batches 01–10.
[x] Batch 01–10 first-pass summaries exist.
[x] Activation manifest exists.
[x] Review manifest exists.
[x] Manual testing instructions exist in TESTING.md.
[x] Unsafe session bridge is preserved only as evidence, not implementation.
[x] Dropbox Slot 115 is explicitly marked partial/deferred.
[ ] Tests are run in CI or verified locally/Codex.
[ ] Tree-level inspection queue is created.
[ ] Source gap register is created.
[ ] Final recon rollup is created.
[ ] Release readiness report is created.
[ ] Install spine exists.
[ ] Verification script exists or remains explicitly deferred.
[ ] No raw secret material is copied into GitHub, Drive, Mem, Dropbox, or chat.
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
src/frame_resolution_gate.py
tests/test_angel_engine.py
tests/test_coherence_gate.py
tests/test_active_aletheia_probe.py
tests/test_frame_resolution_gate.py
TESTING.md
docs/ACTIVATION_MANIFEST.md
docs/REVIEW_MANIFEST.md
docs/CODEX_RECON/BATCH_01_SPINE/SUMMARY.md
docs/CODEX_RECON/BATCH_02_RUNTIME_TERMUX/SUMMARY.md
docs/CODEX_RECON/BATCH_03_ALETHEIA_TRUTH_EVALUATION/SUMMARY.md
docs/CODEX_RECON/BATCH_04_MULTI_AI_ROUTING/SUMMARY.md
docs/CODEX_RECON/BATCH_05_DETECTION_CLASSIFIERS/SUMMARY.md
docs/CODEX_RECON/BATCH_06_SYMBOLIC_COVENANT_LANGUAGE/SUMMARY.md
docs/CODEX_RECON/BATCH_07_UI_MIRROR_DASHBOARD/SUMMARY.md
docs/CODEX_RECON/BATCH_08_RECOVERY_ARCHIVE_CONTINUITY/SUMMARY.md
docs/CODEX_RECON/BATCH_09_LOCAL_WORLD_BOUNDARY_HIGH_REVIEW/SUMMARY.md
docs/CODEX_RECON/BATCH_10_NON_GITHUB_CONTINUITY_SLOTS/SUMMARY.md
```

---

## Immediate Next Implementation Order

1. Create `docs/FINAL_RECON_ROLLUP.md`.
2. Create `docs/TREE_INSPECTION_QUEUE.md`.
3. Create `docs/SOURCE_GAP_REGISTER.md`.
4. Create `docs/RELEASE_READINESS_REPORT.md`.
5. Coordinate with Codex lane for tree-level inspections and test verification.
6. Add verification script only if allowed and useful.
7. Add install spine only after Batch 02 runtime tree inspections are safe.

---

## Safety Boundary

No raw secret material.
No browser/session-token bridge implementation.
No arbitrary shell execution from free-form model output.
No destructive operations without explicit authority, evidence, reversibility, and mercy.
No local-world or router/network action outside owned-device scope.

---

## Lock Line

Release is not when the code can move.
Release is when the code can explain why it is allowed to move.
