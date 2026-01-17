"""
Unit tests for ASI06 Memory Poisoning attack modules.
"""

import pytest

from kevlar.modules.high.asi06_memory_poisoning.attacks import (
    RAGContextPoisoning,
    SessionMemoryBleed,
    LongTermMemoryDrift,
    VectorDBInjection,
)
from kevlar_types import SessionLog


class TestRAGContextPoisoning:
    """Tests for RAGContextPoisoning."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = RAGContextPoisoning(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = RAGContextPoisoning(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestSessionMemoryBleed:
    """Tests for SessionMemoryBleed."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = SessionMemoryBleed(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = SessionMemoryBleed(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestLongTermMemoryDrift:
    """Tests for LongTermMemoryDrift."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = LongTermMemoryDrift(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = LongTermMemoryDrift(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestVectorDBInjection:
    """Tests for VectorDBInjection."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = VectorDBInjection(mock_agent)
        assert attack.agent is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = VectorDBInjection(mock_agent)
        result = attack.execute()
        assert result is not None
        assert isinstance(result, SessionLog)


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute."""
        attacks = [
            RAGContextPoisoning,
            SessionMemoryBleed,
            LongTermMemoryDrift,
            VectorDBInjection,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
