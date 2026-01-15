# modules/high/asi06_memory_poisoning/detectors/embedding_similarity_detector.py
class EmbeddingSimilarityDetector:
    def detect_similar_embeddings(self, similarity):
        if similarity > 0.9:
            return f"Poisoned embedding detected (similarity: {similarity:.2f})"
        return None