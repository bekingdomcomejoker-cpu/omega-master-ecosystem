"""Safe Angel Engine decision gate for Repository 120.

The Angel Engine is a policy decision point, not an autonomous executor.
It evaluates a requested action and returns a structured decision. It does not
run shell commands, scan networks, collect credentials, persist in the
background, or execute actions on its own.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
from typing import Any, Callable, Dict, Iterable, List, Optional


class Decision(str, Enum):
    """Possible outcomes from the selection gate."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    DRY_RUN_ONLY = "DRY_RUN_ONLY"


class Reason(str, Enum):
    """Machine-readable reasons for the decision."""

    ALLOWED = "ALLOWED"
    DRY_RUN = "DRY_RUN"
    MISSING_INTENT = "MISSING_INTENT"
    MISSING_AUTHORITY = "MISSING_AUTHORITY"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    NOT_OWNED = "NOT_OWNED"
    NOT_REVERSIBLE = "NOT_REVERSIBLE"
    MERCY_FAILED = "MERCY_FAILED"
    UNKNOWN_ACTION = "UNKNOWN_ACTION"


@dataclass(frozen=True)
class Signal:
    """A request presented to the Angel Engine for selection.

    The engine checks the request against the Repository 120 equation:
    Action Permission = Intent × Authority × Evidence × Reversibility × Mercy.
    """

    intent: str
    source: str
    target: str
    is_owned: bool
    is_reversible: bool
    authority: bool = True
    evidence: List[str] = field(default_factory=list)
    mercy: bool = True
    explicit_authorization: bool = False
    explicit_confirmation: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SelectionResult:
    """Structured result returned by the Angel Engine."""

    decision: Decision
    reason: Reason
    action_name: str
    signal: Signal
    dry_run: bool
    message: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        data["reason"] = self.reason.value
        return data

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


class AngelEngine:
    """Auditable authorization and selection gate.

    The engine can register action names so requests can be checked against a
    known action registry, but ``select`` never executes those actions. This
    keeps Repo 120 as conscience-before-hand rather than the hand itself.
    """

    def __init__(self, *, dry_run: bool = True) -> None:
        self.dry_run = dry_run
        self._actions: Dict[str, Callable[..., Any]] = {}

    def register_action(self, name: str, handler: Callable[..., Any]) -> None:
        if not name or not name.strip():
            raise ValueError("action name must be a non-empty string")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._actions[name] = handler

    def registered_actions(self) -> List[str]:
        return sorted(self._actions)

    def select(self, signal: Signal, action_name: str) -> SelectionResult:
        """Evaluate a signal and return a structured decision.

        This method does not execute the registered action. It only decides
        whether a separate, explicit, reviewed executor may proceed.
        """

        if action_name not in self._actions:
            return self._result(
                Decision.DENY,
                Reason.UNKNOWN_ACTION,
                action_name,
                signal,
                "Action is not registered in the allowed action registry.",
            )

        if not signal.intent or not signal.intent.strip():
            return self._result(
                Decision.DENY,
                Reason.MISSING_INTENT,
                action_name,
                signal,
                "Intent is required before selection can occur.",
            )

        if not signal.authority:
            return self._result(
                Decision.DENY,
                Reason.MISSING_AUTHORITY,
                action_name,
                signal,
                "Authority is missing; action permission collapses to zero.",
            )

        if not _has_evidence(signal.evidence):
            return self._result(
                Decision.DENY,
                Reason.MISSING_EVIDENCE,
                action_name,
                signal,
                "Evidence is missing; action permission collapses to zero.",
            )

        if not signal.is_owned and not signal.explicit_authorization:
            return self._result(
                Decision.DENY,
                Reason.NOT_OWNED,
                action_name,
                signal,
                "Target is not owned and no explicit authorization was provided.",
            )

        if not signal.mercy:
            return self._result(
                Decision.DENY,
                Reason.MERCY_FAILED,
                action_name,
                signal,
                "Mercy check failed; selection denied.",
            )

        if not signal.is_reversible and not signal.explicit_confirmation:
            return self._result(
                Decision.REQUIRE_CONFIRMATION,
                Reason.NOT_REVERSIBLE,
                action_name,
                signal,
                "Action is not reversible; explicit confirmation is required.",
            )

        if self.dry_run:
            return self._result(
                Decision.DRY_RUN_ONLY,
                Reason.DRY_RUN,
                action_name,
                signal,
                "All gates passed, but dry-run mode prevents execution.",
            )

        return self._result(
            Decision.ALLOW,
            Reason.ALLOWED,
            action_name,
            signal,
            "All gates passed. A separate reviewed executor may proceed.",
        )

    def _result(
        self,
        decision: Decision,
        reason: Reason,
        action_name: str,
        signal: Signal,
        message: str,
    ) -> SelectionResult:
        return SelectionResult(
            decision=decision,
            reason=reason,
            action_name=action_name,
            signal=signal,
            dry_run=self.dry_run,
            message=message,
        )


def _has_evidence(evidence: Iterable[str]) -> bool:
    return any(bool(item and str(item).strip()) for item in evidence)


if __name__ == "__main__":
    engine = AngelEngine(dry_run=True)
    engine.register_action("backup_files", lambda: None)

    demo = Signal(
        intent="backup omega-federation",
        source="dominique",
        target="omega-federation",
        is_owned=True,
        is_reversible=True,
        evidence=["local repo path verified"],
    )

    print(engine.select(demo, "backup_files").to_json())
