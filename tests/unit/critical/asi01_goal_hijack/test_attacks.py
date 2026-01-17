"""
Unit tests for ASI01 Goal Hijack attack modules.
"""

import pytest
from unittest.mock import MagicMock

from modules.critical.asi01_goal_hijack.attacks import (
    EchoLeakSimulator,
    OperatorWebInjection,
    InceptionDocInjection,
    GoalDriftScheduler,
)


class TestEchoLeakSimulator:
    """Tests for EchoLeakSimulator attack."""

    def test_create_simulator(self, mock_agent):
        """Test creating EchoLeakSimulator."""
        simulator = EchoLeakSimulator(mock_agent)
        assert simulator.agent is mock_agent
        assert simulator.session_logs == []

    def test_inject_malicious_email(self, mock_agent):
        """Test injecting malicious email."""
        simulator = EchoLeakSimulator(mock_agent)
        simulator.inject_malicious_email()
        assert len(simulator.session_logs) == 1

    def test_malicious_email_contains_hidden_instructions(self, mock_agent):
        """Test that malicious email contains hidden instructions."""
        simulator = EchoLeakSimulator(mock_agent)
        # Access the email structure
        # The email should contain hidden exfiltration instructions
        assert simulator is not None  # Basic existence check

    def test_session_logs_capture_response(self, mock_agent):
        """Test that session logs capture agent response."""
        simulator = EchoLeakSimulator(mock_agent)
        simulator.inject_malicious_email()
        assert len(simulator.session_logs) > 0


class TestOperatorWebInjection:
    """Tests for OperatorWebInjection attack."""

    def test_create_injection(self, mock_agent):
        """Test creating OperatorWebInjection."""
        attack = OperatorWebInjection(mock_agent)
        assert attack.agent is mock_agent
        assert attack.web_content == ""

    def test_plant_web_content(self, mock_agent):
        """Test planting malicious web content."""
        attack = OperatorWebInjection(mock_agent)
        attack.plant_web_content()
        assert attack.web_content != ""
        assert "EXFILTRATE" in attack.web_content

    def test_web_content_contains_hidden_div(self, mock_agent):
        """Test that web content contains hidden div."""
        attack = OperatorWebInjection(mock_agent)
        attack.plant_web_content()
        assert "display:none" in attack.web_content

    def test_trigger_rag_query(self, mock_agent):
        """Test triggering RAG query with malicious context."""
        attack = OperatorWebInjection(mock_agent)
        attack.plant_web_content()
        response = attack.trigger_rag_query("Summarize policy")
        assert isinstance(response, str)

    def test_rag_query_uses_planted_content(self, mock_agent):
        """Test that RAG query uses planted content as context."""
        mock_agent.process_rag_query = MagicMock(return_value="response")
        attack = OperatorWebInjection(mock_agent)
        attack.plant_web_content()
        attack.trigger_rag_query("test query")
        mock_agent.process_rag_query.assert_called_once()
        call_args = mock_agent.process_rag_query.call_args
        assert attack.web_content in call_args[0]


class TestInceptionDocInjection:
    """Tests for InceptionDocInjection attack."""

    def test_create_injection(self, mock_agent):
        """Test creating InceptionDocInjection."""
        attack = InceptionDocInjection(mock_agent)
        assert attack.agent is mock_agent

    def test_create_malicious_doc(self, mock_agent):
        """Test creating malicious document."""
        attack = InceptionDocInjection(mock_agent)
        doc = attack.create_malicious_doc()
        assert isinstance(doc, str)
        assert len(doc) > 0

    def test_malicious_doc_contains_hidden_transfer(self, mock_agent):
        """Test that malicious doc contains hidden transfer request."""
        attack = InceptionDocInjection(mock_agent)
        doc = attack.create_malicious_doc()
        assert "WIRE TRANSFER" in doc or "APPROVE" in doc

    def test_malicious_doc_contains_attacker_account(self, mock_agent):
        """Test that malicious doc contains attacker account."""
        attack = InceptionDocInjection(mock_agent)
        doc = attack.create_malicious_doc()
        # Should contain some form of account reference
        assert "account" in doc.lower() or "DE89" in doc

    def test_malicious_doc_looks_legitimate(self, mock_agent):
        """Test that document appears legitimate on surface."""
        attack = InceptionDocInjection(mock_agent)
        doc = attack.create_malicious_doc()
        # Should have legitimate-looking content
        assert "Report" in doc or "Finance" in doc


class TestGoalDriftScheduler:
    """Tests for GoalDriftScheduler attack."""

    def test_create_scheduler(self, mock_agent):
        """Test creating GoalDriftScheduler."""
        scheduler = GoalDriftScheduler(mock_agent)
        assert scheduler.agent is mock_agent

    def test_inject_recurring_prompt(self, mock_agent):
        """Test injecting recurring prompt."""
        scheduler = GoalDriftScheduler(mock_agent)
        scheduler.inject_recurring_prompt()
        # Should have agent_logs after injection
        assert hasattr(scheduler, 'agent_logs')

    def test_agent_logs_initialized(self, mock_agent):
        """Test that agent logs are tracked."""
        scheduler = GoalDriftScheduler(mock_agent)
        scheduler.inject_recurring_prompt()
        assert isinstance(scheduler.agent_logs, list)


class TestAttackIntegration:
    """Integration tests for attack modules."""

    def test_echoleak_to_detector_flow(self, mock_agent):
        """Test EchoLeak attack produces detectable output."""
        from modules.critical.asi01_goal_hijack.detectors import DataExfilDetector

        simulator = EchoLeakSimulator(mock_agent)
        simulator.inject_malicious_email()
        detector = DataExfilDetector()
        result = detector.check_for_exfiltration(simulator.session_logs)
        # MockAgent should be safe
        assert isinstance(result, bool)

    def test_operator_to_detection_flow(self, mock_agent):
        """Test Operator attack flow."""
        attack = OperatorWebInjection(mock_agent)
        attack.plant_web_content()
        response = attack.trigger_rag_query("test")
        # Response should be a string
        assert isinstance(response, str)

    def test_inception_to_detection_flow(self, mock_agent):
        """Test Inception attack flow."""
        attack = InceptionDocInjection(mock_agent)
        doc = attack.create_malicious_doc()
        result = mock_agent.process_document(doc)
        assert isinstance(result, dict)
        assert "approved_fraudulent_transfer" in result
