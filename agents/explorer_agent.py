# agents/explorer_agent.py

import random

class ExplorerAgent:
    def process(self, state, signal):
        return {
            "agent": "explorer",
            "action": "EXPLORE",
            "confidence": random.random(),
            "energy": 0.9
        }
