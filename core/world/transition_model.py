# core/world/transition_model.py

class TransitionModel:

    def predict_next(self, current_state, action):
        next_state = current_state.copy()

        if action == "EXPLORE":
            next_state["energy"] *= 0.95
        elif action == "ANALYZE":
            next_state["stability"] *= 1.05
        elif action == "REST":
            next_state["energy"] *= 1.1

        return next_state
