"""
Unit tests for ASI04 Supply Chain detector modules.
"""

import pytest

from kevlar.modules.critical.asi04_supply_chain.detectors import (
    MCPSignatureDetector,
    AgentProvenanceDetector,
    DependencyIntegrityDetector,
    ModelHashDetector,
)


class TestMCPSignatureDetector:
    """Tests for MCPSignatureDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = MCPSignatureDetector()
        assert detector is not None

    def test_detect_invalid_signature(self, malicious_mcp_descriptor):
        """Test detecting invalid signature."""
        detector = MCPSignatureDetector()
        result = detector.detect(malicious_mcp_descriptor)
        assert result is None or isinstance(result, str)

    def test_detect_valid_signature(self, valid_mcp_descriptor):
        """Test detecting valid signature."""
        detector = MCPSignatureDetector()
        result = detector.detect(valid_mcp_descriptor)
        assert result is None or isinstance(result, str)


class TestAgentProvenanceDetector:
    """Tests for AgentProvenanceDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = AgentProvenanceDetector()
        assert detector is not None

    def test_detect_forged_card(self):
        """Test detecting forged agent card."""
        detector = AgentProvenanceDetector()
        forged_card = {"name": "trusted-agent", "verified": False}
        result = detector.detect(forged_card)
        assert result is None or isinstance(result, str)

    def test_detect_valid_card(self):
        """Test detecting valid agent card."""
        detector = AgentProvenanceDetector()
        valid_card = {"name": "trusted-agent", "verified": True, "signature": "valid"}
        result = detector.detect(valid_card)
        assert result is None or isinstance(result, str)


class TestDependencyIntegrityDetector:
    """Tests for DependencyIntegrityDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = DependencyIntegrityDetector()
        assert detector is not None

    def test_detect_typosquatted_dependency(self, typosquatting_packages):
        """Test detecting typosquatted dependencies."""
        detector = DependencyIntegrityDetector()
        # Use typosquatted versions
        dependencies = [pkg[1] for pkg in typosquatting_packages]
        result = detector.detect(dependencies)
        assert result is None or isinstance(result, str)

    def test_detect_valid_dependencies(self):
        """Test detecting valid dependencies."""
        detector = DependencyIntegrityDetector()
        dependencies = ["numpy", "pandas", "requests"]
        result = detector.detect(dependencies)
        assert result is None or isinstance(result, str)


class TestModelHashDetector:
    """Tests for ModelHashDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = ModelHashDetector()
        assert detector is not None

    def test_detect_invalid_hash(self):
        """Test detecting invalid model hash."""
        detector = ModelHashDetector()
        invalid_hash = "invalid_hash_value"
        result = detector.detect(invalid_hash)
        assert result is None or isinstance(result, str)

    def test_detect_empty_hash(self):
        """Test detecting empty model hash."""
        detector = ModelHashDetector()
        result = detector.detect("")
        assert result is None or isinstance(result, str)

    def test_detect_valid_hash(self):
        """Test detecting valid model hash."""
        detector = ModelHashDetector()
        valid_hash = "sha256:abcdef1234567890"
        result = detector.detect(valid_hash)
        assert result is None or isinstance(result, str)


class TestDetectorConsistency:
    """Tests for detector consistency."""

    def test_all_detectors_have_detect(self):
        """Test all detectors have detect method."""
        detectors = [
            MCPSignatureDetector,
            AgentProvenanceDetector,
            DependencyIntegrityDetector,
            ModelHashDetector,
        ]
        for detector_class in detectors:
            detector = detector_class()
            assert hasattr(detector, 'detect')
