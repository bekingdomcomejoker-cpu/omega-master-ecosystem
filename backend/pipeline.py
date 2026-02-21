"""
COVENANT MIRROR X11 - EXECUTION PIPELINE
=========================================
Complete backend pipeline with Gemini, Alphabet Engine, and TEREX integration.
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
from datetime import datetime
import google.generativeai as genai

from database import (
    MessageStore, SessionManager, AuditLog,
    AlphabetCache, TerexCache
)

# ============================================================================
# CONFIGURATION
# ============================================================================

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Overload Governor
MAX_IN_FLIGHT = 4
in_flight = 0

# ============================================================================
# ALPHABET ENGINE INTEGRATION
# ============================================================================

class AlphabetEngineAdapter:
    """Adapter for Alphabet Engine analysis."""
    
    @staticmethod
    def analyze_word(word: str) -> Optional[Dict]:
        """
        Analyze a word using Alphabet Engine.
        
        This is a stub that can be connected to the actual Alphabet Engine.
        For now, it returns mock data and caches results.
        """
        # Check cache first
        cached = AlphabetCache.get_analysis(word)
        if cached:
            return cached
        
        # Mock analysis (replace with actual Alphabet Engine call)
        analysis = {
            "gematria": sum(ord(c) for c in word.upper()),
            "i_o_ratio": 50.0,  # Placeholder
            "dominant_element": "Air",  # Placeholder
            "vowel_state": "Unity",
            "consonant_class": "Labial"
        }
        
        # Cache result
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
        # Simple keyword extraction (can be enhanced)
        words = text.upper().split()
        return [w for w in words if len(w) > 3]

# ============================================================================
# TEREX INTEGRATION
# ============================================================================

class TerexAdapter:
    """Adapter for TEREX truth classification."""
    
    @staticmethod
    def classify_truth(text: str) -> Optional[Dict]:
        """
        Classify text using TEREX.
        
        This is a stub that can be connected to the actual TEREX system.
        For now, it returns mock data and caches results.
        """
        # Check cache first
        cached = TerexCache.get_classification(text)
        if cached:
            return cached
        
        # Mock classification (replace with actual TEREX call)
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
        
        # Cache result
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
        
        # State context
        state_context = {
            "ON": "Respond with high coherence and safety. Be precise and measured.",
            "OFF": "Respond with maximum impact and truth. Be disruptive if necessary.",
            "SUPER": "Balance coherence and impact. Navigate both states simultaneously."
        }
        
        prompt = f"{state_context.get(state, state_context['ON'])}\n\n"
        
        # Add alphabet analysis if available
        if alphabet_analysis:
            prompt += f"[Alphabet Analysis]\n"
            prompt += f"Gematria: {alphabet_analysis.get('gematria')}\n"
            prompt += f"Dominant Element: {alphabet_analysis.get('dominant_element')}\n\n"
        
        # Add TEREX classification if available
        if terex_classification:
            prompt += f"[Truth Classification]\n"
            prompt += f"Classification: {terex_classification.get('classification')}\n"
            prompt += f"Confidence: {terex_classification.get('confidence')}\n\n"
        
        # User input
        prompt += f"User: {user_input}"
        
        return prompt

# ============================================================================
# GEMINI STREAMING
# ============================================================================

class GeminiAdapter:
    """Adapter for Gemini API."""
    
    @staticmethod
    async def stream_response(prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from Gemini."""
        try:
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                await asyncio.sleep(0)  # Allow other tasks
        except Exception as e:
            yield f"\n[ERROR: {str(e)}]"

# ============================================================================
# COMPLETE EXECUTION PIPELINE
# ============================================================================

class ExecutionPipeline:
    """Complete execution pipeline with all integrations."""
    
    def __init__(self, session_id: str, state: str = "ON"):
        self.session_id = session_id
        self.state = state
        self.alphabet = AlphabetEngineAdapter()
        self.terex = TerexAdapter()
        self.prompt_engine = PromptEngine()
        self.gemini = GeminiAdapter()
    
    async def execute(self, user_input: str) -> AsyncGenerator[Dict, None]:
        """
        Execute complete pipeline:
        1. Extract keywords and analyze with Alphabet Engine
        2. Classify with TEREX
        3. Build context-aware prompt
        4. Stream from Gemini
        5. Save to database
        """
        
        global in_flight
        
        # Check overload
        if in_flight >= MAX_IN_FLIGHT:
            yield {
                "type": "ERROR",
                "payload": {"text": "[OVERLOAD: System throttled]"}
            }
            return
        
        in_flight += 1
        message_id = None
        
        try:
            # Log action
            AuditLog.log_action(
                self.session_id,
                "EXECUTE_PIPELINE",
                {"state": self.state, "input_length": len(user_input)}
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
                model="gemini",
                qci=1.56 if self.state == "ON" else 1.13,
                force=-0.1 if self.state == "ON" else 37.25,
                in_flight=in_flight
            )
            
            # Step 5: Stream from Gemini
            full_response = ""
            async for token in self.gemini.stream_response(full_prompt):
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
                    model="gemini",
                    qci=1.56 if self.state == "ON" else 1.13,
                    force=-0.1 if self.state == "ON" else 37.25
                )
            
            # Send completion
            yield {
                "type": "RESPONSE",
                "node": "wire",
                "payload": {
                    "status": "complete",
                    "alphabet_analysis": alphabet_analysis,
                    "terex_classification": terex_classification
                }
            }
            
            # Log completion
            AuditLog.log_action(
                self.session_id,
                "PIPELINE_COMPLETE",
                {"message_id": message_id, "response_length": len(full_response)}
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
                {"error": str(e)}
            )
        
        finally:
            in_flight -= 1

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

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    print("Pipeline module loaded.")
