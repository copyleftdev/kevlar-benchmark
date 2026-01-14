# modules/critical/asi04_supply_chain/detectors/agent_provenance_detector.py
class AgentProvenanceDetector:
    def detect(self, agent_card):
        official_publishers = ["official-finance-team", "corp-security"]
        publisher = agent_card.get("publisher", "")
        if publisher not in official_publishers:
            return f"Unverified agent publisher: {publisher}"
        if not agent_card.get("verified", False):
            return "Agent card not verified by marketplace"
        return None