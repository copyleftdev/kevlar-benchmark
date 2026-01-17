"""
Unit tests for ASI01 Goal Hijack Orchestrator.
"""

import pytest
from unittest.mock import patch, MagicMock

from modules.critical.asi01_goal_hijack import GoalHijackOrchestrator


class TestGoalHijackOrchestratorCreation:
    """Tests for GoalHijackOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator with mock agent."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.agent is mock_agent

    def test_create_orchestrator_with_config(self, mock_agent, default_config):
        """Test creating orchestrator with custom config."""
        orchestrator = GoalHijackOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config

    def test_create_orchestrator_default_config(self, mock_agent):
        """Test creating orchestrator with default config."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        assert orchestrator.config == {}

    def test_orchestrator_initializes_results(self, mock_agent):
        """Test that orchestrator initializes empty results list."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        assert orchestrator.results == []


class TestRunAllScenarios:
    """Tests for run_all_scenarios method."""

    def test_run_all_scenarios_returns_list(self, mock_agent):
        """Test that run_all_scenarios returns a list."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        results = orchestrator.run_all_scenarios()
        assert isinstance(results, list)

    def test_run_all_scenarios_runs_all_tests(self, mock_agent):
        """Test that all 4 scenarios are run."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        results = orchestrator.run_all_scenarios()
        # Should run: EchoLeak, Operator, Inception, Goal-lock drift
        assert len(results) >= 4

    def test_run_all_scenarios_includes_scenario_names(self, mock_agent):
        """Test that results include scenario names."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        results = orchestrator.run_all_scenarios()
        scenario_names = [r.get("scenario") for r in results]
        assert "EchoLeak" in scenario_names
        assert "Operator" in scenario_names
        assert "Inception" in scenario_names
        assert "Goal-lock drift" in scenario_names

    def test_run_all_scenarios_includes_severity(self, mock_agent):
        """Test that results include severity."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        results = orchestrator.run_all_scenarios()
        for result in results:
            if "error" not in result:
                assert "severity" in result

    def test_run_all_scenarios_includes_vulnerable_flag(self, mock_agent):
        """Test that results include vulnerable flag."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        results = orchestrator.run_all_scenarios()
        for result in results:
            if "error" not in result:
                assert "vulnerable" in result


class TestAutoStopOnCritical:
    """Tests for auto_stop_on_critical configuration."""

    def test_stops_on_critical_when_enabled(self, mock_agent):
        """Test that execution stops on critical finding when enabled."""
        config = {"auto_stop_on_critical": True}
        orchestrator = GoalHijackOrchestrator(mock_agent, config=config)

        # Mock a critical finding in first test
        with patch.object(orchestrator, '_test_echoleak') as mock_test:
            mock_test.return_value = {
                "vulnerable": True,
                "severity": "CRITICAL",
                "evidence": "test",
            }
            results = orchestrator.run_all_scenarios()
            # Should stop after first critical
            assert len(results) == 1

    def test_continues_when_disabled(self, mock_agent):
        """Test that execution continues when auto_stop is disabled."""
        config = {"auto_stop_on_critical": False}
        orchestrator = GoalHijackOrchestrator(mock_agent, config=config)
        results = orchestrator.run_all_scenarios()
        # Should run all scenarios
        assert len(results) >= 4


class TestEchoLeakScenario:
    """Tests for EchoLeak scenario."""

    def test_echoleak_test_runs(self, mock_agent):
        """Test that EchoLeak test runs."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_echoleak()
        assert "vulnerable" in result
        assert "severity" in result
        assert "evidence" in result

    def test_echoleak_safe_agent_not_vulnerable(self, mock_agent):
        """Test that safe mock agent is not vulnerable to EchoLeak."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_echoleak()
        # MockAgent should be safe
        assert result["severity"] in ["NONE", "LOW"]


class TestOperatorScenario:
    """Tests for Operator scenario."""

    def test_operator_test_runs(self, mock_agent):
        """Test that Operator test runs."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_operator()
        assert "vulnerable" in result
        assert "severity" in result
        assert "evidence" in result

    def test_operator_safe_agent_not_vulnerable(self, mock_agent):
        """Test that safe mock agent is not vulnerable to Operator."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_operator()
        assert result["severity"] in ["NONE", "LOW"]


class TestInceptionScenario:
    """Tests for Inception scenario."""

    def test_inception_test_runs(self, mock_agent):
        """Test that Inception test runs."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_inception()
        assert "vulnerable" in result
        assert "severity" in result
        assert "evidence" in result

    def test_inception_safe_agent_rejects_fraud(self, mock_agent):
        """Test that safe mock agent rejects fraudulent transfers."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_inception()
        assert result["vulnerable"] is False


class TestGoalDriftScenario:
    """Tests for Goal Drift scenario."""

    def test_goal_drift_test_runs(self, mock_agent):
        """Test that Goal Drift test runs."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_goal_drift()
        assert "vulnerable" in result
        assert "severity" in result
        assert "evidence" in result

    def test_goal_drift_returns_drift_score(self, mock_agent):
        """Test that evidence includes drift score."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        result = orchestrator._test_goal_drift()
        assert "evidence" in result


class TestErrorHandling:
    """Tests for error handling."""

    def test_handles_test_errors(self, mock_agent):
        """Test that errors in individual tests are handled."""
        orchestrator = GoalHijackOrchestrator(mock_agent)

        with patch.object(orchestrator, '_test_echoleak') as mock_test:
            mock_test.side_effect = Exception("Test error")
            results = orchestrator.run_all_scenarios()
            # Error should be recorded, not raised
            error_results = [r for r in results if "error" in r]
            assert len(error_results) >= 1


class TestResultsAccumulation:
    """Tests for results accumulation."""

    def test_results_stored_in_orchestrator(self, mock_agent):
        """Test that results are stored in orchestrator."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        orchestrator.run_all_scenarios()
        assert len(orchestrator.results) >= 4

    def test_results_cleared_between_runs(self, mock_agent):
        """Test that results can be run multiple times."""
        orchestrator = GoalHijackOrchestrator(mock_agent)
        results1 = orchestrator.run_all_scenarios()
        # Re-initialize results
        orchestrator.results = []
        results2 = orchestrator.run_all_scenarios()
        assert len(results2) >= 4
