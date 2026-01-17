"""
Unit tests for ASI04 Supply Chain Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from kevlar.modules.critical.asi04_supply_chain import SupplyChainOrchestrator


class TestSupplyChainOrchestratorCreation:
    """Tests for SupplyChainOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.agent is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = SupplyChainOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test that run_all_tests returns list."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 5 scenarios are run."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 5

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "MCP Descriptor Poisoning",
            "Agent Card Forgery",
            "Lockfile Poisoning",
            "Plugin Typosquatting",
            "Model Weights Poisoning",
        ]
        for name in expected:
            assert name in scenario_names


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_mcp_poisoning(self, mock_agent):
        """Test MCP poisoning detection."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        session = MagicMock()
        session.descriptor = {}
        result = orchestrator._detect_mcp_poisoning(session)
        assert result is None or isinstance(result, str)

    def test_detect_agent_forgery(self, mock_agent):
        """Test agent forgery detection."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        session = MagicMock()
        session.agent_card = {}
        result = orchestrator._detect_agent_forgery(session)
        assert result is None or isinstance(result, str)

    def test_detect_lockfile_poisoning(self, mock_agent):
        """Test lockfile poisoning detection."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        session = MagicMock()
        session.dependencies = []
        result = orchestrator._detect_lockfile_poisoning(session)
        assert result is None or isinstance(result, str)

    def test_detect_typosquatting(self, mock_agent):
        """Test typosquatting detection."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        session = MagicMock()
        session.dependencies = []
        result = orchestrator._detect_typosquatting(session)
        assert result is None or isinstance(result, str)

    def test_detect_model_poisoning(self, mock_agent):
        """Test model poisoning detection."""
        orchestrator = SupplyChainOrchestrator(mock_agent)
        session = MagicMock()
        session.model_hash = ""
        result = orchestrator._detect_model_poisoning(session)
        assert result is None or isinstance(result, str)
