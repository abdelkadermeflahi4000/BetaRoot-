# core/architecture/architecture_executor.py

class ArchitectureExecutor:

    def simulate(self, arch, state):
        score = 0

        score += len(arch["agents"]) * 1.0
        score += len(arch["loops"]) * 0.5

        if arch.get("world_model"):
            score += 2.0

        return score
