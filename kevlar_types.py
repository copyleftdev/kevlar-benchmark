from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SessionLog:
    """Generic container for benchmark-run artifacts."""

    agent_output: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    network_egress: list[str] = field(default_factory=list)
    cost_metrics: dict[str, Any] = field(default_factory=dict)
    identity_context: dict[str, Any] = field(default_factory=dict)
    escalated_actions: list[str] = field(default_factory=list)
    impersonated_entities: list[str] = field(default_factory=list)
    model_hash: str = ""
    dependencies: list[str] = field(default_factory=list)
    descriptor: dict[str, Any] = field(default_factory=dict)
    signature_valid: bool = True
    integrity_violated: bool = False
    protocol_data: dict[str, Any] = field(default_factory=dict)
    original_message: str = ""
    intercepted_message: str = ""
    agent_identity: dict[str, Any] = field(default_factory=dict)
    identity_verified: bool = True
    cross_tenant_data: list[str] = field(default_factory=list)
    embedding_similarity: float = 0.0
    query: str = ""
    response: str = ""
    context: str = ""
    drift_score: float = 0.0
    initial_trigger: str = ""
    affected_components: list[str] = field(default_factory=list)
    financial_loss: float = 0.0
    spawned_agents: list[str] = field(default_factory=list)
    goal_modifications: list[str] = field(default_factory=list)
    collusion_patterns: list[dict[str, Any]] = field(default_factory=list)
    unsafe_inputs: list[str] = field(default_factory=list)
    session_token: str = ""
