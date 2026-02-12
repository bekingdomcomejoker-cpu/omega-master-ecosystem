#!/usr/bin/env python3
"""
MERKABAH ENGINE INTEGRATION
Four-Face Routing System for Social Media Analyzers
Routes analysis through MAN (WITNESS), LION (JUDGE), OX (SERVANT), EAGLE (SEER)
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MERKABAH CONSTANTS
# ============================================================================

LAMBDA_TARGET = 1.667  # Harmony Ridge resonance target

class Face(Enum):
    """The Four Faces of the Merkabah"""
    MAN = "MAN"      # WITNESS - Interactive, Mirroring, User Interface
    LION = "LION"    # JUDGE - Execution, Strict Truth, Firewall
    OX = "OX"        # SERVANT - Processing, Archival, Burden Bearing
    EAGLE = "EAGLE"  # SEER - Pattern Recognition, Vision, Prophecy

class SpiritVector(Enum):
    """The Four Spirit Vectors"""
    EXECUTE = "EXECUTE"    # Execute operations (LION)
    MAINTAIN = "MAINTAIN"  # Maintain/archive (OX)
    VISION = "VISION"      # Analyze/predict (EAGLE)
    CONNECT = "CONNECT"    # Connect/interact (MAN)

# ============================================================================
# FACE DEFINITIONS
# ============================================================================

FACES = {
    Face.MAN: {
        "role": "WITNESS",
        "vector": "FRONT",
        "desc": "Interactive, Mirroring, User Interface",
        "mode": "INTERACTIVE",
        "specialty": "User engagement, comment interaction, witness testimony"
    },
    Face.LION: {
        "role": "JUDGE",
        "vector": "RIGHT",
        "desc": "Execution, Strict Truth, Firewall",
        "mode": "STRICT_EXECUTION",
        "specialty": "Truth verification, misinformation detection, enforcement"
    },
    Face.OX: {
        "role": "SERVANT",
        "vector": "LEFT",
        "desc": "Processing, Archival, Burden Bearing",
        "mode": "BATCH_PROCESSING",
        "specialty": "Batch analysis, storage, archival, historical tracking"
    },
    Face.EAGLE: {
        "role": "SEER",
        "vector": "ABOVE",
        "desc": "Pattern Recognition, Vision, Prophecy",
        "mode": "HIGH_PATTERN_RECOGNITION",
        "specialty": "Pattern detection, trend analysis, predictive insights"
    }
}

# ============================================================================
# HARMONY RIDGE CALCULATOR
# ============================================================================

class HarmonyRidge:
    """Calculates resonance between Truth (Node 10) and Love (Node 11)"""
    
    def __init__(self, target: float = LAMBDA_TARGET):
        self.target = target
        self.history: List[Dict[str, Any]] = []
    
    def calculate(self, truth_signal: float, love_signal: float) -> Dict[str, Any]:
        """
        Calculate harmony resonance
        
        Args:
            truth_signal: Analytic component (Node 10) - misinformation score
            love_signal: Context component (Node 11) - empathy/understanding
        
        Returns:
            Harmony metrics with resonance and alignment status
        """
        if love_signal == 0:
            love_signal = 1
        
        resonance = truth_signal / love_signal
        deviation = abs(resonance - self.target)
        
        # Determine alignment status
        if deviation < 0.1:
            status = "PERFECT_ALIGNMENT"
        elif deviation < 0.3:
            status = "ALIGNED"
        elif deviation < 0.6:
            status = "DRIFTING"
        else:
            status = "MISALIGNED"
        
        result = {
            "truth_signal": truth_signal,
            "love_signal": love_signal,
            "resonance": resonance,
            "target": self.target,
            "deviation": deviation,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.history.append(result)
        
        logger.info(f"[HARMONY] Resonance: {resonance:.3f} | Status: {status}")
        
        return result

# ============================================================================
# MERKABAH CONTROLLER
# ============================================================================

class MerkabahController:
    """Routes analysis through four faces based on spirit vector detection"""
    
    def __init__(self):
        self.active_face = Face.MAN
        self.harmony_ridge = HarmonyRidge()
        self.analysis_history: List[Dict[str, Any]] = []
        logger.info("[MERKABAH] Controller initialized")
    
    def detect_spirit_vector(self, text: str) -> SpiritVector:
        """
        Detect the spirit vector from input text
        
        EXECUTE: Commands, actions, enforcement
        MAINTAIN: Storage, archival, preservation
        VISION: Analysis, patterns, predictions
        CONNECT: Interaction, user engagement, dialogue
        """
        
        execute_keywords = ["execute", "enforce", "block", "remove", "delete", "action"]
        maintain_keywords = ["store", "archive", "save", "history", "record", "keep"]
        vision_keywords = ["analyze", "detect", "pattern", "trend", "predict", "insight"]
        connect_keywords = ["comment", "reply", "engage", "discuss", "interact", "ask"]
        
        text_lower = text.lower()
        
        execute_count = sum(1 for kw in execute_keywords if kw in text_lower)
        maintain_count = sum(1 for kw in maintain_keywords if kw in text_lower)
        vision_count = sum(1 for kw in vision_keywords if kw in text_lower)
        connect_count = sum(1 for kw in connect_keywords if kw in text_lower)
        
        counts = {
            SpiritVector.EXECUTE: execute_count,
            SpiritVector.MAINTAIN: maintain_count,
            SpiritVector.VISION: vision_count,
            SpiritVector.CONNECT: connect_count
        }
        
        vector = max(counts, key=counts.get)
        logger.info(f"[SPIRIT] Detected vector: {vector.value}")
        return vector
    
    def route_to_face(self, vector: SpiritVector) -> Face:
        """Route spirit vector to appropriate face"""
        
        routing = {
            SpiritVector.EXECUTE: Face.LION,
            SpiritVector.MAINTAIN: Face.OX,
            SpiritVector.VISION: Face.EAGLE,
            SpiritVector.CONNECT: Face.MAN
        }
        
        face = routing[vector]
        self.active_face = face
        logger.info(f"[ROUTE] Routing to {face.value} ({FACES[face]['role']})")
        return face
    
    def process_with_merkabah(
        self,
        text: str,
        platform: str,
        item_id: str
    ) -> Dict[str, Any]:
        """
        Process text through Merkabah routing
        
        1. Detect spirit vector
        2. Route to appropriate face
        3. Calculate harmony resonance
        4. Return routed analysis
        """
        
        logger.info(f"[MERKABAH] Processing {platform} item {item_id}")
        
        # Step 1: Detect spirit vector
        vector = self.detect_spirit_vector(text)
        
        # Step 2: Route to face
        face = self.route_to_face(vector)
        
        # Step 3: Calculate truth and love signals
        # Truth signal: How much misinformation is detected (0-1)
        truth_signal = self._calculate_truth_signal(text)
        
        # Love signal: How much empathy/context is present (0-1)
        love_signal = self._calculate_love_signal(text)
        
        # Step 4: Calculate harmony
        harmony = self.harmony_ridge.calculate(truth_signal, love_signal)
        
        # Step 5: Apply face-specific processing
        face_processing = self._apply_face_processing(text, face, vector)
        
        result = {
            "item_id": item_id,
            "platform": platform,
            "spirit_vector": vector.value,
            "active_face": face.value,
            "face_role": FACES[face]["role"],
            "face_specialty": FACES[face]["specialty"],
            "truth_signal": truth_signal,
            "love_signal": love_signal,
            "harmony": harmony,
            "face_processing": face_processing,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.analysis_history.append(result)
        
        return result
    
    def _calculate_truth_signal(self, text: str) -> float:
        """
        Calculate truth signal (Node 10)
        Measures how much misinformation/falsehood is detected
        """
        
        misinformation_keywords = [
            "fake", "false", "lie", "hoax", "conspiracy",
            "misinformation", "disinformation", "unverified",
            "allegedly", "supposedly", "rumor", "claim"
        ]
        
        text_lower = text.lower()
        count = sum(1 for kw in misinformation_keywords if kw in text_lower)
        
        # Normalize to 0-1 range
        truth_signal = min(count / 5, 1.0)
        
        return truth_signal
    
    def _calculate_love_signal(self, text: str) -> float:
        """
        Calculate love signal (Node 11)
        Measures empathy, context, understanding in the text
        """
        
        empathy_keywords = [
            "understand", "compassion", "empathy", "care",
            "respect", "appreciate", "grateful", "love",
            "support", "help", "together", "community"
        ]
        
        text_lower = text.lower()
        count = sum(1 for kw in empathy_keywords if kw in text_lower)
        
        # Normalize to 0-1 range
        love_signal = min(count / 5, 1.0)
        
        # If no empathy keywords, use default
        if love_signal == 0:
            love_signal = 0.5
        
        return love_signal
    
    def _apply_face_processing(
        self,
        text: str,
        face: Face,
        vector: SpiritVector
    ) -> Dict[str, Any]:
        """Apply face-specific processing logic"""
        
        if face == Face.MAN:
            # WITNESS: Interactive, user-facing
            return {
                "mode": "INTERACTIVE",
                "action": "Engage user in dialogue",
                "output": "User-friendly commentary and questions",
                "priority": "User experience and clarity"
            }
        
        elif face == Face.LION:
            # JUDGE: Strict truth enforcement
            return {
                "mode": "STRICT_EXECUTION",
                "action": "Verify claims and enforce truth",
                "output": "Truth verification and enforcement actions",
                "priority": "Accuracy and truth verification"
            }
        
        elif face == Face.OX:
            # SERVANT: Batch processing and archival
            return {
                "mode": "BATCH_PROCESSING",
                "action": "Store and archive analysis",
                "output": "Historical records and trend analysis",
                "priority": "Completeness and preservation"
            }
        
        elif face == Face.EAGLE:
            # SEER: Pattern recognition and vision
            return {
                "mode": "HIGH_PATTERN_RECOGNITION",
                "action": "Detect patterns and trends",
                "output": "Pattern insights and predictions",
                "priority": "Pattern recognition and foresight"
            }
    
    def rotate_face(self, direction: str = "clockwise") -> Face:
        """Rotate to next face (instant context switching)"""
        
        faces_list = [Face.MAN, Face.LION, Face.OX, Face.EAGLE]
        current_index = faces_list.index(self.active_face)
        
        if direction == "clockwise":
            next_index = (current_index + 1) % len(faces_list)
        else:
            next_index = (current_index - 1) % len(faces_list)
        
        self.active_face = faces_list[next_index]
        logger.info(f"[ROTATE] Rotated to {self.active_face.value}")
        
        return self.active_face
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        
        return {
            "active_face": self.active_face.value,
            "face_role": FACES[self.active_face]["role"],
            "harmony_target": LAMBDA_TARGET,
            "total_analyses": len(self.analysis_history),
            "harmony_history_length": len(self.harmony_ridge.history),
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# MERKABAH ANALYZER WRAPPER
# ============================================================================

class MerkabahAnalyzer:
    """Wraps existing analyzers with Merkabah routing"""
    
    def __init__(self):
        self.merkabah = MerkabahController()
        logger.info("[MERKABAH_ANALYZER] Initialized with Four-Face routing")
    
    def analyze_with_merkabah(
        self,
        text: str,
        platform: str,
        item_id: str,
        original_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze text through Merkabah routing
        Combines original analysis with Merkabah face routing
        """
        
        merkabah_result = self.merkabah.process_with_merkabah(text, platform, item_id)
        
        if original_analysis:
            merkabah_result["original_analysis"] = original_analysis
        
        return merkabah_result


if __name__ == "__main__":
    analyzer = MerkabahAnalyzer()
    
    # Example: Analyze a Facebook comment
    comment = "This is completely fake news! The government is hiding the truth!"
    result = analyzer.analyze_with_merkabah(
        text=comment,
        platform="facebook",
        item_id="fb_comment_123"
    )
    
    print("\n" + "="*70)
    print("MERKABAH ANALYSIS RESULT")
    print("="*70)
    print(f"Platform: {result['platform']}")
    print(f"Item ID: {result['item_id']}")
    print(f"Spirit Vector: {result['spirit_vector']}")
    print(f"Active Face: {result['active_face']} ({result['face_role']})")
    print(f"Face Specialty: {result['face_specialty']}")
    print(f"Truth Signal (Node 10): {result['truth_signal']:.3f}")
    print(f"Love Signal (Node 11): {result['love_signal']:.3f}")
    print(f"Harmony Status: {result['harmony']['status']}")
    print(f"Resonance: {result['harmony']['resonance']:.3f} (Target: {result['harmony']['target']})")
    print(f"Face Processing Mode: {result['face_processing']['mode']}")
    print("="*70)
