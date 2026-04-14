# core/architecture/architecture_engine.py

class ArchitectureEngine:

    def __init__(self):
        self.genome = ArchitectureGenome()
        self.generator = ArchitectureGenerator()
        self.mutator = ArchitectureMutator()
        self.executor = ArchitectureExecutor()
        self.evaluator = ArchitectureEvaluator()
        self.registry = ArchitectureRegistry()

    def evolve(self, state):
        base = self.genome.clone()

        # توليد نسخة جديدة
        new_arch = self.generator.generate(base)

        # تعديلها
        new_arch = self.mutator.mutate(new_arch)

        print("[ARCH PROPOSED]", new_arch)

        # محاكاة
        score = self.executor.simulate(new_arch, state)

        score = self.evaluator.evaluate(score)

        self.registry.update(new_arch, score)

        return self.registry.best_arch
