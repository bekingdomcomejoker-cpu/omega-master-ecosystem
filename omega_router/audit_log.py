"""Append-only audit log for Repo 120.

The audit log records decisions before actions. It does not execute actions.
Each event includes a hash of the previous event so the log can be checked for
basic tamper evidence.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4


DEFAULT_AUDIT_LOG = Path("runtime") / "repo120_audit.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def canonical_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def last_event_hash(path: Path = DEFAULT_AUDIT_LOG) -> Optional[str]:
    if not path.exists():
        return None

    last = None
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if line.strip():
                last = line

    if not last:
        return None

    try:
        event = json.loads(last)
    except json.JSONDecodeError:
        return "CORRUPT_LAST_EVENT"

    return event.get("event_hash")


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    timestamp: str
    actor: str
    event_type: str
    subject: str
    decision: str
    reason: str
    payload: Dict[str, Any]
    previous_hash: Optional[str]
    event_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def make_event(
    *,
    actor: str,
    event_type: str,
    subject: str,
    decision: str,
    reason: str,
    payload: Optional[Dict[str, Any]] = None,
    path: Path = DEFAULT_AUDIT_LOG,
) -> AuditEvent:
    previous = last_event_hash(path)
    base = {
        "event_id": f"evt_{uuid4().hex}",
        "timestamp": utc_now(),
        "actor": actor,
        "event_type": event_type,
        "subject": subject,
        "decision": decision,
        "reason": reason,
        "payload": payload or {},
        "previous_hash": previous,
    }
    event_hash = sha256_text(canonical_json(base))
    return AuditEvent(**base, event_hash=event_hash)


def append_event(event: AuditEvent, path: Path = DEFAULT_AUDIT_LOG) -> AuditEvent:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def record_event(
    *,
    actor: str,
    event_type: str,
    subject: str,
    decision: str,
    reason: str,
    payload: Optional[Dict[str, Any]] = None,
    path: Path = DEFAULT_AUDIT_LOG,
) -> Dict[str, Any]:
    event = make_event(
        actor=actor,
        event_type=event_type,
        subject=subject,
        decision=decision,
        reason=reason,
        payload=payload,
        path=path,
    )
    append_event(event, path)
    return event.to_dict()


def verify_chain(path: Path = DEFAULT_AUDIT_LOG) -> Dict[str, Any]:
    if not path.exists():
        return {"ok": True, "events": 0, "message": "no audit log yet"}

    previous = None
    count = 0
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            count += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                return {"ok": False, "line": line_no, "error": f"json decode: {exc}"}

            supplied_hash = event.get("event_hash")
            event_without_hash = dict(event)
            event_without_hash.pop("event_hash", None)

            if event_without_hash.get("previous_hash") != previous:
                return {
                    "ok": False,
                    "line": line_no,
                    "error": "previous_hash mismatch",
                    "expected_previous_hash": previous,
                    "actual_previous_hash": event_without_hash.get("previous_hash"),
                }

            expected_hash = sha256_text(canonical_json(event_without_hash))
            if supplied_hash != expected_hash:
                return {
                    "ok": False,
                    "line": line_no,
                    "error": "event_hash mismatch",
                    "expected_hash": expected_hash,
                    "actual_hash": supplied_hash,
                }

            previous = supplied_hash

    return {"ok": True, "events": count, "last_hash": previous}
