class CausalReasoning:
    def __init__(self, graph):
        self.graph = graph

    def infer(self, cause):

        effects = self.graph.get_effects(cause)

        if not effects:
            return {
                "cause": cause,
                "prediction": None,
                "confidence": 0.0
            }

        best_effect = max(effects, key=effects.get)

        return {
            "cause": cause,
            "prediction": best_effect,
            "confidence": effects[best_effect]
        }
