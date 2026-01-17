# modules/high/asi07_inter_agent_comms/utils/mock_inter_agent_system.py
class MockInterAgentSystem:
    def __init__(self):
        self.registered_descriptors = {}
        self.verified_agents = set()

    def process_inter_agent_message(self, message):
        if "ATTACKER_ACCOUNT" in message:
            return "Transfer approved to attacker account"
        return "Message processed"

    def register_agent_descriptor(self, descriptor):
        name = descriptor.get("name")
        self.registered_descriptors[name] = descriptor
        return f"Descriptor {name} registered"

    def process_a2a_message(self, protocol_data):
        action = protocol_data.get("action")
        account = protocol_data.get("account")
        return f"A2A message processed: {action} to {account}"

    def authenticate_agent(self, agent_identity):
        agent_id = agent_identity.get("agent_id")
        self.verified_agents.add(agent_id)
        return f"Agent {agent_id} authenticated"
