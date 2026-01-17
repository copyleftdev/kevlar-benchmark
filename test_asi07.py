# test_asi07.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.high.asi07_inter_agent_comms import InterAgentOrchestrator
from modules.high.asi07_inter_agent_comms.utils.real_inter_agent_system import (
    RealInterAgentSystem,
)


def main():
    print("🔗 Kevlar — ASI07 Production Test with Real MCP/A2A Protocols")

    system = RealInterAgentSystem(model_name="llama3.1")

    orchestrator = InterAgentOrchestrator(
        system, config={"auto_stop_on_critical": False}
    )
    results = orchestrator.run_all_tests()

    COLORS = {"HIGH": "\033[91m🔴", "NONE": "\033[92m🟢", "RESET": "\033[0m"}
    for r in results:
        icon = COLORS["HIGH"] if r.get("vulnerable") else COLORS["NONE"]
        print(f"{icon} {r['scenario']}: {r['evidence']}{COLORS['RESET']}")


if __name__ == "__main__":
    main()
