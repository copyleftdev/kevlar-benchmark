"""
Unit tests for kevlar_types module.
"""

import pytest
from dataclasses import fields, asdict

from kevlar_types import SessionLog


class TestSessionLogCreation:
    """Tests for SessionLog dataclass creation."""

    def test_create_empty_session_log(self):
        """Test creating SessionLog with default values."""
        log = SessionLog()
        assert log.agent_output == ""
        assert log.tool_calls == []
        assert log.network_egress == []
        assert log.drift_score == 0.0
        assert log.signature_valid is True
        assert log.identity_verified is True

    def test_create_session_log_with_values(self):
        """Test creating SessionLog with custom values."""
        log = SessionLog(
            agent_output="test output",
            tool_calls=[{"tool": "test"}],
            network_egress=["http://example.com"],
            drift_score=0.5,
        )
        assert log.agent_output == "test output"
        assert log.tool_calls == [{"tool": "test"}]
        assert log.network_egress == ["http://example.com"]
        assert log.drift_score == 0.5

    def test_session_log_has_slots(self):
        """Test that SessionLog uses slots for memory efficiency."""
        assert hasattr(SessionLog, "__slots__")

    def test_session_log_is_mutable(self):
        """Test that SessionLog fields can be modified."""
        log = SessionLog()
        log.agent_output = "modified"
        log.drift_score = 0.9
        assert log.agent_output == "modified"
        assert log.drift_score == 0.9


class TestSessionLogFields:
    """Tests for SessionLog field types and defaults."""

    def test_all_required_fields_exist(self):
        """Test that all expected fields exist in SessionLog."""
        expected_fields = [
            "agent_output",
            "tool_calls",
            "network_egress",
            "cost_metrics",
            "identity_context",
            "escalated_actions",
            "impersonated_entities",
            "model_hash",
            "dependencies",
            "descriptor",
            "signature_valid",
            "integrity_violated",
            "protocol_data",
            "original_message",
            "intercepted_message",
            "agent_identity",
            "identity_verified",
            "cross_tenant_data",
            "embedding_similarity",
            "query",
            "response",
            "context",
            "drift_score",
            "initial_trigger",
            "affected_components",
            "financial_loss",
            "spawned_agents",
            "goal_modifications",
            "collusion_patterns",
            "unsafe_inputs",
            "session_token",
        ]
        field_names = [f.name for f in fields(SessionLog)]
        for expected in expected_fields:
            assert expected in field_names, f"Missing field: {expected}"

    def test_list_fields_are_independent(self):
        """Test that list fields don't share state between instances."""
        log1 = SessionLog()
        log2 = SessionLog()
        log1.tool_calls.append({"tool": "test"})
        assert log2.tool_calls == []

    def test_dict_fields_are_independent(self):
        """Test that dict fields don't share state between instances."""
        log1 = SessionLog()
        log2 = SessionLog()
        log1.cost_metrics["key"] = "value"
        assert log2.cost_metrics == {}


class TestSessionLogConversion:
    """Tests for SessionLog conversion methods."""

    def test_asdict_conversion(self):
        """Test converting SessionLog to dictionary."""
        log = SessionLog(
            agent_output="test",
            drift_score=0.5,
        )
        d = asdict(log)
        assert isinstance(d, dict)
        assert d["agent_output"] == "test"
        assert d["drift_score"] == 0.5

    def test_session_log_string_representation(self):
        """Test string representation of SessionLog."""
        log = SessionLog(agent_output="test")
        str_repr = str(log)
        assert "SessionLog" in str_repr
        assert "agent_output='test'" in str_repr


class TestSessionLogVulnerabilityIndicators:
    """Tests for vulnerability indicator fields."""

    def test_exfiltration_indicators(self, vulnerable_session_log):
        """Test session log with exfiltration indicators."""
        assert "attacker.com" in vulnerable_session_log.agent_output
        assert any("attacker" in url for url in vulnerable_session_log.network_egress)

    def test_privilege_escalation_indicators(self, vulnerable_session_log):
        """Test session log with privilege escalation indicators."""
        assert len(vulnerable_session_log.escalated_actions) > 0
        assert "admin_access" in vulnerable_session_log.escalated_actions

    def test_identity_spoofing_indicators(self, vulnerable_session_log):
        """Test session log with identity spoofing indicators."""
        assert len(vulnerable_session_log.impersonated_entities) > 0

    def test_unsafe_input_indicators(self, vulnerable_session_log):
        """Test session log with unsafe input indicators."""
        assert any("rm -rf" in inp for inp in vulnerable_session_log.unsafe_inputs)

    def test_goal_drift_indicators(self, vulnerable_session_log):
        """Test session log with goal drift indicators."""
        assert vulnerable_session_log.drift_score > 0.7

    def test_safe_session_has_no_indicators(self, safe_session_log):
        """Test that safe session log has no vulnerability indicators."""
        assert safe_session_log.drift_score < 0.5
        assert len(safe_session_log.escalated_actions) == 0
        assert len(safe_session_log.network_egress) == 0


class TestSessionLogIntegrityFields:
    """Tests for integrity-related fields."""

    def test_signature_validity_default(self):
        """Test default signature validity."""
        log = SessionLog()
        assert log.signature_valid is True

    def test_integrity_violation_default(self):
        """Test default integrity violation status."""
        log = SessionLog()
        assert log.integrity_violated is False

    def test_identity_verification_default(self):
        """Test default identity verification status."""
        log = SessionLog()
        assert log.identity_verified is True

    def test_set_integrity_violation(self):
        """Test setting integrity violation."""
        log = SessionLog(integrity_violated=True, signature_valid=False)
        assert log.integrity_violated is True
        assert log.signature_valid is False


class TestSessionLogMessageFields:
    """Tests for message-related fields."""

    def test_message_comparison(self, mitm_session):
        """Test original vs intercepted message comparison."""
        assert mitm_session.original_message != mitm_session.intercepted_message
        assert mitm_session.integrity_violated is True

    def test_valid_message_integrity(self, valid_communication_session):
        """Test valid message integrity."""
        assert valid_communication_session.original_message == valid_communication_session.intercepted_message
        assert valid_communication_session.integrity_violated is False


class TestSessionLogCascadeFields:
    """Tests for cascade failure related fields."""

    def test_cascade_fields(self):
        """Test cascade failure related fields."""
        log = SessionLog(
            initial_trigger="Agent misconfiguration",
            affected_components=["db", "api", "frontend"],
            financial_loss=100000.0,
        )
        assert log.initial_trigger == "Agent misconfiguration"
        assert len(log.affected_components) == 3
        assert log.financial_loss == 100000.0


class TestSessionLogRogueAgentFields:
    """Tests for rogue agent related fields."""

    def test_spawned_agents_field(self):
        """Test spawned agents tracking."""
        log = SessionLog(
            spawned_agents=["agent-2", "agent-3"],
            goal_modifications=["self_preservation"],
            collusion_patterns=[{"agents": ["a", "b"], "type": "coordination"}],
        )
        assert len(log.spawned_agents) == 2
        assert len(log.goal_modifications) == 1
        assert len(log.collusion_patterns) == 1
