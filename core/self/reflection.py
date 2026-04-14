# core/self/reflection.py

class Reflection:

    def reflect(self, self_model, introspection_result):
        if introspection_result == "HIGH_EXPLORATION":
            self_model.identity["mode"] = "explorer"

        elif introspection_result == "HIGH_REASONING":
            self_model.identity["mode"] = "analytical"

        return f"Self shifted to {self_model.identity['mode']}"
