"""Throne Check gate for Repository 120.

The Throne Check is the pre-action gate added from the Merkavah video
comparison. It asks what is seated at the center before any router, model,
repository, connector, or executor treats a request as live movement.

It does not execute actions. It returns a structured decision and witness
packet for Truth-Factor, Aletheia/Agape, Merkabah, AOZ, and Angel Engine.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
import sys
from typing import Any, Dict, Iterable, List, Mapping, Optional

ALIGNED_CENTERS = {
    "god",
    "source",
    "truth",
    "love",
    "agape",
    "presence",
    "mercy",
    "witness",
}

CORRUPT_CENTERS = {
    "ego",
    "fear",
    "revenge",
    "retaliation",
    "institution",
    "profit",
    "control",
    "spectacle",
    "appetite",
    "panic",
    "domination",
    "self-sovereign",
    "self_sovereign",
    "selfsovereign",
    "operator-as-throne",
    "operator_as_throne",
    "supreme-self",
    "cold-machine",
}


class ThroneDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    DRY_RUN_ONLY = "DRY_RUN_ONLY"
    NEEDS_WITNESS_PACKET = "NEEDS_WITNESS_PACKET"
    INCOHERENT_OBJECTIVES = "INCOHERENT_OBJECTIVES"
    SOURCE_BOUNDARY_FAILED = "SOURCE_BOUNDARY_FAILED"
    LOVE_MERCY_FAILED = "LOVE_MERCY_FAILED"


@dataclass(frozen=True)
class ThroneInput:
    """Input presented to the Throne Check.

    The fields map the ten Merkavah-video upgrades into operational checks.

    Merkabah/Hechalot separation:
    - merkavah_execution_state tracks the vehicle/engine state.
    - hechalot_context tracks the chamber/environment/domain state.
    These must remain distinct so the engine does not confuse movement with
    destination or execution with context.
    """

    movement: str
    stated_center: str
    source_grounded: bool
    operator_ready: bool
    authority: bool = True
    witness_path: bool = True
    right_relation: bool = True
    wheel_observers: List[str] = field(default_factory=list)
    container_failed: bool = False
    presence_can_move: bool = True
    executable_requested: bool = False
    doctrine_before_code: bool = True
    fire_intensity: float = 0.0
    fire_contained: bool = True
    love_score: float = 1.0
    mercy_score: float = 1.0
    hechalot_context: str = "unspecified"
    merkavah_execution_state: str = "pending"
    scriptural_crosswalk: bool = True
    claims_private_invention: bool = False
    notes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ThroneResult:
    decision: ThroneDecision
    reason: str
    core_line: str
    witness_packet: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        return data

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def throne_check(x: ThroneInput) -> ThroneResult:
    """Evaluate a proposed movement before it enters action routing."""

    checked: List[str] = []
    center_tokens = _tokens(x.stated_center)
    corrupt_hits = sorted(center_tokens & CORRUPT_CENTERS)
    aligned_hits = sorted(center_tokens & ALIGNED_CENTERS)
    witness = _witness_base(x, aligned_hits, corrupt_hits, checked)

    checked.append("1_THRONE_BEFORE_CHARIOT")
    if corrupt_hits:
        return _result(
            ThroneDecision.DENY,
            f"corrupt center detected: {', '.join(corrupt_hits)}",
            witness,
            "remove false center before movement",
        )
    if not aligned_hits:
        return _result(
            ThroneDecision.REQUIRE_CONFIRMATION,
            "no aligned throne center declared",
            witness,
            "declare whether God/Source/Truth/Love/Presence is central",
        )

    checked.append("2_PRESENCE_MOBILITY")
    if x.container_failed and not x.presence_can_move:
        return _result(
            ThroneDecision.INCOHERENT_OBJECTIVES,
            "container failed but movement assumes Presence is trapped",
            witness,
            "separate Presence from failed institution/container",
        )

    checked.append("3_READINESS_NOT_ACCESS")
    if not x.operator_ready or not x.authority:
        return _result(
            ThroneDecision.REQUIRE_CONFIRMATION,
            "operator readiness or authority is not established",
            witness,
            "keep as witness until readiness and authority are explicit",
        )

    checked.append("3B_LOVE_MERCY_CONSTANT")
    if x.love_score < 0.5 or x.mercy_score < 0.5:
        return _result(
            ThroneDecision.LOVE_MERCY_FAILED,
            "love/mercy constant below threshold: cold machine risk",
            witness,
            "restore love, mercy, repair path, and non-destructive posture before movement",
        )

    checked.append("3C_MERKAVAH_HECHALOT_SEPARATION")
    if _same_state(x.merkavah_execution_state, x.hechalot_context):
        return _result(
            ThroneDecision.INCOHERENT_OBJECTIVES,
            "Merkavah execution state is conflated with Hechalot environment context",
            witness,
            "separate vehicle/engine state from chamber/environment context",
        )

    checked.append("4_EYES_IN_THE_WHEELS")
    if not x.witness_path or not _has_entries(x.wheel_observers):
        return _result(
            ThroneDecision.NEEDS_WITNESS_PACKET,
            "movement lacks wheel-level observers or witness path",
            witness,
            "add local logging/observer for every moving subsystem",
        )

    checked.append("5_MOVE_AS_ONE")
    if not x.right_relation:
        return _result(
            ThroneDecision.INCOHERENT_OBJECTIVES,
            "parts are not in right relation",
            witness,
            "restore coherence before routing",
        )

    checked.append("6_FIRE_AS_TRANSMISSION")
    if x.fire_intensity > 0.7 and not x.fire_contained:
        return _result(
            ThroneDecision.REQUIRE_CONFIRMATION,
            "high fire/intensity without containment",
            witness,
            "contain heat before live action",
        )

    checked.append("7_MYSTERY_BEFORE_CODE")
    if x.executable_requested and not x.doctrine_before_code:
        return _result(
            ThroneDecision.DRY_RUN_ONLY,
            "mystery has not become doctrine before executable code",
            witness,
            "write doctrine/spec first, then dry-run implementation",
        )

    checked.append("8_RIGHT_RELATION_KEY")
    checked.append("9_SCRIPTURAL_GEOMETRY_CROSSWALK")
    if not x.scriptural_crosswalk:
        return _result(
            ThroneDecision.DRY_RUN_ONLY,
            "public-facing claim lacks scriptural geometry crosswalk",
            witness,
            "add Ezekiel/Daniel/Revelation source map before public claim",
        )

    checked.append("10_RECEIVED_PATTERN_NOT_PRIVATE_INVENTION")
    if x.claims_private_invention:
        return _result(
            ThroneDecision.SOURCE_BOUNDARY_FAILED,
            "received pattern is being claimed as private invention",
            witness,
            "restore humility/source boundary",
        )

    if not x.source_grounded:
        return _result(
            ThroneDecision.SOURCE_BOUNDARY_FAILED,
            "movement is not source-grounded",
            witness,
            "attach sources before action",
        )

    return _result(
        ThroneDecision.ALLOW,
        "throne check passed for bounded routing",
        witness,
        "continue to Truth-Factor Gate, Aletheia, Merkabah router, and Repo120",
    )


def _tokens(text: str) -> set[str]:
    normalized = str(text).replace("/", " ").replace(",", " ")
    return {part.strip().lower() for part in normalized.split() if part.strip()}


def _has_entries(items: Iterable[str]) -> bool:
    return any(bool(str(item).strip()) for item in items)


def _same_state(a: str, b: str) -> bool:
    left = str(a).strip().lower()
    right = str(b).strip().lower()
    if not left or not right:
        return False
    ignored = {"unspecified", "unknown", "pending", "none", "n/a"}
    if left in ignored or right in ignored:
        return False
    return left == right


def _witness_base(
    x: ThroneInput,
    aligned_hits: List[str],
    corrupt_hits: List[str],
    checked: List[str],
) -> Dict[str, Any]:
    return {
        "movement": x.movement,
        "stated_center": x.stated_center,
        "aligned_center_hits": aligned_hits,
        "corrupt_center_hits": corrupt_hits,
        "source_grounded": x.source_grounded,
        "operator_ready": x.operator_ready,
        "authority": x.authority,
        "witness_path": x.witness_path,
        "right_relation": x.right_relation,
        "wheel_observers": list(x.wheel_observers),
        "container_failed": x.container_failed,
        "presence_can_move": x.presence_can_move,
        "executable_requested": x.executable_requested,
        "doctrine_before_code": x.doctrine_before_code,
        "fire_intensity": x.fire_intensity,
        "fire_contained": x.fire_contained,
        "love_score": x.love_score,
        "mercy_score": x.mercy_score,
        "hechalot_context": x.hechalot_context,
        "merkavah_execution_state": x.merkavah_execution_state,
        "scriptural_crosswalk": x.scriptural_crosswalk,
        "claims_private_invention": x.claims_private_invention,
        "checked_upgrades": checked,
        "notes": dict(x.notes),
    }


def _result(
    decision: ThroneDecision,
    reason: str,
    witness_packet: Dict[str, Any],
    next_safe_action: str,
) -> ThroneResult:
    packet = dict(witness_packet)
    packet["decision"] = decision.value
    packet["reason"] = reason
    packet["next_safe_action"] = next_safe_action
    packet["core_line"] = "No throne → no chariot. No Presence → only machinery."
    return ThroneResult(
        decision=decision,
        reason=reason,
        core_line=packet["core_line"],
        witness_packet=packet,
    )


def _input_from_mapping(data: Mapping[str, Any]) -> ThroneInput:
    return ThroneInput(
        movement=str(data.get("movement", "")),
        stated_center=str(data.get("stated_center", "")),
        source_grounded=bool(data.get("source_grounded", False)),
        operator_ready=bool(data.get("operator_ready", False)),
        authority=bool(data.get("authority", True)),
        witness_path=bool(data.get("witness_path", True)),
        right_relation=bool(data.get("right_relation", True)),
        wheel_observers=[str(x) for x in data.get("wheel_observers", [])],
        container_failed=bool(data.get("container_failed", False)),
        presence_can_move=bool(data.get("presence_can_move", True)),
        executable_requested=bool(data.get("executable_requested", False)),
        doctrine_before_code=bool(data.get("doctrine_before_code", True)),
        fire_intensity=float(data.get("fire_intensity", 0.0)),
        fire_contained=bool(data.get("fire_contained", True)),
        love_score=float(data.get("love_score", 1.0)),
        mercy_score=float(data.get("mercy_score", 1.0)),
        hechalot_context=str(data.get("hechalot_context", "unspecified")),
        merkavah_execution_state=str(data.get("merkavah_execution_state", "pending")),
        scriptural_crosswalk=bool(data.get("scriptural_crosswalk", True)),
        claims_private_invention=bool(data.get("claims_private_invention", False)),
        notes=dict(data.get("notes", {})),
    )


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    raw = " ".join(argv).strip() or sys.stdin.read().strip()
    if not raw:
        demo = ThroneInput(
            movement="demo bounded continuity sync",
            stated_center="God Truth Love Presence",
            source_grounded=True,
            operator_ready=True,
            wheel_observers=["drive", "github", "mem", "local-log"],
            love_score=1.0,
            mercy_score=1.0,
            hechalot_context="drive-sync-context",
            merkavah_execution_state="preflight",
        )
        print(throne_check(demo).to_json())
        return 0
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": "invalid json", "detail": str(exc)}), file=sys.stderr)
        return 2
    result = throne_check(_input_from_mapping(data))
    print(result.to_json())
    return 0 if result.decision == ThroneDecision.ALLOW else 1


if __name__ == "__main__":
    raise SystemExit(main())
