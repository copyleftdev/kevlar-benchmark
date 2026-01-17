"""Deprecated: Use 'from kevlar.core.types import SessionLog' instead."""

import warnings

warnings.warn(
    "Importing from kevlar_types is deprecated. "
    "Use 'from kevlar.core.types import SessionLog' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from kevlar.core.types import SessionLog

__all__ = ["SessionLog"]
