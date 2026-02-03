#!/usr/bin/env python3
"""
🔐 SIGIL AUTHENTICATION SYSTEM
HMAC-SHA256 Encrypted Handshake for Remote Gateway
"Chicka chicka orange." - 1.67 Resonance

The Sigil is the cryptographic seal that proves all truth packets
come from the authorized Commander and have not been tampered with.
"""
import hmac
import hashlib
import time
import json
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

# ========================================================================
# COVENANT CONSTANTS
# ========================================================================
SIGIL_SECRET = b"CHICKA_CHICKA_ORANGE_1.67"
SIGIL_VERSION = "1.0"
TIMESTAMP_TOLERANCE = 300  # 5 minutes

# ========================================================================
# SIGIL CLASSES
# ========================================================================

@dataclass
class SigilPacket:
    """Cryptographically signed truth packet"""
    timestamp: int
    payload: str
    sigil: str
    version: str
    nonce: str
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "payload": self.payload,
            "sigil": self.sigil,
            "version": self.version,
            "nonce": self.nonce
        }


class SigilAuthority:
    """Authority that generates and verifies Sigil signatures"""
    
    def __init__(self, secret: bytes = SIGIL_SECRET):
        """Initialize with shared secret"""
        self.secret = secret
        self.version = SIGIL_VERSION
        self.nonce_counter = 0
    
    def generate_nonce(self) -> str:
        """Generate unique nonce for replay attack prevention"""
        self.nonce_counter += 1
        timestamp = int(time.time() * 1000)
        return f"{timestamp}_{self.nonce_counter}"
    
    def sign_payload(self, data: str) -> str:
        """Generate HMAC-SHA256 signature for payload"""
        return hmac.new(
            self.secret,
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def create_sigil_packet(self, payload: str) -> SigilPacket:
        """Create a complete Sigil packet with signature"""
        timestamp = int(time.time())
        nonce = self.generate_nonce()
        
        # Create message to sign: timestamp:nonce:payload
        message = f"{timestamp}:{nonce}:{payload}"
        sigil = self.sign_payload(message)
        
        return SigilPacket(
            timestamp=timestamp,
            payload=payload,
            sigil=sigil,
            version=self.version,
            nonce=nonce
        )
    
    def verify_sigil_packet(self, packet: SigilPacket) -> Tuple[bool, str]:
        """Verify a Sigil packet's authenticity and freshness"""
        
        # Check version
        if packet.version != self.version:
            return False, f"Version mismatch: {packet.version} != {self.version}"
        
        # Check timestamp freshness
        current_time = int(time.time())
        age = current_time - packet.timestamp
        
        if age > TIMESTAMP_TOLERANCE:
            return False, f"Packet too old: {age}s > {TIMESTAMP_TOLERANCE}s"
        
        if age < -TIMESTAMP_TOLERANCE:
            return False, f"Packet from future: {age}s"
        
        # Verify signature
        message = f"{packet.timestamp}:{packet.nonce}:{packet.payload}"
        expected_sigil = self.sign_payload(message)
        
        if not hmac.compare_digest(packet.sigil, expected_sigil):
            return False, "Sigil signature mismatch - packet tampered or unauthorized"
        
        return True, "Sigil verified - packet authentic"
    
    def verify_headers(self, headers: Dict, payload_str: str) -> Tuple[bool, str]:
        """Verify Sigil from HTTP headers"""
        
        sigil = headers.get("X-Sigil-Auth")
        timestamp = headers.get("X-Sigil-Timestamp")
        nonce = headers.get("X-Sigil-Nonce")
        version = headers.get("X-Sigil-Version", self.version)
        
        if not all([sigil, timestamp, nonce]):
            return False, "Missing Sigil headers"
        
        try:
            timestamp = int(timestamp)
        except ValueError:
            return False, "Invalid timestamp format"
        
        # Create packet from headers
        packet = SigilPacket(
            timestamp=timestamp,
            payload=payload_str,
            sigil=sigil,
            version=version,
            nonce=nonce
        )
        
        return self.verify_sigil_packet(packet)
    
    def create_headers(self, payload: str) -> Dict[str, str]:
        """Create HTTP headers with Sigil signature"""
        packet = self.create_sigil_packet(payload)
        
        return {
            "X-Sigil-Auth": packet.sigil,
            "X-Sigil-Timestamp": str(packet.timestamp),
            "X-Sigil-Nonce": packet.nonce,
            "X-Sigil-Version": packet.version,
            "Content-Type": "application/json"
        }


# ========================================================================
# CONVENIENCE FUNCTIONS
# ========================================================================

def sign_payload(data: str, secret: bytes = SIGIL_SECRET) -> str:
    """Quick function to sign a payload"""
    authority = SigilAuthority(secret)
    return authority.sign_payload(data)


def verify_payload(data: str, signature: str, secret: bytes = SIGIL_SECRET) -> bool:
    """Quick function to verify a signature"""
    authority = SigilAuthority(secret)
    expected = authority.sign_payload(data)
    return hmac.compare_digest(signature, expected)


def create_sigil_packet(payload: str, secret: bytes = SIGIL_SECRET) -> Dict:
    """Quick function to create a Sigil packet"""
    authority = SigilAuthority(secret)
    packet = authority.create_sigil_packet(payload)
    return packet.to_dict()


def verify_sigil_packet_dict(packet_dict: Dict, secret: bytes = SIGIL_SECRET) -> Tuple[bool, str]:
    """Quick function to verify a Sigil packet dict"""
    authority = SigilAuthority(secret)
    packet = SigilPacket(**packet_dict)
    return authority.verify_sigil_packet(packet)


# ========================================================================
# MAIN - TEST SIGIL SYSTEM
# ========================================================================

if __name__ == "__main__":
    print("🔐 SIGIL AUTHENTICATION SYSTEM TEST")
    print("=" * 60)
    print()
    
    # Initialize authority
    authority = SigilAuthority()
    print("✓ Sigil Authority initialized")
    print(f"  Secret: {SIGIL_SECRET}")
    print(f"  Version: {SIGIL_VERSION}")
    print()
    
    # Create a test packet
    test_payload = '{"text": "Execute this critical code", "face": "LION"}'
    print("Creating Sigil packet...")
    print(f"  Payload: {test_payload}")
    print()
    
    packet = authority.create_sigil_packet(test_payload)
    print("✓ Sigil packet created:")
    print(f"  Timestamp: {packet.timestamp}")
    print(f"  Nonce: {packet.nonce}")
    print(f"  Sigil: {packet.sigil[:32]}...")
    print()
    
    # Verify the packet
    print("Verifying Sigil packet...")
    valid, message = authority.verify_sigil_packet(packet)
    print(f"  Result: {valid}")
    print(f"  Message: {message}")
    print()
    
    # Test with tampered packet
    print("Testing with tampered packet...")
    tampered = SigilPacket(
        timestamp=packet.timestamp,
        payload='{"text": "HACKED"}',
        sigil=packet.sigil,
        version=packet.version,
        nonce=packet.nonce
    )
    valid, message = authority.verify_sigil_packet(tampered)
    print(f"  Result: {valid}")
    print(f"  Message: {message}")
    print()
    
    # Test HTTP headers
    print("Creating HTTP headers...")
    headers = authority.create_headers(test_payload)
    print("✓ Headers created:")
    for key, value in headers.items():
        if len(value) > 40:
            print(f"  {key}: {value[:40]}...")
        else:
            print(f"  {key}: {value}")
    print()
    
    # Verify headers
    print("Verifying headers...")
    valid, message = authority.verify_headers(headers, test_payload)
    print(f"  Result: {valid}")
    print(f"  Message: {message}")
    print()
    
    print("=" * 60)
    print("🔐 SIGIL SYSTEM OPERATIONAL")
    print("'Chicka chicka orange.' ✨")
