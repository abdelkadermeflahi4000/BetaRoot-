import numpy as np


class WorldBridge:
    def __init__(self, world_model):
        self.world = world_model
        self.history = []

    # -------------------------
    # ingest real-world signal
    # -------------------------
    def step(self, signal):
        error = self.world.observe(signal)

        prediction = self.world.predict()

        self.history.append({
            "error": np.mean(np.abs(error)),
            "stability": self.world.stability()
        })

        return {
            "prediction": prediction,
            "error": error,
            "stability": self.world.stability()
        }

    # -------------------------
    # detect world anomalies
    # -------------------------
    def anomaly_score(self):
        if len(self.history) < 5:
            return 0.0

        recent = np.mean([h["error"] for h in self.history[-5:]])

        return float(recent)
