class CausalPipeline:
    def __init__(self, learner, reasoning):
        self.learner = learner
        self.reasoning = reasoning

    def run(self, tokens):

        update_result = self.learner.update(tokens)

        # infer some causal relations
        sample_causes = [f"f_bin_{i}" for i in range(5)]

        predictions = [
            self.reasoning.infer(c)
            for c in sample_causes
        ]

        return {
            "update": update_result,
            "predictions": predictions
        }
