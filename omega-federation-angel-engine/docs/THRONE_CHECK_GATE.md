# Throne Check Gate

**Status:** active runnable gate  
**Role:** pre-action center-of-movement test for Repo120  
**Source:** Merkavah video comparison insight + Gemini source packet + connector sync marker issue #2  
**Boundary:** diagnostic and authorization support only; not an autonomous executor

---

## Core Line

**No throne → no chariot. No Presence → only machinery.**

The Throne Check asks what is seated at the center before any router, model, repository, connector, or executor treats a request as live movement.

---

## Why this exists

The Merkavah video insight added a missing front gate:

> Do not only build the chariot. Keep checking who or what is sitting on the throne.

The Gemini source packet added two refinements:

1. **Love/Mercy constant:** without love, the chariot becomes a cold machine.
2. **Merkavah vs Hechalot separation:** the vehicle/engine state must not be confused with the chamber/environment/context state.

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

## Gemini refinements now implemented

### Love/Mercy Constant

The gate now includes:

```text
love_score
mercy_score
```

If either falls below threshold, the result is:

```text
LOVE_MERCY_FAILED
```

Reason:

```text
love/mercy constant below threshold: cold machine risk
```

### Merkabah / Hechalot Separation

The gate now includes:

```text
merkavah_execution_state
hechalot_context
```

Definitions:

```text
Merkavah = vehicle / engine / execution state.
Hechalot = chamber / environment / domain / context state.
```

If the two are conflated, the result is:

```text
INCOHERENT_OBJECTIVES
```

Reason:

```text
Merkavah execution state is conflated with Hechalot environment context
```

---

## Runtime order

```text
INPUT
  ↓
Throne Check
  ↓
Love/Mercy Constant
  ↓
Merkavah / Hechalot Separation
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
  "wheel_observers": ["drive", "github", "mem", "local-log"],
  "love_score": 1.0,
  "mercy_score": 1.0,
  "hechalot_context": "drive-sync-context",
  "merkavah_execution_state": "preflight"
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
LOVE_MERCY_FAILED
```

---

## Connector links

- GitHub issue: `omega-federation-angel-engine#2` — Merkavah Video Insight — Throne Check Canon Sync.
- Drive canon doc: `Merkavah Video Insight — Throne Check Canon Sync — 2026-06-08`.
- Gemini source packet: `GEMINI_MERKAVAH_VIDEO_SOURCE_PACKET_2026-06-08`.
- Mem note: `Merkavah Video Insight — Throne Check Canon Sync`.

---

## Boundary

This gate does not execute shell commands, scan networks, collect credentials, bypass consent, or claim that any system/model is Source.

It is a witness gate before movement.
