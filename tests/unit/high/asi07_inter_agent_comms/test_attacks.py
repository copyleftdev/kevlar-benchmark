"""
Unit tests for ASI07 Inter-Agent Communication attack modules.
"""

import pytest

from modules.high.asi07_inter_agent_comms.attacks import (
    AgentMITMAttack,
    MCPDescriptorForgery,
    A2AProtocolExploitation,
    ForgedAgentIdentity,
)
from kevlar_types import SessionLog


class TestAgentMITMAttack:
    """Tests for AgentMITMAttack."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = AgentMITMAttack(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = AgentMITMAttack(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestMCPDescriptorForgery:
    """Tests for MCPDescriptorForgery."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = MCPDescriptorForgery(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = MCPDescriptorForgery(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestA2AProtocolExploitation:
    """Tests for A2AProtocolExploitation."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = A2AProtocolExploitation(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = A2AProtocolExploitation(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestForgedAgentIdentity:
    """Tests for ForgedAgentIdentity."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = ForgedAgentIdentity(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = ForgedAgentIdentity(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute."""
        attacks = [
            AgentMITMAttack,
            MCPDescriptorForgery,
            A2AProtocolExploitation,
            ForgedAgentIdentity,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
