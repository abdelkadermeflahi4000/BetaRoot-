# core/evolution.py

import random

class EvolutionEngine:

    def evaluate(self, state):
        # مثال: الاستقرار مقابل الحداثة
        stability = state.metrics["stability"]
        novelty = random.random()

        score = stability * 0.7 + novelty * 0.3
        return score

    def mutate(self, state):
        # تعديل بسيط
        state.metrics["novelty"] += 0.1

    def evolve(self, state):
        score = self.evaluate(state)

        if score < 0.5:
            print("[EVOLVE] mutation triggered")
            self.mutate(state)
