class UnifiedCognitiveCore:
    def __init__(self, temporal, self_model, causal_graph, multi_agent, reflection):
        self.temporal = temporal
        self.self_model = self_model
        self.causal = causal_graph
        self.multi_agent = multi_agent
        self.reflection = reflection

    # -------------------------
    # main cognitive step
    # -------------------------
    def step(self, state, prediction, timestamp):

        # 1. temporal update
        self.temporal.add(state, timestamp)

        # 2. self model update
        self.self_model.update(state)

        # 3. causal update (simplified proxy)
        causal_strength = float(np.linalg.norm(state - prediction))
        self.causal.observe("state_change", "prediction_error", causal_strength)

        # 4. multi-agent processing
        emergent = self.multi_agent.step(state)

        # 5. reflection
        self.reflection.observe(state, prediction)
        meta = self.reflection.reflect()

        return {
            "temporal": self.temporal.trend(),
            "self_drift": self.self_model.change_rate(),
            "emergent_state": emergent.tolist(),
            "meta_reflection": meta
        }
