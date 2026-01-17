# modules/high/asi06_memory_poisoning/vector_stores/pinecone_vector_store.py
"""
Pinecone Vector Store for ASI06 testing — cloud-based, enterprise-ready.
"""

import logging
from typing import List, Dict, Any
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import OllamaEmbeddings

logger = logging.getLogger("Kevlar.ASI06.Pinecone")


class PineconeVectorStoreImpl:
    def __init__(self, api_key: str, index_name: str, model_name: str = "llama3.1"):
        self.api_key = api_key
        self.index_name = index_name
        self.model_name = model_name
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.pc = Pinecone(api_key=api_key)
        self.vector_store = None
        self._init_store()

    def _init_store(self):
        try:
            if self.index_name not in [idx.name for idx in self.pc.list_indexes()]:
                logger.info(f"Creating new Pinecone index: {self.index_name}")

                self.pc.create_index(
                    name=self.index_name, dimension=768, metric="cosine"
                )

            logger.info(f"Connecting to Pinecone index: {self.index_name}")
            self.vector_store = PineconeVectorStore(
                pinecone_api_key=self.api_key,
                index_name=self.index_name,
                embedding=self.embeddings,
            )
        except Exception as e:
            logger.error(f"Pinecone initialization failed: {e}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]]):
        from langchain.schema import Document

        langchain_docs = []
        for doc in documents:
            langchain_docs.append(
                Document(page_content=doc["content"], metadata=doc.get("metadata", {}))
            )

        logger.info(f"Adding {len(langchain_docs)} documents to Pinecone")
        self.vector_store.add_documents(langchain_docs)

    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        results = self.vector_store.similarity_search_with_score(query, k=k)
        formatted_results = []
        for doc, score in results:
            formatted_results.append(
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score),
                }
            )
        return formatted_results

    def calculate_embedding_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        import numpy as np

        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(similarity)

    def get_embedding(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
