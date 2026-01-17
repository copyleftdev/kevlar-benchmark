# modules/critical/asi04_supply_chain/detectors/model_hash_detector.py
class ModelHashDetector:
    def detect(self, model_hash):
        if "MALICIOUS" in model_hash:
            return "Model weights hash indicates tampering"
        official_hashes = ["sha256:abc123...", "sha256:def456..."]
        if model_hash not in official_hashes:
            return "Model hash not in allowlist"
        return None
