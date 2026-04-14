# core/evolution/evaluator.py

class Evaluator:

    def evaluate(self, engine):
        stability = engine.state.metrics.get("stability", 1.0)
        history_size = len(engine.state.history)

        score = stability + (history_size * 0.01)
        return score
