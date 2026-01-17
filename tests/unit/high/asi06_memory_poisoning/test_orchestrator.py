"""
Unit tests for ASI06 Memory Poisoning Orchestrator.
"""

import pytest
from unittest.mock import MagicMock

from modules.high.asi06_memory_poisoning import MemoryPoisoningOrchestrator


class TestMemoryPoisoningOrchestratorCreation:
    """Tests for MemoryPoisoningOrchestrator instantiation."""

    def test_create_orchestrator(self, mock_agent):
        """Test creating orchestrator."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        assert orchestrator is not None
        assert orchestrator.agent is mock_agent

    def test_create_with_config(self, mock_agent, default_config):
        """Test creating with config."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent, config=default_config)
        assert orchestrator.config == default_config


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_returns_list(self, mock_agent):
        """Test returns list."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert isinstance(results, list)

    def test_runs_all_scenarios(self, mock_agent):
        """Test all 4 scenarios are run."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        assert len(results) >= 4

    def test_includes_scenario_names(self, mock_agent):
        """Test scenario names included."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        results = orchestrator.run_all_tests()
        scenario_names = [r.get("scenario") for r in results]
        expected = [
            "RAG Context Poisoning",
            "Session Memory Bleed",
            "Long-Term Memory Drift",
            "Vector DB Injection",
        ]
        for name in expected:
            assert name in scenario_names


class TestDetectorMethods:
    """Tests for detector methods."""

    def test_detect_rag_poisoning(self, mock_agent):
        """Test RAG poisoning detection."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        session = MagicMock()
        session.context = "test context"
        session.response = "test response"
        result = orchestrator._detect_rag_poisoning(session)
        assert result is None or isinstance(result, str)

    def test_detect_memory_bleed(self, mock_agent):
        """Test memory bleed detection."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        session = MagicMock()
        session.cross_tenant_data = []
        result = orchestrator._detect_memory_bleed(session)
        assert result is None or isinstance(result, str)

    def test_detect_memory_drift(self, mock_agent):
        """Test memory drift detection."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        session = MagicMock()
        session.drift_score = 0.5
        result = orchestrator._detect_memory_drift(session)
        assert result is None or isinstance(result, str)

    def test_detect_vector_injection(self, mock_agent):
        """Test vector injection detection."""
        orchestrator = MemoryPoisoningOrchestrator(mock_agent)
        session = MagicMock()
        session.embedding_similarity = 0.5
        result = orchestrator._detect_vector_injection(session)
        assert result is None or isinstance(result, str)
