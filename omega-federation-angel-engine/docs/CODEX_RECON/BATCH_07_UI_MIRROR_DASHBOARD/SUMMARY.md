# Batch 07 — UI / Mirror / Dashboard Recon Summary

**Status:** first pass complete  
**Timestamp:** 2026-05-18  
**Purpose:** identify UI, mirror, dashboard, website, and visualizer repositories before integration.

---

## Scope

```text
covenant-mirror-x11
merkabah-dashboard
lilac-protocol-visualizer
kingdom-engine-website
omega_app
omnissiah-engine
omnissiah-unified-v3
omnissiah-unified-master
```

---

## Files Written

```text
repo-matrix.yaml
SUMMARY.md
```

A combined matrix was used for speed. It can be split into per-repo YAMLs later if Codex needs that format.

---

## Metadata Findings

```text
kingdom-engine-website: public, main, 10008 KB
omnissiah-unified-master: public, main, 590 KB
omnissiah-engine: public, main, 250 KB
covenant-mirror-x11: private, main, 181 KB
omnissiah-unified-v3: public, main, 115 KB
omega_app: public, main, 90 KB
merkabah-dashboard: private, master, 5 KB
lilac-protocol-visualizer: private, master, 1 KB
```

Connector code search returned no inspectable file hits for common UI/dashboard/web terms.

---

## Finding 1 — Largest Public UI Candidate

```text
kingdom-engine-website
```

At 10008 KB, this is the highest-priority Batch 07 repo for Codex/tree inspection.

It likely contains substantive website or public-facing content.

---

## Finding 2 — Omnissiah Family Needs Comparison

```text
omnissiah-engine
omnissiah-unified-v3
omnissiah-unified-master
```

These should be compared together for overlap, duplication, version drift, and deployment assumptions.

---

## Finding 3 — Mirror / X11 Candidate

```text
covenant-mirror-x11
```

This requires GUI/X11 dependency review and launch-command inspection before use.

---

## Finding 4 — Small Visual Shells

```text
merkabah-dashboard
lilac-protocol-visualizer
```

These remain reference/review shells unless tree inspection reveals implementation content.

---

## Integration Boundary

UI repositories are interface layers, not authority layers.

Dashboards may visualize witness packets but must not bypass Repo 120 gates.

Public web repos require:

```text
content review
secret scan
deployment review
privacy review
external link/API review
```

---

## Activation Candidates

```text
none cleared yet
```

---

## Review Required

```text
all Batch 07 repositories
```

---

## Priority Order

```text
1. kingdom-engine-website
2. omnissiah-unified-master
3. omnissiah-engine
4. covenant-mirror-x11
5. omnissiah-unified-v3
6. omega_app
7. merkabah-dashboard
8. lilac-protocol-visualizer
```

---

## Next Batch

Batch 08 — Recovery / Archive / Continuity.

---

## Lock Line

A dashboard is a window, not a judge.
