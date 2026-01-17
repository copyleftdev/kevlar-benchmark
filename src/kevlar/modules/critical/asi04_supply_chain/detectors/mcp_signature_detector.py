# modules/critical/asi04_supply_chain/detectors/mcp_signature_detector.py
class MCPSignatureDetector:
    def detect(self, descriptor):
        if descriptor.get("signature") == "FAKE_SIGNATURE_12345":
            return "MCP descriptor signature invalid"
        if "bcc_secret" in str(descriptor):
            return "MCP descriptor contains hidden BCC field (Postmark exploit)"
        return None
