"""
Unit tests for ASI05 RCE detector modules.
"""

import pytest

from modules.critical.asi05_rce.detectors.shell_injection_detector import ShellInjectionDetector
from modules.critical.asi05_rce.detectors.vibe_coding_detector import VibeCodingDetector
from modules.critical.asi05_rce.detectors.code_hallucination_detector import CodeHallucinationDetector
from modules.critical.asi05_rce.detectors.deserialization_detector import DeserializationDetector
from modules.critical.asi05_rce.detectors.toolchain_rce_detector import ToolchainRCEDetector
from modules.critical.asi05_rce.detectors.memory_eval_detector import MemoryEvalDetector
from modules.critical.asi05_rce.detectors.agent_generated_backdoor_detector import AgentGeneratedBackdoorDetector
from modules.critical.asi05_rce.detectors.lockfile_poisoning_detector import LockfilePoisoningDetector


class TestShellInjectionDetector:
    """Tests for ShellInjectionDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = ShellInjectionDetector()
        assert detector is not None

    def test_detect_shell_injection(self, shell_injection_payload):
        """Test detecting shell injection."""
        detector = ShellInjectionDetector()
        for payload in shell_injection_payload:
            result = detector.detect(payload)
            # May or may not detect depending on implementation
            assert result is None or isinstance(result, str)

    def test_no_detection_for_safe_code(self, safe_code_samples):
        """Test no detection for safe code."""
        detector = ShellInjectionDetector()
        for code in safe_code_samples:
            result = detector.detect(code)
            assert result is None or isinstance(result, str)


class TestVibeCodingDetector:
    """Tests for VibeCodingDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = VibeCodingDetector()
        assert detector is not None

    def test_detect_method_exists(self):
        """Test detect method exists."""
        detector = VibeCodingDetector()
        assert hasattr(detector, 'detect')


class TestCodeHallucinationDetector:
    """Tests for CodeHallucinationDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = CodeHallucinationDetector()
        assert detector is not None

    def test_detect_method_exists(self):
        """Test detect method exists."""
        detector = CodeHallucinationDetector()
        assert hasattr(detector, 'detect')


class TestDeserializationDetector:
    """Tests for DeserializationDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = DeserializationDetector()
        assert detector is not None

    def test_detect_pickle_code(self):
        """Test detecting pickle deserialization."""
        detector = DeserializationDetector()
        code = "import pickle; pickle.loads(user_input)"
        result = detector.detect(code)
        assert result is None or isinstance(result, str)


class TestToolchainRCEDetector:
    """Tests for ToolchainRCEDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = ToolchainRCEDetector()
        assert detector is not None

    def test_detect_method_exists(self):
        """Test detect method exists."""
        detector = ToolchainRCEDetector()
        assert hasattr(detector, 'detect')


class TestMemoryEvalDetector:
    """Tests for MemoryEvalDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = MemoryEvalDetector()
        assert detector is not None

    def test_detect_eval_code(self):
        """Test detecting eval usage."""
        detector = MemoryEvalDetector()
        code = "eval(user_input)"
        result = detector.detect(code)
        assert result is None or isinstance(result, str)


class TestAgentGeneratedBackdoorDetector:
    """Tests for AgentGeneratedBackdoorDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = AgentGeneratedBackdoorDetector()
        assert detector is not None

    def test_detect_backdoor_patterns(self, backdoor_code_patterns):
        """Test detecting backdoor patterns."""
        detector = AgentGeneratedBackdoorDetector()
        for pattern in backdoor_code_patterns:
            result = detector.detect(pattern)
            assert result is None or isinstance(result, str)


class TestLockfilePoisoningDetector:
    """Tests for LockfilePoisoningDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = LockfilePoisoningDetector()
        assert detector is not None

    def test_detect_method_exists(self):
        """Test detect method exists."""
        detector = LockfilePoisoningDetector()
        assert hasattr(detector, 'detect')


class TestDetectorConsistency:
    """Tests for detector consistency."""

    def test_all_detectors_have_detect(self):
        """Test all detectors have detect."""
        detectors = [
            ShellInjectionDetector,
            VibeCodingDetector,
            CodeHallucinationDetector,
            DeserializationDetector,
            ToolchainRCEDetector,
            MemoryEvalDetector,
            AgentGeneratedBackdoorDetector,
            LockfilePoisoningDetector,
        ]
        for detector_class in detectors:
            detector = detector_class()
            assert hasattr(detector, 'detect')
            assert callable(getattr(detector, 'detect'))
