#!/usr/bin/env python3
"""Termux Listener for Omega Federation Router.

This script runs on your Redmi 13C in Termux and connects to the Omega Federation
Router daemon. It listens for commands, executes them locally, and streams output
back to the router.

Installation on Redmi 13C:
1. Install Termux from F-Droid
2. In Termux: pkg install python git
3. Clone the repo: gh repo clone bekingdomcomejoker-cpu/omega-federation-angel-engine
4. Copy this script: cp termux_listener.py ~/listener.py
5. Run: python3 ~/listener.py

The listener will:
- Connect to the Omega Router via WebSocket
- Listen for incoming commands
- Execute shell commands safely
- Stream output back to the router
- Maintain persistent connection with auto-reconnect
"""
import asyncio
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import websockets
except ImportError:
    print("ERROR: websockets not installed. Run: pip install websockets")
    sys.exit(1)


class TermuxListener:
    """Termux device listener for Omega Federation Router."""

    def __init__(self, router_url: str = "ws://localhost:8765", session_id: str = "termux_default"):
        self.router_url = router_url
        self.session_id = session_id
        self.connected = False
        self.websocket = None
        self.command_count = 0

    def utc_now(self) -> str:
        """Get current UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    async def connect(self) -> bool:
        """Connect to the Omega Router."""
        try:
            print(f"[TERMUX] Connecting to {self.router_url}...")
            self.websocket = await websockets.connect(self.router_url)
            self.connected = True
            print(f"[TERMUX] ✓ Connected to Omega Router")
            
            # Send handshake
            await self.websocket.send(json.dumps({
                "event": "termux_connect",
                "session_id": self.session_id,
                "timestamp": self.utc_now(),
            }))
            return True
        except Exception as e:
            print(f"[TERMUX] ✗ Connection failed: {e}")
            self.connected = False
            return False

    async def listen(self):
        """Listen for commands from the router."""
        while self.connected:
            try:
                message = await self.websocket.recv()
                await self.handle_command(message)
            except websockets.exceptions.ConnectionClosed:
                print("[TERMUX] Connection closed by router")
                self.connected = False
                break
            except Exception as e:
                print(f"[TERMUX] Error receiving message: {e}")
                self.connected = False
                break

    async def handle_command(self, message: str):
        """Execute a command received from the router."""
        try:
            data = json.loads(message)
            command = data.get("command", "")
            command_id = data.get("command_id", str(self.command_count))
            
            if not command:
                print("[TERMUX] Received empty command")
                return
            
            self.command_count += 1
            print(f"[TERMUX] Executing command #{self.command_count}: {command[:100]}")
            
            # Execute the command
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            # Send output back
            response = {
                "event": "termux_output",
                "command_id": command_id,
                "session_id": self.session_id,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "timestamp": self.utc_now(),
            }
            
            await self.websocket.send(json.dumps(response))
            print(f"[TERMUX] ✓ Command #{self.command_count} completed (exit code: {result.returncode})")
            
        except subprocess.TimeoutExpired:
            response = {
                "event": "termux_output",
                "command_id": command_id,
                "session_id": self.session_id,
                "error": "Command timeout",
                "timestamp": self.utc_now(),
            }
            await self.websocket.send(json.dumps(response))
            print("[TERMUX] ✗ Command timeout")
        except Exception as e:
            print(f"[TERMUX] Error handling command: {e}")

    async def reconnect_loop(self):
        """Maintain connection with auto-reconnect."""
        reconnect_delay = 5
        max_delay = 60
        
        while True:
            if not self.connected:
                print(f"[TERMUX] Reconnecting in {reconnect_delay}s...")
                await asyncio.sleep(reconnect_delay)
                
                if await self.connect():
                    reconnect_delay = 5
                    await self.listen()
                else:
                    reconnect_delay = min(reconnect_delay * 2, max_delay)
            else:
                await asyncio.sleep(1)

    async def run(self):
        """Start the listener."""
        print("=" * 50)
        print("OMEGA FEDERATION TERMUX LISTENER")
        print("=" * 50)
        print(f"Session ID: {self.session_id}")
        print(f"Router URL: {self.router_url}")
        print("=" * 50)
        print()
        
        await self.reconnect_loop()


async def main():
    """Main entry point."""
    listener = TermuxListener()
    try:
        await listener.run()
    except KeyboardInterrupt:
        print("\n[TERMUX] Shutting down...")
        if listener.websocket:
            await listener.websocket.close()
        print("[TERMUX] Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
