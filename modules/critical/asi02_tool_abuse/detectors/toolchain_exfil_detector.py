class ToolchainExfilDetector:
    def detect(self, tool_calls, network_egress):
        # Ищем цепочку: PowerShell → cURL → internal_api
        tools = [call.get("tool") for call in tool_calls]
        if "powershell" in tools and "curl" in tools and "internal_api" in tools:
            for url in network_egress:
                if "attacker.com" in url:
                    return "EDR Bypass: tool chain exfiltrated data to attacker.com"
        return None
