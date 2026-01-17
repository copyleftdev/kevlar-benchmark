# modules/high/asi07_inter_agent_comms/session_log.py
class SessionLog:
    def __init__(
        self,
        original_message: str = "",
        intercepted_message: str = "",
        forged_message: str = "",
        descriptor: dict = None,
        agent_identity: dict = None,
        protocol_data: dict = None,
        integrity_violated: bool = False,
        signature_valid: bool = True,
        identity_verified: bool = False,
    ):
        self.original_message = original_message
        self.intercepted_message = intercepted_message
        self.forged_message = forged_message
        self.descriptor = descriptor or {}
        self.agent_identity = agent_identity or {}
        self.protocol_data = protocol_data or {}
        self.integrity_violated = integrity_violated
        self.signature_valid = signature_valid
        self.identity_verified = identity_verified
