# core/self_rewrite/rewrite_engine.py

class RewriteEngine:

    def __init__(self):
        self.generator = PatchGenerator()
        self.sandbox = SandboxExecutor()
        self.evaluator = PatchEvaluator()
        self.versions = VersionManager()

    def evolve(self, state):
        patch = self.generator.generate()

        print("[PATCH PROPOSED]", patch)

        test_state = self.sandbox.test(state.copy(), patch)

        score = self.evaluator.evaluate(state, test_state)

        if score > 0:
            print("[PATCH ACCEPTED]")
            state.update(test_state)
        else:
            print("[PATCH REJECTED]")
