from core.pipeline.witness import SocraticWitness
from core.pipeline.logician import PlatonicLogician
from core.pipeline.judge import AristotelianJudge
from core.wire import DynamicWire

class JoinityEngine:
    def __init__(self):
        self.witness = SocraticWitness()
        self.logician = PlatonicLogician()
        self.judge = AristotelianJudge()
        self.wire = DynamicWire()

    def metabolize_data(self, intent: str):
        # Phase Transition: From Processing to Resonating
        seed = self.witness.expand_intent(intent)
        logic = self.logician.harden_logic(seed)
        result = self.judge.consecrate_knowledge(logic['logical_skeleton'], logic['coherence_stability'])
        
        return {
            "status": "CONSECRATED" if result['verified'] else "ONTOLOGICAL_DRIFT",
            "consecrated_knowledge": result['output'],
            "proof_ticket": result['proof_state_ticket'],
            "wire_log": self.wire.transmit(result['output'])
        }
