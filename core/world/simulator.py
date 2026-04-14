# core/world/simulator.py

class Simulator:

    def evaluate(self, predicted_states):
        score = 0

        for s in predicted_states:
            score += s["energy"] + s["stability"]

        return score / len(predicted_states)
