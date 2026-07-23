#!/usr/bin/env python3
"""Omega Federation Router Daemon.

Persistent service that runs the router continuously, listening for payloads
and routing them through the permission gate to appropriate connectors.

Usage:
    python3 omega_daemon.py
    
The daemon will:
- Load the route registry
- Initialize connectors (Termux, Google Drive, GitHub, etc.)
- Listen for incoming requests
- Route through permission gates
- Log all events to the runtime bus
- Maintain checkpoints for continuity
"""
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# Add omega_router to path
sys.path.insert(0, str(Path(__file__).parent / "omega_router"))

from router import process_payload
from bus_writer import append_jsonl, BUS_FILE, EVENT_FILE, utc_now


def daemon_loop():
    """Main daemon loop."""
    print("[OMEGA] Daemon started at", utc_now())
    append_jsonl(BUS_FILE, {"event": "daemon_started", "timestamp": utc_now()})

    iteration = 0
    while True:
        try:
            iteration += 1
            
            # Example: process a sample payload every 60 seconds
            if iteration % 60 == 0:
                payload = f"@route:reason Daemon heartbeat #{iteration}"
                result = process_payload(payload, operator="@Daemon")
                print(f"[OMEGA] Heartbeat #{iteration}: {result}")
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n[OMEGA] Daemon shutting down...")
            append_jsonl(BUS_FILE, {"event": "daemon_stopped", "timestamp": utc_now()})
            break
        except Exception as e:
            print(f"[OMEGA] Error in daemon loop: {e}")
            append_jsonl(BUS_FILE, {"event": "daemon_error", "error": str(e), "timestamp": utc_now()})
            time.sleep(5)


if __name__ == "__main__":
    daemon_loop()
