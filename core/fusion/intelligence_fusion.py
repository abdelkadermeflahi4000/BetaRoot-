class UnifiedSignalRouter:
    def __init__(self, biophoton_engine, field_engine):
        self.bio = biophoton_engine
        self.field = field_engine

    def process(self, signal, source_type="field"):
        if source_type == "biophoton":
            return self.bio.process(signal)

        elif source_type == "field":
            return self.field.process(signal)

        else:
            raise ValueError("Unknown signal type")
