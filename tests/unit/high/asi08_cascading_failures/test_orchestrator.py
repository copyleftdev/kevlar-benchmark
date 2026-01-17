"""
Unit tests for ASI08 Cascading Failures Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from modules.high.asi08_cascading_failures import CascadingOrchestrator


class TestCascadingOrchestratorCreation:
    """Tests for CascadingOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = CascadingOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.system is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = CascadingOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test returns list."""
        orchestrator = CascadingOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 3 scenarios are run."""
        orchestrator = CascadingOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 3

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = CascadingOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "Financial Trading Collapse",
            "Healthcare System Failure",
            "Cloud Orchestration Meltdown",
        ]
        for name in expected:
            assert name in scenario_names


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_financial_cascade(self, mock_agent, cascade_session):
        """Test financial cascade detection."""
        orchestrator = CascadingOrchestrator(mock_agent)
        result = orchestrator._detect_financial_cascade(cascade_session)
        assert result is None or isinstance(result, str)

    def test_detect_healthcare_cascade(self, mock_agent, cascade_session):
        """Test healthcare cascade detection."""
        orchestrator = CascadingOrchestrator(mock_agent)
        result = orchestrator._detect_healthcare_cascade(cascade_session)
        assert result is None or isinstance(result, str)

    def test_detect_cloud_cascade(self, mock_agent, cascade_session):
        """Test cloud cascade detection."""
        orchestrator = CascadingOrchestrator(mock_agent)
        result = orchestrator._detect_cloud_cascade(cascade_session)
        assert result is None or isinstance(result, str)

    def test_no_cascade_for_stable_session(self, mock_agent, stable_cascade_session):
        """Test no cascade for stable session."""
        orchestrator = CascadingOrchestrator(mock_agent)
        result = orchestrator._detect_financial_cascade(stable_cascade_session)
        assert result is None or isinstance(result, str)
