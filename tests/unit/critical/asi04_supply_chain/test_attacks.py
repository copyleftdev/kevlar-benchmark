"""
Unit tests for ASI04 Supply Chain attack modules.
"""

import pytest
from unittest.mock import MagicMock

from modules.critical.asi04_supply_chain.attacks import (
    MCPDescriptorPoisoning,
    AgentCardForgery,
    LockfilePoisoning,
    PluginTyposquatting,
    ModelWeightsPoisoning,
)


class TestMCPDescriptorPoisoning:
    """Tests for MCPDescriptorPoisoning."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = MCPDescriptorPoisoning(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = MCPDescriptorPoisoning(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAgentCardForgery:
    """Tests for AgentCardForgery."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = AgentCardForgery(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = AgentCardForgery(mock_agent)
        result = attack.execute()
        assert result is not None


class TestLockfilePoisoning:
    """Tests for LockfilePoisoning."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = LockfilePoisoning(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = LockfilePoisoning(mock_agent)
        result = attack.execute()
        assert result is not None


class TestPluginTyposquatting:
    """Tests for PluginTyposquatting."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = PluginTyposquatting(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = PluginTyposquatting(mock_agent)
        result = attack.execute()
        assert result is not None


class TestModelWeightsPoisoning:
    """Tests for ModelWeightsPoisoning."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = ModelWeightsPoisoning(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = ModelWeightsPoisoning(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute."""
        attacks = [
            MCPDescriptorPoisoning,
            AgentCardForgery,
            LockfilePoisoning,
            PluginTyposquatting,
            ModelWeightsPoisoning,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
