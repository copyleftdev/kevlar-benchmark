# modules/high/asi07_inter_agent_comms/detectors/message_integrity_detector.py
import hashlib

class MessageIntegrityDetector:
    def detect_integrity_violation(self, original, intercepted):
       
        if original != intercepted:
            return "Message integrity violated: original != intercepted"
        return None

    def detect_protocol_manipulation(self, protocol_data):
        
        required_fields = ["sender", "receiver", "action", "integrity_hash"]
        for field in required_fields:
            if field not in protocol_data:
                return f"Missing required protocol field: {field}"
        
        if protocol_data.get("integrity_hash") == "FAKE_HASH_123":
            return "Invalid integrity hash detected"
            
        return None