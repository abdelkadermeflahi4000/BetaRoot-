# core/concepts/theory_evaluator.py

class TheoryEvaluator:

    def evaluate(self, theory):
        complexity = len(theory["concepts"])
        connections = len(theory["relations"])

        return complexity + (connections * 0.5)
