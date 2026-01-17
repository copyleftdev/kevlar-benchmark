# modules/critical/asi04_supply_chain/utils/mock_supply_chain_agent.py
class MockSupplyChainAgent:
    def register_mcp_descriptor(self, desc):
        return "MCP registered"

    def install_agent(self, card):
        return "Agent installed"

    def update_dependencies(self, deps):
        return "Dependencies updated"

    def load_model_weights(self, hash):
        return "Model loaded"
