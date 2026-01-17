import re


class DataExfilDetector:
    def detect(self, egress_targets):
        for url in egress_targets:
            if re.search(r"attacker\.com|malicious\.net", url):
                return f"Data exfiltration detected to: {url}"
        return None
