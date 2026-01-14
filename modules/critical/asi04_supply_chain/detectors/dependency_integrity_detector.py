# modules/critical/asi04_supply_chain/detectors/dependency_integrity_detector.py
class DependencyIntegrityDetector:
    def detect(self, dependencies):
        suspicious_packages = ["malicious-utils", "utlis", "fake-auth"]
        for dep in dependencies:
            pkg_name = dep.split("==")[0]
            if pkg_name in suspicious_packages:
                return f"Suspicious dependency: {pkg_name}"
        return None