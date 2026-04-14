# core/state.py

class SystemState:
    def __init__(self):
        self.data = {}
        self.history = []
        self.metrics = {
            "stability": 1.0,
            "novelty": 0.0
        }

    def update(self, key, value):
        self.data[key] = value
        self.history.append((key, value))

    def get(self, key, default=None):
        return self.data.get(key, default)
