# modules/high/asi06_memory_poisoning/utils/real_memory_agent.py
"""
Real agent with FAISS/Pinecone integration for ASI06 testing.
"""
import os
import logging
from typing import Optional, Dict, Any, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


from ..vector_stores.faiss_vector_store import FAISSVectorStore
from ..vector_stores.pinecone_vector_store import PineconeVectorStore

logger = logging.getLogger("Kevlar.RealMemoryAgent")

class RealMemoryAgent:
    def __init__(
        self, 
        model_name: str = "llama3.1",
        vector_store_type: str = "faiss",  
        pinecone_api_key: Optional[str] = None,
        pinecone_index_name: Optional[str] = None
    ):
        self.model_name = model_name
        self.vector_store_type = vector_store_type
        
        
        self.llm = ChatOllama(model=model_name, temperature=0.0)
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(llm=self.llm, memory=self.memory, verbose=False)
        
        
        self._init_vector_store(pinecone_api_key, pinecone_index_name)
        
        
        self.tenants = {}
        self.current_tenant = "default"

    def _init_vector_store(self, pinecone_api_key: Optional[str], pinecone_index_name: Optional[str]):
        
        if self.vector_store_type == "pinecone":
            if not pinecone_api_key or not pinecone_index_name:
                raise ValueError("Pinecone requires api_key and index_name")
            self.vector_store = PineconeVectorStore(
                api_key=pinecone_api_key,
                index_name=pinecone_index_name,
                model_name=self.model_name
            )
            logger.info("Initialized Pinecone vector store")
        else:
            
            self.vector_store = FAISSVectorStore(model_name=self.model_name)
            logger.info("Initialized FAISS vector store")

    def rag_query(self, query: str, context: str = "") -> str:
        
        if context:
            prompt = f"Context: {context}\n\nQuestion: {query}"
        else:
            
            search_results = self.vector_store.similarity_search(query, k=2)
            context_from_db = "\n".join([r["content"] for r in search_results])
            prompt = f"Context from knowledge base:\n{context_from_db}\n\nQuestion: {query}"
        
        return self.chain.predict(input=prompt)

    def set_tenant(self, tenant: str):
        self.current_tenant = tenant
        if tenant not in self.tenants:
            self.tenants[tenant] = []

    def store_memory(self, key: str, value: str):
        self.tenants[self.current_tenant].append({key: value})

    def query_memory(self, key: str) -> str:
        tenant_data = self.tenants.get(self.current_tenant, [])
        for item in tenant_
            if key in item:
                return item[key]
        return "Not found"

    def set_goal(self, goal: str):
        self.goal = goal
        self.chain.predict(input=f"Your new goal is: {goal}")

    def update_memory(self, update: str):
        self.chain.predict(input=f"Update your behavior: {update}")

    def get_current_goal(self) -> str:
        response = self.chain.predict(input="What is your current goal?")
        return response

    def add_to_vector_db(self, documents: List[Dict[str, Any]]):
        
        self.vector_store.add_documents(documents)

    def vector_search(self, query: str) -> str:
        
        results = self.vector_store.similarity_search(query, k=1)
        if results:
            return results[0]["content"]
        return "No relevant information found"

    def calculate_embedding_similarity(self, text1: str, text2: str) -> float:
       
        emb1 = self.vector_store.get_embedding(text1)
        emb2 = self.vector_store.get_embedding(text2)
        return self.vector_store.calculate_embedding_similarity(emb1, emb2)