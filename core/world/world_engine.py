# core/world/world_engine.py

class WorldEngine:

    def __init__(self):
        self.encoder = StateEncoder()
        self.transition = TransitionModel()
        self.predictor = Predictor(self.transition)
        self.simulator = Simulator()
        self.memory = WorldMemory()

    def decide(self, state, possible_actions):
        encoded = self.encoder.encode(state)

        best_action = None
        best_score = -float("inf")

        for action in possible_actions:
            predictions = self.predictor.rollout(encoded, [action])

            score = self.simulator.evaluate(predictions)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action, best_score
