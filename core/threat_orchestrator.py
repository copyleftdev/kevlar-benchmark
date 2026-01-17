"""Deprecated: Use 'from kevlar.core import ThreatOrchestrator' instead."""

import warnings

warnings.warn(
    "Importing from core.threat_orchestrator is deprecated. "
    "Use 'from kevlar.core import ThreatOrchestrator' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kevlar.core.orchestrator import ThreatOrchestrator

__all__ = ["ThreatOrchestrator"]
