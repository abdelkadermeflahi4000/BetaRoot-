class WorldIntelligencePipeline:
    def __init__(self, world_bridge, temporal, causal, self_model):
        self.world = world_bridge
        self.temporal = temporal
        self.causal = causal
        self.self_model = self_model

    def run(self, signal, timestamp):

        # 1. world observation
        world_out = self.world.step(signal)

        # 2. temporal tracking
        self.temporal.add(world_out["prediction"], timestamp)

        # 3. self-model update
        self.self_model.update(world_out["prediction"])

        # 4. causal relation (world dynamics)
        self.causal.observe(
            "earth_state",
            "prediction_error",
            float(np.mean(np.abs(world_out["error"])))
        )

        return {
            "world_prediction": world_out["prediction"].tolist(),
            "stability": world_out["stability"],
            "anomaly": self.world.anomaly_score()
        }
