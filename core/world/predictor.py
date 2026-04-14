# core/world/predictor.py

class Predictor:

    def __init__(self, transition_model):
        self.model = transition_model

    def rollout(self, state, actions, steps=3):
        predictions = []
        current = state

        for _ in range(steps):
            for action in actions:
                current = self.model.predict_next(current, action)

            predictions.append(current.copy())

        return predictions
