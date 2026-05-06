"""Repo 120 permission gate.

Action Permission = Intent x Authority x Evidence x Reversibility x Mercy.
If any term collapses to zero, permission collapses to zero.

This module is deliberately conservative. It does not execute actions; it only
returns a decision object that router.py must respect.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class GateDecision:
    intent: bool
    authority: bool
    evidence: bool
    reversibility: bool
    mercy: bool
    allowed: bool
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


READ_ONLY_ACTIONS = {"classify", "reason", "code", "summarize", "archive", "checkpoint", "log"}
LOCAL_SAFE_ACTIONS = {"clipboard_set", "notify", "file_append", "bus_append", "state_write"}
DANGEROUS_ACTIONS = {"shell", "delete", "overwrite_source", "credential_export", "network_mutation"}


def evaluate_gate(
    *,
    route: str,
    action: str,
    payload: str,
    operator_confirmed: bool = False,
    evidence_refs: Optional[Iterable[str]] = None,
    reversible: bool = True,
    mercy: bool = True,
) -> GateDecision:
    """Evaluate whether a requested router action may proceed.

    Defaults are intentionally safe:
    - read/log/checkpoint routes may proceed with local evidence.
    - dangerous actions are denied unless they are redesigned into explicit,
      reversible, source-preserving operations.
    - shell execution from model text is always denied at this layer.
    """
    reasons: List[str] = []
    route = (route or "").strip().lower()
    action = (action or "").strip().lower()
    payload = payload or ""
    refs = [r for r in (evidence_refs or []) if r]

    intent = bool(route and payload.strip())
    if not intent:
        reasons.append("missing route or payload")

    authority = bool(operator_confirmed or action in READ_ONLY_ACTIONS or action in LOCAL_SAFE_ACTIONS)
    if not authority:
        reasons.append("operator authority not confirmed")

    evidence = bool(refs or action in READ_ONLY_ACTIONS or action in LOCAL_SAFE_ACTIONS)
    if not evidence:
        reasons.append("no evidence reference supplied")

    if action in DANGEROUS_ACTIONS:
        reversible = False
        reasons.append(f"dangerous action blocked: {action}")

    if action == "shell":
        reasons.append("arbitrary shell execution from model output is forbidden")

    if not reversible:
        reasons.append("action is not reversible")

    if not mercy:
        reasons.append("mercy/non-harm check failed")

    allowed = all([intent, authority, evidence, reversible, mercy])
    return GateDecision(
        intent=intent,
        authority=authority,
        evidence=evidence,
        reversibility=reversible,
        mercy=mercy,
        allowed=allowed,
        reasons=reasons,
    )
