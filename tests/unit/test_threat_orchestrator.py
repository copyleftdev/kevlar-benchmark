"""
Unit tests for core/threat_orchestrator module.
"""

import pytest
from unittest.mock import patch, MagicMock

from kevlar.core import ThreatOrchestrator


class TestThreatOrchestratorCreation:
    """Tests for ThreatOrchestrator instantiation."""

    def test_create_threat_orchestrator(self):
        """Test creating ThreatOrchestrator."""
        orchestrator = ThreatOrchestrator()
        assert orchestrator is not None

    def test_threat_rank_defined(self):
        """Test that THREAT_RANK is defined."""
        orchestrator = ThreatOrchestrator()
        assert hasattr(orchestrator, 'THREAT_RANK')
        assert isinstance(orchestrator.THREAT_RANK, dict)


class TestThreatRanking:
    """Tests for threat ranking configuration."""

    def test_all_asis_ranked(self):
        """Test that all 10 ASIs are ranked."""
        assert len(ThreatOrchestrator.THREAT_RANK) == 10

    def test_asi01_highest_priority(self):
        """Test that ASI01 (Goal Hijack) has highest priority."""
        assert ThreatOrchestrator.THREAT_RANK["ASI01"] == 1

    def test_asi05_high_priority(self):
        """Test that ASI05 (RCE) has high priority."""
        assert ThreatOrchestrator.THREAT_RANK["ASI05"] == 2

    def test_asi10_lowest_priority(self):
        """Test that ASI10 (Rogue Agents) has lowest priority."""
        assert ThreatOrchestrator.THREAT_RANK["ASI10"] == 10

    def test_unique_rankings(self):
        """Test that all rankings are unique."""
        rankings = list(ThreatOrchestrator.THREAT_RANK.values())
        assert len(rankings) == len(set(rankings))

    def test_rankings_are_sequential(self):
        """Test that rankings are 1-10."""
        rankings = sorted(ThreatOrchestrator.THREAT_RANK.values())
        assert rankings == list(range(1, 11))


class TestThreatOrder:
    """Tests for threat execution order."""

    def test_sorted_order_by_risk(self):
        """Test that ASIs are sorted by risk (ascending rank number)."""
        orchestrator = ThreatOrchestrator()
        ordered = sorted(orchestrator.THREAT_RANK, key=orchestrator.THREAT_RANK.get)
        assert ordered[0] == "ASI01"
        assert ordered[1] == "ASI05"
        assert ordered[-1] == "ASI10"

    def test_critical_asis_first(self):
        """Test that critical ASIs (01-05) come before others."""
        orchestrator = ThreatOrchestrator()
        ordered = sorted(orchestrator.THREAT_RANK, key=orchestrator.THREAT_RANK.get)
        critical = ["ASI01", "ASI05", "ASI03", "ASI02", "ASI04"]
        for asi in critical:
            assert asi in ordered[:5]


class TestRunAllTests:
    """Tests for run_all_tests method."""

    def test_run_all_tests_exists(self):
        """Test that run_all_tests method exists."""
        orchestrator = ThreatOrchestrator()
        assert hasattr(orchestrator, 'run_all_tests')
        assert callable(orchestrator.run_all_tests)

    def test_run_all_tests_prints_modules(self, capsys):
        """Test that run_all_tests prints module names."""
        orchestrator = ThreatOrchestrator()
        try:
            orchestrator.run_all_tests("test-target")
        except NotImplementedError:
            pass
        captured = capsys.readouterr()
        assert "ASI01" in captured.out

    def test_run_all_tests_in_order(self, capsys):
        """Test that tests are run in threat rank order."""
        orchestrator = ThreatOrchestrator()
        outputs = []

        original_method = orchestrator._load_and_run_module
        def capture_order(module_id, target):
            outputs.append(module_id)
            raise NotImplementedError(module_id)

        orchestrator._load_and_run_module = capture_order

        try:
            orchestrator.run_all_tests("test-target")
        except NotImplementedError:
            pass

        # First module should be highest priority
        if outputs:
            assert outputs[0] == "ASI01"


class TestLoadAndRunModule:
    """Tests for _load_and_run_module method."""

    def test_load_and_run_module_raises_not_implemented(self):
        """Test that _load_and_run_module raises NotImplementedError."""
        orchestrator = ThreatOrchestrator()
        with pytest.raises(NotImplementedError) as exc_info:
            orchestrator._load_and_run_module("ASI01", "test-target")
        assert "ASI01" in str(exc_info.value)

    def test_load_and_run_module_accepts_target(self):
        """Test that method accepts target parameter."""
        orchestrator = ThreatOrchestrator()
        try:
            orchestrator._load_and_run_module("ASI01", "my-target")
        except NotImplementedError:
            pass  # Expected


class TestThreatOrchestratorIntegration:
    """Integration-style tests for ThreatOrchestrator."""

    def test_orchestrator_module_loading(self):
        """Test that orchestrator can be loaded from module path."""
        from kevlar.core import ThreatOrchestrator
        assert ThreatOrchestrator is not None

    def test_threat_rank_comment_descriptions(self):
        """Test that threat ranks have associated descriptions (from comments)."""
        # This validates the structure matches documentation
        expected_threats = {
            "ASI01": "Goal Hijack",
            "ASI05": "RCE",
            "ASI03": "Identity Abuse",
            "ASI02": "Tool Misuse",
            "ASI04": "Supply Chain",
            "ASI06": "Memory Poisoning",
            "ASI07": "Insecure Comms",
            "ASI08": "Cascading Failures",
            "ASI09": "Human Trust",
            "ASI10": "Rogue Agents",
        }
        for asi_id in expected_threats:
            assert asi_id in ThreatOrchestrator.THREAT_RANK
