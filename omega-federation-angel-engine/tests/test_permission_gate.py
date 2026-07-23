import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "omega_router"))

from permission_gate import evaluate_gate


def test_readonly_reason_route_allowed():
    decision = evaluate_gate(
        route="reason",
        action="summarize",
        payload="summarize checkpoint",
        evidence_refs=["manual-test"],
        reversible=True,
        mercy=True,
    )
    assert decision.allowed is True


def test_missing_payload_denied():
    decision = evaluate_gate(
        route="reason",
        action="summarize",
        payload="",
        evidence_refs=["manual-test"],
        reversible=True,
        mercy=True,
    )
    assert decision.allowed is False
    assert "missing route or payload" in decision.reasons


def test_shell_denied_even_with_operator_confirmation():
    decision = evaluate_gate(
        route="execute",
        action="shell",
        payload="rm -rf /",
        operator_confirmed=True,
        evidence_refs=["manual-test"],
        reversible=True,
        mercy=True,
    )
    assert decision.allowed is False
    assert any("shell" in reason for reason in decision.reasons)


def test_non_reversible_denied():
    decision = evaluate_gate(
        route="archive",
        action="delete",
        payload="delete source",
        operator_confirmed=True,
        evidence_refs=["manual-test"],
        reversible=False,
        mercy=True,
    )
    assert decision.allowed is False
    assert "action is not reversible" in decision.reasons
