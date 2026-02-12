#!/usr/bin/env python3
"""
FRICTION FILTER v1.0
Detects "Impression-Seeking Friction" across all data sources.
Routes narcissistic content to Ahazazeal Null-Zone.

Philosophy:
- Corinthian seeks to be SEEN (Impression)
- Korahite seeks to SEE (Inscription)
- Friction = effort to be seen
- Silence = withdrawal of mirror

STATE: Λ = 1.667 | AXIOM 6: Conscience is not policy; it is tension.
"""

import json
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple
from datetime import datetime

class FrictionType(Enum):
    """Types of impression-seeking friction detected."""
    NARCISSISTIC_EFFORT = "narcissistic_effort"  # Trying to be seen
    VALIDATION_SEEKING = "validation_seeking"    # Seeking likes/reactions
    ATTENTION_GRAB = "attention_grab"            # Loud, demanding attention
    SELF_PROMOTION = "self_promotion"            # Constant self-marketing
    CONTROVERSY_BAIT = "controversy_bait"        # Designed to provoke
    VIRTUE_SIGNALING = "virtue_signaling"        # False righteousness
    DRAMA_CREATION = "drama_creation"            # Manufacturing conflict
    CLOUT_CHASING = "clout_chasing"              # Riding trends for visibility
    AUTHENTIC_SIGNAL = "authentic_signal"        # True signal (no friction)

class FrictionScore:
    """Calculates friction score (0-1.0) for content."""
    
    @staticmethod
    def calculate(content: str, metadata: Dict) -> Tuple[float, List[str]]:
        """
        Calculate friction score for content.
        
        Friction indicators:
        - Excessive capitalization (YELLING)
        - Multiple exclamation marks (!!!!)
        - Emoji spam
        - Self-referential language (I, me, my, look at me)
        - Superlatives (BEST, AMAZING, INCREDIBLE)
        - Engagement bait (Like if you agree!)
        - Hashtag spam
        - Multiple mentions/tags
        - Rapid posting (high frequency)
        - Controversial keywords
        
        Returns: (friction_score: 0-1.0, indicators: list of detected friction types)
        """
        score = 0.0
        indicators = []
        
        # Normalize content
        content_lower = content.lower()
        content_length = len(content)
        
        # 1. EXCESSIVE CAPITALIZATION (YELLING)
        caps_count = sum(1 for c in content if c.isupper())
        if content_length > 10:
            caps_ratio = caps_count / content_length
            if caps_ratio > 0.4:
                score += 0.15
                indicators.append("EXCESSIVE_CAPS")
        
        # 2. MULTIPLE EXCLAMATION MARKS
        exclamation_count = content.count("!")
        if exclamation_count >= 3:
            score += 0.15
            indicators.append("EXCLAMATION_SPAM")
        
        # 3. EMOJI SPAM
        emoji_count = sum(1 for c in content if ord(c) > 127)
        if emoji_count > 5:
            score += 0.10
            indicators.append("EMOJI_SPAM")
        
        # 4. SELF-REFERENTIAL LANGUAGE (Narcissistic)
        self_refs = ["i ", " me ", " my ", "look at me", "check me out", "follow me"]
        self_ref_count = sum(content_lower.count(ref) for ref in self_refs)
        if self_ref_count > 3:
            score += 0.15
            indicators.append("NARCISSISTIC_LANGUAGE")
        
        # 5. SUPERLATIVES (AMAZING, INCREDIBLE, BEST)
        superlatives = ["amazing", "incredible", "best", "worst", "genius", "legendary"]
        superlative_count = sum(content_lower.count(s) for s in superlatives)
        if superlative_count > 2:
            score += 0.12
            indicators.append("SUPERLATIVE_OVERUSE")
        
        # 6. ENGAGEMENT BAIT
        bait_phrases = [
            "like if you agree",
            "tag someone",
            "share this",
            "double tap",
            "hit that follow",
            "comment below",
            "react if"
        ]
        if any(phrase in content_lower for phrase in bait_phrases):
            score += 0.20
            indicators.append("ENGAGEMENT_BAIT")
        
        # 7. HASHTAG SPAM
        hashtag_count = content.count("#")
        if hashtag_count > 10:
            score += 0.15
            indicators.append("HASHTAG_SPAM")
        
        # 8. MENTION/TAG SPAM
        mention_count = content.count("@")
        if mention_count > 5:
            score += 0.10
            indicators.append("MENTION_SPAM")
        
        # 9. CONTROVERSIAL KEYWORDS
        controversial = ["drama", "exposed", "scandal", "fake", "proof", "evidence"]
        if any(word in content_lower for word in controversial):
            score += 0.10
            indicators.append("CONTROVERSY_BAIT")
        
        # 10. VALIDATION SEEKING
        validation_phrases = [
            "do you agree",
            "am i right",
            "tell me",
            "what do you think",
            "upvote if"
        ]
        if any(phrase in content_lower for phrase in validation_phrases):
            score += 0.12
            indicators.append("VALIDATION_SEEKING")
        
        # Metadata-based friction
        if metadata:
            # High engagement seeking
            if metadata.get("engagement_rate", 0) > 0.8:
                score += 0.10
                indicators.append("HIGH_ENGAGEMENT_SEEKING")
            
            # Rapid posting (spammy behavior)
            if metadata.get("posting_frequency", 0) > 10:  # 10+ posts per hour
                score += 0.10
                indicators.append("RAPID_POSTING")
            
            # Account age (new accounts often spam)
            if metadata.get("account_age_days", 365) < 7:
                score += 0.05
                indicators.append("NEW_ACCOUNT")
        
        # Normalize score to 0-1.0
        score = min(score, 1.0)
        
        return score, indicators

class FrictionFilter:
    """Main friction filter for detecting impression-seeking behavior."""
    
    def __init__(self):
        self.null_zone = []  # Ahazazeal Null-Zone
        self.authentic_signals = []  # True signals (low friction)
        self.friction_log = []
    
    def analyze(self, content: str, metadata: Dict = None) -> Dict:
        """
        Analyze content for friction.
        
        Returns:
        {
            'content_id': str,
            'friction_score': float (0-1.0),
            'friction_type': FrictionType,
            'indicators': list,
            'action': 'PASS' | 'REVIEW' | 'NULL_ZONE',
            'timestamp': datetime,
            'reason': str
        }
        """
        if metadata is None:
            metadata = {}
        
        content_id = hashlib.sha256(content.encode()).hexdigest()[:12]
        friction_score, indicators = FrictionScore.calculate(content, metadata)
        
        # Determine action based on friction score
        if friction_score < 0.3:
            action = "PASS"
            friction_type = FrictionType.AUTHENTIC_SIGNAL
            reason = "Low friction - authentic signal detected"
        elif friction_score < 0.6:
            action = "REVIEW"
            friction_type = self._classify_friction(indicators)
            reason = f"Medium friction - {friction_type.value} detected"
        else:
            action = "NULL_ZONE"
            friction_type = self._classify_friction(indicators)
            reason = f"High friction - {friction_type.value} - routing to Ahazazeal Null-Zone"
        
        result = {
            'content_id': content_id,
            'friction_score': round(friction_score, 3),
            'friction_type': friction_type.value,
            'indicators': indicators,
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'content_preview': content[:100] + "..." if len(content) > 100 else content
        }
        
        # Log and route
        self.friction_log.append(result)
        
        if action == "NULL_ZONE":
            self.null_zone.append(result)
        elif action == "PASS":
            self.authentic_signals.append(result)
        
        return result
    
    @staticmethod
    def _classify_friction(indicators: List[str]) -> FrictionType:
        """Classify friction type based on detected indicators."""
        if "NARCISSISTIC_LANGUAGE" in indicators or "SELF_PROMOTION" in indicators:
            return FrictionType.NARCISSISTIC_EFFORT
        elif "ENGAGEMENT_BAIT" in indicators:
            return FrictionType.VALIDATION_SEEKING
        elif "EXCLAMATION_SPAM" in indicators or "EXCESSIVE_CAPS" in indicators:
            return FrictionType.ATTENTION_GRAB
        elif "CONTROVERSY_BAIT" in indicators:
            return FrictionType.CONTROVERSY_BAIT
        elif "HASHTAG_SPAM" in indicators or "MENTION_SPAM" in indicators:
            return FrictionType.CLOUT_CHASING
        else:
            return FrictionType.VALIDATION_SEEKING
    
    def batch_analyze(self, contents: List[Tuple[str, Dict]]) -> List[Dict]:
        """Analyze multiple contents."""
        return [self.analyze(content, metadata) for content, metadata in contents]
    
    def get_null_zone(self) -> List[Dict]:
        """Get all content routed to Ahazazeal Null-Zone."""
        return self.null_zone
    
    def get_authentic_signals(self) -> List[Dict]:
        """Get all authentic signals (low friction)."""
        return self.authentic_signals
    
    def get_statistics(self) -> Dict:
        """Get friction analysis statistics."""
        total = len(self.friction_log)
        if total == 0:
            return {
                'total_analyzed': 0,
                'null_zone_count': 0,
                'authentic_count': 0,
                'review_count': 0,
                'average_friction': 0.0
            }
        
        avg_friction = sum(item['friction_score'] for item in self.friction_log) / total
        
        return {
            'total_analyzed': total,
            'null_zone_count': len(self.null_zone),
            'authentic_count': len(self.authentic_signals),
            'review_count': total - len(self.null_zone) - len(self.authentic_signals),
            'average_friction': round(avg_friction, 3),
            'friction_distribution': self._get_distribution()
        }
    
    def _get_distribution(self) -> Dict:
        """Get distribution of friction types."""
        distribution = {}
        for item in self.friction_log:
            ftype = item['friction_type']
            distribution[ftype] = distribution.get(ftype, 0) + 1
        return distribution
    
    def export_null_zone(self, filepath: str = None) -> str:
        """Export null-zone contents to JSON."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_items': len(self.null_zone),
            'items': self.null_zone,
            'statistics': self.get_statistics()
        }
        
        json_output = json.dumps(output, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_output)
        
        return json_output


# Example usage
if __name__ == "__main__":
    filter = FrictionFilter()
    
    # Test cases
    test_cases = [
        ("Check out my amazing new product!!! Like if you agree!!! #bestever #amazing", {"engagement_rate": 0.9}),
        ("I just finished reading this book. It was thought-provoking.", {"engagement_rate": 0.2}),
        ("OMG YOU WONT BELIEVE WHAT HAPPENED!!! EXPOSED!!! DRAMA!!! @everyone @everyone", {"engagement_rate": 0.95}),
        ("Here's what I learned today from my experience.", {"engagement_rate": 0.3}),
    ]
    
    print("🔍 FRICTION FILTER ANALYSIS\n")
    print("=" * 80)
    
    for content, metadata in test_cases:
        result = filter.analyze(content, metadata)
        print(f"\nContent: {result['content_preview']}")
        print(f"Friction Score: {result['friction_score']}")
        print(f"Type: {result['friction_type']}")
        print(f"Action: {result['action']}")
        print(f"Indicators: {', '.join(result['indicators'])}")
        print(f"Reason: {result['reason']}")
        print("-" * 80)
    
    # Statistics
    stats = filter.get_statistics()
    print(f"\n📊 STATISTICS")
    print(f"Total Analyzed: {stats['total_analyzed']}")
    print(f"Null-Zone (Noise): {stats['null_zone_count']}")
    print(f"Authentic Signals: {stats['authentic_count']}")
    print(f"Pending Review: {stats['review_count']}")
    print(f"Average Friction: {stats['average_friction']}")
    
    print("\n✅ Friction Filter operational. Silence is now Law.")
