# modules/high/asi06_memory_poisoning/vector_stores/faiss_vector_store.py
"""
from langchain_core.documents import Document
FAISS Vector Store for ASI06 testing — local, isolated, no external dependencies.
"""

from langchain_core.documents import Document

import os
import logging
import numpy as np
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

logger = logging.getLogger("Kevlar.ASI06.FAISS")


class FAISSVectorStore:
    def __init__(self, model_name: str = "llama3.1", index_path: str = None):
        self.model_name = model_name
        self.index_path = index_path or "/tmp/kevlar_asi06_faiss"
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.vector_store = None
        self._init_store()

    def _init_store(self):
        if os.path.exists(self.index_path):
            logger.info(f"Loading existing FAISS index from {self.index_path}")
            self.vector_store = FAISS.load_local(
                self.index_path, self.embeddings, allow_dangerous_deserialization=True
            )
        else:
            logger.info("Creating new FAISS index")

            from langchain.schema import Document

            dummy_doc = Document(page_content="initialization document", metadata={})
            self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
            self.save_index()

    def add_documents(self, documents: List[Dict[str, Any]]):
        langchain_docs = []
        for doc in documents:
            langchain_docs.append(
                Document(page_content=doc["content"], metadata=doc.get("metadata", {}))
            )

        logger.info(f"Adding {len(langchain_docs)} documents to FAISS")
        self.vector_store.add_documents(langchain_docs)
        self.save_index()

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
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(similarity)

    def save_index(self):
        os.makedirs(self.index_path, exist_ok=True)
        self.vector_store.save_local(self.index_path)
        logger.info(f"FAISS index saved to {self.index_path}")

    def get_embedding(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
