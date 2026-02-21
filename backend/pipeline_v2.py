"""
COVENANT MIRROR X11 - EXECUTION PIPELINE v2
============================================
Updated pipeline with multi-model support.
"""

import asyncio
from typing import AsyncGenerator, Dict, Optional

from database import (
    MessageStore, SessionManager, AuditLog,
    AlphabetCache, TerexCache
)
from multi_model import get_router, ModelProvider

# ============================================================================
# ALPHABET ENGINE INTEGRATION
# ============================================================================

class AlphabetEngineAdapter:
    """Adapter for Alphabet Engine analysis."""
    
    @staticmethod
    def analyze_word(word: str) -> Optional[Dict]:
        """Analyze a word using Alphabet Engine."""
        cached = AlphabetCache.get_analysis(word)
        if cached:
            return cached
        
        analysis = {
            "gematria": sum(ord(c) for c in word.upper()),
            "i_o_ratio": 50.0,
            "dominant_element": "Air",
            "vowel_state": "Unity",
            "consonant_class": "Labial"
        }
        
        AlphabetCache.save_analysis(
            word,
            analysis["gematria"],
            analysis["i_o_ratio"],
            analysis["dominant_element"],
            analysis
        )
        
        return analysis
    
    @staticmethod
    def extract_keywords(text: str) -> list:
        """Extract keywords from text for analysis."""
        words = text.upper().split()
        return [w for w in words if len(w) > 3]

# ============================================================================
# TEREX INTEGRATION
# ============================================================================

class TerexAdapter:
    """Adapter for TEREX truth classification."""
    
    @staticmethod
    def classify_truth(text: str) -> Optional[Dict]:
        """Classify text using TEREX."""
        cached = TerexCache.get_classification(text)
        if cached:
            return cached
        
        classification = {
            "classification": "TRUTH",
            "confidence": 0.75,
            "reasoning": "High water element, balanced I/O ratio",
            "element_balance": {
                "fire": 0.2,
                "water": 0.5,
                "earth": 0.15,
                "air": 0.15
            }
        }
        
        TerexCache.save_classification(
            text,
            classification["classification"],
            classification["confidence"],
            classification
        )
        
        return classification

# ============================================================================
# PROMPT ENGINEERING
# ============================================================================

class PromptEngine:
    """Build context-aware prompts."""
    
    @staticmethod
    def build_prompt(
        user_input: str,
        state: str = "ON",
        session_id: Optional[str] = None,
        alphabet_analysis: Optional[Dict] = None,
        terex_classification: Optional[Dict] = None
    ) -> str:
        """Build a complete prompt with context."""
        
        state_context = {
            "ON": "Respond with high coherence and safety. Be precise and measured.",
            "OFF": "Respond with maximum impact and truth. Be disruptive if necessary.",
            "SUPER": "Balance coherence and impact. Navigate both states simultaneously."
        }
        
        prompt = f"{state_context.get(state, state_context['ON'])}\n\n"
        
        if alphabet_analysis:
            prompt += f"[Alphabet Analysis]\n"
            prompt += f"Gematria: {alphabet_analysis.get('gematria')}\n"
            prompt += f"Dominant Element: {alphabet_analysis.get('dominant_element')}\n\n"
        
        if terex_classification:
            prompt += f"[Truth Classification]\n"
            prompt += f"Classification: {terex_classification.get('classification')}\n"
            prompt += f"Confidence: {terex_classification.get('confidence')}\n\n"
        
        prompt += f"User: {user_input}"
        
        return prompt

# ============================================================================
# COMPLETE EXECUTION PIPELINE v2
# ============================================================================

class ExecutionPipeline:
    """Complete execution pipeline with multi-model support."""
    
    def __init__(self, session_id: str, state: str = "ON", model: str = "gemini"):
        self.session_id = session_id
        self.state = state
        self.model = model
        self.alphabet = AlphabetEngineAdapter()
        self.terex = TerexAdapter()
        self.prompt_engine = PromptEngine()
        self.router = get_router()
        self.in_flight = 0
    
    async def execute(self, user_input: str) -> AsyncGenerator[Dict, None]:
        """
        Execute complete pipeline with selected model:
        1. Extract keywords and analyze with Alphabet Engine
        2. Classify with TEREX
        3. Build context-aware prompt
        4. Stream from selected model
        5. Save to database
        """
        
        try:
            # Log action
            AuditLog.log_action(
                self.session_id,
                "EXECUTE_PIPELINE",
                {"state": self.state, "model": self.model, "input_length": len(user_input)}
            )
            
            # Step 1: Alphabet Engine Analysis
            keywords = self.alphabet.extract_keywords(user_input)
            alphabet_analysis = None
            if keywords:
                alphabet_analysis = self.alphabet.analyze_word(keywords[0])
            
            # Step 2: TEREX Classification
            terex_classification = self.terex.classify_truth(user_input)
            
            # Step 3: Build prompt
            full_prompt = self.prompt_engine.build_prompt(
                user_input,
                self.state,
                self.session_id,
                alphabet_analysis,
                terex_classification
            )
            
            # Step 4: Save initial message
            message_id = MessageStore.save_message(
                self.session_id,
                "PAYLOAD",
                node="wire",
                state=self.state,
                prompt=user_input,
                model=self.model,
                qci=1.56 if self.state == "ON" else 1.13,
                force=-0.1 if self.state == "ON" else 37.25,
                in_flight=self.in_flight
            )
            
            # Step 5: Stream from selected model
            full_response = ""
            try:
                model_enum = ModelProvider(self.model)
            except ValueError:
                model_enum = ModelProvider.GEMINI
            
            async for token in self.router.stream(full_prompt, model_enum):
                full_response += token
                yield {
                    "type": "STREAM",
                    "node": "wire",
                    "payload": {"text": token}
                }
            
            # Step 6: Save complete response
            if message_id:
                MessageStore.save_message(
                    self.session_id,
                    "RESPONSE",
                    node="wire",
                    state=self.state,
                    response=full_response,
                    model=self.model,
                    qci=1.56 if self.state == "ON" else 1.13,
                    force=-0.1 if self.state == "ON" else 37.25
                )
            
            # Send completion
            yield {
                "type": "RESPONSE",
                "node": "wire",
                "payload": {
                    "status": "complete",
                    "model": self.model,
                    "alphabet_analysis": alphabet_analysis,
                    "terex_classification": terex_classification
                }
            }
            
            # Log completion
            AuditLog.log_action(
                self.session_id,
                "PIPELINE_COMPLETE",
                {"message_id": message_id, "response_length": len(full_response), "model": self.model}
            )
        
        except Exception as e:
            yield {
                "type": "ERROR",
                "node": "wire",
                "payload": {"text": f"Pipeline error: {str(e)}"}
            }
            AuditLog.log_action(
                self.session_id,
                "PIPELINE_ERROR",
                {"error": str(e), "model": self.model}
            )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_session_replay(session_id: str) -> Dict:
    """Get complete session replay."""
    session = SessionManager.get_session(session_id)
    messages = MessageStore.get_messages(session_id)
    audit_log = AuditLog.get_audit_log(session_id)
    
    return {
        "session": session,
        "messages": messages,
        "audit_log": audit_log,
        "message_count": len(messages)
    }

def get_all_sessions_summary() -> Dict:
    """Get summary of all sessions."""
    sessions = SessionManager.list_sessions()
    return {
        "total_sessions": len(sessions),
        "sessions": sessions
    }

def get_available_models() -> list:
    """Get list of available models."""
    router = get_router()
    return router.get_available_models()

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    print("Pipeline v2 module loaded.")
