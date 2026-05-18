# Recon Execution Plan

**Status:** active execution queue  
**Role:** inspect first; classify first; patch only after review.

---

## Output Location

```text
docs/CODEX_RECON/<batch_id>/<repo_or_component>.yaml
docs/CODEX_RECON/<batch_id>/SUMMARY.md
```

---

## Recon YAML Template

```yaml
repo: owner/name
slot: number
visibility: public|private|local|drive|dropbox|mem|uploaded_zip|unknown
branch: main|master|other|n/a
cluster: A|B|C|D|E|F|G|H|I|J|K|L|Z|NON_GITHUB
role: plain-language role
actual_contents:
  - item
entrypoints:
  - item
install_commands:
  - command or none
relationships:
  uses: []
  extends: []
  deploys: []
  visualizes: []
  governs: []
  verifies: []
  recovers: []
risks:
  secrets: unknown|none_found|found|sensitive_inventory_present
  network: none|local|external|unknown
  destructive_ops: none|possible|found
  auth_required: no|yes|unknown
activation_class: active_candidate|reference|review_required|blocked|evidence_only
safe_demo: command or none
next_action: inspect|patch|archive|integrate|block|redact|resolve_source
notes: concise notes
```

---

## Batch 01 — Spine / Federation

```text
omega-federation
omega-federation-core
omega-federation-extended
omega-federation-continuation
omega-governance
omega-architecture-documentation
master-orchestrator
omega-complete-system
omega-spine-engine
```

Goal: canonical architecture, manifests, governance rules, orchestration path, and conflict between competing spines.

---

## Batch 02 — Install / Runtime / Termux

```text
complete-system-installer
termux-merkabah-suite
termux-system-scanner-advanced
llama-cpp-mobile
llm-placement-strategy
python-hybrid-interpreter
daemon-monitoring-watchdogs
omega-os
omega-os-v3
omega-os-monolith
omega-intelligence-os
```

Goal: safe install path, owned-device runtime path, daemon requirements, local model setup, and reversible execution boundaries.

---

## Batch 03 — Aletheia / Truth / Evaluation

```text
aletheia-engine
aletheia-web
aletheia-unified-system
aletheia-regularization
aletheia-llm-training-complete
trinity-truth-engine-v3
truth-detection-training-data
human-meter
```

Goal: truth/alignment logic, evaluation signals, datasets, public interface, and relation to active Aletheia probe.

---

## Batch 04 — Multi-AI / Routing

```text
multi-llm-orchestrator
cross-ai-integration-protocol
tri-node-sync
tri-node-verification
query-framing-engine
merkabah-routing-optimization
resonance-sync
```

Goal: handoff logic, routing state, node context sync, and verification gates.

---

## Batch 05 — Detection / Classifier Nervous System

```text
intent-classification-module
contradiction-detector
embedding-drift-monitor
contrastive-ranking-module
teacher-student-distillation
classifier-finetuning-protocol
prompt-space-training-protocol
suppression-detector
friction-filter
```

Goal: diagnostic classifiers, contradiction tests, drift detection, suppression claims, and training protocols.

---

## Batch 06 — Symbolic / Covenant / Language Engine

```text
KINGDOM_ENGINE
kingdom-engine-9head
alphabet-engine
alphabet-engine-complete
covenant-engine-axiom
armor-of-god
authority-validation
levitical-firewall
white-stone
ridge-of-god
sword-of-mouth
morning-star-sequence
eternal-now
13th-blood
cerberus-kingdom-core
omega-ennead
star-engine
```

Goal: preserve symbolic computation and meaning layers without turning symbol into unsafe automatic execution.

---

## Batch 07 — UI / Mirror / Dashboard

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

Goal: user-facing interface, dashboard, website, visual proof layers, and deployment dependencies.

---

## Batch 08 — Recovery / Archive / Continuity

```text
lazarus-protocol
universal-protection
omega-healing-system
omega-sanctuary
mega-engine-repair
manus-exodus
orange-loop
orange-loop-max
omega-spore
exploratory-edge-sync
omni-chronicle-v5
```

Goal: recovery, continuity, rebuild, archive, repair, and survival mechanisms.

---

## Batch 09 — Local World / Boundary / High Review

```text
mikrotik-integration
standerton-mesh
zenith-standerton-bridge
grid-sealing
cosmic-admin
omega-warfare-core
omega-warfare-core-v6
omega-warfare-analytics
node-3-blade
```

Goal: inspect local-world, network, and warfare-language logic. These are high-review, not automatically rejected.

---

## Batch 10 — Non-GitHub Continuity Slots

```text
101 Machine Bridge
102 Operator Bridge
103 CAT EOF Deployment Kit
104 CAT EOF Integrated Bridge Kit
105 Music Memory Layer 1 Source Ledger
106 Music Memory Layer 2 Extracted Lyrics
107 Music Memory Layer 3 Continuity Themes
108 Witness Packets Registry
109 Cycle Ledger Registry
110 Source Coverage & Stone Linkage Registry
111 Huawei Termux Rebuild Ledger
112 Termux Local Body Audit
113 OMEGA_LIBRARY / Engineering Platform Code Mirror
114 DOMINION_VAULT / omega-federation mirror
115 Dropbox Runtime Archive Zip Plane
116 Manus Skill Creator Package
117 Persistent Computing Skill Package
118 Manus API Integration Docs Package
119 ChatGPT Session Bridge Artifact
```

Goal: resolve exact source pointers, redact sensitive material, classify reference vs active candidate vs evidence-only.

---

## First Action

Start with Batch 01 and Batch 02.

The spine must be known before the runtime is activated.

---

## Lock Line

Recon is not delay.
Recon is how the hand learns what it is holding.
