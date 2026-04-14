# core/self/introspection.py

class Introspection:

    def analyze(self, state):
        last = state.get("last_action")

        if not last:
            return "NO_ACTION"

        if "EXPLORE" in last:
            return "HIGH_EXPLORATION"

        if "ANALYZE" in last:
            return "HIGH_REASONING"

        return "UNKNOWN"
