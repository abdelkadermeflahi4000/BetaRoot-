# agents/multi_agent.py

class Agent:
    def __init__(self, name, mode, reasoning_engine):
        self.name = name
        self.mode = mode
        self.engine = reasoning_engine

    def run(self, query):
        self.engine.mode_engine.set_mode(self.mode)
        return self.engine.reason(query)


class MultiAgentSystem:
    def __init__(self, reasoning_engine):
        self.agents = [
            Agent("MemoryAgent", "theta", reasoning_engine),
            Agent("CreativeAgent", "alpha", reasoning_engine),
            Agent("LogicAgent", "beta", reasoning_engine),
            Agent("IntegrationAgent", "gamma", reasoning_engine),
        ]

    def process(self, query):
        results = []

        for agent in self.agents:
            result = agent.run(query)
            results.append({
                "agent": agent.name,
                "output": result
            })

        return results
