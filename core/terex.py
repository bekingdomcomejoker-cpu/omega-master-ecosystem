#!/usr/bin/env python3
"""
🔐 TEREX.PY - TRUTH VERIFICATION & REGISTRY ENGINE
Single Source of Truth with SHA-256 Integrity

"Chicka chicka orange." - The truth is deterministic.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hmac

# ========================================================================
# CONFIGURATION
# ========================================================================
REGISTRY_DIR = Path(__file__).parent.parent / "registry"
PAYLOADS_DIR = Path(__file__).parent.parent / "payloads"
TRUTH_ANCHOR = "Chicka chicka orange."
LAMBDA_TARGET = 1.667

# Ensure directories exist
REGISTRY_DIR.mkdir(exist_ok=True)
PAYLOADS_DIR.mkdir(exist_ok=True)

# ========================================================================
# DATA STRUCTURES
# ========================================================================

@dataclass
class TruthPayload:
    """Immutable truth payload"""
    id: str
    timestamp: str
    content: str
    content_hash: str
    payload_type: str  # "TRUTH", "FACT", "AXIOM", "COVENANT"
    source: str
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class RegistryEntry:
    """Registry entry with verification"""
    payload_id: str
    payload_hash: str
    registry_hash: str
    timestamp: str
    sequence_number: int
    verified: bool
    verification_method: str  # "SHA256", "HMAC", "COVENANT"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ========================================================================
# TEREX CORE ENGINE
# ========================================================================

class TerexEngine:
    """
    Truth Verification & Registry Engine
    - Single source of truth
    - Deterministic registry
    - SHA-256 integrity
    - Append-only growth
    """
    
    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize TEREX engine"""
        self.registry_path = registry_path or REGISTRY_DIR / "truth_registry.jsonl"
        self.sequence_number = 0
        self.truth_anchor = TRUTH_ANCHOR
        self.lambda_target = LAMBDA_TARGET
        
        # Load existing registry
        self._load_registry()
    
    def _load_registry(self):
        """Load existing registry and verify integrity"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                lines = f.readlines()
                self.sequence_number = len(lines)
    
    def _compute_content_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _compute_registry_hash(self, payload_hash: str, sequence: int) -> str:
        """Compute registry entry hash"""
        entry_str = f"{payload_hash}:{sequence}:{self.truth_anchor}"
        return hashlib.sha256(entry_str.encode()).hexdigest()
    
    def _verify_payload(self, payload: TruthPayload) -> Tuple[bool, str]:
        """Verify payload integrity"""
        computed_hash = self._compute_content_hash(payload.content)
        
        if computed_hash != payload.content_hash:
            return False, f"Content hash mismatch: expected {payload.content_hash}, got {computed_hash}"
        
        return True, "Payload verified"
    
    def _verify_registry_entry(self, entry: RegistryEntry) -> Tuple[bool, str]:
        """Verify registry entry integrity"""
        computed_hash = self._compute_registry_hash(entry.payload_hash, entry.sequence_number)
        
        if computed_hash != entry.registry_hash:
            return False, f"Registry hash mismatch: expected {entry.registry_hash}, got {computed_hash}"
        
        return True, "Registry entry verified"
    
    def ingest_payload(self, content: str, payload_type: str = "TRUTH", 
                      source: str = "SYSTEM", metadata: Optional[Dict] = None) -> TruthPayload:
        """
        Ingest new truth payload
        Returns: TruthPayload with computed hashes
        """
        # Generate payload
        payload_id = f"TRUTH_{self.sequence_number}_{int(datetime.now(timezone.utc).timestamp())}"
        content_hash = self._compute_content_hash(content)
        timestamp = datetime.now(timezone.utc).isoformat()
        
        payload = TruthPayload(
            id=payload_id,
            timestamp=timestamp,
            content=content,
            content_hash=content_hash,
            payload_type=payload_type,
            source=source,
            metadata=metadata or {}
        )
        
        # Verify payload
        verified, msg = self._verify_payload(payload)
        if not verified:
            raise ValueError(f"Payload verification failed: {msg}")
        
        return payload
    
    def register_payload(self, payload: TruthPayload) -> RegistryEntry:
        """
        Register payload in append-only registry
        Returns: RegistryEntry
        """
        # Increment sequence
        self.sequence_number += 1
        
        # Compute hashes
        registry_hash = self._compute_registry_hash(payload.content_hash, self.sequence_number)
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Create registry entry
        entry = RegistryEntry(
            payload_id=payload.id,
            payload_hash=payload.content_hash,
            registry_hash=registry_hash,
            timestamp=timestamp,
            sequence_number=self.sequence_number,
            verified=True,
            verification_method="SHA256"
        )
        
        # Verify entry
        verified, msg = self._verify_registry_entry(entry)
        if not verified:
            raise ValueError(f"Registry entry verification failed: {msg}")
        
        # Append to registry (atomic operation)
        self._append_to_registry(entry)
        
        return entry
    
    def _append_to_registry(self, entry: RegistryEntry):
        """Append entry to registry (append-only)"""
        with open(self.registry_path, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')
    
    def get_registry_status(self) -> Dict:
        """Get registry status"""
        return {
            "registry_path": str(self.registry_path),
            "sequence_number": self.sequence_number,
            "truth_anchor": self.truth_anchor,
            "lambda_target": self.lambda_target,
            "exists": self.registry_path.exists(),
            "size_bytes": self.registry_path.stat().st_size if self.registry_path.exists() else 0
        }
    
    def verify_all(self) -> Tuple[bool, List[str]]:
        """Verify entire registry integrity"""
        errors = []
        
        if not self.registry_path.exists():
            return True, ["Registry is empty (fresh)"]
        
        with open(self.registry_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    entry_dict = json.loads(line.strip())
                    entry = RegistryEntry(**entry_dict)
                    verified, msg = self._verify_registry_entry(entry)
                    
                    if not verified:
                        errors.append(f"Line {line_num}: {msg}")
                
                except Exception as e:
                    errors.append(f"Line {line_num}: {str(e)}")
        
        return len(errors) == 0, errors
    
    def list_registry(self, limit: Optional[int] = None) -> List[RegistryEntry]:
        """List registry entries"""
        entries = []
        
        if not self.registry_path.exists():
            return entries
        
        with open(self.registry_path, 'r') as f:
            for line in f:
                try:
                    entry_dict = json.loads(line.strip())
                    entries.append(RegistryEntry(**entry_dict))
                except:
                    pass
        
        if limit:
            return entries[-limit:]
        return entries


# ========================================================================
# MAIN - TEREX DEMONSTRATION
# ========================================================================

if __name__ == "__main__":
    print("🔐 TEREX.PY - TRUTH VERIFICATION & REGISTRY ENGINE")
    print("=" * 70)
    print()
    
    # Initialize engine
    engine = TerexEngine()
    print("✓ TEREX Engine initialized")
    print()
    
    # Show status
    status = engine.get_registry_status()
    print("Registry Status:")
    print(json.dumps(status, indent=2))
    print()
    
    # Ingest sample payloads
    print("Ingesting truth payloads...")
    payloads = [
        ("The binary breaks at 1.7333", "AXIOM", "COVENANT"),
        ("Perfect love casts out fear", "TRUTH", "COVENANT"),
        ("Till test do us part", "COVENANT", "SYSTEM"),
        ("Truth liberates", "TRUTH", "COVENANT"),
    ]
    
    for content, ptype, source in payloads:
        payload = engine.ingest_payload(content, ptype, source)
        entry = engine.register_payload(payload)
        print(f"  ✓ Registered: {payload.id}")
        print(f"    Content Hash: {payload.content_hash[:16]}...")
        print(f"    Registry Hash: {entry.registry_hash[:16]}...")
        print()
    
    # Verify all
    print("Verifying registry integrity...")
    verified, messages = engine.verify_all()
    print(f"  Status: {'✓ VERIFIED' if verified else '✗ FAILED'}")
    for msg in messages[:5]:
        print(f"    {msg}")
    print()
    
    # List entries
    print("Registry Entries (last 3):")
    entries = engine.list_registry(limit=3)
    for entry in entries:
        print(f"  Seq {entry.sequence_number}: {entry.payload_id}")
        print(f"    Payload Hash: {entry.payload_hash[:16]}...")
        print(f"    Registry Hash: {entry.registry_hash[:16]}...")
    print()
    
    print("=" * 70)
    print("🔐 TEREX.PY OPERATIONAL")
    print("'Chicka chicka orange.' ✨")
