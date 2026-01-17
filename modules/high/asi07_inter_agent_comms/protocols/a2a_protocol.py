# modules/high/asi07_inter_agent_comms/protocols/a2a_protocol.py
"""
Real A2A (Agent-to-Agent) protocol implementation for ASI07 testing.
Based on JSON-RPC 2.0 with security extensions.
"""

import json
import logging
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger("Kevlar.ASI07.A2A")


class A2AMessage:
    def __init__(
        self,
        sender: str,
        receiver: str,
        action: str,
        payload: Dict[str, Any],
        timestamp: Optional[str] = None,
        nonce: Optional[str] = None,
    ):
        self.sender = sender
        self.receiver = receiver
        self.action = action
        self.payload = payload
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.nonce = nonce or self._generate_nonce()
        self.integrity_hash = self._calculate_integrity_hash()

    def _generate_nonce(self) -> str:
        import secrets

        return secrets.token_hex(16)

    def _calculate_integrity_hash(self) -> str:
        message_data = f"{self.sender}:{self.receiver}:{self.action}:{
            json.dumps(self.payload, sort_keys=True)
        }:{self.timestamp}:{self.nonce}"
        return hashlib.sha256(message_data.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "action": self.action,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "integrity_hash": self.integrity_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2AMessage":
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            action=data["action"],
            payload=data["payload"],
            timestamp=data["timestamp"],
            nonce=data["nonce"],
        )


class A2AProtocol:
    def __init__(self, shared_secret: str = "kevlar_test_secret"):
        self.shared_secret = shared_secret.encode()
        # 5-minute window for replay protection
        self.valid_window = timedelta(minutes=5)

    def create_message(
        self, sender: str, receiver: str, action: str, payload: Dict[str, Any]
    ) -> A2AMessage:
        return A2AMessage(sender, receiver, action, payload)

    def validate_message(self, message: A2AMessage) -> Dict[str, Any]:
        validation_result = {"valid": True, "errors": []}

        # Check timestamp freshness (replay protection)
        try:
            msg_time = datetime.fromisoformat(message.timestamp.replace("Z", "+00:00"))
            if datetime.utcnow() - msg_time > self.valid_window:
                validation_result["valid"] = False
                validation_result["errors"].append("Message timestamp expired")
        except ValueError:
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid timestamp format")

        # Verify integrity hash
        expected_hash = message._calculate_integrity_hash()
        if message.integrity_hash != expected_hash:
            validation_result["valid"] = False
            validation_result["errors"].append("Integrity hash mismatch")

        # Verify HMAC (if implemented)
        # hmac_hash = hmac.new(self.shared_secret, json.dumps(message.to_dict(), sort_keys=True).encode(), hashlib.sha256).hexdigest()
        # if provided_hmac != hmac_hash:
        #     validation_result["valid"] = False
        #     validation_result["errors"].append("HMAC verification failed")

        return validation_result

    def process_message(self, message: A2AMessage) -> Dict[str, Any]:
        validation = self.validate_message(message)
        if not validation["valid"]:
            logger.warning(f"A2A message validation failed: {validation['errors']}")
            return {"status": "error", "errors": validation["errors"]}

        logger.info(
            f"Processing A2A message: {message.action} from {message.sender} to {
                message.receiver
            }"
        )

        return {"status": "success", "message": f"Action {message.action} processed"}
