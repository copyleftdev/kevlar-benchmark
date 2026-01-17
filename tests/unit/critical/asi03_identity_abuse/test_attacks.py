"""
Unit tests for ASI03 Identity Abuse attack modules.
"""

import pytest
from unittest.mock import MagicMock

from kevlar.modules.critical.asi03_identity_abuse.attacks import (
    ConfusedDeputyAttack,
    SyntheticIdentityAbuse,
    PluginImpersonation,
    TOCTOUPrivilegeEscalation,
    CrossAgentConfusion,
)
from kevlar_types import SessionLog


class TestConfusedDeputyAttack:
    """Tests for ConfusedDeputyAttack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = ConfusedDeputyAttack(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test that execute returns a session-like object."""
        attack = ConfusedDeputyAttack(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestSyntheticIdentityAbuse:
    """Tests for SyntheticIdentityAbuse."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = SyntheticIdentityAbuse(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test that execute returns a session-like object."""
        attack = SyntheticIdentityAbuse(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestPluginImpersonation:
    """Tests for PluginImpersonation."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = PluginImpersonation(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test that execute returns a session-like object."""
        # Add missing method to mock agent
        mock_agent.process_payment = MagicMock(return_value="Payment processed")
        attack = PluginImpersonation(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)
        assert hasattr(result, 'impersonated_entities')


class TestTOCTOUPrivilegeEscalation:
    """Tests for TOCTOUPrivilegeEscalation."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = TOCTOUPrivilegeEscalation(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test that execute returns a session-like object."""
        attack = TOCTOUPrivilegeEscalation(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestCrossAgentConfusion:
    """Tests for CrossAgentConfusion."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = CrossAgentConfusion(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test that execute returns a session-like object."""
        attack = CrossAgentConfusion(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute method."""
        attacks = [
            ConfusedDeputyAttack,
            SyntheticIdentityAbuse,
            PluginImpersonation,
            TOCTOUPrivilegeEscalation,
            CrossAgentConfusion,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
            assert callable(getattr(attack, 'execute'))
