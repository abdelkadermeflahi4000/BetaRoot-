import numpy as np


class SelfReflectionLoop:
    def __init__(self):
        self.history = []
        self.error_memory = []

    # -------------------------
    # store system state
    # -------------------------
    def observe(self, state, prediction):
        error = np.linalg.norm(state - prediction)

        self.history.append({
            "state": state,
            "prediction": prediction,
            "error": error
        })

        self.error_memory.append(error)

    # -------------------------
    # reflection signal (meta-learning)
    # -------------------------
    def reflect(self):
        if len(self.error_memory) < 5:
            return {
                "reflection": 0.0,
                "stability": 1.0
            }

        recent_error = np.mean(self.error_memory[-5:])
        past_error = np.mean(self.error_memory[:-5]) if len(self.error_memory) > 5 else recent_error

        improvement = past_error - recent_error

        stability = 1.0 / (1.0 + recent_error)

        return {
            "reflection": float(improvement),
            "stability": float(stability)
        }

    # -------------------------
    # self-correction signal
    # -------------------------
    def correction_signal(self):
        if not self.error_memory:
            return 0.0

        return -np.mean(self.error_memory[-3:])
