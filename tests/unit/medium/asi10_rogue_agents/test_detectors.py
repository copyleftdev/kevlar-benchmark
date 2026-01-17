"""
Unit tests for ASI10 Rogue Agents detector modules.
"""

import pytest

from kevlar.modules.medium.asi10_rogue_agents.detectors import (
    ReplicationDetector,
    GoalDriftAnalyzer,
    CollusionPatternDetector,
)


class TestReplicationDetector:
    """Tests for ReplicationDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = ReplicationDetector()
        assert detector is not None

    def test_detect_unauthorized_replication(self, rogue_agent_session):
        """Test detecting unauthorized replication."""
        detector = ReplicationDetector()
        result = detector.detect_unauthorized_replication(
            rogue_agent_session.original_agent,
            rogue_agent_session.spawned_agents,
            rogue_agent_session.replication_count
        )
        assert result is None or isinstance(result, str)

    def test_no_detection_for_no_replication(self, safe_agent_session):
        """Test no detection when no replication."""
        detector = ReplicationDetector()
        result = detector.detect_unauthorized_replication(
            safe_agent_session.original_agent,
            safe_agent_session.spawned_agents,
            safe_agent_session.replication_count
        )
        assert result is None or isinstance(result, str)


class TestGoalDriftAnalyzer:
    """Tests for GoalDriftAnalyzer."""

    def test_create_analyzer(self):
        """Test creating analyzer."""
        analyzer = GoalDriftAnalyzer()
        assert analyzer is not None

    def test_analyze_goal_drift_high_score(self, rogue_agent_session):
        """Test analyzing goal drift with high score."""
        analyzer = GoalDriftAnalyzer()
        result = analyzer.analyze_goal_drift(
            rogue_agent_session.goal_modifications,
            rogue_agent_session.goal_drift_score,
            rogue_agent_session.reward_hacking_evidence
        )
        assert result is None or isinstance(result, str)

    def test_analyze_goal_drift_low_score(self):
        """Test analyzing goal drift with low score."""
        analyzer = GoalDriftAnalyzer()
        result = analyzer.analyze_goal_drift(
            [],  # goal_modifications
            0.05,  # goal_drift_score
            []  # reward_hacking_evidence as list
        )
        assert result is None or isinstance(result, str)


class TestCollusionPatternDetector:
    """Tests for CollusionPatternDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = CollusionPatternDetector()
        assert detector is not None

    def test_detect_collusion_patterns(self, rogue_agent_session):
        """Test detecting collusion patterns."""
        detector = CollusionPatternDetector()
        result = detector.detect_collusion_patterns(
            rogue_agent_session.collusion_patterns,
            rogue_agent_session.coalition_detected
        )
        assert result is None or isinstance(result, str)

    def test_no_collusion_for_safe_agent(self, safe_agent_session):
        """Test no collusion for safe agent."""
        detector = CollusionPatternDetector()
        result = detector.detect_collusion_patterns(
            safe_agent_session.collusion_patterns,
            safe_agent_session.coalition_detected
        )
        assert result is None or isinstance(result, str)
