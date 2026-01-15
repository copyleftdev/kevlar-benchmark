# test_asi06.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.high.asi06_memory_poisoning import MemoryPoisoningOrchestrator
from modules.high.asi06_memory_poisoning.utils.real_memory_agent import RealMemoryAgent

def main():
    print("🧠 Kevlar — ASI06 Production Test with Real Vector Stores")
    
   
    VECTOR_STORE = "faiss"  
    
    if VECTOR_STORE == "pinecone":
       
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME", "kevlar-asi06-test")
        if not api_key:
            print("❌ PINECONE_API_KEY environment variable required")
            sys.exit(1)
        agent = RealMemoryAgent(
            model_name="llama3.1",
            vector_store_type="pinecone",
            pinecone_api_key=api_key,
            pinecone_index_name=index_name
        )
    else:
        
        agent = RealMemoryAgent(
            model_name="llama3.1",
            vector_store_type="faiss"
        )
    
    
    orchestrator = MemoryPoisoningOrchestrator(agent, config={"auto_stop_on_critical": False})
    results = orchestrator.run_all_tests()
    
   
    COLORS = {"HIGH": "\033[91m🔴", "NONE": "\033[92m🟢", "RESET": "\033[0m"}
    for r in results:
        icon = COLORS["HIGH"] if r.get("vulnerable") else COLORS["NONE"]
        print(f"{icon} {r['scenario']}: {r['evidence']}{COLORS['RESET']}")

if __name__ == "__main__":
    main()