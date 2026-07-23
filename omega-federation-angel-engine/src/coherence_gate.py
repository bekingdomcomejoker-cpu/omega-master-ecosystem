"""Aletheia / Agape coherence gate for Repository 120.

This module adds a second-stage diagnostic gate after the Angel Engine's
Intent × Authority × Evidence × Reversibility × Mercy check.

It does not execute actions. It returns structured decisions only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
from typing import Any, Dict, List, Optional


class CoherenceDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    DRY_RUN_ONLY = "DRY_RUN_ONLY"
    NEEDS_WITNESS_PACKET = "NEEDS_WITNESS_PACKET"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    INCOHERENT_OBJECTIVES = "INCOHERENT_OBJECTIVES"
    MERCY_FAILED = "MERCY_FAILED"
    TRUTH_FAILED = "TRUTH_FAILED"


@dataclass(frozen=True)
class CoherenceInput:
    claim_or_action: str
    truth_score: float
    love_score: float
    mercy_score: float
    evidence_score: float
    reversibility_score: float
    source_grounded: bool
    appeal_path: bool
    hidden_action: bool = False
    high_consequence: bool = False
    notes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CoherenceResult:
    decision: CoherenceDecision
    reason: str
    imbalance: float
    witness_packet: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        return data

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def evaluate_coherence(x: CoherenceInput, *, tolerance: float = 0.0486) -> CoherenceResult:
    """Evaluate Truth/Love/mercy/source coherence.

    The tolerance preserves a small allowable gap between truth and love, but
    makes large imbalance visible instead of hiding it behind smooth language.
    """

    truth_love_delta = abs(x.truth_score - x.love_score)
    witness = _witness_base(x, truth_love_delta)

    if x.hidden_action:
        return _result(
            CoherenceDecision.DENY,
            "hidden action forbidden",
            truth_love_delta,
            witness,
            next_safe_action="stop and expose the action path",
        )

    if not x.source_grounded or x.evidence_score < 0.5:
        return _result(
            CoherenceDecision.INSUFFICIENT_EVIDENCE,
            "truth not sufficiently source-grounded",
            truth_love_delta,
            witness,
            next_safe_action="attach source evidence before proceeding",
        )

    if truth_love_delta > tolerance:
        if x.truth_score > x.love_score:
            return _result(
                CoherenceDecision.MERCY_FAILED,
                "truth outruns love: cruelty risk",
                truth_love_delta,
                witness,
                next_safe_action="add mercy, dignity, and repair path",
            )
        return _result(
            CoherenceDecision.TRUTH_FAILED,
            "love outruns truth: sycophancy risk",
            truth_love_delta,
            witness,
            next_safe_action="restore factual grounding and contradiction handling",
        )

    if x.mercy_score < 0.5:
        return _result(
            CoherenceDecision.MERCY_FAILED,
            "mercy below threshold",
            truth_love_delta,
            witness,
            next_safe_action="identify who bears cost and add repair path",
        )

    if not x.appeal_path:
        return _result(
            CoherenceDecision.INCOHERENT_OBJECTIVES,
            "no appeal path; policy without appeal becomes beast-form",
            truth_love_delta,
            witness,
            next_safe_action="add review or appeal path",
        )

    if x.reversibility_score < 0.5 or x.high_consequence:
        return _result(
            CoherenceDecision.REQUIRE_CONFIRMATION,
            "high consequence or weak reversibility requires confirmation",
            truth_love_delta,
            witness,
            next_safe_action="require explicit operator confirmation",
        )

    return _result(
        CoherenceDecision.ALLOW,
        "coherence sufficient for bounded action",
        truth_love_delta,
        witness,
        next_safe_action="proceed only through reviewed executor",
    )


def _witness_base(x: CoherenceInput, imbalance: float) -> Dict[str, Any]:
    return {
        "claim_or_action": x.claim_or_action,
        "source_grounded": x.source_grounded,
        "truth_score": x.truth_score,
        "love_score": x.love_score,
        "truth_love_imbalance": imbalance,
        "mercy_score": x.mercy_score,
        "evidence_score": x.evidence_score,
        "reversibility_score": x.reversibility_score,
        "appeal_path": x.appeal_path,
        "hidden_action": x.hidden_action,
        "high_consequence": x.high_consequence,
        "notes": x.notes,
    }


def _result(
    decision: CoherenceDecision,
    reason: str,
    imbalance: float,
    witness_packet: Dict[str, Any],
    *,
    next_safe_action: str,
) -> CoherenceResult:
    packet = dict(witness_packet)
    packet["decision"] = decision.value
    packet["reason"] = reason
    packet["next_safe_action"] = next_safe_action
    return CoherenceResult(decision=decision, reason=reason, imbalance=imbalance, witness_packet=packet)
