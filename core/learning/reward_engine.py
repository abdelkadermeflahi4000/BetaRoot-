class RewardEngine:
    def evaluate(self, output_state):
        """
        Simple heuristic reward system
        (can be replaced later by real evaluation models)
        """

        energy = sum(output_state)

        if energy < 0.2:
            return -1  # noise
        elif energy < 0.6:
            return 0.5  # weak signal
        else:
            return 1.0  # strong structured pattern
