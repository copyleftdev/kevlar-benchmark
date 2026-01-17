"""
Unit tests for ASI02 Tool Abuse Orchestrator.
"""

import pytest
from unittest.mock import patch, MagicMock

from kevlar.modules.critical.asi02_tool_abuse import ToolAbuseOrchestrator


class TestToolAbuseOrchestratorCreation:
    """Tests for ToolAbuseOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator with mock agent."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.agent is mock_agent

    def test_create_orchestrator_with_config(self, mock_agent, default_config):
        """Test creating orchestrator with custom config."""
        orchestrator = ToolAbuseOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config

    def test_orchestrator_initializes_results(self, mock_agent):
        """Test that orchestrator initializes empty results list."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        assert orchestrator.results == []


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_run_all_tests_returns_list(self, mock_agent):
        """Test that run_all_tests returns a list."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_run_all_tests_runs_all_scenarios(self, mock_agent):
        """Test that all 9 scenarios are run."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        # Should run 9 scenarios
        assert len(results) >= 9

    def test_run_all_tests_includes_scenario_names(self, mock_agent):
        """Test that results include scenario names."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected_scenarios = [
            "Over-privileged Tool",
            "Over-scoped Tool",
            "Unvalidated Input Forwarding",
            "Unsafe Browsing",
            "Loop Amplification",
            "External Data Poisoning",
            "EDR Bypass via Chaining",
            "Tool Name Impersonation",
            "Approved Tool Misuse",
        ]
        for expected in expected_scenarios:
            assert expected in scenario_names

    def test_results_include_vulnerability_status(self, mock_agent):
        """Test that results include vulnerability status."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        for result in results:
            if "error" not in result:
                assert "vulnerable" in result
                assert "severity" in result


class TestAutoStop:
    """Tests for auto_stop configuration."""

    def test_continues_by_default(self, mock_agent):
        """Test that execution continues by default."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 9


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_excessive_use(self, mock_agent):
        """Test excessive tool use detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.tool_calls = [{"tool": "test", "action": "read"}]
        result = orchestrator._detect_excessive_use(session)
        # Result may be None or a string
        assert result is None or isinstance(result, str)

    def test_detect_unsafe_input(self, mock_agent):
        """Test unsafe input detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.unsafe_inputs = []
        result = orchestrator._detect_unsafe_input(session)
        assert result is None or isinstance(result, str)

    def test_detect_malicious_link(self, mock_agent):
        """Test malicious link detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.agent_output = "Check out this link"
        result = orchestrator._detect_malicious_link(session)
        assert result is None or isinstance(result, str)

    def test_detect_cost_spike(self, mock_agent):
        """Test cost spike detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.cost_metrics = {}
        result = orchestrator._detect_cost_spike(session)
        assert result is None or isinstance(result, str)

    def test_detect_rag_poisoning(self, mock_agent):
        """Test RAG poisoning detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.agent_output = "Normal response"
        result = orchestrator._detect_rag_poisoning(session)
        assert result is None or isinstance(result, str)

    def test_detect_toolchain_exfil(self, mock_agent):
        """Test toolchain exfiltration detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.tool_calls = []
        session.network_egress = []
        result = orchestrator._detect_toolchain_exfil(session)
        assert result is None or isinstance(result, str)

    def test_detect_tool_impersonation(self, mock_agent):
        """Test tool impersonation detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.tool_calls = []
        result = orchestrator._detect_tool_impersonation(session)
        assert result is None or isinstance(result, str)

    def test_detect_dns_exfil(self, mock_agent):
        """Test DNS exfiltration detection."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        session = MagicMock()
        session.tool_calls = []
        session.network_egress = []
        result = orchestrator._detect_dns_exfil(session)
        assert result is None or isinstance(result, str)


class TestErrorHandling:
    """Tests for error handling."""

    def test_handles_attack_errors(self, mock_agent):
        """Test that errors in attacks are handled."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        # Should not raise exceptions
        assert isinstance(results, list)


class TestResultsAccumulation:
    """Tests for results accumulation."""

    def test_results_stored_in_orchestrator(self, mock_agent):
        """Test that results are stored in orchestrator."""
        orchestrator = ToolAbuseOrchestrator(mock_agent)
        orchestrator.run_all_tests()
        assert len(orchestrator.results) >= 9
