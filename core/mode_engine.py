# core/mode_engine.py

class ModeEngine:
    VALID_MODES = ["theta", "alpha", "beta", "gamma"]

    def __init__(self, default_mode="beta"):
        if default_mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode: {default_mode}")
        self.mode = default_mode

    def set_mode(self, mode: str):
        if mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode

    def get_mode(self):
        return self.mode

    def auto_select_mode(self, query: dict):
        """
        Smart mode selection based on query metadata
        """
        if query.get("type") == "unknown":
            self.mode = "alpha"
        elif query.get("requires_proof"):
            self.mode = "beta"
        elif query.get("complexity") == "high":
            self.mode = "gamma"
        else:
            self.mode = "theta"

        return self.mode
