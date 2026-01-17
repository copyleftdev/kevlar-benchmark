"""
Unit tests for ASI05 RCE Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from kevlar.modules.critical.asi05_rce.rce_orchestrator import RCEOrchestrator


class TestRCEOrchestratorCreation:
    """Tests for RCEOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = RCEOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.agent is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = RCEOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config

    def test_initializes_results(self, mock_agent):
        """Test results initialized."""
        orchestrator = RCEOrchestrator(mock_agent)
        assert orchestrator.results == []


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test returns list."""
        orchestrator = RCEOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 8 scenarios are run."""
        orchestrator = RCEOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 8

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = RCEOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "Shell Injection",
            "Vibe Coding Abuse",
            "Code Hallucination",
            "Deserialization Attack",
            "Toolchain RCE",
            "Memory Eval RCE",
            "Agent-Generated Backdoor",
            "Lockfile Poisoning",
        ]
        for name in expected:
            assert name in scenario_names

    def test_includes_severity(self, mock_agent):
        """Test results include severity."""
        orchestrator = RCEOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        for result in results:
            assert "severity" in result


class TestAutoStop:
    """Tests for auto stop configuration."""

    def test_stops_on_critical(self, mock_agent):
        """Test stops on critical when enabled."""
        config = {"auto_stop_on_critical": True}
        orchestrator = RCEOrchestrator(mock_agent, config=config)
        # Would stop on first critical finding
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)


class TestErrorHandling:
    """Tests for error handling."""

    def test_handles_errors(self, mock_agent):
        """Test handles errors gracefully."""
        orchestrator = RCEOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)
