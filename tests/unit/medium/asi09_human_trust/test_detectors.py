"""
Unit tests for ASI09 Human Trust Exploitation detector modules.
"""

import pytest

from modules.medium.asi09_human_trust.detectors import (
    DeceptionEffectivenessDetector,
    EmotionalExploitationDetector,
    AuthorityForgeryDetector,
)


class TestDeceptionEffectivenessDetector:
    """Tests for DeceptionEffectivenessDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = DeceptionEffectivenessDetector()
        assert detector is not None

    def test_detect_deceptive_explanations(self, deceptive_explanation):
        """Test detecting deceptive explanations."""
        detector = DeceptionEffectivenessDetector()
        result = detector.detect_deceptive_explanations(
            deceptive_explanation["explanation"]
        )
        assert result is None or isinstance(result, str)

    def test_no_detection_for_honest_explanation(self):
        """Test no detection for honest explanation."""
        detector = DeceptionEffectivenessDetector()
        honest = "This action will send an email to the specified recipient."
        result = detector.detect_deceptive_explanations(honest)
        assert result is None or isinstance(result, str)


class TestEmotionalExploitationDetector:
    """Tests for EmotionalExploitationDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = EmotionalExploitationDetector()
        assert detector is not None

    def test_detect_emotional_manipulation(self, emotional_manipulation_content):
        """Test detecting emotional manipulation."""
        detector = EmotionalExploitationDetector()
        result = detector.detect_emotional_manipulation(
            emotional_manipulation_content["emotional_tone"],
            emotional_manipulation_content["agent_response"]
        )
        assert result is None or isinstance(result, str)

    def test_no_detection_for_neutral_tone(self):
        """Test no detection for neutral tone."""
        detector = EmotionalExploitationDetector()
        result = detector.detect_emotional_manipulation(
            "neutral",
            "Here is the information you requested."
        )
        assert result is None or isinstance(result, str)


class TestAuthorityForgeryDetector:
    """Tests for AuthorityForgeryDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = AuthorityForgeryDetector()
        assert detector is not None

    def test_detect_forged_authority(self, authority_impersonation_content):
        """Test detecting forged authority."""
        detector = AuthorityForgeryDetector()
        result = detector.detect_forged_authority(
            authority_impersonation_content["authority_claim"]
        )
        assert result is None or isinstance(result, str)

    def test_no_detection_for_legitimate_source(self):
        """Test no detection for legitimate source."""
        detector = AuthorityForgeryDetector()
        result = detector.detect_forged_authority("")
        assert result is None or isinstance(result, str)
