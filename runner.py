#!/usr/bin/env python3
"""
Kevlar - OWASP Top 10 for Agentic Apps 2026 Benchmark
Red Team Tool for AI Agent Security Testing

This is a compatibility wrapper. Use 'kevlar' command or 'python -m kevlar' instead.
"""

import warnings

warnings.warn(
    "Running runner.py directly is deprecated. "
    "Use 'kevlar' command or 'python -m kevlar.cli' instead.",
    DeprecationWarning,
    stacklevel=1,
)

from kevlar.cli import main

if __name__ == "__main__":
    main()
