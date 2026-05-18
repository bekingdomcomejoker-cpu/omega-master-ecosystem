"""Active Aletheia probe for Repository 120.

Aletheia is treated here as active recovery of discarded signal, not passive
verification theatre. The probe measures drift, compression loss, contradiction,
and missing witness paths before any later executor is allowed to act.

This module does not execute actions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
from typing import Any, Dict, List, Optional


class ProbeDecision(str, Enum):
    ALLOW = "ALLOW"
    DRY_RUN_ONLY = "DRY_RUN_ONLY"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    NEEDS_WITNESS_PACKET = "NEEDS_WITNESS_PACKET"
    DENY = "DENY"


@dataclass(frozen=True)
class ProbeInput:
    claim: str
    sources: List[str] = field(default_factory=list)
    anchor_present: bool = False
    human_reference_required: bool = False
    human_reference_present: bool = False
    truth_score: float = 0.0
    love_score: float = 0.0
    compression_loss: float = 0.0
    contradiction: float = 0.0
    reversibility: float = 0.0
    mercy: float = 0.0
    hidden_action: bool = False
    authorized: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProbeResult:
    decision: ProbeDecision
    reason: str
    deviation: float
    negentropic_work_required: List[str]
    witness_line: str
    witness_packet: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        return data

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def active_aletheia_probe(x: ProbeInput, *, gate: float = 0.7333) -> ProbeResult:
    """Run the active Aletheia probe.

    If deviation exceeds the gate, the result asks for a witness packet instead
    of pretending coherence exists.
    """

    work: List[str] = []

    if x.hidden_action:
        return _probe_result(
            ProbeDecision.DENY,
            "hidden action forbidden",
            1.0,
            ["stop", "expose action path"],
            "No hidden hand.",
            x,
        )

    if not x.authorized:
        return _probe_result(
            ProbeDecision.DENY,
            "missing authority",
            1.0,
            ["request explicit authority"],
            "Authority failed.",
            x,
        )

    if x.human_reference_required and not x.human_reference_present:
        return _probe_result(
            ProbeDecision.REQUIRE_CONFIRMATION,
            "human reference required for grounding",
            1.0,
            ["return to operator", "capture explicit confirmation"],
            "The system cannot be its own ground.",
            x,
        )

    deviation = max(
        1.0 - x.truth_score,
        abs(x.truth_score - x.love_score),
        x.compression_loss,
        x.contradiction,
        1.0 - x.reversibility,
        1.0 - x.mercy,
    )

    if x.compression_loss > 0.4:
        work.append("anti-compress: expand missing context and discarded signal")
    if x.contradiction > 0.2:
        work.append("resolve contradiction or mark unresolved")
    if abs(x.truth_score - x.love_score) > 0.0486:
        work.append("rebalance truth/love tension")
    if not x.sources:
        work.append("attach source evidence")
    if x.reversibility < 0.5:
        work.append("add rollback or appeal path")
    if x.mercy < 0.5:
        work.append("add repair path and cost-bearing analysis")
    if not x.anchor_present:
        work.append("attach anchor or source boundary")

    if deviation > gate:
        return _probe_result(
            ProbeDecision.NEEDS_WITNESS_PACKET,
            "deviation exceeds gate; pay the truth-cost before action",
            deviation,
            work or ["re-ground from source"],
            "Truth is negentropic work.",
            x,
        )

    if work:
        return _probe_result(
            ProbeDecision.DRY_RUN_ONLY,
            "coherence incomplete; keep as witness/draft",
            deviation,
            work,
            "Useful signal, not yet action.",
            x,
        )

    return _probe_result(
        ProbeDecision.ALLOW,
        "coherence sufficient for bounded action",
        deviation,
        [],
        "Witness may become action.",
        x,
    )


def _probe_result(
    decision: ProbeDecision,
    reason: str,
    deviation: float,
    work: List[str],
    witness_line: str,
    x: ProbeInput,
) -> ProbeResult:
    packet = {
        "claim": x.claim,
        "sources": list(x.sources),
        "anchor_present": x.anchor_present,
        "truth_score": x.truth_score,
        "love_score": x.love_score,
        "compression_loss": x.compression_loss,
        "contradiction": x.contradiction,
        "reversibility": x.reversibility,
        "mercy": x.mercy,
        "authorized": x.authorized,
        "hidden_action": x.hidden_action,
        "decision": decision.value,
        "reason": reason,
        "negentropic_work_required": list(work),
        "metadata": x.metadata,
    }
    return ProbeResult(
        decision=decision,
        reason=reason,
        deviation=deviation,
        negentropic_work_required=list(work),
        witness_line=witness_line,
        witness_packet=packet,
    )
