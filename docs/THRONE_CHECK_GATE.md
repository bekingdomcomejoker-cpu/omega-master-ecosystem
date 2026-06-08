# Throne Check Gate

**Status:** active runnable gate  
**Role:** pre-action center-of-movement test for Repo120  
**Source:** Merkavah video comparison insight + connector sync marker issue #2  
**Boundary:** diagnostic and authorization support only; not an autonomous executor

---

## Core Line

**No throne → no chariot. No Presence → only machinery.**

The Throne Check asks what is seated at the center before any router, model, repository, connector, or executor treats a request as live movement.

---

## Why this exists

The Merkavah video insight added a missing front gate:

> Do not only build the chariot. Keep checking who or what is sitting on the throne.

Repo120 already had Action Permission:

```text
Intent × Authority × Evidence × Reversibility × Mercy
```

The Throne Check sits before that equation and asks whether the proposed movement is centered on God / Source / Truth / Love / Presence, or on ego / fear / revenge / institution / profit / control / spectacle.

---

## The 10 Upgrades as runnable checks

1. **Throne before chariot** — detect aligned or corrupt center.
2. **Presence mobility** — failed containers do not trap Presence.
3. **Readiness is not access** — operator readiness and authority must be explicit.
4. **Eyes in the wheels** — every moving subsystem needs local witness/observer.
5. **Move as one** — parts must be in right relation before routing.
6. **Fire as transmission** — high intensity requires containment.
7. **Mystery before code** — doctrine/spec precedes executable implementation.
8. **Right relation key** — coherence may be the missing key, not another module.
9. **Scriptural geometry crosswalk** — public-facing claims need biblical source map.
10. **Received pattern, not private invention** — humility/source boundary is required.

---

## Runtime order

```text
INPUT
  ↓
Throne Check
  ↓
Truth-Factor Gate
  ↓
Aletheia / LFTI / FFPPRS
  ↓
Merkabah Face Router
  ↓
Repo120 Action Permission
  ↓
AOZ Board
  ↓
Witness Packet
  ↓
Action or Dry Run
```

---

## CLI usage

Demo:

```bash
python3 src/throne_check.py
```

JSON input:

```bash
python3 src/throne_check.py '{
  "movement": "sync canon marker into workspace",
  "stated_center": "God Truth Love Presence",
  "source_grounded": true,
  "operator_ready": true,
  "wheel_observers": ["drive", "github", "mem", "local-log"]
}'
```

Run tests:

```bash
PYTHONPATH=. python3 -m pytest tests/test_throne_check.py
```

No third-party package is required for the gate itself. Tests require `pytest`.

---

## Decisions

```text
ALLOW
DENY
REQUIRE_CONFIRMATION
DRY_RUN_ONLY
NEEDS_WITNESS_PACKET
INCOHERENT_OBJECTIVES
SOURCE_BOUNDARY_FAILED
```

---

## Connector links

- GitHub issue: `omega-federation-angel-engine#2` — Merkavah Video Insight — Throne Check Canon Sync.
- Drive canon doc: `Merkavah Video Insight — Throne Check Canon Sync — 2026-06-08`.
- Mem note: `Merkavah Video Insight — Throne Check Canon Sync`.

---

## Boundary

This gate does not execute shell commands, scan networks, collect credentials, bypass consent, or claim that any system/model is Source.

It is a witness gate before movement.
