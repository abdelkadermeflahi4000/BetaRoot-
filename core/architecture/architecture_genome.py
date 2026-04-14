# core/architecture/architecture_genome.py

class ArchitectureGenome:

    def __init__(self):
        self.structure = {
            "agents": ["explorer", "analyzer"],
            "loops": ["cycle", "decision"],
            "memory": ["short", "long"],
            "world_model": True
        }

    def clone(self):
        import copy
        return copy.deepcopy(self.structure)
