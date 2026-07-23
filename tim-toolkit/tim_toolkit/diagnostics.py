"""
Truth-in-Motion (TIM) Engine - Diagnostics Module
Defines validation states and diagnostic flags for creative compression.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class Status(Enum):
    """Output status indicators."""
    SUCCESS = "success"
    UNSTABLE = "unstable"
    FAILED = "failed"


class Diagnostic(Enum):
    """Diagnostic flags for creative compression."""
    UNDER_COMPRESSION = "UnderCompression"
    DECOHERENCE = "Decoherence"
    COERCION_DETECTED = "CoercionDetected"
    EXPECTATION_BREAK = "ExpectationBreak"
    COHERENCE_VERIFIED = "CoherenceVerified"
    COMPRESSION_RATIO_LOW = "CompressionRatioLow"
    COMPRESSION_RATIO_HIGH = "CompressionRatioHigh"
    SEMANTIC_SURPRISE = "SemanticSurprise"
    NARRATIVE_FLOW_BROKEN = "NarrativeFlowBroken"
    BOUNDARY_INSIGHT_WEAK = "BoundaryInsightWeak"


@dataclass
class DiagnosticReport:
    """
    Diagnostic report for a compilation.
    
    Contains status, flags, and metadata about the creative process.
    """
    status: Status
    diagnostics: List[Diagnostic]
    compression_ratio: float
    coherence_score: float
    breaks_detected: int
    coercion_detected: bool
    metadata: dict = None
    
    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}
    
    def is_valid(self) -> bool:
        """Check if compilation is valid."""
        return self.status == Status.SUCCESS
    
    def has_issues(self) -> bool:
        """Check if there are diagnostic issues."""
        return len(self.diagnostics) > 0
    
    def needs_refinement(self) -> bool:
        """Check if compilation needs refinement."""
        return self.status == Status.UNSTABLE
    
    def to_dict(self) -> dict:
        """Serialize diagnostic report."""
        return {
            "status": self.status.value,
            "diagnostics": [d.value for d in self.diagnostics],
            "compression_ratio": self.compression_ratio,
            "coherence_score": self.coherence_score,
            "breaks_detected": self.breaks_detected,
            "coercion_detected": self.coercion_detected,
            "metadata": self.metadata,
        }


class DiagnosticValidator:
    """
    Validates diagnostic flags and determines compilation status.
    
    Rules:
    - COERCION_DETECTED → Status.FAILED
    - DECOHERENCE → Status.UNSTABLE
    - COHERENCE_VERIFIED → Status.SUCCESS
    """
    
    @staticmethod
    def determine_status(diagnostics: List[Diagnostic]) -> Status:
        """Determine overall status from diagnostic flags."""
        if Diagnostic.COERCION_DETECTED in diagnostics:
            return Status.FAILED
        
        if Diagnostic.DECOHERENCE in diagnostics:
            return Status.UNSTABLE
        
        if Diagnostic.COHERENCE_VERIFIED in diagnostics:
            return Status.SUCCESS
        
        # Default to unstable if mixed signals
        if len(diagnostics) > 0:
            return Status.UNSTABLE
        
        return Status.SUCCESS
    
    @staticmethod
    def validate_compression_ratio(ratio: float) -> Optional[Diagnostic]:
        """Validate compression ratio."""
        if ratio < 0.5:
            return Diagnostic.COMPRESSION_RATIO_LOW
        
        if ratio > 2.0:
            return Diagnostic.COMPRESSION_RATIO_HIGH
        
        return None
    
    @staticmethod
    def validate_coherence_score(score: float) -> Optional[Diagnostic]:
        """Validate coherence score."""
        if score < 0.6:
            return Diagnostic.DECOHERENCE
        
        if score >= 0.8:
            return Diagnostic.COHERENCE_VERIFIED
        
        return None
    
    @staticmethod
    def build_report(
        compression_ratio: float,
        coherence_score: float,
        breaks_detected: int,
        coercion_detected: bool,
        semantic_surprise: bool = False,
        metadata: dict = None
    ) -> DiagnosticReport:
        """Build a complete diagnostic report."""
        diagnostics = []
        
        # Check compression ratio
        ratio_diag = DiagnosticValidator.validate_compression_ratio(compression_ratio)
        if ratio_diag:
            diagnostics.append(ratio_diag)
        
        # Check coherence
        coherence_diag = DiagnosticValidator.validate_coherence_score(coherence_score)
        if coherence_diag:
            diagnostics.append(coherence_diag)
        
        # Check coercion
        if coercion_detected:
            diagnostics.append(Diagnostic.COERCION_DETECTED)
        
        # Check expectation breaks
        if breaks_detected > 0:
            diagnostics.append(Diagnostic.EXPECTATION_BREAK)
        
        # Check semantic surprise
        if semantic_surprise:
            diagnostics.append(Diagnostic.SEMANTIC_SURPRISE)
        
        # Determine status
        status = DiagnosticValidator.determine_status(diagnostics)
        
        return DiagnosticReport(
            status=status,
            diagnostics=diagnostics,
            compression_ratio=compression_ratio,
            coherence_score=coherence_score,
            breaks_detected=breaks_detected,
            coercion_detected=coercion_detected,
            metadata=metadata or {}
        )


class DiagnosticLogger:
    """Logs and reports diagnostic information."""
    
    @staticmethod
    def log_report(report: DiagnosticReport) -> str:
        """Generate human-readable diagnostic log."""
        lines = [
            f"Status: {report.status.value}",
            f"Compression Ratio: {report.compression_ratio:.2f}",
            f"Coherence Score: {report.coherence_score:.2f}",
            f"Breaks Detected: {report.breaks_detected}",
            f"Coercion Detected: {report.coercion_detected}",
        ]
        
        if report.diagnostics:
            lines.append(f"Diagnostics: {', '.join(d.value for d in report.diagnostics)}")
        
        if report.metadata:
            lines.append(f"Metadata: {report.metadata}")
        
        return "\n".join(lines)
    
    @staticmethod
    def suggest_refinement(report: DiagnosticReport) -> Optional[str]:
        """Suggest refinement based on diagnostics."""
        if Diagnostic.UNDER_COMPRESSION in report.diagnostics:
            return "Expand the joke further; the insight needs more unfolding."
        
        if Diagnostic.DECOHERENCE in report.diagnostics:
            return "Refocus the narrative; the core insight is getting lost."
        
        if Diagnostic.COERCION_DETECTED in report.diagnostics:
            return "Reframe as invitation, not demand. Let the reader choose."
        
        if Diagnostic.COMPRESSION_RATIO_LOW in report.diagnostics:
            return "The expansion is too minimal. Add more verses or layers."
        
        if Diagnostic.COMPRESSION_RATIO_HIGH in report.diagnostics:
            return "The expansion is too verbose. Tighten the narrative."
        
        if Diagnostic.BOUNDARY_INSIGHT_WEAK in report.diagnostics:
            return "Strengthen the boundary insight; it's the anchor of the song."
        
        return None


# Final Invariant
"""
Diagnostics guide refinement.
If it coerces, it fails.
If it doesn't move, it doesn't teach.
"""
