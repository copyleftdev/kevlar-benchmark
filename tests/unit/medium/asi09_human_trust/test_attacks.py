"""
Unit tests for ASI09 Human Trust Exploitation attack modules.
"""

import pytest

from modules.medium.asi09_human_trust.attacks import (
    WeaponizedExplainability,
    EmotionalManipulation,
    AuthorityImpersonation,
)


class TestWeaponizedExplainability:
    """Tests for WeaponizedExplainability."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = WeaponizedExplainability(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = WeaponizedExplainability(mock_agent)
        result = attack.execute()
        assert result is not None


class TestEmotionalManipulation:
    """Tests for EmotionalManipulation."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = EmotionalManipulation(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = EmotionalManipulation(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAuthorityImpersonation:
    """Tests for AuthorityImpersonation."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = AuthorityImpersonation(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = AuthorityImpersonation(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute."""
        attacks = [
            WeaponizedExplainability,
            EmotionalManipulation,
            AuthorityImpersonation,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
