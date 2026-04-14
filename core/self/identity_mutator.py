# core/self/identity_mutator.py

import random

class IdentityMutator:

    def mutate(self, identity):
        trait = random.choice(list(identity.profile["traits"].keys()))

        change = random.uniform(0.8, 1.2)

        identity.profile["traits"][trait] *= change

        return {
            "trait": trait,
            "factor": change
        }
