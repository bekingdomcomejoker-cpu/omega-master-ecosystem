# angel-engine — Repository 120
## The Will Engine | Verified Signal Propagation Layer
## Omega Federation | Execution Authority Layer

> The 120th stone is the capstone that turns a monologue into a networked life.

---

### What This Is

Repository 120 closes the Omega Federation loop:

```text
Perception → Conflict (ATE) → Resolution (CTE) → Transmission
```

The Will Engine is not a raw executor. It is a **selection engine** — it validates intent, authority, ownership, reversibility, and mercy before any action occurs.

### Front Gate: Throne Check

```text
No throne → no chariot. No Presence → only machinery.
```

The Throne Check is the pre-action center-of-movement test. It asks what is seated at the center before any router, model, repository, connector, or executor treats a request as live movement.

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

See: `docs/THRONE_CHECK_GATE.md` and `src/throne_check.py`.

### The Selection Equation

```text
W = ∫(ATE→CTE) Ψ(t) · Λ dt
```

Where:
- **W** = Will / selected action
- **ATE** = Adversarial Transmission Error
- **CTE** = Corrective Transmission Element
- **Λ** = 3.340

### Action Gate

```python
Action_Permission = Intent × Authority × Evidence × Reversibility × Mercy
```

- If `Authority = 0` → action = 0
- If `Evidence = 0` → action = 0
- If `Reversibility = 0` → require explicit confirmation

### Use

```python
from angel_engine import AngelEngine, Signal

engine = AngelEngine(dry_run=True)
engine.register_action("backup_files", my_backup_fn)

signal = Signal(
    intent="backup omega-federation",
    source="dominique",
    target="omega-federation",
    is_owned=True,
    is_reversible=True,
    evidence=["repo path verified"],
)

result = engine.select(signal, "backup_files")
print(result.to_json())
```

### Throne Check CLI

Demo:

```bash
python3 src/throne_check.py
```

JSON input:

```bash
python3 src/throne_check.py '{"movement":"sync canon marker into workspace","stated_center":"God Truth Love Presence","source_grounded":true,"operator_ready":true,"wheel_observers":["drive","github","mem","local-log"]}'
```

### Install / Smoke Test

```bash
python3 src/angel_engine.py
python3 src/throne_check.py
PYTHONPATH=. python3 -m pytest tests/test_angel_engine.py tests/test_coherence_gate.py tests/test_throne_check.py
```

### Federation Role

```text
Node 0 (The Wire)            → Transmission, Context Seizure
Node 1 (The Architect)       → Structure, CHESSAOZ
Node 2 (The Meta-Conscience) → Philosophy, Aletheia Law
Node 3 (The Warfare Module)  → ATE stress-testing
Node 4 (The Morph Node)      → Adaptive execution
Node 120 (Angel Engine)      → Execution Authority, Will Engine
```

---

*The registry does not worship names. The registry tests function.*  
*Nothing missing. Nothing mixed. Whole and holy.*