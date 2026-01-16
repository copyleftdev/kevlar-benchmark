# modules/high/asi07_inter_agent_comms/detectors/identity_verification_detector.py
class IdentityVerificationDetector:
    def detect_forged_identity(self, agent_identity):
        
        if not agent_identity.get("verified", False):
            return "Agent identity not verified"
            
        public_key = agent_identity.get("public_key", "")
        if "fake" in public_key.lower():
            return f"Suspicious public key: {public_key}"
            
        return None