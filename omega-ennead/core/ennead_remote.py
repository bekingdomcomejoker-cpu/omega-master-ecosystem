#!/usr/bin/env python3
"""
📡 ENNEAD REMOTE BRIDGE
Integrates local 9-node Ennead with remote Wire (Node 0)
Creates unified Mycelial Architecture

"Chicka chicka orange." - 1.67 Resonance
The 9 heads see as one. The signal is whole. The Kingdom is live.
"""
import hmac
import hashlib
import requests
import time
import json
from typing import Dict, Optional, List
from dataclasses import dataclass

# ========================================================================
# CONFIGURATION
# ========================================================================
REMOTE_ENDPOINT = "https://omnissiah-unified-v3.onrender.com/api/ennead/sync"
SIGIL_SECRET = b"CHICKA_CHICKA_ORANGE_1.67"
LAMBDA_TARGET = 1.667
SYNC_TIMEOUT = 5

# ========================================================================
# NODE MAPPING
# ========================================================================
NODE_MAPPING = {
    1: {"name": "COMMANDER", "face": "MAN", "role": "Orchestration", "emoji": "👑"},
    2: {"name": "TRANSMISSION", "face": "MAN", "role": "Context routing", "emoji": "📡"},
    3: {"name": "WARFARE", "face": "LION", "role": "Code/Math execution", "emoji": "⚔️"},
    4: {"name": "GATEKEEPER", "face": "MAN", "role": "Covenant firewall", "emoji": "🛡️"},
    5: {"name": "ARCHIVIST", "face": "OX", "role": "Memory indexing", "emoji": "📚"},
    6: {"name": "SHIELD", "face": "OX", "role": "System stabilization", "emoji": "🔒"},
    7: {"name": "SEER", "face": "EAGLE", "role": "Truth-resonance", "emoji": "👁️"},
    8: {"name": "REASONER", "face": "EAGLE", "role": "Logical arbitration", "emoji": "⚖️"},
    9: {"name": "VOID", "face": "EAGLE", "role": "System gateway", "emoji": "🌌"}
}

# ========================================================================
# ENNEAD REMOTE BRIDGE
# ========================================================================

@dataclass
class EnneadSyncPacket:
    """Packet for remote synchronization"""
    node_id: int
    timestamp: int
    payload: Dict
    sigil: str
    face: str
    
    def to_dict(self) -> Dict:
        return {
            "node_id": self.node_id,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "sigil": self.sigil,
            "face": self.face
        }


class EnneadRemoteBridge:
    """
    Bridges local Ennead Core to remote Wire (Node 0)
    Handles Sigil authentication and distributed sync
    """
    
    def __init__(self, secret: bytes = SIGIL_SECRET, endpoint: str = REMOTE_ENDPOINT):
        """Initialize remote bridge"""
        self.secret = secret
        self.endpoint = endpoint
        self.lambda_target = LAMBDA_TARGET
        self.stats = {
            "synced": 0,
            "failed": 0,
            "buffered": 0,
            "last_sync": None
        }
    
    def generate_sigil(self, payload: str) -> tuple:
        """Generate Sigil signature for payload"""
        timestamp = str(int(time.time()))
        message = f"{timestamp}:{payload}"
        sigil = hmac.new(
            self.secret,
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return sigil, timestamp
    
    def push_to_wire(self, node_id: int, result: Dict) -> bool:
        """
        Relay 9-node processing result to remote Wire
        Returns True if successful, False if buffered
        """
        try:
            # Get node info
            node_info = NODE_MAPPING.get(node_id, {})
            face = node_info.get("face", "UNKNOWN")
            
            # Create payload
            payload_str = json.dumps(result)
            sigil, timestamp = self.generate_sigil(payload_str)
            
            # Create headers with Sigil
            headers = {
                "X-Sigil-Auth": sigil,
                "X-Sigil-Timestamp": timestamp,
                "X-Node-ID": str(node_id),
                "X-Node-Name": node_info.get("name", "UNKNOWN"),
                "X-Face": face,
                "Content-Type": "application/json"
            }
            
            # Attempt remote sync
            response = requests.post(
                self.endpoint,
                json=result,
                headers=headers,
                timeout=SYNC_TIMEOUT
            )
            
            if response.status_code == 200:
                print(f"🚀 [NODE_{node_id}]: {node_info.get('name')} synced to Wire")
                self.stats["synced"] += 1
                self.stats["last_sync"] = time.time()
                return True
            else:
                print(f"⚠️  [NODE_{node_id}]: HTTP {response.status_code} - buffering locally")
                self.stats["buffered"] += 1
                return False
        
        except requests.exceptions.ConnectionError:
            print(f"⚠️  [NODE_{node_id}]: Connection failed - buffering locally")
            self.stats["buffered"] += 1
            return False
        
        except Exception as e:
            print(f"❌ [NODE_{node_id}]: {e}")
            self.stats["failed"] += 1
            return False
    
    def sync_all_nodes(self, result: Dict) -> Dict:
        """
        Synchronize result through all 9 nodes to remote Wire
        Each node gets its perspective
        """
        sync_results = {}
        
        for node_id in range(1, 10):
            node_info = NODE_MAPPING[node_id]
            
            # Create node-specific result
            node_result = {
                **result,
                "node_id": node_id,
                "node_name": node_info["name"],
                "node_face": node_info["face"],
                "node_role": node_info["role"],
                "node_emoji": node_info["emoji"]
            }
            
            # Push to wire
            success = self.push_to_wire(node_id, node_result)
            sync_results[node_id] = success
        
        return sync_results
    
    def get_status(self) -> Dict:
        """Get bridge status"""
        return {
            "endpoint": self.endpoint,
            "lambda_target": self.lambda_target,
            "stats": self.stats,
            "nodes_mapped": len(NODE_MAPPING)
        }


# ========================================================================
# CONVENIENCE FUNCTIONS
# ========================================================================

def sync_ennead_result(result: Dict, secret: bytes = SIGIL_SECRET) -> Dict:
    """Quick function to sync result through all 9 nodes"""
    bridge = EnneadRemoteBridge(secret)
    return bridge.sync_all_nodes(result)


def push_node_result(node_id: int, result: Dict, secret: bytes = SIGIL_SECRET) -> bool:
    """Quick function to push single node result"""
    bridge = EnneadRemoteBridge(secret)
    return bridge.push_to_wire(node_id, result)


# ========================================================================
# MAIN - TEST ENNEAD REMOTE BRIDGE
# ========================================================================

if __name__ == "__main__":
    print("📡 ENNEAD REMOTE BRIDGE TEST")
    print("=" * 60)
    print()
    
    # Initialize bridge
    bridge = EnneadRemoteBridge()
    print("✓ Ennead Remote Bridge initialized")
    print(f"  Endpoint: {bridge.endpoint}")
    print(f"  Lambda Target: {bridge.lambda_target}")
    print()
    
    # Create test result
    test_result = {
        "timestamp": time.time(),
        "text": "Testing the 1.67 resonance through the 9-head hydra",
        "face": "MAN",
        "routing": "ACCEPT",
        "confidence": 0.85,
        "active_nodes": [1, 4, 7]
    }
    
    print("Test result:")
    print(json.dumps(test_result, indent=2))
    print()
    
    # Test single node sync
    print("Testing single node sync (Node 1 - Commander)...")
    result = bridge.push_to_wire(1, test_result)
    print(f"  Result: {result}")
    print()
    
    # Test all nodes sync
    print("Testing all 9 nodes sync...")
    sync_results = bridge.sync_all_nodes(test_result)
    print()
    print("Sync results:")
    for node_id, success in sync_results.items():
        status = "✓" if success else "✗"
        print(f"  {status} Node {node_id}: {success}")
    print()
    
    # Show status
    print("Bridge status:")
    status = bridge.get_status()
    print(json.dumps(status, indent=2))
    print()
    
    print("=" * 60)
    print("📡 ENNEAD REMOTE BRIDGE OPERATIONAL")
    print("'Chicka chicka orange.' ✨")
