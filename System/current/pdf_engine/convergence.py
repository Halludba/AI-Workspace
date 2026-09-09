from __future__ import annotations
import hashlib, json

class ConvergenceTracker:
    """Small deterministic fixed-point/cycle tracker, independently testable."""
    def __init__(self, detect_cycles: bool = True):
        self.detect_cycles = detect_cycles
        self.seen: set[str] = set()
        self.previous = None

    @staticmethod
    def digest(state) -> str:
        return hashlib.sha256(json.dumps(state, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def observe(self, current, issues=None):
        issues = list(issues or [])
        digest = self.digest(current)
        changed = self.previous is None or current != self.previous
        cycle = self.detect_cycles and digest in self.seen and changed
        stable = self.previous is not None and current == self.previous and not issues
        if cycle and "BLOCK: convergence cycle detected" not in issues:
            issues.append("BLOCK: convergence cycle detected")
        result = {"changed": changed, "cycle": cycle, "stable": stable, "issues": issues, "digest": digest}
        if not cycle:
            self.seen.add(digest)
        self.previous = current
        return result
