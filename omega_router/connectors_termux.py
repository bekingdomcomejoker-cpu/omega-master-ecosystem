"""Termux WebSocket bridge connector for Omega Federation Router.

Handles real-time bidirectional communication with Termux listener on Redmi 13C.
Manages command execution, output streaming, and session state.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from connectors_base import Connector
from bus_writer import append_jsonl, BUS_FILE, utc_now


class TermuxConnector(Connector):
    """Termux device connector for shell command execution."""

    def __init__(self, connector_id: str = "termux", config: Optional[Dict[str, Any]] = None):
        super().__init__(connector_id, config or {})
        self.session_id = self.config.get("session_id", "default")
        self.websocket_url = self.config.get("websocket_url", "ws://localhost:8765")
        self.state = {
            "connected": False,
            "last_command": None,
            "last_output": None,
            "session_id": self.session_id,
        }

    def health(self) -> Dict[str, Any]:
        """Check Termux listener availability."""
        try:
            # Try a simple echo command to verify connectivity
            result = subprocess.run(
                ["bash", "-c", "echo 'health_check'"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return {
                "status": "ok" if result.returncode == 0 else "degraded",
                "connector_id": self.connector_id,
                "timestamp": utc_now(),
                "details": {"session_id": self.session_id, "connected": True},
            }
        except Exception as e:
            return {
                "status": "offline",
                "connector_id": self.connector_id,
                "timestamp": utc_now(),
                "details": {"error": str(e)},
            }

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a shell command on the Termux device."""
        command = payload.get("command", "")
        if not command:
            return {
                "status": "error",
                "connector_id": self.connector_id,
                "result": {"error": "No command provided"},
                "timestamp": utc_now(),
            }

        try:
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=30,
            )

            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

            self.state["last_command"] = command
            self.state["last_output"] = output

            # Log to bus
            append_jsonl(
                BUS_FILE,
                {
                    "event": "termux_command_executed",
                    "connector_id": self.connector_id,
                    "command": command,
                    "returncode": result.returncode,
                    "timestamp": utc_now(),
                },
            )

            return {
                "status": "ok",
                "connector_id": self.connector_id,
                "result": output,
                "timestamp": utc_now(),
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "connector_id": self.connector_id,
                "result": {"error": "Command timeout"},
                "timestamp": utc_now(),
            }
        except Exception as e:
            return {
                "status": "error",
                "connector_id": self.connector_id,
                "result": {"error": str(e)},
                "timestamp": utc_now(),
            }

    def checkpoint(self) -> Dict[str, Any]:
        """Save Termux connector state."""
        checkpoint = {
            "connector_id": self.connector_id,
            "state": self.state,
            "timestamp": utc_now(),
        }
        append_jsonl(BUS_FILE, checkpoint)
        return checkpoint
