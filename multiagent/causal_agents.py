import numpy as np


class CausalAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.local_memory = []
        self.bias = np.random.rand(16)

    def perceive(self, state):
        weighted = state * self.bias
        self.local_memory.append(weighted)
        return weighted

    def share(self):
        if len(self.local_memory) == 0:
            return np.zeros(16)

        return np.mean(self.local_memory, axis=0)


class MultiAgentSystem:
    def __init__(self, n_agents=3):
        self.agents = [CausalAgent(i) for i in range(n_agents)]

    # -------------------------
    # distributed processing
    # -------------------------
    def step(self, global_state):
        outputs = []

        for agent in self.agents:
            local = agent.perceive(global_state)
            outputs.append(local)

        # consensus (causal fusion)
        return np.mean(outputs, axis=0)

    # -------------------------
    # emergent causal signal
    # -------------------------
    def emergent_state(self):
        shared = [a.share() for a in self.agents]
        return np.mean(shared, axis=0)
