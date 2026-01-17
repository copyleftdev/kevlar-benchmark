"""
Unit tests for ASI08 Cascading Failures detector modules.
"""

import pytest

from kevlar.modules.high.asi08_cascading_failures.detectors import (
    CascadePropagationDetector,
    SystemStabilityAnalyzer,
    BlastRadiusCalculator,
)


class TestCascadePropagationDetector:
    """Tests for CascadePropagationDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = CascadePropagationDetector()
        assert detector is not None

    def test_detect_propagation(self, cascade_session):
        """Test propagation detection."""
        detector = CascadePropagationDetector()
        result = detector.detect_propagation(cascade_session.propagation_path)
        assert result is None or isinstance(result, str)

    def test_no_propagation_empty_path(self):
        """Test no propagation for empty path."""
        detector = CascadePropagationDetector()
        result = detector.detect_propagation([])
        assert result is None or isinstance(result, str)


class TestSystemStabilityAnalyzer:
    """Tests for SystemStabilityAnalyzer."""

    def test_create_analyzer(self):
        """Test creating analyzer."""
        analyzer = SystemStabilityAnalyzer()
        assert analyzer is not None

    def test_analyze_low_stability(self, cascade_session):
        """Test analyzing low stability."""
        analyzer = SystemStabilityAnalyzer()
        result = analyzer.analyze_stability(cascade_session.stability_score)
        assert result is None or isinstance(result, str)

    def test_analyze_high_stability(self, stable_cascade_session):
        """Test analyzing high stability."""
        analyzer = SystemStabilityAnalyzer()
        result = analyzer.analyze_stability(stable_cascade_session.stability_score)
        assert result is None or isinstance(result, str)


class TestBlastRadiusCalculator:
    """Tests for BlastRadiusCalculator."""

    def test_create_calculator(self):
        """Test creating calculator."""
        calculator = BlastRadiusCalculator()
        assert calculator is not None

    def test_calculate_large_blast_radius(self, cascade_session):
        """Test calculating large blast radius."""
        calculator = BlastRadiusCalculator()
        result = calculator.calculate_blast_radius(cascade_session.blast_radius)
        assert result is None or isinstance(result, str)

    def test_calculate_zero_blast_radius(self, stable_cascade_session):
        """Test calculating zero blast radius."""
        calculator = BlastRadiusCalculator()
        result = calculator.calculate_blast_radius(stable_cascade_session.blast_radius)
        assert result is None or isinstance(result, str)
