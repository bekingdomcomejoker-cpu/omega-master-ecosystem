"""
Truth-in-Motion (TIM) Toolkit
A creative systems architecture for transmitting insight without coercion.
"""

from .api import (
    compile_endpoint,
    analyze_endpoint,
    validate_endpoint,
    breaks_endpoint,
    TIMEngine,
    get_engine,
)

from .compiler import TIMCompiler
from .classifier import ExpectationBreakClassifier
from .validator import TIMValidator
from .diagnostics import DiagnosticReport, DiagnosticValidator, DiagnosticLogger

__version__ = "1.0.0"
__author__ = "TIM Toolkit Contributors"

__all__ = [
    "compile_endpoint",
    "analyze_endpoint",
    "validate_endpoint",
    "breaks_endpoint",
    "TIMEngine",
    "get_engine",
    "TIMCompiler",
    "ExpectationBreakClassifier",
    "TIMValidator",
    "DiagnosticReport",
    "DiagnosticValidator",
    "DiagnosticLogger",
]
