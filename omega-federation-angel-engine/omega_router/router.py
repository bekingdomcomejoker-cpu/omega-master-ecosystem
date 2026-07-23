"""Omega Continuity Fabric router skeleton.

Safe local-first routing daemon.
No arbitrary shell execution.
Provider models are callable nodes, not owners of continuity.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict

from bus_writer import BUS_FILE, EVENT_FILE, append_jsonl, save_state, utc_now
from permission_gate import evaluate_gate


ROUTE_REGISTRY = Path(__file__).with_name("route_registry.json")


def load_registry() -> Dict[str, Any]:
    return json.loads(ROUTE_REGISTRY.read_text(encoding="utf-8"))


def call_local(route: str, payload: str) -> str:
    return f"[LOCAL:{route}] {payload[:200]}"


def call_external(route: str, payload: str) -> str:
    return f"[EXTERNAL:{route}] placeholder response for: {payload[:200]}"


def classify_route(payload: str) -> str:
    lowered = payload.lower()
    if "@route:" in lowered:
        marker = lowered.split("@route:", 1)[1].split()[0].strip()
        return marker
    if "code" in lowered:
        return "code"
    return "reason"


def process_payload(payload: str, operator: str = "@Operator") -> Dict[str, Any]:
    registry = load_registry()
    route = classify_route(payload)
    route_config = registry["routes"].get(route, registry["routes"]["reason"])

    decision = evaluate_gate(
        route=route,
        action=route_config["default_action"],
        payload=payload,
        operator_confirmed=True,
        evidence_refs=["local-trigger"],
        reversible=True,
        mercy=True,
    )

    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": utc_now(),
        "operator": operator,
        "route": route,
        "payload_preview": payload[:240],
        "permission_gate": decision.to_dict(),
    }

    append_jsonl(EVENT_FILE, event)

    if not decision.allowed:
        result = {
            "status": "blocked",
            "reasons": decision.reasons,
        }
        append_jsonl(BUS_FILE, result)
        return result

    preferred_model = route_config.get("preferred_model", "local")

    if preferred_model == "local":
        output = call_local(route, payload)
        source = "local"
    else:
        output = call_external(route, payload)
        source = "external"

    result = {
        "timestamp": utc_now(),
        "source": source,
        "route": route,
        "output_preview": output[:240],
    }

    append_jsonl(BUS_FILE, result)

    save_state(
        {
            "last_route": route,
            "last_source": source,
            "last_output_preview": output[:240],
            "timestamp": utc_now(),
        }
    )

    return result


if __name__ == "__main__":
    sample = "@route:reason summarize the Omega Continuity Fabric"
    response = process_payload(sample)
    print(json.dumps(response, indent=2))
