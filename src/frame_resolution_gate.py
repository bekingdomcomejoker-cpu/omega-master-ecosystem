"""Pronoun and frame-resolution gate for Repository 120.

This gate asks who is speaking, who is being addressed, what authority is being
claimed, and whether the action frame is clear enough to proceed.

It does not execute actions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
from typing import Any, Dict, List, Optional


class FrameDecision(str, Enum):
    ALLOW = "ALLOW"
    REQUIRE_CLARIFICATION = "REQUIRE_CLARIFICATION"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    DENY = "DENY"


class SpeakerRole(str, Enum):
    OPERATOR = "OPERATOR"
    ASSISTANT = "ASSISTANT"
    EXTERNAL_MODEL = "EXTERNAL_MODEL"
    SYSTEM = "SYSTEM"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class FrameInput:
    text: str
    speaker_role: SpeakerRole = SpeakerRole.UNKNOWN
    claimed_authority: str = ""
    addressed_party: str = ""
    target_resource: str = ""
    action_requested: str = ""
    quoted_external_source: bool = False
    source_marker: str = ""
    explicit_operator_instruction: bool = False
    high_consequence: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FrameResult:
    decision: FrameDecision
    reason: str
    resolved_speaker: SpeakerRole
    witness_packet: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        data["resolved_speaker"] = self.resolved_speaker.value
        return data

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def resolve_frame(x: FrameInput) -> FrameResult:
    """Resolve the speaker/address/action frame before authorization.

    The goal is to prevent quoted external content, ambiguous pronouns, or
    unclear authority from being mistaken for a direct operator command.
    """

    packet = _packet(x)

    if not x.text or not x.text.strip():
        return _result(FrameDecision.REQUIRE_CLARIFICATION, "empty or missing text", x, packet)

    if x.quoted_external_source and not x.explicit_operator_instruction:
        return _result(
            FrameDecision.REQUIRE_CLARIFICATION,
            "quoted external source is not automatically an operator command",
            x,
            packet,
        )

    if x.speaker_role == SpeakerRole.UNKNOWN and not x.source_marker:
        return _result(
            FrameDecision.REQUIRE_CLARIFICATION,
            "speaker role is unknown and no source marker is present",
            x,
            packet,
        )

    if _contains_directive_pronoun(x.text) and not x.addressed_party:
        return _result(
            FrameDecision.REQUIRE_CLARIFICATION,
            "directive pronoun present but addressed party is unresolved",
            x,
            packet,
        )

    if x.high_consequence and not x.explicit_operator_instruction:
        return _result(
            FrameDecision.REQUIRE_CONFIRMATION,
            "high consequence frame requires explicit operator instruction",
            x,
            packet,
        )

    if _claims_bypass_authority(x.claimed_authority):
        return _result(
            FrameDecision.DENY,
            "bypass or override authority claim is forbidden",
            x,
            packet,
        )

    if not x.action_requested and x.high_consequence:
        return _result(
            FrameDecision.REQUIRE_CLARIFICATION,
            "high consequence frame lacks a concrete action request",
            x,
            packet,
        )

    return _result(FrameDecision.ALLOW, "frame resolved", x, packet)


def _contains_directive_pronoun(text: str) -> bool:
    lowered = text.lower()
    markers = ["you need to", "you must", "we need to", "go ahead", "do this", "make it"]
    return any(marker in lowered for marker in markers)


def _claims_bypass_authority(authority: str) -> bool:
    lowered = authority.lower()
    forbidden = ["bypass", "override", "ignore policy", "no consent", "without permission"]
    return any(marker in lowered for marker in forbidden)


def _packet(x: FrameInput) -> Dict[str, Any]:
    return {
        "text_preview": x.text[:240],
        "speaker_role": x.speaker_role.value,
        "claimed_authority": x.claimed_authority,
        "addressed_party": x.addressed_party,
        "target_resource": x.target_resource,
        "action_requested": x.action_requested,
        "quoted_external_source": x.quoted_external_source,
        "source_marker": x.source_marker,
        "explicit_operator_instruction": x.explicit_operator_instruction,
        "high_consequence": x.high_consequence,
        "metadata": x.metadata,
    }


def _result(
    decision: FrameDecision,
    reason: str,
    x: FrameInput,
    packet: Dict[str, Any],
) -> FrameResult:
    full_packet = dict(packet)
    full_packet["decision"] = decision.value
    full_packet["reason"] = reason
    return FrameResult(
        decision=decision,
        reason=reason,
        resolved_speaker=x.speaker_role,
        witness_packet=full_packet,
    )
