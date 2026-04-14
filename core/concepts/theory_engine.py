# core/concepts/theory_engine.py

class TheoryEngine:

    def __init__(self, memory, builder, evaluator):
        self.memory = memory
        self.builder = builder
        self.evaluator = evaluator
        self.current_theory = None

    def evolve(self, concepts):
        relations = RelationBuilder().build(concepts)

        theory = self.builder.build(concepts, relations)

        score = self.evaluator.evaluate(theory)

        if not self.current_theory or score > self.evaluator.evaluate(self.current_theory):
            self.current_theory = theory
            print("[THEORY UPDATED]")

        return self.current_theory
