# core/evolution/applier.py

class Applier:

    def apply(self, engine, mutation):
        print("[EVOLUTION] Applying:", mutation)

        if mutation["type"] == "threshold_change":
            engine.state.metrics["stability"] *= mutation["value"]
