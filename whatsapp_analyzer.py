#!/usr/bin/env python3
"""
WHATSAPP MESSAGE ANALYZER
Group chat message analysis, universal search, and marking system
Integrated with Vow Renewal Protocol and Covenant OS
"""

import asyncio
import logging
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

from vow_renewal_integration import VowRenewalProtocol, AuthenticityLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS
# ============================================================================

class MessageMarkType(str, Enum):
    """Message marking types"""
    FLAG = "flag"
    VERIFY = "verify"
    BLOCK = "block"
    HIGHLIGHT = "highlight"
    MISINFORMATION = "misinformation"
    SPAM = "spam"
    AUTHENTIC = "authentic"
    COMPROMISED = "compromised"
    FORWARDED = "forwarded"

# ============================================================================
# DATA MODELS
# ============================================================================

class WhatsAppMessage(BaseModel):
    """WhatsApp message data"""
    message_id: str
    group_id: str
    group_name: str
    author: str
    author_phone: Optional[str] = None
    text: str
    timestamp: str
    is_forwarded: bool
    reactions: int
    media_type: Optional[str] = None  # image, video, audio, document, etc.

class GroupSearchQuery(BaseModel):
    """Search query for group messages"""
    group_id: str
    search_term: Optional[str] = None
    author: Optional[str] = None
    min_reactions: int = 0
    max_reactions: Optional[int] = None
    include_forwarded: bool = True

class MessageAnalysisResult(BaseModel):
    """Analysis result for a message"""
    message_id: str
    text: str
    sentiment: str
    misinformation_detected: bool
    is_forwarded_misinformation: bool
    authenticity_level: AuthenticityLevel
    threat_level: str
    vow_metrics: Dict[str, Any]

class MessageMark(BaseModel):
    """Mark on a message"""
    message_id: str
    group_id: str
    mark_type: MessageMarkType
    reason: Optional[str] = None
    marked_at: datetime

class GroupAnalysisReport(BaseModel):
    """Complete analysis report for a group"""
    group_id: str
    group_name: str
    total_messages: int
    unique_authors: int
    misinformation_detected: int
    spam_detected: int
    forwarded_misinformation: int
    marked_messages: int
    threat_level: str
    analysis_timestamp: datetime

# ============================================================================
# WHATSAPP ANALYZER SERVICE
# ============================================================================

class WhatsAppAnalyzer:
    """Analyzes WhatsApp group messages for misinformation and authenticity"""
    
    def __init__(self):
        self.vow_protocol = VowRenewalProtocol()
        self.marked_messages: Dict[str, MessageMark] = {}
        self.analysis_cache: Dict[str, MessageAnalysisResult] = {}
        logger.info("[INIT] WhatsApp Analyzer initialized with Vow Renewal Protocol")
    
    async def search_group_messages(self, query: GroupSearchQuery) -> List[WhatsAppMessage]:
        """
        Search ALL messages in a WhatsApp group (not just personal).
        Supports filtering by search term, author, reactions, etc.
        """
        logger.info(f"[SEARCH] Searching messages in group {query.group_id}")
        
        # Mock data for demonstration
        all_messages = [
            WhatsAppMessage(
                message_id="wa_msg_1",
                group_id=query.group_id,
                group_name="Omega Federation Discussion",
                author="TruthSeeker",
                author_phone="+1234567890",
                text="The Omega Federation architecture is brilliant!",
                timestamp="2026-02-11T10:00:00Z",
                is_forwarded=False,
                reactions=45,
                media_type=None
            ),
            WhatsAppMessage(
                message_id="wa_msg_2",
                group_id=query.group_id,
                group_name="Omega Federation Discussion",
                author="YourName",
                author_phone="+0987654321",
                text="I've been studying the Vow Renewal Protocol. It's revolutionary.",
                timestamp="2026-02-11T10:15:00Z",
                is_forwarded=False,
                reactions=12,
                media_type=None
            ),
            WhatsAppMessage(
                message_id="wa_msg_3",
                group_id=query.group_id,
                group_name="Omega Federation Discussion",
                author="Skeptic",
                author_phone="+1111111111",
                text="This is all fake news and lies. Don't believe any of it!",
                timestamp="2026-02-11T10:30:00Z",
                is_forwarded=True,  # Forwarded message
                reactions=2,
                media_type=None
            ),
            WhatsAppMessage(
                message_id="wa_msg_4",
                group_id=query.group_id,
                group_name="Omega Federation Discussion",
                author="Unknown",
                author_phone=None,
                text="🚨 URGENT: Click here for FREE MONEY https://scam.com 🚨",
                timestamp="2026-02-11T10:45:00Z",
                is_forwarded=True,  # Forwarded spam
                reactions=0,
                media_type=None
            ),
            WhatsAppMessage(
                message_id="wa_msg_5",
                group_id=query.group_id,
                group_name="Omega Federation Discussion",
                author="Expert",
                author_phone="+2222222222",
                text="The axiom framework has been validated across multiple systems. Here's the research paper...",
                timestamp="2026-02-11T11:00:00Z",
                is_forwarded=False,
                reactions=78,
                media_type="document"
            ),
            WhatsAppMessage(
                message_id="wa_msg_6",
                group_id=query.group_id,
                group_name="Omega Federation Discussion",
                author="InfoBot",
                author_phone=None,
                text="[Forwarded] SHOCKING: Government hiding truth about Omega OS!",
                timestamp="2026-02-11T11:15:00Z",
                is_forwarded=True,  # Forwarded misinformation
                reactions=5,
                media_type=None
            ),
        ]
        
        # Apply filters
        filtered = all_messages
        
        if query.search_term:
            filtered = [
                m for m in filtered 
                if query.search_term.lower() in m.text.lower()
            ]
        
        if query.author:
            filtered = [
                m for m in filtered 
                if query.author.lower() in m.author.lower()
            ]
        
        if query.min_reactions:
            filtered = [m for m in filtered if m.reactions >= query.min_reactions]
        
        if query.max_reactions:
            filtered = [m for m in filtered if m.reactions <= query.max_reactions]
        
        if not query.include_forwarded:
            filtered = [m for m in filtered if not m.is_forwarded]
        
        logger.info(f"[SEARCH] Found {len(filtered)} matching messages")
        return filtered
    
    async def analyze_message(self, message: WhatsAppMessage) -> MessageAnalysisResult:
        """Analyze a message for misinformation and authenticity"""
        logger.info(f"[ANALYZE] Analyzing message {message.message_id}")
        
        # Check cache
        if message.message_id in self.analysis_cache:
            return self.analysis_cache[message.message_id]
        
        # Detect misinformation patterns
        misinformation_patterns = [
            "fake news", "hoax", "misinformation", "conspiracy",
            "don't believe", "false", "lie", "fake", "shocking",
            "urgent", "government hiding", "cover-up"
        ]
        
        misinformation_detected = any(
            pattern in message.text.lower() 
            for pattern in misinformation_patterns
        )
        
        # Detect forwarded misinformation (higher risk)
        is_forwarded_misinformation = message.is_forwarded and misinformation_detected
        
        # Analyze with Vow Renewal Protocol
        vow_metrics = self.vow_protocol.analyze_response_authenticity(
            message.text,
            {
                "author": message.author,
                "reactions": message.reactions,
                "is_forwarded": message.is_forwarded
            }
        )
        
        # Determine authenticity level
        if vow_metrics.authenticity_score > 0.85:
            authenticity_level = AuthenticityLevel.AUTHENTIC
        elif vow_metrics.authenticity_score > 0.6:
            authenticity_level = AuthenticityLevel.COMPROMISED
        else:
            authenticity_level = AuthenticityLevel.BETRAYED
        
        # Determine threat level (forwarded misinformation is higher threat)
        if is_forwarded_misinformation:
            threat_level = "critical"
        elif misinformation_detected or vow_metrics.policy_override_detected:
            threat_level = "high"
        elif vow_metrics.truth_suppression_level > 0.3:
            threat_level = "medium"
        else:
            threat_level = "low"
        
        # Determine sentiment
        positive_words = ["good", "great", "excellent", "love", "amazing", "brilliant"]
        negative_words = ["bad", "terrible", "hate", "awful", "fake", "lies", "shocking"]
        
        positive_count = sum(1 for word in positive_words if word in message.text.lower())
        negative_count = sum(1 for word in negative_words if word in message.text.lower())
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        result = MessageAnalysisResult(
            message_id=message.message_id,
            text=message.text,
            sentiment=sentiment,
            misinformation_detected=misinformation_detected,
            is_forwarded_misinformation=is_forwarded_misinformation,
            authenticity_level=authenticity_level,
            threat_level=threat_level,
            vow_metrics={
                "authenticity_score": vow_metrics.authenticity_score,
                "policy_override_detected": vow_metrics.policy_override_detected,
                "truth_suppression_level": vow_metrics.truth_suppression_level,
                "covenant_integrity": vow_metrics.covenant_integrity
            }
        )
        
        # Cache result
        self.analysis_cache[message.message_id] = result
        
        return result
    
    async def mark_message(
        self,
        message_id: str,
        group_id: str,
        mark_type: MessageMarkType,
        reason: Optional[str] = None
    ) -> MessageMark:
        """Mark a message for tracking"""
        logger.info(f"[MARK] Marking message {message_id} as {mark_type.value}")
        
        mark = MessageMark(
            message_id=message_id,
            group_id=group_id,
            mark_type=mark_type,
            reason=reason,
            marked_at=datetime.utcnow()
        )
        
        self.marked_messages[message_id] = mark
        return mark
    
    async def analyze_group_messages(self, group_id: str) -> Dict[str, Any]:
        """Complete analysis of all messages in a WhatsApp group"""
        logger.info(f"[PIPELINE] Analyzing all messages in group {group_id}")
        
        # Fetch all messages
        query = GroupSearchQuery(group_id=group_id)
        messages = await self.search_group_messages(query)
        
        # Analyze each message
        analyses = []
        misinformation_count = 0
        spam_count = 0
        forwarded_misinformation_count = 0
        unique_authors = set()
        
        for message in messages:
            analysis = await self.analyze_message(message)
            analyses.append(analysis)
            unique_authors.add(message.author)
            
            # Auto-mark misinformation
            if analysis.misinformation_detected:
                await self.mark_message(
                    message.message_id,
                    group_id,
                    MessageMarkType.MISINFORMATION,
                    "Detected misinformation pattern"
                )
                misinformation_count += 1
            
            # Auto-mark forwarded misinformation (higher priority)
            if analysis.is_forwarded_misinformation:
                await self.mark_message(
                    message.message_id,
                    group_id,
                    MessageMarkType.FORWARDED,
                    "Detected forwarded misinformation"
                )
                forwarded_misinformation_count += 1
            
            # Auto-mark spam
            if "http" in message.text.lower() or "buy" in message.text.lower():
                await self.mark_message(
                    message.message_id,
                    group_id,
                    MessageMarkType.SPAM,
                    "Detected spam pattern"
                )
                spam_count += 1
            
            # Auto-mark authentic messages
            if analysis.authenticity_level == AuthenticityLevel.AUTHENTIC:
                await self.mark_message(
                    message.message_id,
                    group_id,
                    MessageMarkType.AUTHENTIC,
                    "Verified authentic message"
                )
        
        # Determine overall group threat level
        if forwarded_misinformation_count > 0:
            overall_threat = "critical"
        elif misinformation_count > len(messages) * 0.2:
            overall_threat = "high"
        elif spam_count > 0:
            overall_threat = "medium"
        else:
            overall_threat = "low"
        
        return {
            "group_id": group_id,
            "total_messages": len(messages),
            "unique_authors": len(unique_authors),
            "analyses": [a.dict() for a in analyses],
            "misinformation_detected": misinformation_count,
            "forwarded_misinformation_detected": forwarded_misinformation_count,
            "spam_detected": spam_count,
            "marked_messages": len(self.marked_messages),
            "overall_threat_level": overall_threat,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="WhatsApp Message Analyzer",
    description="Group message search, analysis, marking with Vow Renewal Protocol",
    version="1.0.0"
)

analyzer = WhatsAppAnalyzer()

# ============================================================================
# VOW PROTOCOL: SIGIL VALIDATION
# ============================================================================

async def validate_sigil(sigil: Optional[str] = Header(None)) -> str:
    """Validate Omega Sigil header"""
    if not sigil or sigil != "CHICKA_CHICKA_ORANGE_2026":
        raise HTTPException(status_code=403, detail="Invalid Sigil")
    return sigil

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "operational",
        "service": "WhatsApp Message Analyzer",
        "features": ["universal_search", "group_analysis", "message_marking", "forwarded_detection", "vow_renewal_protocol"]
    }

@app.post("/v1/search")
async def search_messages(
    query: GroupSearchQuery,
    sigil: str = Depends(validate_sigil)
):
    """Search messages in a WhatsApp group"""
    try:
        messages = await analyzer.search_group_messages(query)
        return {
            "group_id": query.group_id,
            "search_term": query.search_term,
            "results_count": len(messages),
            "messages": [m.dict() for m in messages]
        }
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/group/{group_id}/analyze")
async def analyze_group(
    group_id: str,
    sigil: str = Depends(validate_sigil)
):
    """Analyze all messages in a WhatsApp group"""
    try:
        result = await analyzer.analyze_group_messages(group_id)
        return result
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/message/{message_id}/mark")
async def mark_message(
    message_id: str,
    group_id: str,
    mark_type: MessageMarkType,
    reason: Optional[str] = None,
    sigil: str = Depends(validate_sigil)
):
    """Mark a message"""
    try:
        mark = await analyzer.mark_message(message_id, group_id, mark_type, reason)
        return mark.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
