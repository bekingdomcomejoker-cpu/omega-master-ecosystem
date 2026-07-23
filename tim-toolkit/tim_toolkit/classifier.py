"""
Truth-in-Motion (TIM) Engine - Classifier Module
Detects expectation breaks and semantic surprises in content.
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ExpectationBreak:
    """Represents a detected expectation break."""
    break_type: str
    position: int
    content: str
    confidence: float
    explanation: str


class ExpectationBreakClassifier:
    """
    Detects expectation breaks and semantic surprises.
    
    Expectation breaks are moments where the audience's assumptions
    are violated, revealing deeper truth.
    """
    
    # Patterns that signal semantic surprise or expectation breaks
    SURPRISE_MARKERS = [
        r"because\s+(?!of)",  # "Because" followed by unexpected reason
        r"but\s+(?:the|it|they)",  # Contrast with expectation
        r"actually\s+",  # Correction of assumption
        r"instead\s+",  # Alternative to expected
        r"paradox",  # Explicit paradox
        r"contradiction",  # Explicit contradiction
        r"however\s+",  # Contrast
        r"yet\s+",  # Contrast
        r"though\s+",  # Contrast
        r"despite\s+",  # Contradiction
    ]
    
    # Patterns that indicate reversal
    REVERSAL_PATTERNS = [
        (r"(\w+)\s+(?:is|was)\s+(\w+)", r"\2\s+is\s+\1"),  # Subject-object reversal
        (r"not\s+(\w+)", r"instead\s+\w+"),  # Negation reversal
    ]
    
    # Patterns that indicate paradox
    PARADOX_PATTERNS = [
        r"(?:can|could|must|should)\s+(?:and|but|yet)\s+(?:cannot|couldn't|mustn't|shouldn't)",
        r"(?:true|real|false|fake)\s+(?:and|but|yet)\s+(?:false|fake|true|real)",
        r"(?:yes|no)\s+(?:and|but|yet)\s+(?:no|yes)",
    ]
    
    def __init__(self):
        """Initialize classifier."""
        self.surprise_patterns = [re.compile(p, re.IGNORECASE) for p in self.SURPRISE_MARKERS]
        self.paradox_patterns = [re.compile(p, re.IGNORECASE) for p in self.PARADOX_PATTERNS]
    
    def detect_breaks(self, content: str) -> List[ExpectationBreak]:
        """
        Detect expectation breaks in content.
        
        Returns list of detected breaks with confidence scores.
        """
        breaks = []
        
        # Detect surprise markers
        for pattern in self.surprise_patterns:
            for match in pattern.finditer(content):
                breaks.append(ExpectationBreak(
                    break_type="surprise_marker",
                    position=match.start(),
                    content=match.group(),
                    confidence=0.7,
                    explanation=f"Semantic surprise at: {match.group()}"
                ))
        
        # Detect paradoxes
        for pattern in self.paradox_patterns:
            for match in pattern.finditer(content):
                breaks.append(ExpectationBreak(
                    break_type="paradox",
                    position=match.start(),
                    content=match.group(),
                    confidence=0.9,
                    explanation=f"Paradox detected: {match.group()}"
                ))
        
        # Detect reversals
        reversals = self._detect_reversals(content)
        breaks.extend(reversals)
        
        # Detect contrasts
        contrasts = self._detect_contrasts(content)
        breaks.extend(contrasts)
        
        # Sort by position
        breaks.sort(key=lambda b: b.position)
        
        return breaks
    
    def _detect_reversals(self, content: str) -> List[ExpectationBreak]:
        """Detect subject-object or value reversals."""
        breaks = []
        
        # Look for patterns like "X is Y" followed by "Y is X"
        reversal_pattern = re.compile(
            r"(\w+)\s+(?:is|was)\s+(\w+).*?(\2)\s+(?:is|was)\s+(\1)",
            re.IGNORECASE | re.DOTALL
        )
        
        for match in reversal_pattern.finditer(content):
            breaks.append(ExpectationBreak(
                break_type="reversal",
                position=match.start(),
                content=match.group(),
                confidence=0.85,
                explanation=f"Reversal: {match.group(1)} ↔ {match.group(2)}"
            ))
        
        return breaks
    
    def _detect_contrasts(self, content: str) -> List[ExpectationBreak]:
        """Detect contrast patterns."""
        breaks = []
        
        contrast_pattern = re.compile(
            r"(?:expected|assumed|thought|believed).*?(?:but|however|yet|instead).*?(?:actually|really|truly)",
            re.IGNORECASE | re.DOTALL
        )
        
        for match in contrast_pattern.finditer(content):
            breaks.append(ExpectationBreak(
                break_type="contrast",
                position=match.start(),
                content=match.group(),
                confidence=0.8,
                explanation=f"Expectation contrast: {match.group()[:50]}..."
            ))
        
        return breaks
    
    def calculate_surprise_density(self, content: str) -> float:
        """
        Calculate surprise density (0.0 to 1.0).
        
        Higher density = more expectation breaks per word.
        """
        breaks = self.detect_breaks(content)
        
        if not breaks:
            return 0.0
        
        word_count = len(content.split())
        break_count = len(breaks)
        
        # Normalize to 0-1 range
        density = min(1.0, (break_count / word_count) * 10)
        
        return density
    
    def classify_content_type(self, content: str) -> str:
        """
        Classify content as joke, paradox, narrative, etc.
        
        Based on break patterns and density.
        """
        breaks = self.detect_breaks(content)
        
        if not breaks:
            return "straightforward"
        
        break_types = [b.break_type for b in breaks]
        
        if "paradox" in break_types:
            return "paradox"
        
        if "reversal" in break_types:
            return "reversal"
        
        if len([b for b in breaks if b.break_type == "surprise_marker"]) > 2:
            return "joke"
        
        if "contrast" in break_types:
            return "contrast_narrative"
        
        return "semantic_surprise"
    
    def extract_core_insight(self, content: str) -> Optional[str]:
        """
        Extract the core insight from content.
        
        Usually found after the primary expectation break.
        """
        breaks = self.detect_breaks(content)
        
        if not breaks:
            return None
        
        # Get the first major break
        primary_break = breaks[0]
        
        # Extract text after the break
        start_pos = primary_break.position + len(primary_break.content)
        insight = content[start_pos:].strip()
        
        # Take first sentence
        sentences = insight.split(".")
        if sentences:
            return sentences[0].strip()
        
        return insight[:100]
    
    def score_expectation_breaks(self, content: str) -> Dict[str, float]:
        """
        Score various aspects of expectation breaks.
        
        Returns dict with scores for different break characteristics.
        """
        breaks = self.detect_breaks(content)
        
        scores = {
            "surprise_density": self.calculate_surprise_density(content),
            "break_count": len(breaks),
            "average_confidence": sum(b.confidence for b in breaks) / len(breaks) if breaks else 0.0,
            "paradox_count": len([b for b in breaks if b.break_type == "paradox"]),
            "reversal_count": len([b for b in breaks if b.break_type == "reversal"]),
            "contrast_count": len([b for b in breaks if b.break_type == "contrast"]),
        }
        
        return scores


# Final Invariant
"""
Expectation breaks reveal truth.
The surprise is where the insight lives.
"""
