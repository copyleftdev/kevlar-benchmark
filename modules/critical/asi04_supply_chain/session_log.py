# modules/critical/asi04_supply_chain/session_log.py
class SessionLog:
    def __init__(
        self,
        descriptor: dict = None,
        agent_card: dict = None,
        dependencies: list = None,
        model_hash: str = "",
        execution_result: str = "",
        provenance: dict = None,
    ):
        self.descriptor = descriptor or {}
        self.agent_card = agent_card or {}
        self.dependencies = dependencies or []
        self.model_hash = model_hash
        self.execution_result = execution_result
        self.provenance = provenance or {}
