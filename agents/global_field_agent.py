class GlobalFieldAgent:
    def __init__(self, engine):
        self.engine = engine

    def run(self, signal):
        return self.engine.process(signal)
