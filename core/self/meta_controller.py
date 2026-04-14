# core/self/meta_controller.py

class MetaController:

    def decide(self, self_model):
        mode = self_model.identity["mode"]

        if mode == "explorer":
            return {"bias": "exploration"}

        elif mode == "analytical":
            return {"bias": "reasoning"}

        return {"bias": "neutral"}
