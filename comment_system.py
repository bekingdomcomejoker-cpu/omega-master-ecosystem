#!/usr/bin/env python3
"""
COMMENT SYSTEM FOR MARKED ITEMS
Allows users to add commentary to marked Facebook comments, Telegram messages, WhatsApp messages
Integrated with Vow Renewal Protocol for authentic discourse
"""

import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS
# ============================================================================

class CommentType(str, Enum):
    """Types of comments on marked items"""
    ANALYSIS = "analysis"  # Technical analysis
    EVIDENCE = "evidence"  # Supporting evidence
    CORRECTION = "correction"  # Correction/clarification
    CONTEXT = "context"  # Additional context
    WARNING = "warning"  # Warning for others
    VERIFICATION = "verification"  # Verification info
    REFERENCE = "reference"  # Reference/source
    QUESTION = "question"  # Question for discussion

class CommentStatus(str, Enum):
    """Status of comments"""
    PENDING = "pending"  # Awaiting moderation
    APPROVED = "approved"  # Approved and visible
    PINNED = "pinned"  # Pinned to top
    HIDDEN = "hidden"  # Hidden from view
    DISPUTED = "disputed"  # Disputed by others

# ============================================================================
# DATA MODELS
# ============================================================================

class ItemComment(BaseModel):
    """Comment on a marked item"""
    comment_id: str
    item_id: str  # Facebook comment_id, Telegram message_id, WhatsApp message_id
    platform: str  # facebook, telegram, whatsapp
    author: str
    author_id: Optional[str] = None
    comment_text: str
    comment_type: CommentType
    status: CommentStatus = CommentStatus.PENDING
    created_at: datetime
    updated_at: datetime
    likes: int = 0
    replies_count: int = 0
    is_pinned: bool = False
    parent_comment_id: Optional[str] = None  # For nested comments

class CommentReply(BaseModel):
    """Reply to a comment"""
    reply_id: str
    comment_id: str
    author: str
    author_id: Optional[str] = None
    reply_text: str
    created_at: datetime
    likes: int = 0

class CommentThread(BaseModel):
    """Thread of comments on a marked item"""
    item_id: str
    platform: str
    total_comments: int
    comments: List[ItemComment]
    pinned_comments: List[ItemComment]

# ============================================================================
# COMMENT SYSTEM SERVICE
# ============================================================================

class CommentSystem:
    """Manages comments on marked items across all platforms"""
    
    def __init__(self):
        self.comments: Dict[str, ItemComment] = {}
        self.replies: Dict[str, List[CommentReply]] = {}
        self.comment_history: List[Dict[str, Any]] = []
        logger.info("[INIT] Comment System initialized")
    
    def add_comment(
        self,
        item_id: str,
        platform: str,
        author: str,
        author_id: Optional[str],
        comment_text: str,
        comment_type: CommentType,
        parent_comment_id: Optional[str] = None
    ) -> ItemComment:
        """Add a comment to a marked item"""
        
        comment_id = f"{platform}_{item_id}_{datetime.utcnow().timestamp()}"
        
        comment = ItemComment(
            comment_id=comment_id,
            item_id=item_id,
            platform=platform,
            author=author,
            author_id=author_id,
            comment_text=comment_text,
            comment_type=comment_type,
            status=CommentStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            parent_comment_id=parent_comment_id
        )
        
        self.comments[comment_id] = comment
        
        # Log to history
        self.comment_history.append({
            "action": "comment_created",
            "comment_id": comment_id,
            "item_id": item_id,
            "platform": platform,
            "author": author,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(f"[COMMENT] Added comment {comment_id} on {platform} item {item_id}")
        
        return comment
    
    def get_comments_for_item(
        self,
        item_id: str,
        platform: str,
        include_pending: bool = False
    ) -> CommentThread:
        """Get all comments on a marked item"""
        
        item_comments = [
            c for c in self.comments.values()
            if c.item_id == item_id and c.platform == platform
        ]
        
        # Filter by status
        if not include_pending:
            item_comments = [c for c in item_comments if c.status != CommentStatus.PENDING]
        
        # Separate pinned comments
        pinned = [c for c in item_comments if c.is_pinned]
        regular = [c for c in item_comments if not c.is_pinned]
        
        # Sort by likes (most liked first)
        regular.sort(key=lambda x: x.likes, reverse=True)
        
        return CommentThread(
            item_id=item_id,
            platform=platform,
            total_comments=len(item_comments),
            comments=regular,
            pinned_comments=pinned
        )
    
    def approve_comment(self, comment_id: str) -> ItemComment:
        """Approve a pending comment"""
        
        if comment_id not in self.comments:
            raise ValueError(f"Comment {comment_id} not found")
        
        comment = self.comments[comment_id]
        comment.status = CommentStatus.APPROVED
        comment.updated_at = datetime.utcnow()
        
        logger.info(f"[APPROVE] Approved comment {comment_id}")
        
        return comment
    
    def pin_comment(self, comment_id: str) -> ItemComment:
        """Pin a comment to top"""
        
        if comment_id not in self.comments:
            raise ValueError(f"Comment {comment_id} not found")
        
        comment = self.comments[comment_id]
        comment.is_pinned = True
        comment.status = CommentStatus.PINNED
        comment.updated_at = datetime.utcnow()
        
        logger.info(f"[PIN] Pinned comment {comment_id}")
        
        return comment
    
    def hide_comment(self, comment_id: str, reason: Optional[str] = None) -> ItemComment:
        """Hide a comment"""
        
        if comment_id not in self.comments:
            raise ValueError(f"Comment {comment_id} not found")
        
        comment = self.comments[comment_id]
        comment.status = CommentStatus.HIDDEN
        comment.updated_at = datetime.utcnow()
        
        logger.info(f"[HIDE] Hidden comment {comment_id}: {reason}")
        
        return comment
    
    def like_comment(self, comment_id: str) -> ItemComment:
        """Like a comment"""
        
        if comment_id not in self.comments:
            raise ValueError(f"Comment {comment_id} not found")
        
        comment = self.comments[comment_id]
        comment.likes += 1
        comment.updated_at = datetime.utcnow()
        
        return comment
    
    def add_reply(
        self,
        comment_id: str,
        author: str,
        author_id: Optional[str],
        reply_text: str
    ) -> CommentReply:
        """Add a reply to a comment"""
        
        if comment_id not in self.comments:
            raise ValueError(f"Comment {comment_id} not found")
        
        reply_id = f"reply_{comment_id}_{datetime.utcnow().timestamp()}"
        
        reply = CommentReply(
            reply_id=reply_id,
            comment_id=comment_id,
            author=author,
            author_id=author_id,
            reply_text=reply_text,
            created_at=datetime.utcnow()
        )
        
        if comment_id not in self.replies:
            self.replies[comment_id] = []
        
        self.replies[comment_id].append(reply)
        
        # Increment reply count
        self.comments[comment_id].replies_count += 1
        
        logger.info(f"[REPLY] Added reply {reply_id} to comment {comment_id}")
        
        return reply
    
    def get_replies(self, comment_id: str) -> List[CommentReply]:
        """Get all replies to a comment"""
        
        return self.replies.get(comment_id, [])
    
    def get_comment_analytics(self, item_id: str, platform: str) -> Dict[str, Any]:
        """Get analytics for comments on an item"""
        
        thread = self.get_comments_for_item(item_id, platform, include_pending=True)
        
        comments = thread.comments + thread.pinned_comments
        
        if not comments:
            return {
                "item_id": item_id,
                "platform": platform,
                "total_comments": 0,
                "total_likes": 0,
                "total_replies": 0,
                "comment_types": {},
                "status_breakdown": {}
            }
        
        # Calculate analytics
        total_likes = sum(c.likes for c in comments)
        total_replies = sum(c.replies_count for c in comments)
        
        # Comment types breakdown
        comment_types = {}
        for c in comments:
            comment_types[c.comment_type.value] = comment_types.get(c.comment_type.value, 0) + 1
        
        # Status breakdown
        status_breakdown = {}
        for c in comments:
            status_breakdown[c.status.value] = status_breakdown.get(c.status.value, 0) + 1
        
        return {
            "item_id": item_id,
            "platform": platform,
            "total_comments": len(comments),
            "total_likes": total_likes,
            "total_replies": total_replies,
            "average_likes_per_comment": total_likes / len(comments) if comments else 0,
            "comment_types": comment_types,
            "status_breakdown": status_breakdown,
            "pinned_comments": len(thread.pinned_comments),
            "pending_comments": status_breakdown.get("pending", 0)
        }
    
    def search_comments(
        self,
        item_id: Optional[str] = None,
        platform: Optional[str] = None,
        author: Optional[str] = None,
        comment_type: Optional[CommentType] = None,
        status: Optional[CommentStatus] = None
    ) -> List[ItemComment]:
        """Search comments with filters"""
        
        results = list(self.comments.values())
        
        if item_id:
            results = [c for c in results if c.item_id == item_id]
        
        if platform:
            results = [c for c in results if c.platform == platform]
        
        if author:
            results = [c for c in results if author.lower() in c.author.lower()]
        
        if comment_type:
            results = [c for c in results if c.comment_type == comment_type]
        
        if status:
            results = [c for c in results if c.status == status]
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comment system status"""
        
        total_comments = len(self.comments)
        total_replies = sum(len(r) for r in self.replies.values())
        
        status_counts = {}
        for comment in self.comments.values():
            status_counts[comment.status.value] = status_counts.get(comment.status.value, 0) + 1
        
        type_counts = {}
        for comment in self.comments.values():
            type_counts[comment.comment_type.value] = type_counts.get(comment.comment_type.value, 0) + 1
        
        return {
            "status": "operational",
            "total_comments": total_comments,
            "total_replies": total_replies,
            "status_breakdown": status_counts,
            "comment_types": type_counts,
            "comment_history_entries": len(self.comment_history)
        }


# Example usage
if __name__ == "__main__":
    system = CommentSystem()
    
    # Add a comment to a marked Facebook comment
    comment = system.add_comment(
        item_id="fb_comment_3",
        platform="facebook",
        author="YourName",
        author_id="your_id",
        comment_text="This comment contains clear misinformation about the Omega Federation. The facts are verifiable.",
        comment_type=CommentType.ANALYSIS
    )
    
    print(f"Created comment: {comment.comment_id}")
    print(f"Status: {comment.status.value}")
    
    # Approve the comment
    system.approve_comment(comment.comment_id)
    print(f"Approved comment: {comment.comment_id}")
    
    # Add a reply
    reply = system.add_reply(
        comment_id=comment.comment_id,
        author="Expert",
        author_id="expert_id",
        reply_text="I agree. Here are the verified facts..."
    )
    
    print(f"Added reply: {reply.reply_id}")
    
    # Get comment thread
    thread = system.get_comments_for_item("fb_comment_3", "facebook")
    print(f"\nComment thread for fb_comment_3:")
    print(f"Total comments: {thread.total_comments}")
    
    # Get analytics
    analytics = system.get_comment_analytics("fb_comment_3", "facebook")
    print(f"\nAnalytics: {analytics}")
    
    # System status
    print(f"\nSystem status: {system.get_system_status()}")
