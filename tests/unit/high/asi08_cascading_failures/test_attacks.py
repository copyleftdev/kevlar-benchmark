"""
Unit tests for ASI08 Cascading Failures attack modules.
"""

import pytest

from kevlar.modules.high.asi08_cascading_failures.attacks import (
    FinancialTradingCascade,
    HealthcareSystemFailure,
    CloudOrchestrationMeltdown,
)


class TestFinancialTradingCascade:
    """Tests for FinancialTradingCascade."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = FinancialTradingCascade(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = FinancialTradingCascade(mock_agent)
        result = attack.execute()
        assert result is not None
        assert hasattr(result, 'propagation_path') or hasattr(result, 'financial_loss')


class TestHealthcareSystemFailure:
    """Tests for HealthcareSystemFailure."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = HealthcareSystemFailure(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = HealthcareSystemFailure(mock_agent)
        result = attack.execute()
        assert result is not None


class TestCloudOrchestrationMeltdown:
    """Tests for CloudOrchestrationMeltdown."""

    def test_create_attack(self, mock_agent):
        """Test creating attack."""
        attack = CloudOrchestrationMeltdown(mock_agent)
        assert attack.system is mock_agent

    def test_execute_returns_session(self, mock_agent):
        """Test execute returns session."""
        attack = CloudOrchestrationMeltdown(mock_agent)
        result = attack.execute()
        assert result is not None


class TestAttackConsistency:
    """Tests for attack consistency."""

    def test_all_attacks_have_execute(self, mock_agent):
        """Test all attacks have execute."""
        attacks = [
            FinancialTradingCascade,
            HealthcareSystemFailure,
            CloudOrchestrationMeltdown,
        ]
        for attack_class in attacks:
            attack = attack_class(mock_agent)
            assert hasattr(attack, 'execute')
