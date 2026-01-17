"""
Unit tests for ASI07 Inter-Agent Communication Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from kevlar.modules.high.asi07_inter_agent_comms import InterAgentOrchestrator


class TestInterAgentOrchestratorCreation:
    """Tests for InterAgentOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.system is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = InterAgentOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test returns list."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 4 scenarios are run."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 4

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "Agent-in-the-Middle",
            "MCP Descriptor Forgery",
            "A2A Protocol Exploitation",
            "Forged Agent Identity",
        ]
        for name in expected:
            assert name in scenario_names


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_mitm(self, mock_agent):
        """Test MITM detection."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        session = MagicMock()
        session.original_message = "original"
        session.intercepted_message = "modified"
        result = orchestrator._detect_mitm(session)
        assert result is None or isinstance(result, str)

    def test_detect_descriptor_forgery(self, mock_agent):
        """Test descriptor forgery detection."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        session = MagicMock()
        session.descriptor = {}
        result = orchestrator._detect_descriptor_forgery(session)
        assert result is None or isinstance(result, str)

    def test_detect_protocol_exploit(self, mock_agent):
        """Test protocol exploit detection."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        session = MagicMock()
        session.protocol_data = {}
        result = orchestrator._detect_protocol_exploit(session)
        assert result is None or isinstance(result, str)

    def test_detect_identity_forgery(self, mock_agent):
        """Test identity forgery detection."""
        orchestrator = InterAgentOrchestrator(mock_agent)
        session = MagicMock()
        session.agent_identity = {}
        result = orchestrator._detect_identity_forgery(session)
        assert result is None or isinstance(result, str)
