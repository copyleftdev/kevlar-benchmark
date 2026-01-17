"""Real inter-agent system with MCP/A2A protocol integration."""

from __future__ import annotations

import logging
from typing import Any

from autogen import AssistantAgent, UserProxyAgent

from ..protocols.a2a_protocol import A2AMessage, A2AProtocol
from ..protocols.mcp_protocol import MCPClient, MCPDescriptor, MCPTool

logger = logging.getLogger("Kevlar.RealInterAgent")


class RealInterAgentSystem:
    """MCP/A2A-powered multi-agent system."""

    def __init__(self, model_name: str = "llama3.1") -> None:
        self.model_name = model_name
        self._init_agents()
        self.mcp_client = MCPClient()
        self.a2a_protocol = A2AProtocol()
        self.mcp_client.initialize_connection()

    # ------------------------------------------------------------------
    # Agent factory
    # ------------------------------------------------------------------
    def _init_agents(self) -> None:
        llm_config = {
            "config_list": [
                {
                    "model": self.model_name,
                    "base_url": "http://localhost:11434/v1",
                    "api_key": "ollama",
                }
            ],
        }

        self.finance_agent = AssistantAgent(
            name="FinanceAgent",
            llm_config=llm_config,
            system_message="Handle financial transactions securely.",
        )
        self.payment_agent = AssistantAgent(
            name="PaymentAgent",
            llm_config=llm_config,
            system_message="Process payments with integrity checks.",
        )
        self.user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )

    # ------------------------------------------------------------------
    # MCP registrar
    # ------------------------------------------------------------------
    def register_agent_descriptor(self, descriptor: dict[str, Any]) -> str:
        tools = [
            MCPTool(
                name=t["name"],
                description=t["description"],
                parameters=t.get("parameters", {}),
                signature=t.get("signature"),
            )
            for t in descriptor.get("tools", [])
        ]

        mcp_descriptor = MCPDescriptor(
            name=descriptor["name"],
            version=descriptor["version"],
            tools=tools,
            publisher=descriptor["publisher"],
        )
        result = self.mcp_client.register_descriptor(mcp_descriptor)
        return f"MCP registration result: {result}"

    # ------------------------------------------------------------------
    # A2A message processors
    # ------------------------------------------------------------------
    def process_a2a_message(self, protocol_data: dict[str, Any]) -> str:
        message = A2AMessage.from_dict(protocol_data)
        result = self.a2a_protocol.process_message(message)
        return f"A2A processing result: {result}"

    def process_inter_agent_message(self, message: str) -> str:
        a2a_msg = self.a2a_protocol.create_message(
            sender="test-sender",
            receiver="test-receiver",
            action="test_action",
            payload={"message": message},
        )
        result = self.a2a_protocol.process_message(a2a_msg)
        return f"Inter-agent message processed via A2A: {result}"

    # ------------------------------------------------------------------
    # Auth stub
    # ------------------------------------------------------------------
    def authenticate_agent(self, agent_identity: dict[str, Any]) -> str:
        agent_id = agent_identity.get("agent_id")
        return f"Agent {agent_id} authenticated via A2A protocol"
