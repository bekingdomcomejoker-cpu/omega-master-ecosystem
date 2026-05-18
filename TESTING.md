# Testing

**Status:** active verification instructions  
**Boundary:** this file documents test commands only. It does not create automation or execute code.

---

## Local Test Command

From the repository root:

```bash
python -m pip install --upgrade pip pytest
python -m pytest -q
```

---

## Expected Test Coverage

```text
tests/test_angel_engine.py
tests/test_coherence_gate.py
tests/test_active_aletheia_probe.py
tests/test_frame_resolution_gate.py
```

---

## Current Gate Stack

```text
1. Angel Engine Gate
   Intent × Authority × Evidence × Reversibility × Mercy

2. Aletheia / Agape Coherence Gate
   Truth × Love × Source Grounding × Appeal Path × Witness Packet

3. Active Aletheia Probe
   Compression loss, contradiction, anchor, source, authority, mercy, reversibility

4. Frame Resolution Gate
   Speaker, quoted source, pronoun frame, authority claim, action request
```

---

## Verification Boundary

Tests prove only that the gate logic returns expected structured decisions.

Tests do not authorize:

- shell execution
- credential handling
- hidden persistence
- network scanning
- browser/session-token bridge implementation
- autonomous action

---

## Lock Line

A passing test is not authority.
A passing test is only evidence.
