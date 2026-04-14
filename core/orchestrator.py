# core/orchestrator.py

class Orchestrator:
    def __init__(self, agents):
        self.agents = agents

    def run_agents(self, state, signal):
        decisions = []

        for agent in self.agents:
            try:
                d = agent.process(state, signal)
                if d:
                    decisions.append(d)
            except Exception as e:
                print(f"[Agent Error] {agent}: {e}")

        return decisions

    def resolve(self, decisions):
        # بسيط الآن → لاحقاً نضيف voting
        return decisions
