class ReasoningAgent:
    def __init__(self, engine):
        self.engine = engine

    def execute(self, query):
        return self.engine.reason(query)
