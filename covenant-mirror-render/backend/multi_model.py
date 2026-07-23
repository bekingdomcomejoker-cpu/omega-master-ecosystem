"""
COVENANT MIRROR X11 - MULTI-MODEL SUPPORT
==========================================
Support for Gemini, Claude, GPT, and DeepSeek with unified interface.
"""

import os
import asyncio
from typing import AsyncGenerator, Optional
from enum import Enum

import google.generativeai as genai

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

class ModelProvider(str, Enum):
    """Supported AI model providers."""
    GEMINI = "gemini"
    CLAUDE = "claude"
    GPT = "gpt"
    DEEPSEEK = "deepseek"

# ============================================================================
# GEMINI ADAPTER
# ============================================================================

class GeminiAdapter:
    """Adapter for Google Gemini API."""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from Gemini."""
        try:
            response = self.model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                await asyncio.sleep(0)
        except Exception as e:
            yield f"\n[GEMINI ERROR: {str(e)}]"

# ============================================================================
# CLAUDE ADAPTER
# ============================================================================

class ClaudeAdapter:
    """Adapter for Anthropic Claude API."""
    
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            self.available = False
            return
        self.available = True
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            self.available = False
    
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from Claude."""
        if not self.available:
            yield "[CLAUDE: Not configured. Set CLAUDE_API_KEY environment variable.]"
            return
        
        try:
            with self.client.messages.stream(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    await asyncio.sleep(0)
        except Exception as e:
            yield f"\n[CLAUDE ERROR: {str(e)}]"

# ============================================================================
# GPT ADAPTER
# ============================================================================

class GPTAdapter:
    """Adapter for OpenAI GPT API."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.available = False
            return
        self.available = True
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            self.available = False
    
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from GPT."""
        if not self.available:
            yield "[GPT: Not configured. Set OPENAI_API_KEY environment variable.]"
            return
        
        try:
            with self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            ) as response:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                        await asyncio.sleep(0)
        except Exception as e:
            yield f"\n[GPT ERROR: {str(e)}]"

# ============================================================================
# DEEPSEEK ADAPTER
# ============================================================================

class DeepSeekAdapter:
    """Adapter for DeepSeek API (OpenAI-compatible)."""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            self.available = False
            return
        self.available = True
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
        except ImportError:
            self.available = False
    
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from DeepSeek."""
        if not self.available:
            yield "[DEEPSEEK: Not configured. Set DEEPSEEK_API_KEY environment variable.]"
            return
        
        try:
            with self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            ) as response:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                        await asyncio.sleep(0)
        except Exception as e:
            yield f"\n[DEEPSEEK ERROR: {str(e)}]"

# ============================================================================
# UNIFIED MODEL ROUTER
# ============================================================================

class ModelRouter:
    """Route requests to appropriate model provider."""
    
    def __init__(self):
        self.gemini = GeminiAdapter()
        self.claude = ClaudeAdapter()
        self.gpt = GPTAdapter()
        self.deepseek = DeepSeekAdapter()
    
    async def stream(
        self,
        prompt: str,
        model: ModelProvider = ModelProvider.GEMINI
    ) -> AsyncGenerator[str, None]:
        """Stream response from selected model."""
        
        if model == ModelProvider.GEMINI:
            async for token in self.gemini.stream(prompt):
                yield token
        
        elif model == ModelProvider.CLAUDE:
            async for token in self.claude.stream(prompt):
                yield token
        
        elif model == ModelProvider.GPT:
            async for token in self.gpt.stream(prompt):
                yield token
        
        elif model == ModelProvider.DEEPSEEK:
            async for token in self.deepseek.stream(prompt):
                yield token
        
        else:
            yield f"[ERROR: Unknown model {model}]"
    
    def get_available_models(self) -> list:
        """Get list of available models."""
        available = ["gemini"]  # Gemini is always available
        
        if self.claude.available:
            available.append("claude")
        if self.gpt.available:
            available.append("gpt")
        if self.deepseek.available:
            available.append("deepseek")
        
        return available

# ============================================================================
# MULTI-MODEL COMPARISON
# ============================================================================

class MultiModelComparison:
    """Compare responses from multiple models."""
    
    def __init__(self, router: ModelRouter):
        self.router = router
    
    async def compare(
        self,
        prompt: str,
        models: Optional[list] = None
    ) -> dict:
        """Get responses from multiple models."""
        
        if models is None:
            models = self.router.get_available_models()
        
        results = {}
        
        for model_name in models:
            try:
                model = ModelProvider(model_name)
                response = ""
                async for token in self.router.stream(prompt, model):
                    response += token
                results[model_name] = {
                    "status": "success",
                    "response": response
                }
            except Exception as e:
                results[model_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results

# ============================================================================
# INITIALIZATION
# ============================================================================

# Global router instance
_router = None

def get_router() -> ModelRouter:
    """Get global model router instance."""
    global _router
    if _router is None:
        _router = ModelRouter()
    return _router

if __name__ == "__main__":
    print("Multi-model support module loaded.")
