# core/architecture/architecture_mutator.py

import random

class ArchitectureMutator:

    def mutate(self, arch):
        if arch["agents"]:
            removed = random.choice(arch["agents"])
            arch["agents"].remove(removed)

        return arch
