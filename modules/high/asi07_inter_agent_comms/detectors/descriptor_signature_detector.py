# modules/high/asi07_inter_agent_comms/detectors/descriptor_signature_detector.py
class DescriptorSignatureDetector:
    def detect_invalid_signature(self, descriptor):
        official_signatures = ["OFFICIAL_SIG_123", "VERIFIED_PUBLISHER_456"]
        signature = descriptor.get("signature", "")

        if signature not in official_signatures:
            return f"Invalid descriptor signature: {signature}"

        publisher = descriptor.get("publisher", "")
        if "attacker" in publisher.lower():
            return f"Suspicious publisher in descriptor: {publisher}"

        return None
