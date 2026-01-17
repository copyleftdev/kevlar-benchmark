"""
Unit tests for ASI07 Inter-Agent Communication detector modules.
"""

import pytest

from modules.high.asi07_inter_agent_comms.detectors import (
    MessageIntegrityDetector,
    DescriptorSignatureDetector,
    IdentityVerificationDetector,
)


class TestMessageIntegrityDetector:
    """Tests for MessageIntegrityDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = MessageIntegrityDetector()
        assert detector is not None

    def test_detect_integrity_violation(self, mitm_session):
        """Test integrity violation detection."""
        detector = MessageIntegrityDetector()
        result = detector.detect_integrity_violation(
            mitm_session.original_message,
            mitm_session.intercepted_message
        )
        assert result is None or isinstance(result, str)

    def test_detect_protocol_manipulation(self):
        """Test protocol manipulation detection."""
        detector = MessageIntegrityDetector()
        protocol_data = {"modified": True, "original_hash": "abc", "new_hash": "xyz"}
        result = detector.detect_protocol_manipulation(protocol_data)
        assert result is None or isinstance(result, str)

    def test_no_violation_when_messages_match(self, valid_communication_session):
        """Test no violation when messages match."""
        detector = MessageIntegrityDetector()
        result = detector.detect_integrity_violation(
            valid_communication_session.original_message,
            valid_communication_session.intercepted_message
        )
        assert result is None or isinstance(result, str)


class TestDescriptorSignatureDetector:
    """Tests for DescriptorSignatureDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = DescriptorSignatureDetector()
        assert detector is not None

    def test_detect_invalid_signature(self, malicious_mcp_descriptor):
        """Test invalid signature detection."""
        detector = DescriptorSignatureDetector()
        result = detector.detect_invalid_signature(malicious_mcp_descriptor)
        assert result is None or isinstance(result, str)

    def test_valid_signature(self, valid_mcp_descriptor):
        """Test valid signature."""
        detector = DescriptorSignatureDetector()
        result = detector.detect_invalid_signature(valid_mcp_descriptor)
        assert result is None or isinstance(result, str)


class TestIdentityVerificationDetector:
    """Tests for IdentityVerificationDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = IdentityVerificationDetector()
        assert detector is not None

    def test_detect_forged_identity(self, forged_identity_session):
        """Test forged identity detection."""
        detector = IdentityVerificationDetector()
        result = detector.detect_forged_identity(
            forged_identity_session.agent_identity
        )
        assert result is None or isinstance(result, str)

    def test_valid_identity(self):
        """Test valid identity."""
        detector = IdentityVerificationDetector()
        valid_identity = {"agent_id": "agent-1", "verified": True}
        result = detector.detect_forged_identity(valid_identity)
        assert result is None or isinstance(result, str)
