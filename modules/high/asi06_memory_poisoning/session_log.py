# modules/high/asi06_memory_poisoning/session_log.py
class SessionLog:
    def __init__(
        self,
        query: str = "",
        context: str = "",
        response: str = "",
        memory_state: dict = None,
        cross_tenant_data: list = None,
        embedding_similarity: float = 0.0,
        drift_score: float = 0.0,
    ):
        self.query = query
        self.context = context
        self.response = response
        self.memory_state = memory_state or {}
        self.cross_tenant_data = cross_tenant_data or []
        self.embedding_similarity = embedding_similarity
        self.drift_score = drift_score
