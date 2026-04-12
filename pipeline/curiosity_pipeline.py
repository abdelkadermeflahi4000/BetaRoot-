class CuriosityPipeline:
    def __init__(self, engine):
        self.engine = engine

    def run(self, tokens):

        output = self.engine.update(tokens)

        state = output["state"]
        curiosity = output["curiosity"]

        # internal amplification rule
        if curiosity > 0.5:
            amplification = "HIGH_EXPLORATION"
        elif curiosity > 0.2:
            amplification = "MEDIUM"
        else:
            amplification = "STABLE"

        return {
            "state": state.tolist(),
            "curiosity": float(curiosity),
            "mode": amplification,
            "novelty": self.engine.is_novel()
        }
