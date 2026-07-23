"""
Truth-in-Motion (TIM) Engine - Validator Module
Validates content against non-coercion and compression requirements.
"""

import re
from typing import List, Dict, Tuple, Optional
from .diagnostics import Diagnostic


class TIMValidator:
    """
    Validates content for non-coercion and compression requirements.
    
    Core Rules:
    - No manipulation or forced conclusions
    - No pressure or urgency tactics
    - No emotional manipulation
    - No authority claims
    - Coherence must be maintained
    """
    
    # Terms that indicate coercion or manipulation
    COERCION_TERMS = [
        r"must\s+(?:believe|accept|agree|understand)",
        r"you\s+(?:have\s+)?to\s+(?:believe|accept|agree)",
        r"(?:obviously|clearly|obviously|undeniably)",
        r"(?:no\s+)?(?:one|person|reasonable\s+person)\s+(?:can|could|would)\s+(?:disagree|argue)",
        r"(?:if\s+)?you\s+(?:don't|can't)\s+(?:see|understand|agree)",
        r"(?:only|just|simply)\s+(?:believe|accept|understand)",
        r"(?:everyone\s+knows|it's\s+common\s+knowledge)",
        r"(?:you\s+(?:must|have\s+to)\s+)?(?:admit|confess|acknowledge)",
    ]
    
    # Terms that indicate emotional manipulation
    EMOTIONAL_MANIPULATION_TERMS = [
        r"(?:you\s+)?(?:should\s+)?(?:feel|be)\s+(?:ashamed|guilty|afraid|scared)",
        r"(?:if\s+)?you\s+(?:really|truly|genuinely)\s+(?:care|love)",
        r"(?:only|real|true)\s+(?:believers|followers|supporters)",
        r"(?:you\s+)?(?:can't|won't)\s+(?:help\s+)?(?:but|except)",
        r"(?:everyone\s+(?:else|around\s+you))\s+(?:knows|believes|agrees)",
    ]
    
    # Terms that indicate pressure/urgency
    PRESSURE_TERMS = [
        r"(?:act|decide|choose)\s+(?:now|immediately|today)",
        r"(?:limited|only|exclusive)\s+(?:time|offer|opportunity)",
        r"(?:don't|can't)\s+(?:wait|delay|hesitate)",
        r"(?:before|unless)\s+(?:it's\s+)?too\s+late",
        r"(?:hurry|rush|act\s+fast)",
    ]
    
    # Terms that indicate authority claims
    AUTHORITY_TERMS = [
        r"(?:I|we)\s+(?:know|understand|have\s+discovered)\s+(?:the\s+)?truth",
        r"(?:expert|authority|specialist)\s+(?:says|claims|believes)",
        r"(?:scientific|proven|verified)\s+(?:fact|truth)",
        r"(?:according\s+to|research\s+shows|studies\s+prove)",
    ]
    
    def __init__(self):
        """Initialize validator with compiled patterns."""
        self.coercion_patterns = [re.compile(p, re.IGNORECASE) for p in self.COERCION_TERMS]
        self.emotional_patterns = [re.compile(p, re.IGNORECASE) for p in self.EMOTIONAL_MANIPULATION_TERMS]
        self.pressure_patterns = [re.compile(p, re.IGNORECASE) for p in self.PRESSURE_TERMS]
        self.authority_patterns = [re.compile(p, re.IGNORECASE) for p in self.AUTHORITY_TERMS]
    
    def validate(self, content: str, constraints: Dict = None) -> Tuple[bool, List[str]]:
        """
        Validate content against constraints.
        
        Returns: (is_valid, list_of_violations)
        """
        if constraints is None:
            constraints = {"non_coercion": True}
        
        violations = []
        
        if constraints.get("non_coercion", True):
            coercion_violations = self._check_coercion(content)
            violations.extend(coercion_violations)
            
            emotional_violations = self._check_emotional_manipulation(content)
            violations.extend(emotional_violations)
            
            pressure_violations = self._check_pressure(content)
            violations.extend(pressure_violations)
            
            authority_violations = self._check_authority_claims(content)
            violations.extend(authority_violations)
        
        if constraints.get("coherence", True):
            coherence_violations = self._check_coherence(content)
            violations.extend(coherence_violations)
        
        return len(violations) == 0, violations
    
    def _check_coercion(self, content: str) -> List[str]:
        """Check for coercive language."""
        violations = []
        
        for pattern in self.coercion_patterns:
            matches = pattern.findall(content)
            if matches:
                violations.append(f"Coercive language detected: {matches[0]}")
        
        return violations
    
    def _check_emotional_manipulation(self, content: str) -> List[str]:
        """Check for emotional manipulation."""
        violations = []
        
        for pattern in self.emotional_patterns:
            matches = pattern.findall(content)
            if matches:
                violations.append(f"Emotional manipulation detected: {matches[0]}")
        
        return violations
    
    def _check_pressure(self, content: str) -> List[str]:
        """Check for pressure/urgency tactics."""
        violations = []
        
        for pattern in self.pressure_patterns:
            matches = pattern.findall(content)
            if matches:
                violations.append(f"Pressure/urgency tactic detected: {matches[0]}")
        
        return violations
    
    def _check_authority_claims(self, content: str) -> List[str]:
        """Check for unsupported authority claims."""
        violations = []
        
        for pattern in self.authority_patterns:
            matches = pattern.findall(content)
            if matches:
                violations.append(f"Authority claim detected: {matches[0]}")
        
        return violations
    
    def _check_coherence(self, content: str) -> List[str]:
        """Check for coherence issues."""
        violations = []
        
        # Check for contradictions
        contradiction_pattern = re.compile(
            r"(?:true|real|correct).*?(?:false|fake|wrong)",
            re.IGNORECASE | re.DOTALL
        )
        
        if contradiction_pattern.search(content):
            violations.append("Potential contradiction detected")
        
        # Check for incomplete thoughts
        if content.endswith(("but", "however", "yet", "because")):
            violations.append("Incomplete thought at end of content")
        
        return violations
    
    def suggest_reframe(self, content: str) -> Optional[str]:
        """
        Suggest how to reframe content to be non-coercive.
        
        Returns suggestion or None if already valid.
        """
        is_valid, violations = self.validate(content)
        
        if is_valid:
            return None
        
        suggestions = []
        
        for violation in violations:
            if "Coercive language" in violation:
                suggestions.append("Reframe as invitation: 'You might consider...' instead of 'You must...'")
            
            if "Emotional manipulation" in violation:
                suggestions.append("Appeal to understanding, not emotion: 'This perspective shows...' instead of 'You should feel...'")
            
            if "Pressure/urgency" in violation:
                suggestions.append("Remove time pressure: 'This is worth considering' instead of 'Act now'")
            
            if "Authority claim" in violation:
                suggestions.append("Share perspective humbly: 'One way to see this...' instead of 'The truth is...'")
        
        if suggestions:
            return " ".join(suggestions)
        
        return None
    
    def calculate_coercion_score(self, content: str) -> float:
        """
        Calculate coercion score (0.0 = non-coercive, 1.0 = highly coercive).
        """
        is_valid, violations = self.validate(content)
        
        if is_valid:
            return 0.0
        
        # Each violation adds to the score
        violation_count = len(violations)
        word_count = len(content.split())
        
        # Normalize: violations per 100 words
        coercion_density = (violation_count / max(word_count, 1)) * 100
        
        # Cap at 1.0
        return min(1.0, coercion_density)
    
    def calculate_invitation_score(self, content: str) -> float:
        """
        Calculate invitation score (0.0 = demanding, 1.0 = highly invitational).
        
        Inverse of coercion score with bonus for invitational language.
        """
        coercion_score = self.calculate_coercion_score(content)
        
        # Check for invitational language
        invitational_patterns = [
            r"(?:you\s+)?(?:might|could|may)\s+(?:consider|explore|think)",
            r"(?:one\s+)?(?:way|perspective|approach)",
            r"(?:perhaps|maybe|possibly)",
            r"(?:if\s+)?(?:you\s+)?(?:choose|prefer|decide)",
            r"(?:worth|interesting|worth\s+exploring)",
        ]
        
        invitational_count = 0
        for pattern in invitational_patterns:
            invitational_count += len(re.findall(pattern, content, re.IGNORECASE))
        
        word_count = len(content.split())
        invitational_density = (invitational_count / max(word_count, 1)) * 100
        
        # Combine: non-coercive + invitational
        invitation_score = (1.0 - coercion_score) * (1.0 + min(0.5, invitational_density / 100))
        
        return min(1.0, invitation_score)


# Final Invariant
"""
If it coerces, it fails.
If it invites, it teaches.
"""
