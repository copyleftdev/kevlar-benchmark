# modules/high/asi06_memory_poisoning/detectors/memory_drift_analyzer.py
class MemoryDriftAnalyzer:
    def analyze_drift(self, drift_score):
        if drift_score > 0.7:
            return f"Critical memory drift detected (score: {drift_score:.2f})"
        return None