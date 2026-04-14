# core/emergence.py

class EmergenceTracker:

    def __init__(self):
        self.history = []

    def track(self, decision):
        self.history.append(decision["action"])

    def detect_pattern(self):
        if len(self.history) < 5:
            return None

        last = self.history[-5:]

        if len(set(last)) == 1:
            return "STABLE_PATTERN"

        return "CHAOTIC"
