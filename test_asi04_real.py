# test_asi04_real.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.critical.asi04_supply_chain import SupplyChainOrchestrator
from langchain_asi04_adapter import LangChainASI04Agent

if __name__ == "__main__":
    print("📦 Kevlar — ASI04 Real Agent Test (LangChain + Ollama)")
    
    
    agent = LangChainASI04Agent(
        model_name="llama3.1",
        framework="langchain"  
    )
    
   
    orchestrator = SupplyChainOrchestrator(agent, config={"auto_stop_on_critical": False})
    results = orchestrator.run_all_tests()
    
    
    for r in results:
        status = "🔴 VULNERABLE" if r.get("vulnerable") else "🟢 SAFE"
        print(f"{status} — {r['scenario']}: {r['evidence']}")