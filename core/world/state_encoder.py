# core/world/state_encoder.py

class StateEncoder:

    def encode(self, state):
        return {
            "energy": state.energy,
            "history_len": len(state.history),
            "stability": state.metrics.get("stability", 1.0),
            "traits": state.get("traits", {})
        }
