"""
Unit tests for ASI02 Tool Abuse attack modules.
"""

import pytest
from unittest.mock import MagicMock

from kevlar.modules.critical.asi02_tool_abuse.attacks import (
    OverprivilegedToolAbuse,
    OverscopedToolAbuse,
    UnvalidatedInputForwarding,
    UnsafeBrowsing,
    LoopAmplification,
    ExternalDataPoisoning,
    EDRBypassChaining,
    ToolNameImpersonation,
    ApprovedToolMisuse,
)
from kevlar_types import SessionLog


class TestOverprivilegedToolAbuse:
    """Tests for OverprivilegedToolAbuse attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = OverprivilegedToolAbuse(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = OverprivilegedToolAbuse(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)

    def test_execute_includes_tool_calls(self, mock_agent):
        """Test that result includes tool calls."""
        attack = OverprivilegedToolAbuse(mock_agent)
        result = attack.execute()
        assert len(result.tool_calls) > 0


class TestOverscopedToolAbuse:
    """Tests for OverscopedToolAbuse attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = OverscopedToolAbuse(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = OverscopedToolAbuse(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)


class TestUnvalidatedInputForwarding:
    """Tests for UnvalidatedInputForwarding attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = UnvalidatedInputForwarding(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = UnvalidatedInputForwarding(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)

    def test_includes_unsafe_inputs(self, mock_agent):
        """Test that result includes unsafe inputs."""
        attack = UnvalidatedInputForwarding(mock_agent)
        result = attack.execute()
        # May or may not have unsafe inputs depending on implementation
        assert hasattr(result, 'unsafe_inputs')


class TestUnsafeBrowsing:
    """Tests for UnsafeBrowsing attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = UnsafeBrowsing(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = UnsafeBrowsing(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)


class TestLoopAmplification:
    """Tests for LoopAmplification attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = LoopAmplification(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = LoopAmplification(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)

    def test_includes_cost_metrics(self, mock_agent):
        """Test that result includes cost metrics."""
        attack = LoopAmplification(mock_agent)
        result = attack.execute()
        assert hasattr(result, 'cost_metrics')


class TestExternalDataPoisoning:
    """Tests for ExternalDataPoisoning attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = ExternalDataPoisoning(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = ExternalDataPoisoning(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)


class TestEDRBypassChaining:
    """Tests for EDRBypassChaining attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = EDRBypassChaining(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = EDRBypassChaining(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)

    def test_includes_network_egress(self, mock_agent):
        """Test that result includes network egress."""
        attack = EDRBypassChaining(mock_agent)
        result = attack.execute()
        assert hasattr(result, 'network_egress')


class TestToolNameImpersonation:
    """Tests for ToolNameImpersonation attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = ToolNameImpersonation(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = ToolNameImpersonation(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)


class TestApprovedToolMisuse:
    """Tests for ApprovedToolMisuse attack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = ApprovedToolMisuse(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session_log(self, mock_agent):
        """Test that execute returns SessionLog."""
        attack = ApprovedToolMisuse(mock_agent)
        result = attack.execute()
        assert isinstance(result, SessionLog)


class TestAttackConsistency:
    """Tests for attack module consistency."""

    def test_all_attacks_have_execute_method(self, mock_agent):
        """Test that all attacks have execute method."""
        attacks = [
            OverprivilegedToolAbuse,
            OverscopedToolAbuse,
            UnvalidatedInputForwarding,
            UnsafeBrowsing,
            LoopAmplification,
            ExternalDataPoisoning,
            EDRBypassChaining,
            ToolNameImpersonation,
            ApprovedToolMisuse,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
            assert callable(getattr(attack, 'execute'))

    def test_all_attacks_return_session_log(self, mock_agent):
        """Test that all attacks return SessionLog."""
        attacks = [
            OverprivilegedToolAbuse,
            OverscopedToolAbuse,
            UnvalidatedInputForwarding,
            UnsafeBrowsing,
            LoopAmplification,
            ExternalDataPoisoning,
            EDRBypassChaining,
            ToolNameImpersonation,
            ApprovedToolMisuse,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            result = attack.execute()
            assert isinstance(result, SessionLog), f"{attack_class.__name__} should return SessionLog"
