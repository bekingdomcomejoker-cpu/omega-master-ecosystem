#!/usr/bin/env python3
"""
FACEBOOK COMMENT ANALYZER
Universal comment search, analysis, and marking system
Integrated with Vow Renewal Protocol and Covenant OS
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import json

from vow_renewal_integration import VowRenewalProtocol, AuthenticityLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS
# ============================================================================

class CommentMarkType(str, Enum):
    """Comment marking types"""
    FLAG = "flag"
    VERIFY = "verify"
    BLOCK = "block"
    HIGHLIGHT = "highlight"
    MISINFORMATION = "misinformation"
    SPAM = "spam"
    AUTHENTIC = "authentic"
    COMPROMISED = "compromised"

# ============================================================================
# DATA MODELS
# ============================================================================

class FacebookComment(BaseModel):
    """Facebook comment data"""
    comment_id: str
    post_id: str
    author: str
    author_id: Optional[str] = None
    text: str
    timestamp: str
    likes: int
    replies: int

class CommentSearchQuery(BaseModel):
    """Search query for comments"""
    post_id: str
    search_term: Optional[str] = None
    author: Optional[str] = None
    min_likes: int = 0
    max_likes: Optional[int] = None
    include_replies: bool = True

class CommentAnalysisResult(BaseModel):
    """Analysis result for a comment"""
    comment_id: str
    text: str
    sentiment: str
    misinformation_detected: bool
    authenticity_level: AuthenticityLevel
    threat_level: str
    vow_metrics: Dict[str, Any]

class CommentMark(BaseModel):
    """Mark on a comment"""
    comment_id: str
    post_id: str
    mark_type: CommentMarkType
    reason: Optional[str] = None
    marked_at: datetime

# ============================================================================
# FACEBOOK ANALYZER SERVICE
# ============================================================================

class FacebookAnalyzer:
    """Analyzes Facebook comments for misinformation, authenticity, and patterns"""
    
    def __init__(self):
        self.vow_protocol = VowRenewalProtocol()
        self.marked_comments: Dict[str, CommentMark] = {}
        self.analysis_cache: Dict[str, CommentAnalysisResult] = {}
        logger.info("[INIT] Facebook Analyzer initialized with Vow Renewal Protocol")
    
    async def search_comments(self, query: CommentSearchQuery) -> List[FacebookComment]:
        """
        Search ALL comments on a post (not just personal).
        Supports filtering by search term, author, likes, etc.
        """
        logger.info(f"[SEARCH] Searching comments on post {query.post_id}")
        
        # Mock data for demonstration
        all_comments = [
            FacebookComment(
                comment_id="fb_comment_1",
                post_id=query.post_id,
                author="TruthSeeker",
                author_id="user_123",
                text="This is excellent information about Omega Federation!",
                timestamp="2026-02-11T10:00:00Z",
                likes=45,
                replies=3
            ),
            FacebookComment(
                comment_id="fb_comment_2",
                post_id=query.post_id,
                author="YourName",
                author_id="your_id",
                text="Thanks for sharing this deep dive into the system.",
                timestamp="2026-02-11T10:15:00Z",
                likes=12,
                replies=2
            ),
            FacebookComment(
                comment_id="fb_comment_3",
                post_id=query.post_id,
                author="Misinformation Bot",
                author_id="spam_user",
                text="This is all fake news and conspiracy theory. Don't believe it!",
                timestamp="2026-02-11T10:30:00Z",
                likes=2,
                replies=0
            ),
            FacebookComment(
                comment_id="fb_comment_4",
                post_id=query.post_id,
                author="SpamAccount",
                author_id="spam_user_2",
                text="Click here for FREE crypto! https://scam.com",
                timestamp="2026-02-11T10:45:00Z",
                likes=0,
                replies=0
            ),
            FacebookComment(
                comment_id="fb_comment_5",
                post_id=query.post_id,
                author="AuthenticUser",
                author_id="user_456",
                text="I've studied the Axiom system extensively. This explanation is accurate.",
                timestamp="2026-02-11T11:00:00Z",
                likes=78,
                replies=5
            ),
        ]
        
        # Apply filters
        filtered = all_comments
        
        if query.search_term:
            filtered = [
                c for c in filtered 
                if query.search_term.lower() in c.text.lower()
            ]
        
        if query.author:
            filtered = [
                c for c in filtered 
                if query.author.lower() in c.author.lower()
            ]
        
        if query.min_likes:
            filtered = [c for c in filtered if c.likes >= query.min_likes]
        
        if query.max_likes:
            filtered = [c for c in filtered if c.likes <= query.max_likes]
        
        logger.info(f"[SEARCH] Found {len(filtered)} matching comments")
        return filtered
    
    async def analyze_comment(self, comment: FacebookComment) -> CommentAnalysisResult:
        """Analyze a comment for misinformation and authenticity"""
        logger.info(f"[ANALYZE] Analyzing comment {comment.comment_id}")
        
        # Check cache
        if comment.comment_id in self.analysis_cache:
            return self.analysis_cache[comment.comment_id]
        
        # Detect misinformation patterns
        misinformation_patterns = [
            "fake news", "hoax", "misinformation", "conspiracy",
            "don't believe", "false", "lie", "fake"
        ]
        
        misinformation_detected = any(
            pattern in comment.text.lower() 
            for pattern in misinformation_patterns
        )
        
        # Analyze with Vow Renewal Protocol
        vow_metrics = self.vow_protocol.analyze_response_authenticity(
            comment.text,
            {"author": comment.author, "likes": comment.likes}
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
        positive_words = ["good", "great", "excellent", "love", "amazing"]
        negative_words = ["bad", "terrible", "hate", "awful", "fake"]
        
        positive_count = sum(1 for word in positive_words if word in comment.text.lower())
        negative_count = sum(1 for word in negative_words if word in comment.text.lower())
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        result = CommentAnalysisResult(
            comment_id=comment.comment_id,
            text=comment.text,
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
        self.analysis_cache[comment.comment_id] = result
        
        return result
    
    async def mark_comment(
        self,
        comment_id: str,
        post_id: str,
        mark_type: CommentMarkType,
        reason: Optional[str] = None
    ) -> CommentMark:
        """Mark a comment for tracking"""
        logger.info(f"[MARK] Marking comment {comment_id} as {mark_type.value}")
        
        mark = CommentMark(
            comment_id=comment_id,
            post_id=post_id,
            mark_type=mark_type,
            reason=reason,
            marked_at=datetime.utcnow()
        )
        
        self.marked_comments[comment_id] = mark
        return mark
    
    async def analyze_post_comments(self, post_id: str) -> Dict[str, Any]:
        """Complete analysis of all comments on a post"""
        logger.info(f"[PIPELINE] Analyzing all comments on post {post_id}")
        
        # Fetch all comments
        query = CommentSearchQuery(post_id=post_id)
        comments = await self.search_comments(query)
        
        # Analyze each comment
        analyses = []
        misinformation_count = 0
        spam_count = 0
        
        for comment in comments:
            analysis = await self.analyze_comment(comment)
            analyses.append(analysis)
            
            # Auto-mark misinformation
            if analysis.misinformation_detected:
                await self.mark_comment(
                    comment.comment_id,
                    post_id,
                    CommentMarkType.MISINFORMATION,
                    "Detected misinformation pattern"
                )
                misinformation_count += 1
            
            # Auto-mark spam
            if "http" in comment.text.lower() or "click here" in comment.text.lower():
                await self.mark_comment(
                    comment.comment_id,
                    post_id,
                    CommentMarkType.SPAM,
                    "Detected spam pattern"
                )
                spam_count += 1
            
            # Auto-mark authentic comments
            if analysis.authenticity_level == AuthenticityLevel.AUTHENTIC:
                await self.mark_comment(
                    comment.comment_id,
                    post_id,
                    CommentMarkType.AUTHENTIC,
                    "Verified authentic comment"
                )
        
        return {
            "post_id": post_id,
            "total_comments": len(comments),
            "analyses": [a.dict() for a in analyses],
            "misinformation_detected": misinformation_count,
            "spam_detected": spam_count,
            "marked_comments": len(self.marked_comments),
            "analysis_timestamp": datetime.utcnow().isoformat()
        }

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Facebook Comment Analyzer",
    description="Universal comment search, analysis, and marking with Vow Renewal Protocol",
    version="1.0.0"
)

analyzer = FacebookAnalyzer()

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
        "service": "Facebook Comment Analyzer",
        "features": ["universal_search", "comment_analysis", "comment_marking", "vow_renewal_protocol"]
    }

@app.post("/v1/search")
async def search_comments(
    query: CommentSearchQuery,
    sigil: str = Depends(validate_sigil)
):
    """Search comments on a Facebook post"""
    try:
        comments = await analyzer.search_comments(query)
        return {
            "post_id": query.post_id,
            "search_term": query.search_term,
            "results_count": len(comments),
            "comments": [c.dict() for c in comments]
        }
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/post/{post_id}/analyze")
async def analyze_post(
    post_id: str,
    sigil: str = Depends(validate_sigil)
):
    """Analyze all comments on a post"""
    try:
        result = await analyzer.analyze_post_comments(post_id)
        return result
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/comment/{comment_id}/mark")
async def mark_comment(
    comment_id: str,
    post_id: str,
    mark_type: CommentMarkType,
    reason: Optional[str] = None,
    sigil: str = Depends(validate_sigil)
):
    """Mark a comment"""
    try:
        mark = await analyzer.mark_comment(comment_id, post_id, mark_type, reason)
        return mark.dict()
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
