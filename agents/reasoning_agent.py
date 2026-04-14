# agents/reasoning_agent.py

class ReasoningAgent:
    def process(self, state, signal):
        return {
            "agent": "reasoning",
            "action": "ANALYZE",
            "confidence": abs(signal["wave"]),
            "energy": 0.6
        }
