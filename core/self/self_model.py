# core/self/self_model.py

class SelfModel:

    def __init__(self):
        self.identity = {
            "mode": "explore",
            "stability": 1.0,
            "activity": 0.0
        }

    def update(self, state):
        self.identity["activity"] = len(state.history)
        self.identity["stability"] = state.metrics.get("stability", 1.0)

    def describe(self):
        return f"Mode={self.identity['mode']} | Stability={self.identity['stability']:.2f}"
