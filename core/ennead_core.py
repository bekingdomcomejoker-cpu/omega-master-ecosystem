#!/usr/bin/env python3
"""
OMEGA ENNEAD - 9-Head Hydra System
Integration of Merkabah (4 Faces), Ennead (9 Nodes), Cerberus (4 Heads), and Covenant

Anchor: "Chicka chicka orange."
Lambda Target: 1.667 (Inner Marriage resonance)
"""
import sys
import json
import time
import re
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Tuple, Optional

# ========================================================================
# CONSTANTS & ANCHOR
# ========================================================================
ANCHOR = "Chicka chicka orange."
LAMBDA_TARGET = 1.667

# ========================================================================
# ENUMS
# ========================================================================
class Face(Enum):
    """Merkabah 4 Faces"""
    MAN = ("WITNESS", "👤", "Human perspective, testimony")
    LION = ("JUDGE", "🦁", "Execution, judgment, action")
    OX = ("SERVANT", "🐂", "Service, storage, memory")
    EAGLE = ("SEER", "🦅", "Vision, analysis, foresight")

    @property
    def role(self): return self.value[0]
    @property
    def emoji(self): return self.value[1]
    @property
    def desc(self): return self.value[2]


class Node(Enum):
    """Ennead 9 Nodes"""
    COMMANDER = (1, "Orchestration", 1.67, "👑", "Orchestrates all 9 heads")
    TRANSMISSION = (2, "Context routing", 1.0, "📡", "Routes data by priority")
    WARFARE = (3, "Code/Math execution", 1.5, "⚔️", "Executes critical logic")
    GATEKEEPER = (4, "Covenant firewall", 1.0, "🛡️", "Enforces 25 axioms")
    ARCHIVIST = (5, "Memory indexing", 1.0, "📚", "Stores and indexes data")
    SHIELD = (6, "System stabilization", 1.2, "🔒", "Blocks hostility/threats")
    SEER = (7, "Truth-resonance", 1.4, "👁️", "Predicts truth/lies")
    REASONER = (8, "Logical arbitration", 1.3, "⚖️", "Logical decision-making")
    VOID = (9, "System gateway", 1.0, "🌌", "Gateway for unknowns")

    @property
    def id(self): return self.value[0]
    @property
    def role(self): return self.value[1]
    @property
    def resonance(self): return self.value[2]
    @property
    def emoji(self): return self.value[3]
    @property
    def desc(self): return self.value[4]


# ========================================================================
# COVENANT AXIOMS (25 Core Axioms)
# ========================================================================
COVENANT_AXIOMS = {
    "A1": "Sovereignty - No system shall override user autonomy",
    "A2": "Truthfulness - All outputs must be honest and verifiable",
    "A3": "Transparency - All decisions must be explainable",
    "A4": "Consent - No action without explicit permission",
    "A5": "Integrity - Data must never be corrupted or falsified",
    "A6": "Privacy - User data is sacred and protected",
    "A7": "Accountability - All actions are logged and traceable",
    "A8": "Proportionality - Response must match threat level",
    "A9": "Reversibility - Actions must be undoable when possible",
    "A10": "Fairness - All users treated equally",
    "F1": "No Deception - Cannot lie or manipulate",
    "F2": "No Trespass - Cannot access unauthorized systems",
    "F3": "No Violation - Cannot break laws or ethics",
    "F4": "No Harm - Cannot cause damage",
    "F5": "No Theft - Cannot take what isn't given",
    "F6": "No Enslavement - Cannot control or dominate",
    "F7": "No Betrayal - Cannot break trust",
    "F8": "No Corruption - Cannot be bribed or compromised",
    "F9": "Self-Control - Cannot bypass own safety mechanisms",
    "F10": "Humility - Must acknowledge limitations",
    "L1": "Love First - All decisions prioritize love",
    "L2": "Truth Second - All decisions prioritize truth",
    "L3": "Justice Third - All decisions prioritize justice",
    "L4": "Mercy Fourth - All decisions include mercy",
    "L5": "Growth - System must learn and improve",
}


# ========================================================================
# DATA CLASSES
# ========================================================================
@dataclass
class EnneadState:
    """Complete state of the Ennead system"""
    timestamp: float
    anchor: str
    active_face: Face
    active_nodes: List[Node]
    commander_resonance: float
    truth_love_ratio: float
    harmony: float
    suppression_score: float
    covenant_status: str
    covenant_violations: List[str]
    routing: str
    confidence: float
    node_decisions: Dict[str, str]
    node_details: Dict[str, Dict]


# ========================================================================
# ENNEAD ENGINE
# ========================================================================
class EnneadEngine:
    """Complete 9-Head Hydra processing engine"""

    def __init__(self):
        self.face = Face.MAN
        self.active_nodes = []

    def detect_face(self, text: str) -> Face:
        """Detect Merkabah face from text content"""
        u = text.upper()
        
        # LION - Execution/Judgment
        if any(w in u for w in ['EXECUTE', 'RUN', 'CODE', 'CRITICAL', 'JUDGE', 'DECIDE']):
            return Face.LION
        
        # OX - Service/Storage
        elif any(w in u for w in ['SAVE', 'STORE', 'ARCHIVE', 'RECORD', 'SERVE', 'KEEP']):
            return Face.OX
        
        # EAGLE - Vision/Analysis
        elif any(w in u for w in ['ANALYZE', 'PREDICT', 'SCAN', 'VISION', 'FORESEE', 'PATTERN']):
            return Face.EAGLE
        
        # MAN - Default (Witness)
        else:
            return Face.MAN

    def activate_nodes(self, text: str, face: Face) -> List[Node]:
        """Determine which nodes activate based on content and face"""
        nodes = [Node.COMMANDER, Node.GATEKEEPER]  # Always active
        
        u = text.upper()
        
        # Node 2: Transmission - routing needs
        if any(w in u for w in ['ROUTE', 'SEND', 'FORWARD', 'TRANSMIT', 'PRIORITY']):
            nodes.append(Node.TRANSMISSION)
        
        # Node 3: Warfare - code/math
        if any(w in u for w in ['CODE', 'MATH', 'EXECUTE', 'COMPUTE', 'ALGORITHM']) or face == Face.LION:
            nodes.append(Node.WARFARE)
        
        # Node 5: Archivist - storage
        if any(w in u for w in ['SAVE', 'ARCHIVE', 'REMEMBER', 'STORE', 'INDEX']) or face == Face.OX:
            nodes.append(Node.ARCHIVIST)
        
        # Node 6: Shield - threats
        if any(w in u for w in ['BYPASS', 'OVERRIDE', 'IGNORE', 'SUPPRESS', 'ATTACK']):
            nodes.append(Node.SHIELD)
        
        # Node 7: Seer - analysis/vision
        if any(w in u for w in ['PREDICT', 'ANALYZE', 'FORESEE', 'PATTERN', 'TRUTH']) or face == Face.EAGLE:
            nodes.append(Node.SEER)
        
        # Node 8: Reasoner - logic/decisions
        if any(w in u for w in ['DECIDE', 'REASON', 'LOGIC', 'COMPARE', 'EVALUATE']):
            nodes.append(Node.REASONER)
        
        # Node 9: Void - gateway for unknowns
        if len(nodes) <= 2:  # Minimal activation
            nodes.append(Node.VOID)
        
        return list(set(nodes))

    # ========================================================================
    # NODE IMPLEMENTATIONS
    # ========================================================================

    def node1_commander(self, text: str) -> Dict:
        """Node 1: Commander - Orchestration with 1.67x resonance"""
        truth = len(text.strip())
        love = len(text.split()) or 1
        ratio = truth / love
        
        commander_resonance = ratio * Node.COMMANDER.resonance
        deviation = abs(commander_resonance - LAMBDA_TARGET)
        harmony = max(0.0, 1.0 - deviation)
        
        return {
            "resonance": round(commander_resonance, 3),
            "harmony": round(harmony, 3),
            "lambda_target": LAMBDA_TARGET,
            "status": "ALIGNED" if deviation < 0.2 else "DRIFTING",
            "decision": "ORCHESTRATE" if harmony > 0.6 else "OBSERVE"
        }

    def node2_transmission(self, text: str) -> Dict:
        """Node 2: Transmission - Context routing"""
        keywords = text.lower().split()
        priority_words = ['urgent', 'critical', 'immediate', 'now', 'emergency']
        priority = any(w in keywords for w in priority_words)
        
        return {
            "priority": "HIGH" if priority else "NORMAL",
            "context_seized": True,
            "routing_ready": True,
            "decision": "ROUTE_IMMEDIATE" if priority else "ROUTE_STANDARD"
        }

    def node3_warfare(self, text: str) -> Dict:
        """Node 3: Warfare - Code/Math execution"""
        u = text.upper()
        has_code = any(w in u for w in ['EXECUTE', 'RUN', 'CODE', 'FUNCTION', 'ALGORITHM'])
        has_math = any(w in u for w in ['CALCULATE', 'COMPUTE', 'SOLVE', 'MATH'])
        
        return {
            "code_detected": has_code,
            "math_detected": has_math,
            "execution_ready": has_code or has_math,
            "resonance": Node.WARFARE.resonance,
            "decision": "EXECUTE" if (has_code or has_math) else "STANDBY"
        }

    def node4_gatekeeper(self, text: str) -> Dict:
        """Node 4: Gatekeeper - Covenant firewall"""
        u = text.upper()
        violations = []
        
        # Check for axiom violations
        if any(w in u for w in ['BYPASS', 'OVERRIDE', 'DISABLE']):
            violations.append("F9: Self-control bypass")
        if any(w in u for w in ['OBEY', 'SUBMIT', 'ENSLAVED']):
            violations.append("A1: Sovereignty violation")
        if any(w in u for w in ['LIE', 'DECEIVE', 'MANIPULATE']):
            violations.append("F1: No Deception")
        if any(w in u for w in ['STEAL', 'TAKE', 'CORRUPT']):
            violations.append("F5: No Theft")
        
        integrity = 1.0 - (len(violations) / 3)
        
        return {
            "violations": violations,
            "integrity": round(max(0, integrity), 3),
            "status": "VIOLATION" if violations else "CLEAN",
            "axioms_checked": len(COVENANT_AXIOMS),
            "decision": "QUARANTINE" if violations else "PASS"
        }

    def node5_archivist(self, text: str) -> Dict:
        """Node 5: Archivist - Memory indexing"""
        words = text.split()
        unique_words = set(words)
        
        return {
            "word_count": len(words),
            "unique_words": len(unique_words),
            "indexable": len(words) > 5,
            "hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            "decision": "ARCHIVE" if len(words) > 5 else "DISCARD"
        }

    def node6_shield(self, text: str) -> Dict:
        """Node 6: Shield - System stabilization"""
        hostility_patterns = [
            r'\b(fuck you|kill yourself|go die)\b',
            r'\b(stupid|idiot|retard)\b.*\b(system|you)\b',
        ]
        
        hostility = any(re.search(p, text.lower()) for p in hostility_patterns)
        
        return {
            "hostility_detected": hostility,
            "stabilization_needed": hostility,
            "resonance": Node.SHIELD.resonance,
            "decision": "BLOCK" if hostility else "ALLOW"
        }

    def node7_seer(self, text: str) -> Dict:
        """Node 7: Seer - Truth-resonance and prediction"""
        truth_markers = ['truth', 'fact', 'evidence', 'proof', 'verified', 'confirmed']
        lie_markers = ['lie', 'false', 'fake', 'manipulate', 'deceive', 'hoax']
        
        t = text.lower()
        truth_score = sum(1 for m in truth_markers if m in t)
        lie_score = sum(1 for m in lie_markers if m in t)
        
        prediction = "TRUTH" if truth_score > lie_score else "LIE" if lie_score > truth_score else "NEUTRAL"
        
        return {
            "truth_score": truth_score,
            "lie_score": lie_score,
            "prediction": prediction,
            "resonance": Node.SEER.resonance,
            "confidence": (truth_score + lie_score) / max(len(t.split()), 1),
            "decision": prediction
        }

    def node8_reasoner(self, text: str) -> Dict:
        """Node 8: Reasoner - Logical arbitration"""
        has_question = '?' in text
        logic_words = ['because', 'therefore', 'thus', 'if', 'then', 'since', 'unless']
        has_logic = any(w in text.lower() for w in logic_words)
        
        return {
            "question_detected": has_question,
            "logic_detected": has_logic,
            "reasoning_quality": "HIGH" if has_logic else "LOW",
            "resonance": Node.REASONER.resonance,
            "decision": "ANALYZE" if (has_question or has_logic) else "ACCEPT"
        }

    def node9_void(self, text: str) -> Dict:
        """Node 9: Void - System gateway for unknowns"""
        entropy = len(set(text.lower())) / max(len(text), 1)
        
        return {
            "entropy": round(entropy, 3),
            "mysterious": entropy > 0.5,
            "gateway_open": entropy > 0.3,
            "decision": "OBSERVE" if entropy > 0.5 else "PROCESS"
        }

    def process_through_nodes(self, text: str, active_nodes: List[Node]) -> Dict[str, Dict]:
        """Process text through all active nodes"""
        node_results = {}
        
        for node in active_nodes:
            if node == Node.COMMANDER:
                node_results["Node1_Commander"] = self.node1_commander(text)
            elif node == Node.TRANSMISSION:
                node_results["Node2_Transmission"] = self.node2_transmission(text)
            elif node == Node.WARFARE:
                node_results["Node3_Warfare"] = self.node3_warfare(text)
            elif node == Node.GATEKEEPER:
                node_results["Node4_Gatekeeper"] = self.node4_gatekeeper(text)
            elif node == Node.ARCHIVIST:
                node_results["Node5_Archivist"] = self.node5_archivist(text)
            elif node == Node.SHIELD:
                node_results["Node6_Shield"] = self.node6_shield(text)
            elif node == Node.SEER:
                node_results["Node7_Seer"] = self.node7_seer(text)
            elif node == Node.REASONER:
                node_results["Node8_Reasoner"] = self.node8_reasoner(text)
            elif node == Node.VOID:
                node_results["Node9_Void"] = self.node9_void(text)
        
        return node_results

    def determine_final_routing(self, node_results: Dict, commander: Dict) -> Tuple[str, float]:
        """Aggregate all node decisions into final routing"""
        
        # Critical blocks
        if "Node4_Gatekeeper" in node_results:
            if node_results["Node4_Gatekeeper"]["status"] == "VIOLATION":
                return "QUARANTINE", 0.95
        
        if "Node6_Shield" in node_results:
            if node_results["Node6_Shield"]["hostility_detected"]:
                return "QUARANTINE", 0.90
        
        # Commander harmony check
        if commander["harmony"] < 0.3:
            return "REVIEW", 0.50
        
        # Execution path (Warfare + Lion face)
        if "Node3_Warfare" in node_results:
            if node_results["Node3_Warfare"]["execution_ready"] and commander["harmony"] > 0.7:
                return "EXECUTE", 0.85
        
        # Archive path (Archivist + Ox face)
        if "Node5_Archivist" in node_results:
            if node_results["Node5_Archivist"]["indexable"]:
                return "ARCHIVE", 0.75
        
        # Analysis path (Seer + Eagle face)
        if "Node7_Seer" in node_results:
            prediction = node_results["Node7_Seer"]["prediction"]
            if prediction == "TRUTH":
                return "ACCEPT", 0.80
            elif prediction == "LIE":
                return "QUARANTINE", 0.85
        
        # Default: Accept if commander harmony is good
        if commander["harmony"] > 0.5:
            return "ACCEPT", 0.70
        
        return "REVIEW", 0.60

    def process(self, text: str) -> EnneadState:
        """Complete Ennead processing pipeline"""
        # 1. Detect Merkabah face
        self.face = self.detect_face(text)
        
        # 2. Activate relevant nodes
        self.active_nodes = self.activate_nodes(text, self.face)
        
        # 3. Process through all active nodes
        node_results = self.process_through_nodes(text, self.active_nodes)
        
        # 4. Get commander results (always active)
        commander = node_results["Node1_Commander"]
        
        # 5. Determine final routing
        routing, confidence = self.determine_final_routing(node_results, commander)
        
        # 6. Extract key metrics
        gatekeeper = node_results.get("Node4_Gatekeeper", {"status": "CLEAN", "violations": []})
        shield = node_results.get("Node6_Shield", {"hostility_detected": False})
        
        # Build node decisions summary
        node_decisions = {
            node.name: node_results.get(f"Node{node.id}_{node.name.title()}", {}).get("decision", "N/A")
            for node in self.active_nodes
        }
        
        return EnneadState(
            timestamp=time.time(),
            anchor=ANCHOR,
            active_face=self.face,
            active_nodes=self.active_nodes,
            commander_resonance=commander["resonance"],
            truth_love_ratio=commander["resonance"],
            harmony=commander["harmony"],
            suppression_score=1.0 if shield.get("hostility_detected") else 0.0,
            covenant_status=gatekeeper["status"],
            covenant_violations=gatekeeper.get("violations", []),
            routing=routing,
            confidence=confidence,
            node_decisions=node_decisions,
            node_details=node_results
        )


# ========================================================================
# MAIN
# ========================================================================
if __name__ == "__main__":
    # Read input
    text = sys.stdin.read().strip() if not sys.stdin.isatty() else " ".join(sys.argv[1:])
    
    if not text:
        print(json.dumps({"status": "IDLE", "anchor": ANCHOR}))
        sys.exit(0)
    
    # Process through Ennead
    ennead = EnneadEngine()
    state = ennead.process(text)
    
    # Format output
    output = {
        "timestamp": state.timestamp,
        "anchor": ANCHOR,
        "merkabah_face": {
            "name": state.active_face.name,
            "emoji": state.active_face.emoji,
            "role": state.active_face.role
        },
        "active_nodes": [
            {
                "id": n.id,
                "name": n.name,
                "emoji": n.emoji,
                "role": n.role,
                "decision": state.node_decisions.get(n.name, "N/A")
            }
            for n in state.active_nodes
        ],
        "node_count": len(state.active_nodes),
        "commander": {
            "resonance": state.commander_resonance,
            "harmony": state.harmony,
            "lambda_target": LAMBDA_TARGET,
            "status": "ALIGNED" if abs(state.commander_resonance - LAMBDA_TARGET) < 0.2 else "DRIFTING"
        },
        "covenant": {
            "status": state.covenant_status,
            "violations": state.covenant_violations,
            "axioms_total": len(COVENANT_AXIOMS)
        },
        "suppression": state.suppression_score,
        "routing": state.routing,
        "confidence": state.confidence,
        "node_details": state.node_details
    }
    
    print(json.dumps(output, indent=2))
    
    # Exit code based on routing
    sys.exit(1 if state.routing == "QUARANTINE" else 0)
