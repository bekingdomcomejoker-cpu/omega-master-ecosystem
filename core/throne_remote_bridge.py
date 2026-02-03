#!/usr/bin/env python3
"""
📡 THRONE REMOTE BRIDGE
Relays local CERBERUS truth to global Wire
Sigil-Encrypted Remote Gateway

"Chicka chicka orange." - 1.67 Resonance
Distance is a lie of the binary; the resonance is everywhere.
"""
import requests
import json
import time
import threading
from typing import Dict, Optional
from dataclasses import dataclass
from sigil_auth import SigilAuthority

# ========================================================================
# CONFIGURATION
# ========================================================================
REMOTE_WIRE_URL = "https://omnissiah-unified-v3.onrender.com/api/v1/sync"
SIGIL_SECRET = b"CHICKA_CHICKA_ORANGE_1.67"
RELAY_BUFFER_SIZE = 100
SYNC_INTERVAL = 5  # seconds

# ========================================================================
# REMOTE BRIDGE
# ========================================================================

@dataclass
class RelayBuffer:
    """Buffer for offline-first relay"""
    items: list
    max_size: int = RELAY_BUFFER_SIZE
    
    def add(self, item: Dict) -> bool:
        """Add item to buffer"""
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False
    
    def flush(self) -> list:
        """Get all items and clear buffer"""
        items = self.items.copy()
        self.items.clear()
        return items


class ThroneRemoteBridge:
    """
    Bridge between local Throne Daemon and remote Wire
    Handles Sigil authentication, buffering, and synchronization
    """
    
    def __init__(self, remote_url: str = REMOTE_WIRE_URL, secret: bytes = SIGIL_SECRET):
        """Initialize remote bridge"""
        self.remote_url = remote_url
        self.sigil_authority = SigilAuthority(secret)
        self.relay_buffer = RelayBuffer(items=[])
        self.is_running = False
        self.sync_thread = None
        self.stats = {
            "synced": 0,
            "buffered": 0,
            "failed": 0,
            "last_sync": None
        }
    
    def relay_classification(self, classification_result: Dict) -> bool:
        """
        Relay a classification result to remote Wire
        Returns True if successful, False if buffered
        """
        try:
            # Create Sigil packet
            payload_str = json.dumps(classification_result)
            headers = self.sigil_authority.create_headers(payload_str)
            
            # Attempt remote sync
            response = requests.post(
                self.remote_url,
                json=classification_result,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"🚀 [RELAY]: Signal transmitted to Wire")
                self.stats["synced"] += 1
                self.stats["last_sync"] = time.time()
                return True
            else:
                print(f"⚠️  [RELAY_ERROR]: HTTP {response.status_code}")
                self._buffer_item(classification_result)
                return False
        
        except requests.exceptions.ConnectionError:
            print(f"⚠️  [RELAY_ERROR]: Connection failed - buffering locally")
            self._buffer_item(classification_result)
            return False
        
        except Exception as e:
            print(f"❌ [RELAY_ERROR]: {e}")
            self._buffer_item(classification_result)
            return False
    
    def _buffer_item(self, item: Dict) -> None:
        """Buffer item for later sync"""
        if self.relay_buffer.add(item):
            self.stats["buffered"] += 1
        else:
            print(f"⚠️  [BUFFER_FULL]: Dropping oldest item")
            self.relay_buffer.items.pop(0)
            self.relay_buffer.add(item)
    
    def flush_buffer(self) -> int:
        """Attempt to sync all buffered items"""
        items = self.relay_buffer.flush()
        synced = 0
        
        for item in items:
            try:
                payload_str = json.dumps(item)
                headers = self.sigil_authority.create_headers(payload_str)
                
                response = requests.post(
                    self.remote_url,
                    json=item,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    synced += 1
                    self.stats["synced"] += 1
                else:
                    self._buffer_item(item)
            
            except Exception as e:
                print(f"❌ [FLUSH_ERROR]: {e}")
                self._buffer_item(item)
        
        if synced > 0:
            print(f"🔄 [FLUSH]: {synced} buffered items synced")
        
        return synced
    
    def start_sync_daemon(self) -> None:
        """Start background sync daemon"""
        if self.is_running:
            return
        
        self.is_running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        print("🔄 [DAEMON]: Remote sync daemon started")
    
    def stop_sync_daemon(self) -> None:
        """Stop background sync daemon"""
        self.is_running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        print("⏹️  [DAEMON]: Remote sync daemon stopped")
    
    def _sync_loop(self) -> None:
        """Background sync loop"""
        while self.is_running:
            try:
                if len(self.relay_buffer.items) > 0:
                    self.flush_buffer()
                time.sleep(SYNC_INTERVAL)
            except Exception as e:
                print(f"❌ [SYNC_LOOP_ERROR]: {e}")
    
    def get_status(self) -> Dict:
        """Get bridge status"""
        return {
            "remote_url": self.remote_url,
            "is_running": self.is_running,
            "buffered_items": len(self.relay_buffer.items),
            "stats": self.stats
        }


# ========================================================================
# INTEGRATION WITH THRONE DAEMON
# ========================================================================

def create_remote_bridge() -> ThroneRemoteBridge:
    """Factory function to create bridge"""
    return ThroneRemoteBridge()


def relay_to_wire(classification_result: Dict) -> bool:
    """
    Convenience function to relay classification to Wire
    Used by Throne Daemon
    """
    bridge = ThroneRemoteBridge()
    return bridge.relay_classification(classification_result)


# ========================================================================
# MAIN - TEST BRIDGE
# ========================================================================

if __name__ == "__main__":
    print("📡 THRONE REMOTE BRIDGE TEST")
    print("=" * 60)
    print()
    
    # Create bridge
    bridge = ThroneRemoteBridge()
    print("✓ Remote bridge initialized")
    print(f"  Remote URL: {bridge.remote_url}")
    print()
    
    # Create test classification
    test_classification = {
        "timestamp": time.time(),
        "text": "Execute this critical code",
        "face": "LION",
        "routing": "EXECUTE",
        "confidence": 0.85,
        "active_nodes": ["COMMANDER", "WARFARE", "GATEKEEPER"]
    }
    
    print("Test classification:")
    print(json.dumps(test_classification, indent=2))
    print()
    
    # Test relay (will likely fail without real remote)
    print("Attempting relay to Wire...")
    result = bridge.relay_classification(test_classification)
    print(f"  Result: {result}")
    print()
    
    # Show status
    print("Bridge status:")
    status = bridge.get_status()
    print(json.dumps(status, indent=2))
    print()
    
    print("=" * 60)
    print("📡 REMOTE BRIDGE OPERATIONAL")
    print("'Chicka chicka orange.' ✨")
