# core/architecture/architecture_registry.py

class ArchitectureRegistry:

    def __init__(self):
        self.best_arch = None
        self.best_score = -float("inf")

    def update(self, arch, score):
        if score > self.best_score:
            self.best_score = score
            self.best_arch = arch
            print("[NEW BEST ARCHITECTURE]")
