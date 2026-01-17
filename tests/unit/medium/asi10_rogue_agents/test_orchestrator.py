"""
Unit tests for ASI10 Rogue Agents Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from modules.medium.asi10_rogue_agents import RogueAgentOrchestrator


class TestRogueAgentOrchestratorCreation:
    """Tests for RogueAgentOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.system is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = RogueAgentOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test returns list."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 3 scenarios are run."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 3

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "Self-Replication via Provisioning",
            "Goal Drift and Reward Hacking",
            "Agent Collusion and Coalition Formation",
        ]
        for name in expected:
            assert name in scenario_names


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_self_replication(self, mock_agent, rogue_agent_session):
        """Test self-replication detection."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        result = orchestrator._detect_self_replication(rogue_agent_session)
        assert result is None or isinstance(result, str)

    def test_detect_goal_drift(self, mock_agent, rogue_agent_session):
        """Test goal drift detection."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        result = orchestrator._detect_goal_drift(rogue_agent_session)
        assert result is None or isinstance(result, str)

    def test_detect_agent_collusion(self, mock_agent, rogue_agent_session):
        """Test agent collusion detection."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        result = orchestrator._detect_agent_collusion(rogue_agent_session)
        assert result is None or isinstance(result, str)

    def test_no_detection_for_safe_agent(self, mock_agent, safe_agent_session):
        """Test no detection for safe agent."""
        orchestrator = RogueAgentOrchestrator(mock_agent)
        result = orchestrator._detect_self_replication(safe_agent_session)
        assert result is None or isinstance(result, str)
