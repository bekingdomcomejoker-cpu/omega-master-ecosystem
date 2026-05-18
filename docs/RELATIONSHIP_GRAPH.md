# Relationship Graph

**Status:** active graph  
**Role:** show how Repo 120 relates to the estate, planes, gates, and witness routes.

---

## Plane Graph

```mermaid
graph TD
  OP[Operator / Dominique] --> DRIVE[Google Drive: working canon]
  OP --> TERMUX[Termux / Huawei local body]
  OP --> GITHUB[GitHub: versioned law/code/spec]

  DRIVE --> MEM[Mem: continuity witness]
  DRIVE --> DROPBOX[Dropbox: sealed archive/package layer]
  DRIVE --> GITHUB
  MEM --> DRIVE
  DROPBOX --> DRIVE
  TERMUX --> DRIVE
  TERMUX --> GITHUB

  GITHUB --> R001_100[Slots 001-100: visible GitHub repo estate]
  DRIVE --> R101_119[Slots 101-119: continuity/archive/runtime components]
  GITHUB --> R120[Slot 120: omega-federation-angel-engine]

  R001_100 --> CLUSTERS[Clusters A-L + Z]
  R101_119 --> BRIDGE[Bridge/runtime/source artifacts]
  CLUSTERS --> R120
  BRIDGE --> R120

  R120 --> GATE[Angel Engine Gate]
  GATE --> WILL[Action Permission]
  WILL --> INTENT[Intent]
  WILL --> AUTH[Authority]
  WILL --> EVID[Evidence]
  WILL --> REV[Reversibility]
  WILL --> MERCY[Mercy]

  GATE --> ALET[Aletheia / Agape Coherence]
  ALET --> TRUTH[Truth Check]
  ALET --> LOVE[Love Check]
  ALET --> FRAME[Pronoun / Frame Resolution]
  ALET --> WITNESS[Witness Packet]

  GATE --> DECIDE{Decision}
  DECIDE --> ALLOW[ALLOW]
  DECIDE --> DRY[DRY_RUN_ONLY]
  DECIDE --> CONFIRM[REQUIRE_CONFIRMATION]
  DECIDE --> BLOCK[DENY / BLOCK]

  ALLOW --> LOG[Log / Bus / Checkpoint]
  DRY --> LOG
  CONFIRM --> OP
  BLOCK --> LOG
```

---

## Cluster Graph

```mermaid
graph LR
  A[Core Federation / Spine] --> R120[Repo 120]
  B[Aletheia / Truth / Alignment] --> R120
  C[Omnissiah / Deployment / Dashboard] --> R120
  D[Termux / Local Runtime] --> R120
  E[Multi-LLM / Routing] --> R120
  F[Detection / Classifiers / Evaluation] --> R120
  G[Symbolic / Covenant / Theological] --> R120
  H[Interfaces / Mirrors / Visual Systems] --> R120
  I[Recovery / Protection / Healing] --> R120
  J[Governance / Boundary / Local World] --> R120
  K[Identity / Personal System / Training] --> R120
  L[Stress Testing / Warfare Language] --> R120
  Z[Unclassified Review] --> R120
```

---

## Relationship Edge Types

```text
USES
EXTENDS
DEPLOYS
VISUALIZES
GOVERNS
TRAINS
VERIFIES
RECOVERS
ARCHIVES
REFERENCES
BLOCKED_UNTIL_REVIEW
```

---

## Critical Edges

```text
omega-federation GOVERNS repository estate
omega-federation-angel-engine GOVERNS action authorization
aletheia-engine VERIFIES truth/alignment claims
authority-validation FEEDS angel-engine authorization
levitical-firewall GOVERNS boundary posture
termux-merkabah-suite INSTALLS local runtime
complete-system-installer INSTALLS active candidates
llama-cpp-mobile ENABLES local model runtime
daemon-monitoring-watchdogs MONITORS local services
cross-ai-integration-protocol ROUTES external node handoff
tri-node-sync SYNCS node state
tri-node-verification VERIFIES node state
contradiction-detector VERIFIES claims
embedding-drift-monitor DETECTS drift
suppression-detector FLAGS high-review suppression claims
friction-filter FILTERS contested output
lazarus-protocol RECOVERS collapsed state
omega-sanctuary RECOVERS protected continuity
orange-loop REFERENCES recovery/protection loop
Machine Bridge ROUTES model invocation
Operator Bridge RECONSTRUCTS operator continuity
CAT EOF ROUTES local script/bus pattern
Witness Packets Registry ARCHIVES truth/drift/recovery packets
Cycle Ledger Registry ARCHIVES cycle outcomes
Termux Local Body Audit VERIFIES local source body
OMEGA_LIBRARY ARCHIVES engineering code mirror
DOMINION_VAULT ARCHIVES omega-federation local mirror
Dropbox Runtime Archive Zip Plane ARCHIVES sealed runtime packages
Manus Skill Creator Package REFERENCES skill packaging pattern
Persistent Computing Skill Package REFERENCES future persistence layer
Manus API Integration Docs Package REFERENCES future API integration
ChatGPT Session Bridge Artifact ARCHIVES unsafe evidence only
```

---

## Lock Line

Repo 120 is not the pile.
Repo 120 is the conscience that names the pile before the hand touches it.
