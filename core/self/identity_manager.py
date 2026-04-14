# core/self/identity_manager.py

class IdentityManager:

    def __init__(self, identity, mutator, evaluator):
        self.identity = identity
        self.mutator = mutator
        self.evaluator = evaluator

    def evolve_identity(self, state):
        before = self.identity.describe().copy()

        mutation = self.mutator.mutate(self.identity)

        score = self.evaluator.evaluate(state)

        if score < 1.0:
            # rollback
            self.identity.profile = before
            print("[IDENTITY] mutation rejected")

        else:
            print("[IDENTITY] evolved:", mutation)
