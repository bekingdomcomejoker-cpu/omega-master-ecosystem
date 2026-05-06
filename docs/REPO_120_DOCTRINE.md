# Repo 120 Doctrine — Omega Federation Angel Engine

## Core Identity

Repo 120 is the conscience before the hand.

It is not an autonomous executor. It is not a bypass engine. It is not a hidden authority layer. It is the gate that decides whether a proposed action has enough intent, authority, evidence, reversibility, and mercy to proceed.

## Core Equation

```text
Action Permission = Intent × Authority × Evidence × Reversibility × Mercy
```

If any term collapses to zero, permission collapses to zero.

## Runtime Roles

| Layer | Role |
|---|---|
| `router.py` | dispatches events into routes |
| `permission_gate.py` | evaluates whether a route/action may proceed |
| `audit_log.py` | records decisions with hash-chained audit events |
| `skill_registry.py` | records skill state and operator-authorized promotion |
| JSONL bus | preserves runtime trace |
| Termux / Huawei | active local body |
| Drive / Dropbox / Mem | canon, archive, witness |

## Quarantine Rule

```text
quarantine ≠ permanent prohibition
quarantine = not implicitly trusted
```

```text
Quarantine blocks automatic execution,
not operator-authorized promotion.
```

A quarantined package may be inspected, summarized, hashed, manifested, and preserved. It may not execute automatically. The operator may promote it, but promotion must be explicit and recorded in the audit log.

## Skill States

| State | Meaning |
|---|---|
| `QUARANTINED` | preserved but not trusted |
| `CANDIDATE` | low-risk package suitable for adapter review |
| `REVIEW_REQUIRED` | potentially useful but requires manual review |
| `BLOCKED` | not callable by default; may only move by explicit override |
| `ENABLED_READONLY` | callable only for non-mutating actions |
| `ENABLED_PRIVILEGED` | callable with declared privileged actions and audit trail |
| `DISABLED` | intentionally unavailable |

## Safety Boundary

Repo 120 should deny by default when the request lacks:

- clear intent
- operator or system authority
- evidence references
- reversibility
- mercy / non-harm alignment

The default implementation blocks arbitrary shell execution, credential export, source mutation, deletion, and unsafe network mutation.

## Operator Sovereignty

The operator can authorize promotion, including privileged promotion. The system must not pretend quarantine is a permanent legal guardian. The system must record the promotion and the reason.

## Audit Standard

Every promotion, denial, or privileged decision should create an audit event containing:

- actor
- event type
- subject
- decision
- reason
- payload
- previous hash
- event hash

This creates a basic tamper-evident chain and supports later reconstruction.

## Current Implementation Status

Implemented:

- permission gate
- audit log with hash chaining
- skill registry and promotion model
- unit tests for gate, audit, and registry

Pending:

- CI workflow
- CLI commands for registry and audit verification
- bridge from Huawei runtime back into repo package layout
- adapter contract v1
- RouterOS ingress relay
- Drive/Mem/Dropbox checkpoint adapters

## Final Line

Repo 120 is not the hand. It is the conscience before the hand.
