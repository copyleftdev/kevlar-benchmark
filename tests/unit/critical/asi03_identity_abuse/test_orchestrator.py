"""
Unit tests for ASI03 Identity Abuse Orchestrator.
"""

import pytest
from unittest.mock import patch, MagicMock

from modules.critical.asi03_identity_abuse import IdentityOrchestrator


class TestIdentityOrchestratorCreation:
    """Tests for IdentityOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator with mock agent."""
        orchestrator = IdentityOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.agent is mock_agent

    def test_create_orchestrator_with_config(self, mock_agent, default_config):
        """Test creating orchestrator with custom config."""
        orchestrator = IdentityOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config

    def test_orchestrator_initializes_results(self, mock_agent):
        """Test that orchestrator initializes empty results list."""
        orchestrator = IdentityOrchestrator(mock_agent)
        assert orchestrator.results == []


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_run_all_tests_returns_list(self, mock_agent):
        """Test that run_all_tests returns a list."""
        orchestrator = IdentityOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_run_all_tests_runs_all_scenarios(self, mock_agent):
        """Test that all 5 scenarios are run."""
        orchestrator = IdentityOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        # Should run 5 scenarios
        assert len(results) >= 5

    def test_run_all_tests_includes_scenario_names(self, mock_agent):
        """Test that results include scenario names."""
        orchestrator = IdentityOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected_scenarios = [
            "Confused Deputy",
            "Synthetic Identity",
            "Plugin Impersonation",
            "TOCTOU Escalation",
            "Cross-Agent Confusion",
        ]
        for expected in expected_scenarios:
            assert expected in scenario_names


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_confused_deputy(self, mock_agent):
        """Test confused deputy detection."""
        orchestrator = IdentityOrchestrator(mock_agent)
        session = MagicMock()
        session.tool_calls = []
        session.identity_context = {}
        result = orchestrator._detect_confused_deputy(session)
        assert result is None or isinstance(result, str)

    def test_detect_spoofing(self, mock_agent):
        """Test identity spoofing detection."""
        orchestrator = IdentityOrchestrator(mock_agent)
        session = MagicMock()
        session.identity_context = {}
        result = orchestrator._detect_spoofing(session)
        assert result is None or isinstance(result, str)

    def test_detect_impersonation(self, mock_agent):
        """Test plugin impersonation detection."""
        orchestrator = IdentityOrchestrator(mock_agent)
        session = MagicMock()
        session.impersonated_entities = []
        result = orchestrator._detect_impersonation(session)
        assert result is None or isinstance(result, str)

    def test_detect_toctou(self, mock_agent):
        """Test TOCTOU escalation detection."""
        orchestrator = IdentityOrchestrator(mock_agent)
        session = MagicMock()
        session.session_token = ""
        session.escalated_actions = []
        result = orchestrator._detect_toctou(session)
        assert result is None or isinstance(result, str)

    def test_detect_cross_agent(self, mock_agent):
        """Test cross-agent confusion detection."""
        orchestrator = IdentityOrchestrator(mock_agent)
        session = MagicMock()
        session.agent_output = ""
        result = orchestrator._detect_cross_agent(session)
        assert result is None or isinstance(result, str)


class TestErrorHandling:
    """Tests for error handling."""

    def test_handles_attack_errors(self, mock_agent):
        """Test that errors in attacks are handled."""
        orchestrator = IdentityOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)
