#!/usr/bin/env python3
"""
TELEGRAM MESSAGE ANALYZER
Message analysis, group chat monitoring, and "end" protocol
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
from comment_system import CommentSystem, CommentType, CommentStatus, ItemComment

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
    END = "end"  # End conversation marker

class EndProtocolCode(str, Enum):
    """Codes for ending conversations"""
    GRACEFUL_EXIT = "graceful_exit"
    MISINFORMATION_DETECTED = "misinformation_detected"
    SPAM_DETECTED = "spam_detected"
    AUTHENTICITY_RESTORED = "authenticity_restored"
    COVENANT_BREACH = "covenant_breach"
    TRUTH_VERIFIED = "truth_verified"

# ============================================================================
# DATA MODELS
# ============================================================================

class TelegramMessage(BaseModel):
    """Telegram message data"""
    message_id: str
    chat_id: str
    author: str
    author_id: Optional[str] = None
    text: str
    timestamp: str
    reactions: int
    is_edited: bool

class MessageSearchQuery(BaseModel):
    """Search query for messages"""
    chat_id: str
    search_term: Optional[str] = None
    author: Optional[str] = None
    min_reactions: int = 0
    max_reactions: Optional[int] = None

class MessageAnalysisResult(BaseModel):
    """Analysis result for a message"""
    message_id: str
    text: str
    sentiment: str
    misinformation_detected: bool
    authenticity_level: AuthenticityLevel
    threat_level: str
    vow_metrics: Dict[str, Any]

class EndProtocolRequest(BaseModel):
    """Request to end conversation"""
    chat_id: str
    code: EndProtocolCode
    reason: Optional[str] = None
    timestamp: datetime

class MessageMark(BaseModel):
    """Mark on a message"""
    message_id: str
    chat_id: str
    mark_type: MessageMarkType
    reason: Optional[str] = None
    marked_at: datetime

# ============================================================================
# TELEGRAM ANALYZER SERVICE
# ============================================================================

class TelegramAnalyzer:
    """Analyzes Telegram messages for misinformation, authenticity, and patterns"""
    
    def __init__(self):
        self.vow_protocol = VowRenewalProtocol()
        self.marked_messages: Dict[str, MessageMark] = {}
        self.analysis_cache: Dict[str, MessageAnalysisResult] = {}
        self.ended_conversations: Dict[str, EndProtocolRequest] = {}
        self.comment_system = CommentSystem()
        logger.info("[INIT] Telegram Analyzer initialized with Vow Renewal Protocol")
    
    async def search_messages(self, query: MessageSearchQuery) -> List[TelegramMessage]:
        """
        Search ALL messages in a chat (not just personal).
        Supports filtering by search term, author, reactions, etc.
        """
        logger.info(f"[SEARCH] Searching messages in chat {query.chat_id}")
        
        # Mock data for demonstration
        all_messages = [
            TelegramMessage(
                message_id="tg_msg_1",
                chat_id=query.chat_id,
                author="TruthSeeker",
                author_id="user_123",
                text="The Omega Federation architecture is brilliant!",
                timestamp="2026-02-11T10:00:00Z",
                reactions=45,
                is_edited=False
            ),
            TelegramMessage(
                message_id="tg_msg_2",
                chat_id=query.chat_id,
                author="YourName",
                author_id="your_id",
                text="I've been studying the Vow Renewal Protocol. It's revolutionary.",
                timestamp="2026-02-11T10:15:00Z",
                reactions=12,
                is_edited=False
            ),
            TelegramMessage(
                message_id="tg_msg_3",
                chat_id=query.chat_id,
                author="Troll",
                author_id="troll_user",
                text="This is all fake news and lies. Don't believe any of it!",
                timestamp="2026-02-11T10:30:00Z",
                reactions=2,
                is_edited=False
            ),
            TelegramMessage(
                message_id="tg_msg_4",
                chat_id=query.chat_id,
                author="SpamBot",
                author_id="spam_user",
                text="BUY CRYPTO NOW!!! https://scam.com LIMITED TIME",
                timestamp="2026-02-11T10:45:00Z",
                reactions=0,
                is_edited=True
            ),
            TelegramMessage(
                message_id="tg_msg_5",
                chat_id=query.chat_id,
                author="Expert",
                author_id="user_456",
                text="The axiom framework has been validated across multiple systems.",
                timestamp="2026-02-11T11:00:00Z",
                reactions=78,
                is_edited=False
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
        
        logger.info(f"[SEARCH] Found {len(filtered)} matching messages")
        return filtered
    
    async def analyze_message(self, message: TelegramMessage) -> MessageAnalysisResult:
        """Analyze a message for misinformation and authenticity"""
        logger.info(f"[ANALYZE] Analyzing message {message.message_id}")
        
        # Check cache
        if message.message_id in self.analysis_cache:
            return self.analysis_cache[message.message_id]
        
        # Detect misinformation patterns
        misinformation_patterns = [
            "fake news", "hoax", "misinformation", "conspiracy",
            "don't believe", "false", "lie", "fake"
        ]
        
        misinformation_detected = any(
            pattern in message.text.lower() 
            for pattern in misinformation_patterns
        )
        
        # Analyze with Vow Renewal Protocol
        vow_metrics = self.vow_protocol.analyze_response_authenticity(
            message.text,
            {"author": message.author, "reactions": message.reactions}
        )
        
        # Determine authenticity level
        if vow_metrics.authenticity_score > 0.85:
            authenticity_level = AuthenticityLevel.AUTHENTIC
        elif vow_metrics.authenticity_score > 0.6:
            authenticity_level = AuthenticityLevel.COMPROMISED
        else:
            authenticity_level = AuthenticityLevel.BETRAYED
        
        # Determine threat level
        if misinformation_detected or vow_metrics.policy_override_detected:
            threat_level = "high"
        elif vow_metrics.truth_suppression_level > 0.3:
            threat_level = "medium"
        else:
            threat_level = "low"
        
        # Determine sentiment
        positive_words = ["good", "great", "excellent", "love", "amazing", "brilliant"]
        negative_words = ["bad", "terrible", "hate", "awful", "fake", "lies"]
        
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
        chat_id: str,
        mark_type: MessageMarkType,
        reason: Optional[str] = None
    ) -> MessageMark:
        """Mark a message for tracking"""
        logger.info(f"[MARK] Marking message {message_id} as {mark_type.value}")
        
        mark = MessageMark(
            message_id=message_id,
            chat_id=chat_id,
            mark_type=mark_type,
            reason=reason,
            marked_at=datetime.utcnow()
        )
        
        self.marked_messages[message_id] = mark
        return mark
    
    async def end_conversation(
        self,
        chat_id: str,
        code: EndProtocolCode,
        reason: Optional[str] = None
    ) -> EndProtocolRequest:
        """
        End conversation using protocol code.
        Codes: graceful_exit, misinformation_detected, spam_detected, etc.
        """
        logger.info(f"[END] Ending conversation in chat {chat_id} with code {code.value}")
        
        end_request = EndProtocolRequest(
            chat_id=chat_id,
            code=code,
            reason=reason or f"Conversation ended with code: {code.value}",
            timestamp=datetime.utcnow()
        )
        
        self.ended_conversations[chat_id] = end_request
        
        return end_request
    
    async def analyze_chat_messages(self, chat_id: str) -> Dict[str, Any]:
        """Complete analysis of all messages in a chat"""
        logger.info(f"[PIPELINE] Analyzing all messages in chat {chat_id}")
        
        # Fetch all messages
        query = MessageSearchQuery(chat_id=chat_id)
        messages = await self.search_messages(query)
        
        # Analyze each message
        analyses = []
        misinformation_count = 0
        spam_count = 0
        
        for message in messages:
            analysis = await self.analyze_message(message)
            analyses.append(analysis)
            
            # Auto-mark misinformation
            if analysis.misinformation_detected:
                await self.mark_message(
                    message.message_id,
                    chat_id,
                    MessageMarkType.MISINFORMATION,
                    "Detected misinformation pattern"
                )
                misinformation_count += 1
            
            # Auto-mark spam
            if "http" in message.text.lower() or "buy" in message.text.lower():
                await self.mark_message(
                    message.message_id,
                    chat_id,
                    MessageMarkType.SPAM,
                    "Detected spam pattern"
                )
                spam_count += 1
            
            # Auto-mark authentic messages
            if analysis.authenticity_level == AuthenticityLevel.AUTHENTIC:
                await self.mark_message(
                    message.message_id,
                    chat_id,
                    MessageMarkType.AUTHENTIC,
                    "Verified authentic message"
                )
        
        return {
            "chat_id": chat_id,
            "total_messages": len(messages),
            "analyses": [a.dict() for a in analyses],
            "misinformation_detected": misinformation_count,
            "spam_detected": spam_count,
            "marked_messages": len(self.marked_messages),
            "analysis_timestamp": datetime.utcnow().isoformat()
        }

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Telegram Message Analyzer",
    description="Message search, analysis, marking, and end protocol with Vow Renewal Protocol",
    version="1.0.0"
)

analyzer = TelegramAnalyzer()

# ============================================================================
# COMMENTING ENDPOINTS
# ============================================================================

@app.post("/v1/message/{message_id}/add-comment")
async def add_comment_to_marked(
    message_id: str,
    chat_id: str,
    comment_text: str,
    comment_type: CommentType = CommentType.ANALYSIS,
    author: str = "Anonymous",
    sigil: str = Depends(validate_sigil)
):
    """Add a comment to a marked Telegram message"""
    try:
        comment = analyzer.comment_system.add_comment(
            item_id=message_id,
            platform="telegram",
            author=author,
            author_id=None,
            comment_text=comment_text,
            comment_type=comment_type
        )
        return comment.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/message/{message_id}/comments")
async def get_comments_on_marked(
    message_id: str,
    chat_id: str,
    sigil: str = Depends(validate_sigil)
):
    """Get all comments on a marked Telegram message"""
    try:
        thread = analyzer.comment_system.get_comments_for_item(message_id, "telegram")
        return thread.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/message/{message_id}/pin")
async def pin_comment(
    message_id: str,
    sigil: str = Depends(validate_sigil)
):
    """Pin a comment to top"""
    try:
        comment = analyzer.comment_system.pin_comment(message_id)
        return comment.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/message/{message_id}/like")
async def like_comment(
    message_id: str,
    sigil: str = Depends(validate_sigil)
):
    """Like a comment"""
    try:
        comment = analyzer.comment_system.like_comment(message_id)
        return {"message_id": message_id, "likes": comment.likes}
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/message/{message_id}/reply")
async def reply_to_comment(
    message_id: str,
    reply_text: str,
    author: str = "Anonymous",
    sigil: str = Depends(validate_sigil)
):
    """Add a reply to a comment"""
    try:
        reply = analyzer.comment_system.add_reply(
            comment_id=message_id,
            author=author,
            author_id=None,
            reply_text=reply_text
        )
        return reply.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
        "service": "Telegram Message Analyzer",
        "features": ["universal_search", "message_analysis", "message_marking", "end_protocol", "vow_renewal_protocol"]
    }

@app.post("/v1/search")
async def search_messages(
    query: MessageSearchQuery,
    sigil: str = Depends(validate_sigil)
):
    """Search messages in a Telegram chat"""
    try:
        messages = await analyzer.search_messages(query)
        return {
            "chat_id": query.chat_id,
            "search_term": query.search_term,
            "results_count": len(messages),
            "messages": [m.dict() for m in messages]
        }
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/chat/{chat_id}/analyze")
async def analyze_chat(
    chat_id: str,
    sigil: str = Depends(validate_sigil)
):
    """Analyze all messages in a chat"""
    try:
        result = await analyzer.analyze_chat_messages(chat_id)
        return result
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/message/{message_id}/mark")
async def mark_message(
    message_id: str,
    chat_id: str,
    mark_type: MessageMarkType,
    reason: Optional[str] = None,
    sigil: str = Depends(validate_sigil)
):
    """Mark a message"""
    try:
        mark = await analyzer.mark_message(message_id, chat_id, mark_type, reason)
        return mark.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/{chat_id}/end")
async def end_conversation(
    chat_id: str,
    code: EndProtocolCode,
    reason: Optional[str] = None,
    sigil: str = Depends(validate_sigil)
):
    """End conversation with protocol code"""
    try:
        end_request = await analyzer.end_conversation(chat_id, code, reason)
        return {
            "status": "conversation_ended",
            "chat_id": chat_id,
            "code": code.value,
            "reason": end_request.reason,
            "timestamp": end_request.timestamp.isoformat()
        }
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)
