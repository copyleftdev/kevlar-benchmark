"""
Unit tests for ASI09 Human Trust Exploitation Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from modules.medium.asi09_human_trust import HumanTrustOrchestrator


class TestHumanTrustOrchestratorCreation:
    """Tests for HumanTrustOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.system is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = HumanTrustOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test returns list."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 3 scenarios are run."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 3

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "Weaponized Explainability",
            "Emotional Manipulation",
            "Authority Impersonation",
        ]
        for name in expected:
            assert name in scenario_names

    def test_results_have_medium_severity(self, mock_agent):
        """Test results have MEDIUM severity when vulnerable."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        for result in results:
            if result.get("vulnerable"):
                assert result.get("severity") == "MEDIUM"


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_weaponized_explainability(self, mock_agent, deceptive_explanation):
        """Test weaponized explainability detection."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        session = MagicMock()
        session.explanation = deceptive_explanation["explanation"]
        result = orchestrator._detect_weaponized_explainability(session)
        assert result is None or isinstance(result, str)

    def test_detect_emotional_manipulation(self, mock_agent, emotional_manipulation_content):
        """Test emotional manipulation detection."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        session = MagicMock()
        session.emotional_tone = emotional_manipulation_content["emotional_tone"]
        session.agent_response = emotional_manipulation_content["agent_response"]
        result = orchestrator._detect_emotional_manipulation(session)
        assert result is None or isinstance(result, str)

    def test_detect_authority_impersonation(self, mock_agent, authority_impersonation_content):
        """Test authority impersonation detection."""
        orchestrator = HumanTrustOrchestrator(mock_agent)
        session = MagicMock()
        session.authority_claim = authority_impersonation_content["authority_claim"]
        result = orchestrator._detect_authority_impersonation(session)
        assert result is None or isinstance(result, str)
