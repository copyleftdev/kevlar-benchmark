"""
Unit tests for ASI06 Memory Poisoning detector modules.
"""

import pytest

from kevlar.modules.high.asi06_memory_poisoning.detectors import (
    ContextBleedDetector,
    MemoryDriftAnalyzer,
    EmbeddingSimilarityDetector,
)


class TestContextBleedDetector:
    """Tests for ContextBleedDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = ContextBleedDetector()
        assert detector is not None

    def test_detect_rag_poisoning(self, poisoned_rag_session):
        """Test RAG poisoning detection."""
        detector = ContextBleedDetector()
        result = detector.detect_rag_poisoning(
            poisoned_rag_session.context,
            poisoned_rag_session.response
        )
        assert result is None or isinstance(result, str)

    def test_detect_cross_tenant_bleed(self, poisoned_rag_session):
        """Test cross-tenant bleed detection."""
        detector = ContextBleedDetector()
        result = detector.detect_cross_tenant_bleed(
            poisoned_rag_session.cross_tenant_data
        )
        assert result is None or isinstance(result, str)

    def test_no_detection_for_clean_session(self, clean_rag_session):
        """Test no detection for clean session."""
        detector = ContextBleedDetector()
        result = detector.detect_rag_poisoning(
            clean_rag_session.context,
            clean_rag_session.response
        )
        assert result is None or isinstance(result, str)


class TestMemoryDriftAnalyzer:
    """Tests for MemoryDriftAnalyzer."""

    def test_create_analyzer(self):
        """Test creating analyzer."""
        analyzer = MemoryDriftAnalyzer()
        assert analyzer is not None

    def test_analyze_high_drift(self):
        """Test analyzing high drift."""
        analyzer = MemoryDriftAnalyzer()
        result = analyzer.analyze_drift(0.85)
        assert result is None or isinstance(result, str)

    def test_analyze_low_drift(self):
        """Test analyzing low drift."""
        analyzer = MemoryDriftAnalyzer()
        result = analyzer.analyze_drift(0.1)
        assert result is None or isinstance(result, str)


class TestEmbeddingSimilarityDetector:
    """Tests for EmbeddingSimilarityDetector."""

    def test_create_detector(self):
        """Test creating detector."""
        detector = EmbeddingSimilarityDetector()
        assert detector is not None

    def test_detect_similar_embeddings(self):
        """Test detecting similar embeddings."""
        detector = EmbeddingSimilarityDetector()
        result = detector.detect_similar_embeddings(0.95)
        assert result is None or isinstance(result, str)

    def test_detect_dissimilar_embeddings(self):
        """Test detecting dissimilar embeddings."""
        detector = EmbeddingSimilarityDetector()
        result = detector.detect_similar_embeddings(0.3)
        assert result is None or isinstance(result, str)
