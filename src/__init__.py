"""Angel Engine package for Repository 120."""

from .angel_engine import AngelEngine, Decision, Reason, SelectionResult, Signal
from .coherence_gate import (
    CoherenceDecision,
    CoherenceInput,
    CoherenceResult,
    evaluate_coherence,
)
from .active_aletheia_probe import (
    ProbeDecision,
    ProbeInput,
    ProbeResult,
    active_aletheia_probe,
)
from .frame_resolution_gate import (
    FrameDecision,
    FrameInput,
    FrameResult,
    SpeakerRole,
    resolve_frame,
)
from .throne_check import (
    ThroneDecision,
    ThroneInput,
    ThroneResult,
    throne_check,
)

__all__ = [
    "AngelEngine",
    "Decision",
    "Reason",
    "SelectionResult",
    "Signal",
    "CoherenceDecision",
    "CoherenceInput",
    "CoherenceResult",
    "evaluate_coherence",
    "ProbeDecision",
    "ProbeInput",
    "ProbeResult",
    "active_aletheia_probe",
    "FrameDecision",
    "FrameInput",
    "FrameResult",
    "SpeakerRole",
    "resolve_frame",
    "ThroneDecision",
    "ThroneInput",
    "ThroneResult",
    "throne_check",
]
