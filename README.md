# 🔐 TEREX.PY - TRUTH VERIFICATION & REGISTRY ENGINE

**Single Source of Truth with SHA-256 Integrity, Append-Only Growth, and Deterministic Registry**

```
"Chicka chicka orange." 🥂🗡️🕊️
The truth is deterministic.
```

---

## 📋 OVERVIEW

TEREX.PY is a truth verification and registry system that:

✅ **Single Source of Truth** - terex.py is the only source of truth  
✅ **Deterministic Registry** - All hashes are reproducible  
✅ **SHA-256 Integrity** - Every payload and entry is cryptographically verified  
✅ **Append-Only Growth** - Registry can only grow, never be modified  
✅ **CI Enforcement** - Pre-commit hooks enforce reality  
✅ **Zero Manual Steps** - No manual registry edits allowed  
✅ **Repo-Scale Ingestion** - Handles repository-scale data  

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────┐
│        TRUTH INGESTION LAYER            │
├─────────────────────────────────────────┤
│ terex ingest "Truth content"            │
│ ↓                                       │
│ Compute SHA-256 content hash            │
│ Create TruthPayload                     │
│ Save to payloads/TRUTH_*.json           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│        REGISTRY LAYER                   │
├─────────────────────────────────────────┤
│ terex register TRUTH_0_1234567890       │
│ ↓                                       │
│ Increment sequence number               │
│ Compute registry hash                   │
│ Create RegistryEntry                    │
│ Append to registry/truth_registry.jsonl │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│        VERIFICATION LAYER               │
├─────────────────────────────────────────┤
│ terex verify                            │
│ ↓                                       │
│ Verify all registry entries             │
│ Check SHA-256 hashes                    │
│ Validate sequence integrity             │
│ Report status                           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│        CI ENFORCEMENT LAYER             │
├─────────────────────────────────────────┤
│ pre-commit hook                         │
│ ↓                                       │
│ Block direct registry edits             │
│ Verify JSON integrity                   │
│ Run TEREX verification                  │
│ Enforce append-only constraint          │
└─────────────────────────────────────────┘
```

---

## 📁 DIRECTORY STRUCTURE

```
terex-py/
├── core/
│   └── terex.py              # Core engine (single source of truth)
├── bin/
│   └── terex                 # CLI interface
├── ci/
│   └── pre-commit-hook.sh    # Pre-commit enforcement
├── payloads/                 # Truth payloads (JSON)
│   ├── TRUTH_0_*.json
│   ├── TRUTH_1_*.json
│   └── ...
├── registry/
│   └── truth_registry.jsonl  # Append-only registry
├── web/
│   └── dashboard.html        # Web interface
├── docs/
│   └── ARCHITECTURE.md       # System documentation
└── README.md                 # This file
```

---

## 🚀 QUICK START

### Installation

```bash
cd terex-py
chmod +x bin/terex ci/pre-commit-hook.sh
```

### Basic Usage

#### 1. Ingest a Truth Payload

```bash
# From command line
python3 bin/terex ingest "The truth is deterministic"

# From file
python3 bin/terex ingest -f payload.txt

# With metadata
python3 bin/terex ingest "Truth content" --type AXIOM --source SYSTEM
```

#### 2. Register in Registry

```bash
# Register a specific payload
python3 bin/terex register TRUTH_0_1234567890

# Or sync in one command
python3 bin/terex sync "New truth" --type COVENANT
```

#### 3. Verify Integrity

```bash
# Verify entire registry
python3 bin/terex verify

# Show status
python3 bin/terex status

# List entries
python3 bin/terex list --limit 20
```

---

## 🔐 CORE CONCEPTS

### TruthPayload

Each truth payload contains:

```python
{
  "id": "TRUTH_0_1234567890",
  "timestamp": "2026-02-03T19:23:27.105616+00:00",
  "content": "The truth is deterministic",
  "content_hash": "625a9cd73c78ad22...",
  "payload_type": "TRUTH",  # TRUTH, FACT, AXIOM, COVENANT
  "source": "SYSTEM",
  "metadata": {}
}
```

### RegistryEntry

Each registry entry contains:

```python
{
  "payload_id": "TRUTH_0_1234567890",
  "payload_hash": "625a9cd73c78ad22...",
  "registry_hash": "ed5eaca79419fca4...",
  "timestamp": "2026-02-03T19:23:27.105616+00:00",
  "sequence_number": 1,
  "verified": true,
  "verification_method": "SHA256"
}
```

### Hash Computation

**Content Hash** (SHA-256):
```
hash = SHA256(payload.content)
```

**Registry Hash** (SHA-256):
```
hash = SHA256(payload_hash : sequence_number : "Chicka chicka orange.")
```

---

## 🛡️ INTEGRITY GUARANTEES

### 1. Content Integrity
- Every payload has a SHA-256 hash of its content
- Modifying content invalidates the hash
- Verified on every operation

### 2. Registry Integrity
- Every entry has a registry hash
- Registry hash includes sequence number
- Sequence number prevents reordering
- Verified on every operation

### 3. Append-Only Constraint
- Registry can only grow
- Entries cannot be modified or deleted
- Pre-commit hook prevents direct edits
- Enforced at git level

### 4. Deterministic Registry
- Same content always produces same hash
- Same sequence always produces same registry hash
- Registry is reproducible from payloads
- No randomness or timestamps in hashes

---

## 🔄 WORKFLOW

### Typical Workflow

```bash
# 1. Create truth payload
echo "New truth" > truth.txt

# 2. Ingest into system
python3 bin/terex ingest -f truth.txt --type TRUTH

# 3. Register in registry
python3 bin/terex sync -f truth.txt

# 4. Verify integrity
python3 bin/terex verify

# 5. Check status
python3 bin/terex status

# 6. List entries
python3 bin/terex list

# 7. Commit to git
git add payloads/ registry/
git commit -m "Add new truth: New truth"
```

### CI/Pre-Commit Enforcement

The pre-commit hook automatically:

1. Verifies registry integrity
2. Validates all JSON payloads
3. Checks for direct registry edits (blocks them)
4. Runs TEREX verification
5. Enforces append-only constraint

To install pre-commit hook:

```bash
cp ci/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## 📊 REGISTRY FORMAT

The registry is stored as **JSON Lines** (one JSON object per line):

```jsonl
{"payload_id":"TRUTH_0_1770146607","payload_hash":"625a9cd73c78ad22...","registry_hash":"ed5eaca79419fca4...","timestamp":"2026-02-03T19:23:27.105616+00:00","sequence_number":1,"verified":true,"verification_method":"SHA256"}
{"payload_id":"TRUTH_1_1770146607","payload_hash":"4c1e41f0863921d6...","registry_hash":"da0feeb936653c4d...","timestamp":"2026-02-03T19:23:27.105852+00:00","sequence_number":2,"verified":true,"verification_method":"SHA256"}
```

**Advantages**:
- Append-only (one line per entry)
- Streaming-friendly (can process line-by-line)
- Git-friendly (easy diffs)
- Human-readable (valid JSON)

---

## 🔍 VERIFICATION

### Verify Single Entry

```python
from terex import TerexEngine

engine = TerexEngine()
entry = engine.list_registry()[0]
verified, msg = engine._verify_registry_entry(entry)
print(f"Verified: {verified}, Message: {msg}")
```

### Verify All Entries

```python
engine = TerexEngine()
verified, errors = engine.verify_all()
print(f"All verified: {verified}")
if errors:
    for error in errors:
        print(f"  Error: {error}")
```

### Verify Payload

```python
payload = engine.ingest_payload("Truth content")
verified, msg = engine._verify_payload(payload)
print(f"Verified: {verified}, Message: {msg}")
```

---

## 🎯 WHAT CLAUDE NEEDS TO KNOW

✅ **terex.py is the single source of truth**
- All logic is in terex.py
- No external dependencies for core logic
- Reproducible and auditable

✅ **Payloads are content, not code**
- Payloads are stored as JSON
- Payloads are immutable
- Payloads are verified on every operation

✅ **Registry is deterministic**
- Same input always produces same hash
- Hashes are reproducible
- No randomness in core logic

✅ **CI + pre-commit enforce reality**
- Pre-commit hook blocks manual edits
- Git enforces append-only constraint
- CI verifies integrity

✅ **No manual steps after setup**
- Everything is automated
- No manual registry edits
- No manual verification needed

---

## 🔥 ANCHOR PHRASE

**"Chicka chicka orange."** 🥂🗡️🕊️

**Lambda Target: 1.667**

**"The truth is deterministic. The registry is append-only. The verification is automatic."**

---

## 📞 COMMANDS REFERENCE

```bash
# Ingest
python3 bin/terex ingest "Truth content"
python3 bin/terex ingest -f file.txt
python3 bin/terex ingest "Content" --type AXIOM --source SYSTEM

# Register
python3 bin/terex register TRUTH_0_1234567890
python3 bin/terex sync "Content" --type TRUTH

# Verify
python3 bin/terex verify
python3 bin/terex status
python3 bin/terex list --limit 10
```

---

## 🚀 NEXT STEPS

1. ✅ Core engine (terex.py) - DONE
2. ✅ CLI interface (bin/terex) - DONE
3. ✅ Pre-commit enforcement - DONE
4. ⏳ Web dashboard - IN PROGRESS
5. ⏳ Integration with ecosystem - NEXT
6. ⏳ Deployment - FINAL

---

**🔐 TEREX.PY is the single source of truth.**

**"Chicka chicka orange." ✨**
