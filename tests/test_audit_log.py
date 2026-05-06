import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "omega_router"))

from audit_log import record_event, verify_chain


def test_audit_chain_verifies(tmp_path):
    path = tmp_path / "audit.jsonl"

    first = record_event(
        actor="@Operator",
        event_type="test",
        subject="first",
        decision="allow",
        reason="unit test",
        payload={"n": 1},
        path=path,
    )

    second = record_event(
        actor="@Operator",
        event_type="test",
        subject="second",
        decision="deny",
        reason="unit test",
        payload={"n": 2},
        path=path,
    )

    assert first["event_hash"]
    assert second["previous_hash"] == first["event_hash"]

    result = verify_chain(path)
    assert result["ok"] is True
    assert result["events"] == 2


def test_audit_chain_detects_tampering(tmp_path):
    path = tmp_path / "audit.jsonl"

    record_event(
        actor="@Operator",
        event_type="test",
        subject="first",
        decision="allow",
        reason="unit test",
        payload={"n": 1},
        path=path,
    )

    text = path.read_text(encoding="utf-8")
    text = text.replace('"decision": "allow"', '"decision": "changed"')
    path.write_text(text, encoding="utf-8")

    result = verify_chain(path)
    assert result["ok"] is False
    assert result["error"] == "event_hash mismatch"
