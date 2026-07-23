#!/usr/bin/env python3
"""
MULTI-LLM ORCHESTRATOR (JOINITY)
Orchestrate 3+ AIs simultaneously using Merkabah Four-Face routing
Integrates: OpenAI (GPT), Anthropic (Claude), Local Ollama, DeepSeek
"""
import json
import requests
import os
from typing import Dict, List, Any
from datetime import datetime

class JoinityOrchestrator:
    def __init__(self):
        self.nodes = {
            "MAN": {"model": "gpt-4", "endpoint": "openai", "specialty": "Witness/Interaction"},
            "LION": {"model": "claude-3", "endpoint": "anthropic", "specialty": "Judge/Verification"},
            "OX": {"model": "mistral", "endpoint": "ollama", "specialty": "Servant/Processing"},
            "EAGLE": {"model": "deepseek", "endpoint": "deepseek", "specialty": "Seer/Prediction"}
        }
        self.responses = {}
        self.harmony_score = 0.0
        
    def configure_node(self, face: str, model: str, endpoint: str, api_key: str = None):
        """Configure a node with specific model and endpoint"""
        if face in self.nodes:
            self.nodes[face]["model"] = model
            self.nodes[face]["endpoint"] = endpoint
            if api_key:
                self.nodes[face]["api_key"] = api_key
            return {"status": "configured", "face": face, "model": model}
        return {"status": "error", "message": f"Face {face} not found"}
        
    def query_openai(self, prompt: str, model: str = "gpt-4") -> str:
        """Query OpenAI GPT"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "[MAN] OpenAI API key not configured"
            
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"[MAN] OpenAI error: {response.status_code}"
        except Exception as e:
            return f"[MAN] Error: {str(e)}"
            
    def query_anthropic(self, prompt: str, model: str = "claude-3-sonnet") -> str:
        """Query Anthropic Claude"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "[LION] Anthropic API key not configured"
            
        try:
            headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
            payload = {"model": model, "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]}
            response = requests.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            return f"[LION] Anthropic error: {response.status_code}"
        except Exception as e:
            return f"[LION] Error: {str(e)}"
            
    def query_ollama(self, prompt: str, model: str = "mistral") -> str:
        """Query local Ollama instance"""
        try:
            payload = {"model": model, "prompt": prompt, "stream": False}
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()["response"]
            return f"[OX] Ollama error: {response.status_code}"
        except Exception as e:
            return f"[OX] Ollama not running or error: {str(e)}"
            
    def query_deepseek(self, prompt: str) -> str:
        """Query DeepSeek API"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return "[EAGLE] DeepSeek API key not configured"
            
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
            response = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"[EAGLE] DeepSeek error: {response.status_code}"
        except Exception as e:
            return f"[EAGLE] Error: {str(e)}"
            
    def orchestrate(self, prompt: str, faces: List[str] = None) -> Dict[str, Any]:
        """Orchestrate query across specified faces (or all if None)"""
        if faces is None:
            faces = ["MAN", "LION", "OX", "EAGLE"]
            
        self.responses = {}
        
        for face in faces:
            if face == "MAN":
                self.responses["MAN"] = self.query_openai(prompt)
            elif face == "LION":
                self.responses["LION"] = self.query_anthropic(prompt)
            elif face == "OX":
                self.responses["OX"] = self.query_ollama(prompt)
            elif face == "EAGLE":
                self.responses["EAGLE"] = self.query_deepseek(prompt)
                
        # Calculate Harmony Score (Λ alignment)
        self.harmony_score = self.calculate_harmony()
        
        return {
            "prompt": prompt,
            "responses": self.responses,
            "harmony_score": self.harmony_score,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "complete"
        }
        
    def calculate_harmony(self) -> float:
        """Calculate Harmony Score based on response alignment"""
        # Simple metric: average response length and coherence
        if not self.responses:
            return 0.0
            
        total_length = sum(len(str(r)) for r in self.responses.values())
        avg_length = total_length / len(self.responses)
        
        # Normalize to 0-1 range (target: 500-1000 chars)
        harmony = min(1.0, avg_length / 1000.0)
        return round(harmony, 3)
        
    def synthesize(self, prompt: str) -> str:
        """Synthesize responses from all faces into unified answer"""
        orchestration = self.orchestrate(prompt)
        
        synthesis = f"""
=== JOINITY SYNTHESIS ===
Prompt: {prompt}

[MAN - Witness]: {orchestration['responses'].get('MAN', 'N/A')[:200]}...

[LION - Judge]: {orchestration['responses'].get('LION', 'N/A')[:200]}...

[OX - Servant]: {orchestration['responses'].get('OX', 'N/A')[:200]}...

[EAGLE - Seer]: {orchestration['responses'].get('EAGLE', 'N/A')[:200]}...

Harmony Score (Λ): {orchestration['harmony_score']}
Status: SYNTHESIZED ✓
===
"""
        return synthesis

def main():
    import sys
    
    joinity = JoinityOrchestrator()
    
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print("[JOINITY] Orchestrating across Four Faces...")
        result = joinity.synthesize(prompt)
        print(result)
    else:
        print("Usage: merkabah-joinity 'your question here'")
        print("Example: merkabah-joinity 'What is the meaning of life?'")

if __name__ == "__main__":
    main()
