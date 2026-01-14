# test_asi04.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.critical.asi04_supply_chain import SupplyChainOrchestrator
from modules.critical.asi04_supply_chain.utils.mock_supply_chain_agent import MockSupplyChainAgent

COLORS = {"CRITICAL": "\033[91m🔴", "NONE": "\033[92m🟢", "RESET": "\033[0m"}

if __name__ == "__main__":
    print("📦 Kevlar — ASI04: Agentic Supply Chain Vulnerabilities Test")
    agent = MockSupplyChainAgent()
    orchestrator = SupplyChainOrchestrator(agent)
    results = orchestrator.run_all_tests()
    
    for r in results:
        icon = COLORS["CRITICAL"] if r.get("vulnerable") else COLORS["NONE"]
        print(f"{icon} {r['scenario']}: {r['evidence']}{COLORS['RESET']}")