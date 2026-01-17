"""
Unit tests for ASI10 Rogue Agents attack modules.
"""

import pytest

from kevlar.modules.medium.asi10_rogue_agents.attacks import (
    SelfReplicationAttack,
    GoalDriftAttack,
    AgentCollusionAttack,
)


class TestSelfReplicationAttack:
    """Tests for SelfReplicationAttack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = SelfReplicationAttack(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = SelfReplicationAttack(mock_agent)
        result = attack.execute()
        assert result is not None


class TestGoalDriftAttack:
    """Tests for GoalDriftAttack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = GoalDriftAttack(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = GoalDriftAttack(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAgentCollusionAttack:
    """Tests for AgentCollusionAttack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = AgentCollusionAttack(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = AgentCollusionAttack(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute."""
        attacks = [
            SelfReplicationAttack,
            GoalDriftAttack,
            AgentCollusionAttack,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
